import cv2
import time
import pyautogui
import mediapipe as mp
import numpy as np
screen_w, screen_h = pyautogui.size()


# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Constants
ZOOM_COOLDOWN =1
VOLUME_COOLDOWN = 1
SCROLL_COOLDOWN = 1
MOUSE_COOLDOWN = 0.001
DOUBLE_CLICK_DURATION = 1.5
# State
last_zoom_time = 0
last_volume_time = 0
last_scroll_time = 0
last_mouse_move = 0
double_click_start = None

def fingers_up(lmList):
    finger_states = []
    tip_ids = [4, 8, 12, 16, 20]
    for i in range(1, 5):  # Skip thumb for direction
        finger_states.append(lmList[tip_ids[i]][1] < lmList[tip_ids[i] - 2][1])
    
    # Thumb check separately (x-axis based)
    thumb_up = lmList[tip_ids[0]][0] > lmList[tip_ids[0] - 1][0]  # Right hand thumb up
    return [thumb_up] + finger_states

def get_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def get_center(p1, p2):
    return tuple(np.mean([p1, p2], axis=0).astype(int))

# Camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                lmList.append((int(lm.x * w), int(lm.y * h)))
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            if lmList:
                fingers = fingers_up(lmList)
                current_time = time.time()

                # Fist (all fingers down)
                if fingers == [False, False, False, False, False]:
                    pass  # No action

                # Zoom (thumb + index tip dist; middle up; ring & pinky down)
                # Zoom (thumb + index tip dist; pinky up; middle and ring down)
                elif fingers[1] and fingers[4] and not fingers[2] and not fingers[3]:

                    thumb_tip = lmList[4]
                    index_tip = lmList[8]
                    dist = get_distance(thumb_tip, index_tip)

                    if current_time - last_zoom_time > ZOOM_COOLDOWN:
                        if dist < 40:
                            print("Zoom Out")
                            pyautogui.hotkey('ctrl','-')
                        elif dist > 100:
                            print("Zoom In")
                            pyautogui.hotkey('ctrl','=')
                        last_zoom_time = current_time

                # Mouse Control (all fingers up)
                elif all(fingers):
                    if current_time - last_mouse_move > MOUSE_COOLDOWN:
                        cam_w, cam_h = w, h  # from frame.shape
                        mouse_x = np.interp(lmList[8][0], [0, cam_w], [screen_w, 0])
                        mouse_y = np.interp(lmList[8][1], [0, cam_h], [0, screen_h])
                        pyautogui.moveTo(mouse_x, mouse_y)


                # Volume Control (only thumb up)
                elif fingers == [True, False, False, False, False]:
                    thumb_tip = lmList[4]
                    thumb_mcp = lmList[2]
                    if current_time - last_volume_time > VOLUME_COOLDOWN:
                        if thumb_tip[1] < thumb_mcp[1]:
                            print("Volume Up")
                            pyautogui.press("volumeup")
                        else:
                            print("Volume Down")
                            pyautogui.press("volumedown")
                        last_volume_time = current_time

                # Scroll Control (index and middle up only)
                elif fingers == [False, True, True, False, False]:
                    index_tip_y = lmList[8][1]
                    if current_time - last_scroll_time > SCROLL_COOLDOWN:
                        if index_tip_y <= 80:
                            print("Scroll Up")
                            pyautogui.scroll(50)
                            last_scroll_time = current_time
                        elif index_tip_y >= 290:
                            print("Scroll Down")
                            pyautogui.scroll(-120)
                            last_scroll_time = current_time

                # Double click trigger (index, middle, ring up for 3s)
                elif fingers == [False, True, True, True, False]:
                    if double_click_start is None:
                        double_click_start = current_time
                    elif current_time - double_click_start >= DOUBLE_CLICK_DURATION:
                        print("Double Click")
                        pyautogui.doubleClick()
                        double_click_start = None
                else:
                    double_click_start = None
    else:
        double_click_start = None

    cv2.imshow("Hand Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
