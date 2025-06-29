<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hand Gesture Control Interface</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .gesture-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        .video-container {
            position: relative;
            overflow: hidden;
            border-radius: 1rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        .video-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(to bottom, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.3) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 1.2rem;
        }
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        .status-active {
            background-color: #10B981;
            box-shadow: 0 0 10px #10B981;
        }
        .status-inactive {
            background-color: #EF4444;
        }
        .hand-animation {
            animation: wave 2s infinite;
        }
        @keyframes wave {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(10deg); }
            50% { transform: rotate(-10deg); }
            75% { transform: rotate(5deg); }
        }
    </style>
</head>
<body class="bg-gray-100 min-h-screen font-sans">
    <div class="container mx-auto px-4 py-8">
        <!-- Header -->
        <header class="text-center mb-12">
            <h1 class="text-4xl md:text-5xl font-bold text-indigo-800 mb-4">Hand Gesture Control</h1>
            <p class="text-lg text-gray-600 max-w-2xl mx-auto">
                Control your computer with intuitive hand gestures. No mouse or keyboard required!
            </p>
        </header>

        <!-- Main Content -->
        <div class="flex flex-col lg:flex-row gap-8">
            <!-- Left Column - Video Feed -->
            <div class="lg:w-2/3">
                <div class="video-container bg-gray-800 aspect-video relative">
                    <video id="video" class="w-full h-full object-cover" autoplay playsinline></video>
                    <div id="video-overlay" class="video-overlay">
                        <div class="text-center">
                            <i class="fas fa-hand-paper text-5xl mb-4 hand-animation"></i>
                            <p>Waiting for camera access...</p>
                        </div>
                    </div>
                </div>
                
                <div class="mt-6 bg-white rounded-xl shadow-md p-6">
                    <h2 class="text-xl font-semibold text-gray-800 mb-4">Control Status</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="flex items-center">
                            <span id="mouse-status" class="status-indicator status-inactive"></span>
                            <span class="text-gray-700">Mouse Control</span>
                        </div>
                        <div class="flex items-center">
                            <span id="zoom-status" class="status-indicator status-inactive"></span>
                            <span class="text-gray-700">Zoom Control</span>
                        </div>
                        <div class="flex items-center">
                            <span id="volume-status" class="status-indicator status-inactive"></span>
                            <span class="text-gray-700">Volume Control</span>
                        </div>
                        <div class="flex items-center">
                            <span id="scroll-status" class="status-indicator status-inactive"></span>
                            <span class="text-gray-700">Scroll Control</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Column - Gesture Guide -->
            <div class="lg:w-1/3">
                <div class="bg-white rounded-xl shadow-md p-6 mb-6">
                    <h2 class="text-xl font-semibold text-gray-800 mb-4">Current Action</h2>
                    <div id="current-action" class="text-center py-8 bg-gray-50 rounded-lg">
                        <i class="fas fa-question-circle text-5xl text-gray-400 mb-3"></i>
                        <p class="text-gray-600">No active gesture detected</p>
                    </div>
                </div>

                <div class="bg-white rounded-xl shadow-md p-6">
                    <h2 class="text-xl font-semibold text-gray-800 mb-4">Gesture Guide</h2>
                    <div class="space-y-4">
                        <!-- Mouse Control -->
                        <div class="gesture-card p-4 border border-gray-200 rounded-lg transition-all duration-300">
                            <div class="flex items-center">
                                <div class="mr-4 text-indigo-600">
                                    <i class="fas fa-hand-pointer text-3xl"></i>
                                </div>
                                <div>
                                    <h3 class="font-medium text-gray-800">Mouse Control</h3>
                                    <p class="text-sm text-gray-600">All fingers up to move cursor</p>
                                </div>
                            </div>
                        </div>

                        <!-- Zoom Control -->
                        <div class="gesture-card p-4 border border-gray-200 rounded-lg transition-all duration-300">
                            <div class="flex items-center">
                                <div class="mr-4 text-indigo-600">
                                    <i class="fas fa-search-plus text-3xl"></i>
                                </div>
                                <div>
                                    <h3 class="font-medium text-gray-800">Zoom Control</h3>
                                    <p class="text-sm text-gray-600">Thumb + index + pinky up (pinch to zoom)</p>
                                </div>
                            </div>
                        </div>

                        <!-- Volume Control -->
                        <div class="gesture-card p-4 border border-gray-200 rounded-lg transition-all duration-300">
                            <div class="flex items-center">
                                <div class="mr-4 text-indigo-600">
                                    <i class="fas fa-volume-up text-3xl"></i>
                                </div>
                                <div>
                                    <h3 class="font-medium text-gray-800">Volume Control</h3>
                                    <p class="text-sm text-gray-600">Thumb up (move up/down to adjust)</p>
                                </div>
                            </div>
                        </div>

                        <!-- Scroll Control -->
                        <div class="gesture-card p-4 border border-gray-200 rounded-lg transition-all duration-300">
                            <div class="flex items-center">
                                <div class="mr-4 text-indigo-600">
                                    <i class="fas fa-mouse-pointer text-3xl"></i>
                                </div>
                                <div>
                                    <h3 class="font-medium text-gray-800">Scroll Control</h3>
                                    <p class="text-sm text-gray-600">Index + middle fingers up (move up/down)</p>
                                </div>
                            </div>
                        </div>

                        <!-- Double Click -->
                        <div class="gesture-card p-4 border border-gray-200 rounded-lg transition-all duration-300">
                            <div class="flex items-center">
                                <div class="mr-4 text-indigo-600">
                                    <i class="fas fa-mouse text-3xl"></i>
                                </div>
                                <div>
                                    <h3 class="font-medium text-gray-800">Double Click</h3>
                                    <p class="text-sm text-gray-600">Index + middle + ring fingers up (hold for 1.5s)</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="mt-12 text-center text-gray-500 text-sm">
            <p>Hand Gesture Control Interface | Requires camera access and Chrome/Firefox</p>
            <p class="mt-2">Note: This is a UI demonstration. Actual gesture recognition would require additional backend implementation.</p>
        </footer>
    </div>

    <script>
        // This is a simulation of the gesture control UI
        // In a real implementation, you would connect to the actual gesture detection backend
        
        // Simulate gesture detection for demo purposes
        const gestureTypes = [
            { 
                name: "Mouse Control", 
                icon: "hand-pointer", 
                color: "text-blue-500",
                statusId: "mouse-status",
                description: "Moving cursor with hand"
            },
            { 
                name: "Zoom Control", 
                icon: "search-plus", 
                color: "text-green-500",
                statusId: "zoom-status",
                description: "Zooming in/out"
            },
            { 
                name: "Volume Control", 
                icon: "volume-up", 
                color: "text-purple-500",
                statusId: "volume-status",
                description: "Adjusting volume"
            },
            { 
                name: "Scroll Control", 
                icon: "mouse-pointer", 
                color: "text-yellow-500",
                statusId: "scroll-status",
                description: "Scrolling page"
            },
            { 
                name: "Double Click", 
                icon: "mouse", 
                color: "text-red-500",
                description: "Double click triggered"
            }
        ];

        // Get DOM elements
        const currentActionEl = document.getElementById('current-action');
        const videoOverlayEl = document.getElementById('video-overlay');
        const videoEl = document.getElementById('video');

        // Simulate camera access
        setTimeout(() => {
            videoOverlayEl.innerHTML = `
                <div class="text-center">
                    <i class="fas fa-check-circle text-5xl mb-4 text-green-500"></i>
                    <p>Camera connected</p>
                </div>
            `;
            
            // After another delay, remove overlay
            setTimeout(() => {
                videoOverlayEl.style.display = 'none';
                startGestureSimulation();
            }, 2000);
        }, 2000);

        // Start simulating gesture detection
        function startGestureSimulation() {
            let currentGestureIndex = 0;
            
            setInterval(() => {
                // Cycle through gestures for demo
                const gesture = gestureTypes[currentGestureIndex];
                
                // Update current action display
                currentActionEl.innerHTML = `
                    <i class="fas ${gesture.icon} text-5xl ${gesture.color} mb-3"></i>
                    <h3 class="font-semibold text-gray-800">${gesture.name}</h3>
                    <p class="text-gray-600">${gesture.description}</p>
                `;
                
                // Update status indicators
                document.querySelectorAll('.status-indicator').forEach(el => {
                    el.classList.remove('status-active');
                    el.classList.add('status-inactive');
                });
                
                if (gesture.statusId) {
                    const statusEl = document.getElementById(gesture.statusId);
                    if (statusEl) {
                        statusEl.classList.remove('status-inactive');
                        statusEl.classList.add('status-active');
                    }
                }
                
                // Move to next gesture
                currentGestureIndex = (currentGestureIndex + 1) % gestureTypes.length;
            }, 3000);
        }

        // Try to access camera (for real implementation)
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    videoEl.srcObject = stream;
                })
                .catch(err => {
                    console.error("Error accessing camera:", err);
                    videoOverlayEl.innerHTML = `
                        <div class="text-center">
                            <i class="fas fa-exclamation-triangle text-5xl mb-4 text-red-500"></i>
                            <p>Camera access denied</p>
                            <p class="text-sm mt-2">Using demo mode</p>
                        </div>
                    `;
                });
        }
    </script>
</body>
</html>
