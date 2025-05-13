/**
 * AlphaVox Neural Voice Interface and Self-Learning System
 * This module enables voice interaction and displays system self-improvements
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const voiceMessages = document.getElementById('voiceMessages');
    const voiceTextInput = document.getElementById('voiceTextInput');
    const sendVoiceMessage = document.getElementById('sendVoiceMessage');
    const startListening = document.getElementById('startListening');
    const voiceProfile = document.getElementById('voiceProfile');
    const learningRuntime = document.getElementById('learningRuntime');
    const learningIterations = document.getElementById('learningIterations');
    const modificationLog = document.getElementById('modificationLog');
    
    // Check if the required elements exist on the page
    if (!voiceMessages || !voiceTextInput || !sendVoiceMessage || !startListening) {
        console.log("Voice chat interface elements not found on this page. Skipping voice chat initialization.");
        return;
    }

    // State variables
    let isListening = false;
    let runtimeSeconds = 13337; // Starting value for demonstration
    let iterations = 47;        // Starting value for demonstration
    
    // Initialize voice interface
    function initializeVoiceInterface() {
        // Handle send button click
        sendVoiceMessage.addEventListener('click', function() {
            const message = voiceTextInput.value.trim();
            if (message) {
                addUserMessage(message);
                processUserInput(message);
                voiceTextInput.value = '';
            }
        });
        
        // Handle enter key in input field
        voiceTextInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const message = voiceTextInput.value.trim();
                if (message) {
                    addUserMessage(message);
                    processUserInput(message);
                    voiceTextInput.value = '';
                }
            }
        });
        
        // Handle voice recording button
        startListening.addEventListener('click', function() {
            if (!isListening) {
                startSpeechRecognition();
            } else {
                stopSpeechRecognition();
            }
        });
        
        // Handle voice profile change
        voiceProfile.addEventListener('change', function() {
            addSystemMessage(`Voice profile changed to: ${voiceProfile.options[voiceProfile.selectedIndex].text}`);
        });
    }
    
    // Add user message to chat
    function addUserMessage(message) {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        
        const messageHTML = `
            <div class="user-message">
                <div class="message-content">
                    <div class="message-text">${message}</div>
                    <div class="message-timestamp">${timeString}</div>
                </div>
                <div class="message-icon"><i class="fas fa-user"></i></div>
            </div>
        `;
        
        voiceMessages.insertAdjacentHTML('beforeend', messageHTML);
        scrollMessagesToBottom();
    }
    
    // Add system message to chat
    function addSystemMessage(message) {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        
        const messageHTML = `
            <div class="system-message">
                <div class="message-icon"><i class="fas fa-brain"></i></div>
                <div class="message-content">
                    <div class="message-text">${message}</div>
                    <div class="message-timestamp">${timeString}</div>
                </div>
            </div>
        `;
        
        voiceMessages.insertAdjacentHTML('beforeend', messageHTML);
        scrollMessagesToBottom();
        
        // Simulate voice response (in a real app, this would trigger TTS)
        simulateVoiceResponse(message);
    }
    
    // Scroll messages container to bottom
    function scrollMessagesToBottom() {
        voiceMessages.scrollTop = voiceMessages.scrollHeight;
    }
    
    // Process user input and generate a response
    function processUserInput(message) {
        // Simulate thinking time
        setTimeout(() => {
            let response;
            
            // Simple pattern matching for demo purposes
            if (message.toLowerCase().includes('hello') || message.toLowerCase().includes('hi')) {
                response = "Hello! I'm analyzing your behavioral patterns to assist with communication.";
            } else if (message.toLowerCase().includes('help')) {
                response = "I can help analyze your behavioral patterns, recognize gestures, and provide voice feedback.";
            } else if (message.toLowerCase().includes('name')) {
                response = "I'm AlphaVox, an AI-powered communication system designed to assist nonverbal users.";
            } else if (message.toLowerCase().includes('learn') || message.toLowerCase().includes('learning')) {
                response = "I'm continuously learning from our interactions. My neural networks are optimizing to better understand your communication patterns.";
                
                // Trigger a "learning event" for demonstration
                addLearningEvent();
            } else if (message.toLowerCase().includes('behavior') || message.toLowerCase().includes('pattern')) {
                response = "I'm currently tracking several behavioral patterns including eye movements, micro-expressions, and posture changes.";
            } else {
                // Default response
                const defaultResponses = [
                    "I've analyzed that input and am tracking the associated behavioral patterns.",
                    "Interesting input. I'm correlating this with your nonverbal cues.",
                    "I've recorded that message and am updating my understanding of your communication style.",
                    "That's been processed. I'm adapting my neural networks to better recognize similar patterns in the future."
                ];
                
                // Select a random default response
                response = defaultResponses[Math.floor(Math.random() * defaultResponses.length)];
            }
            
            // Add the response as a system message
            addSystemMessage(response);
        }, 1000); // 1 second delay to simulate processing
    }
    
    // Simulate voice response
    function simulateVoiceResponse(message) {
        // In a real implementation, this would call the TTS service
        console.log("TTS would say:", message);
    }
    
    // Speech recognition functions
    function startSpeechRecognition() {
        // Check if browser supports speech recognition
        if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            
            recognition.continuous = false;
            recognition.interimResults = false;
            
            recognition.onstart = function() {
                isListening = true;
                startListening.classList.add('active');
                addSystemMessage("I'm listening...");
            };
            
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                voiceTextInput.value = transcript;
                
                // Small delay before processing to show the text input
                setTimeout(() => {
                    addUserMessage(transcript);
                    processUserInput(transcript);
                    voiceTextInput.value = '';
                }, 500);
            };
            
            recognition.onerror = function(event) {
                console.error('Speech recognition error', event.error);
                isListening = false;
                startListening.classList.remove('active');
                
                if (event.error === 'not-allowed') {
                    addSystemMessage("Microphone access denied. Please check your browser permissions.");
                } else {
                    addSystemMessage("I couldn't hear that. Please try again.");
                }
            };
            
            recognition.onend = function() {
                isListening = false;
                startListening.classList.remove('active');
            };
            
            // Start recognition
            recognition.start();
        } else {
            addSystemMessage("Your browser doesn't support speech recognition. Please try typing instead.");
        }
    }
    
    function stopSpeechRecognition() {
        // This would stop any active speech recognition
        isListening = false;
        startListening.classList.remove('active');
    }
    
    // Initialize self-learning visualization
    function initializeSelfLearningVisuals() {
        // Check if self-learning elements exist
        if (!learningRuntime || !learningIterations || !modificationLog) {
            console.log("Self-learning visualization elements not found on this page. Skipping self-learning initialization.");
            return;
        }
        
        // Update runtime clock
        setInterval(updateRuntime, 1000);
        
        // Periodically add learning events (for demonstration)
        setInterval(addRandomLearningEvent, 30000); // Every 30 seconds
    }
    
    // Update runtime display
    function updateRuntime() {
        runtimeSeconds++;
        const hours = Math.floor(runtimeSeconds / 3600);
        const minutes = Math.floor((runtimeSeconds % 3600) / 60);
        const seconds = runtimeSeconds % 60;
        
        const formattedTime = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        learningRuntime.textContent = formattedTime;
    }
    
    // Add a learning event to the log
    function addLearningEvent(file, description) {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        
        // If parameters not provided, generate them
        if (!file || !description) {
            const files = ['app.py', 'nonverbal_engine.py', 'conversation_engine.py', 'behavior_capture.py', 'input_analyzer.py'];
            const descriptions = [
                'Optimized pattern recognition algorithm for 17% better performance',
                'Enhanced confidence scoring for micro-expressions',
                'Improved response time for vocalization processing',
                'Added new facial feature detection points',
                'Reduced memory usage by 12% through code optimization',
                'Updated eye movement correlation vectors',
                'Implemented adaptive threshold for movement detection',
                'Enhanced learning rate for repeated patterns',
                'Refined natural language generation for emotional context'
            ];
            
            file = file || files[Math.floor(Math.random() * files.length)];
            description = description || descriptions[Math.floor(Math.random() * descriptions.length)];
        }
        
        // Create log entry HTML
        const logEntryHTML = `
            <div class="log-entry">
                <div class="log-timestamp">${timeString}</div>
                <div class="log-file">${file}</div>
                <div class="log-description">${description}</div>
            </div>
        `;
        
        // Add to log and update iteration count
        modificationLog.insertAdjacentHTML('afterbegin', logEntryHTML);
        iterations++;
        learningIterations.textContent = iterations;
        
        // Trim log if it gets too long
        const entries = modificationLog.querySelectorAll('.log-entry');
        if (entries.length > 10) {
            for (let i = 10; i < entries.length; i++) {
                entries[i].remove();
            }
        }
    }
    
    // Add a random learning event
    function addRandomLearningEvent() {
        addLearningEvent();
    }
    
    // Initialize both components
    initializeVoiceInterface();
    initializeSelfLearningVisuals();
    
    // Add initial welcome message if voice messages element exists
    if (voiceMessages) {
        setTimeout(() => {
            addSystemMessage("Voice interface activated. How can I assist you today?");
        }, 1000);
    }
});