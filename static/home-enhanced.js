// AlphaVox Home Page Enhanced JS
// This script adds modern cyber UI elements and self-learning visualization
// to the AlphaVox home page

// Global state
let audioContext = null;
let audioStarted = false;
// Check if selfLearningEnabled is already defined (from cyber-ui.js)
if (typeof selfLearningEnabled === 'undefined') {
    let selfLearningEnabled = true;
}
let currentVoiceProfile = 'us_male'; // Set to male voice by default
let messageHistory = [];
let speechRecognition = null;
let isListening = false;
let isSpeaking = false;
let recognitionTimeout = null;

// Voice profile options
const voiceProfiles = [
    { id: 'default', name: 'Default Voice', description: 'Standard AlphaVox voice' },
    { id: 'calm', name: 'Calming Voice', description: 'Gentle, soothing tone for relaxation' },
    { id: 'us_female', name: 'US Female', description: 'English (US) female voice' },
    { id: 'us_male', name: 'US Male', description: 'English (US) male voice' },
    { id: 'uk_female', name: 'UK Female', description: 'English (UK) female voice' },
    { id: 'child', name: 'Child Voice', description: 'Higher pitched child-like voice' },
    { id: 'robotic', name: 'AI Assistant', description: 'Digital assistant voice with subtle robotic qualities' }
];

// Self-learning optimizations (simulated data)
const optimizationAreas = [
    'Intent Recognition', 'Eye Tracking', 'Speech Analysis',
    'Gesture Detection', 'Message Generation', 'Voice Synthesis',
    'Behavior Analysis', 'Context Modeling', 'Emotion Detection'
];

// Initialize on document load
document.addEventListener('DOMContentLoaded', function() {
    // Setup UI elements
    setupCyberUI();

    // Initialize form handlers
    initFormHandlers();

    // Initialize gesture buttons
    initGestureButtons();

    // Initialize AI assistant buttons
    initAIControls();

    // Initialize voice conversation
    initVoiceConversation();

    // Add self-learning panel
    addSelfLearningPanel();

    // Add voice profile selector
    addVoiceProfileSelector();

    // Add message history display
    addMessageHistoryPanel();

    // Start animation loop
    requestAnimationFrame(animationLoop);
});

function setupCyberUI() {
    // Add cyber grid background
    const gridOverlay = document.createElement('div');
    gridOverlay.className = 'cyber-grid-overlay';
    document.body.appendChild(gridOverlay);

    // Add glow effects to cards
    document.querySelectorAll('.card').forEach(card => {
        card.classList.add('cyber-card');

        // Add corner accents
        const corners = document.createElement('div');
        corners.className = 'card-corners';
        card.appendChild(corners);
    });

    // Add pulse effect to buttons
    document.querySelectorAll('.btn-primary').forEach(btn => {
        btn.classList.add('cyber-btn');
    });

    // Update styles for the container
    const container = document.querySelector('.container');
    if (container) {
        container.classList.add('cyber-container');
        container.classList.remove('container');
        container.classList.add('container-fluid');
    }
}

function initFormHandlers() {
    // Handle input form submission
    const inputForm = document.getElementById('input-form');
    if (inputForm) {
        inputForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const inputText = document.getElementById('input_text').value.trim();
            if (!inputText) return;

            processTextInput(inputText);
            document.getElementById('input_text').value = '';
        });
    }
}

function initGestureButtons() {
    // Set up gesture buttons
    document.querySelectorAll('.gesture-button').forEach(button => {
        button.addEventListener('click', function() {
            const gesture = this.getAttribute('data-gesture');
            processGesture(gesture);
        });
    });
}

function initAIControls() {
    // Start AI button
    const startAIBtn = document.getElementById('start-ai');
    if (startAIBtn) {
        startAIBtn.addEventListener('click', function() {
            startAI();
        });
    }

    // Stop AI button
    const stopAIBtn = document.getElementById('stop-ai');
    if (stopAIBtn) {
        stopAIBtn.addEventListener('click', function() {
            stopAI();
        });
    }
}

function processTextInput(text) {
    // Show processing state
    const responseContainer = document.getElementById('response-container');
    responseContainer.innerHTML = `
        <div class="alert alert-info">
            Processing: "${text}"
            <div class="spinner-border spinner-border-sm ms-2" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;

    // Call the API
    fetch('/process-input', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'input_text': text
        })
    })
    .then(response => response.json())
    .then(data => {
        // Add to message history
        addToMessageHistory('user', text);
        addToMessageHistory('alphavox', data.message);

        // Update UI with response
        displayResponse(data);

        // Play audio if available
        if (data.speech_url) {
            playAudio(data.speech_url);
        }

        // Simulate self-learning
        updateSelfLearningStatus(`Processing text input: "${text}"`, true);
    })
    .catch(error => {
        console.error('Error processing input:', error);
        responseContainer.innerHTML = `
            <div class="alert alert-danger">
                Error processing your input. Please try again.
            </div>
        `;
    });
}

function processGesture(gesture) {
    // Show processing state
    const responseContainer = document.getElementById('response-container');
    responseContainer.innerHTML = `
        <div class="alert alert-info">
            Processing gesture: ${gesture}
            <div class="spinner-border spinner-border-sm ms-2" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;

    // Call the API
    fetch(`/speak/${gesture}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Add to message history
        addToMessageHistory('gesture', `<i class="fas fa-hand-paper me-2"></i> ${gesture}`);
        addToMessageHistory('alphavox', data.message);

        // Update UI with response
        displayResponse(data);

        // Play audio if available
        if (data.speech_url) {
            playAudio(data.speech_url);
        }

        // Simulate self-learning
        updateSelfLearningStatus(`Processing gesture: "${gesture}"`, true);
    })
    .catch(error => {
        console.error('Error processing gesture:', error);
        responseContainer.innerHTML = `
            <div class="alert alert-danger">
                Error processing your gesture. Please try again.
            </div>
        `;
    });
}

function displayResponse(data) {
    const responseContainer = document.getElementById('response-container');

    // Determine alert type based on expression
    let alertClass = 'alert-info';
    let icon = 'fas fa-comment';

    switch (data.expression) {
        case 'positive':
            alertClass = 'alert-success';
            icon = 'fas fa-smile';
            break;
        case 'negative':
            alertClass = 'alert-secondary';
            icon = 'fas fa-frown';
            break;
        case 'urgent':
            alertClass = 'alert-warning';
            icon = 'fas fa-exclamation-triangle';
            break;
        case 'inquisitive':
            alertClass = 'alert-info';
            icon = 'fas fa-question-circle';
            break;
    }

    // Format the response
    responseContainer.innerHTML = `
        <div class="alert ${alertClass} cyber-response">
            <div class="d-flex align-items-start">
                <div class="me-3">
                    <i class="${icon} fa-2x"></i>
                </div>
                <div>
                    <div class="mb-2">${data.message}</div>
                    <div class="small text-muted d-flex justify-content-between">
                        <span>Intent: ${data.intent}</span>
                        <span>Confidence: ${(data.confidence * 100).toFixed(1)}%</span>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function initVoiceConversation() {
    // Set up the voice conversation toggle button
    const toggleVoiceBtn = document.getElementById('toggle-voice-btn');
    if (toggleVoiceBtn) {
        toggleVoiceBtn.addEventListener('click', toggleVoiceInput);
    }

    // Play welcome greeting with male voice when page loads
    playWelcomeGreeting();

    // Initialize speech recognition if available
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        speechRecognition = new SpeechRecognition();
        speechRecognition.continuous = false;
        speechRecognition.interimResults = false;
        speechRecognition.lang = 'en-US';

        // Configure speech recognition events
        speechRecognition.onstart = function() {
            updateVoiceStatus('listening');
            isListening = true;

            // Start visualizing
            const visualizer = document.getElementById('voice-visualization');
            if (visualizer) {
                visualizer.classList.add('voice-active');
            }

            // Update button text
            const toggleBtn = document.getElementById('toggle-voice-btn');
            if (toggleBtn) {
                toggleBtn.querySelector('span').textContent = 'Stop Listening';
                toggleBtn.classList.add('btn-danger');
                toggleBtn.classList.remove('neural-btn');
                toggleBtn.querySelector('i').classList.remove('fa-microphone');
                toggleBtn.querySelector('i').classList.add('fa-microphone-slash');
            }

            // Auto-stop after 10 seconds if no speech detected
            clearTimeout(recognitionTimeout);
            recognitionTimeout = setTimeout(() => {
                if (isListening) {
                    stopVoiceInput();
                    updateSelfLearningStatus('Voice input timed out', false);
                }
            }, 10000);
        };

        speechRecognition.onresult = function(event) {
            clearTimeout(recognitionTimeout);
            const transcript = event.results[0][0].transcript;
            const confidence = event.results[0][0].confidence;

            updateVoiceStatus('processing');

            // Update self-learning display
            updateSelfLearningStatus(`Processing voice input: "${transcript}"`, true);

            // Process the voice input
            processTextInput(transcript);

            // Stop listening after processing
            stopVoiceInput();
        };

        speechRecognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            updateVoiceStatus('error');
            updateSelfLearningStatus(`Voice recognition error: ${event.error}`, false);
            stopVoiceInput();
        };

        speechRecognition.onend = function() {
            if (isListening) {
                stopVoiceInput();
            }
        };
    } else {
        // Hide or disable voice features if not supported
        const voiceInterface = document.querySelector('.conversation-interface');
        if (voiceInterface) {
            voiceInterface.innerHTML = `
                <div class="alert alert-warning">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Voice conversation is not supported in this browser. Please try using a modern browser like Chrome.
                </div>
            `;
        }

        updateSelfLearningStatus('Voice recognition not supported', false);
    }
}

function toggleVoiceInput() {
    if (isListening) {
        stopVoiceInput();
    } else {
        startVoiceInput();
    }
}

function playWelcomeGreeting() {
    // Get the username from the greeting element
    const userGreeting = document.getElementById('user-greeting');
    const username = userGreeting ? userGreeting.getAttribute('data-username') : 'User';

    // Create a custom greeting with the user's name
    const timeOfDay = getTimeOfDay();
    const greeting = `${timeOfDay}! Welcome back, ${username}. I'm ready to help you communicate.`;

    // Call the greeting API to speak with male voice
    fetch('/speak/greeting', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: greeting
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.speech_url) {
            playAudio(data.speech_url);
        }
    })
    .catch(error => {
        console.error('Error with welcome greeting:', error);
    });
}

function getTimeOfDay() {
    const hour = new Date().getHours();
    if (hour < 12) return "Good morning";
    if (hour < 18) return "Good afternoon";
    return "Good evening";
}

function startVoiceInput() {
    if (!speechRecognition) return;

    try {
        // Play a start tone
        playBeepSound('start');

        // Start after a slight delay to give audio time to play
        setTimeout(() => {
            speechRecognition.start();
            updateSelfLearningStatus('Voice input started', true);
        }, 300);
    } catch (error) {
        console.error('Error starting speech recognition:', error);
        updateVoiceStatus('error');
    }
}

function stopVoiceInput() {
    if (!speechRecognition) return;

    try {
        speechRecognition.stop();
        isListening = false;

        // Play a stop tone
        playBeepSound('stop');

        // Stop visualizing
        const visualizer = document.getElementById('voice-visualization');
        if (visualizer) {
            visualizer.classList.remove('voice-active');
        }

        // Update button text
        const toggleBtn = document.getElementById('toggle-voice-btn');
        if (toggleBtn) {
            toggleBtn.querySelector('span').textContent = 'Start Conversation';
            toggleBtn.classList.remove('btn-danger');
            toggleBtn.classList.add('neural-btn');
            toggleBtn.querySelector('i').classList.add('fa-microphone');
            toggleBtn.querySelector('i').classList.remove('fa-microphone-slash');
        }

        // Reset status
        updateVoiceStatus('ready');
    } catch (error) {
        console.error('Error stopping speech recognition:', error);
    }
}

function updateVoiceStatus(status) {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-text');

    if (!statusDot || !statusText) return;

    // Remove all status classes
    statusDot.classList.remove('listening', 'processing', 'speaking');

    switch (status) {
        case 'listening':
            statusDot.classList.add('listening');
            statusText.textContent = 'Listening...';
            break;
        case 'processing':
            statusDot.classList.add('processing');
            statusText.textContent = 'Processing...';
            break;
        case 'speaking':
            statusDot.classList.add('speaking');
            statusText.textContent = 'Speaking...';
            break;
        case 'error':
            statusText.textContent = 'Error';
            break;
        default:
            statusText.textContent = 'Ready';
    }
}

function processVoiceInput(text) {
    // First, add the voice input to the message history
    addToMessageHistory('user', `<i class="fas fa-microphone me-2"></i> ${text}`);

    // Then process it like a text input
    processTextInput(text);
}

function startAI() {
    // Update AI status
    const aiStatus = document.getElementById('ai-status');
    aiStatus.innerHTML = `<span class="badge bg-success">Active</span>`;

    // Show stop button, hide start button
    document.getElementById('start-ai').style.display = 'none';
    document.getElementById('stop-ai').style.display = 'inline-block';

    // Make API call to start AI
    fetch('/start-ai', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Show success message
            const responseContainer = document.getElementById('response-container');
            responseContainer.innerHTML = `
                <div class="alert alert-success">
                    <i class="fas fa-robot me-2"></i>
                    ${data.message}
                </div>
            `;

            // Play audio if available
            if (data.speech_url) {
                playAudio(data.speech_url);
            }

            // Start self-learning visualization
            window.selfLearningEnabled = true;
            updateSelfLearningStatus('AI Assistant activated', true);
        }
    })
    .catch(error => {
        console.error('Error starting AI:', error);
    });
}

function stopAI() {
    // Update AI status
    const aiStatus = document.getElementById('ai-status');
    aiStatus.innerHTML = `<span class="badge bg-secondary">Inactive</span>`;

    // Show start button, hide stop button
    document.getElementById('start-ai').style.display = 'inline-block';
    document.getElementById('stop-ai').style.display = 'none';

    // Make API call to stop AI
    fetch('/stop-ai', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Show success message
            const responseContainer = document.getElementById('response-container');
            responseContainer.innerHTML = `
                <div class="alert alert-warning">
                    <i class="fas fa-power-off me-2"></i>
                    ${data.message}
                </div>
            `;

            // Pause self-learning visualization
            window.selfLearningEnabled = false;
            updateSelfLearningStatus('AI Assistant deactivated', false);
        }
    })
    .catch(error => {
        console.error('Error stopping AI:', error);
    });
}

function playAudio(url) {
    console.log('Playing audio from:', url);

    // Create a visible audio element to ensure it works across browsers
    let audioContainer = document.getElementById('audio-container');
    if (!audioContainer) {
        audioContainer = document.createElement('div');
        audioContainer.id = 'audio-container';
        audioContainer.style.position = 'absolute';
        audioContainer.style.bottom = '0';
        audioContainer.style.left = '0';
        audioContainer.style.width = '1px';
        audioContainer.style.height = '1px';
        audioContainer.style.overflow = 'hidden';
        document.body.appendChild(audioContainer);
    }

    // Clear previous audio if any
    audioContainer.innerHTML = '';

    // Create the audio element with controls
    const audioPlayer = document.createElement('audio');
    audioPlayer.controls = false; // Set to true for debugging
    audioPlayer.src = url;
    audioPlayer.style.width = '1px';
    audioPlayer.style.height = '1px';

    // Add to DOM
    audioContainer.appendChild(audioPlayer);

    // Add error handling
    audioPlayer.onerror = function(error) {
        console.error('Error playing audio:', error);
    };

    // Play the audio
    setTimeout(() => {
        try {
            audioPlayer.play()
                .then(() => console.log('Audio playback started successfully'))
                .catch(error => {
                    console.error('Error playing audio:', error);

                    // If autoplay fails, show controls and try again
                    audioPlayer.controls = true;
                    audioPlayer.style.width = '300px';
                    audioPlayer.style.height = '40px';
                });
        } catch (error) {
            console.error('Exception while playing audio:', error);
        }
    }, 100);
}

function addSelfLearningPanel() {
    // Create the self-learning panel
    const row = document.createElement('div');
    row.className = 'row mt-4';
    row.innerHTML = `
        <div class="col-md-12">
            <div class="card bg-dark text-white cyber-card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">
                        <i class="fas fa-brain me-2"></i>
                        Self-Learning Status
                    </h5>
                    <div class="form-check form-switch">
                        <input class="form-check-input" type="checkbox" id="enable-learning" checked>
                        <label class="form-check-label" for="enable-learning">Enable Learning</label>
                    </div>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-7">
                            <div id="learning-status-container" class="learning-status-container">
                                <div class="status-line">
                                    <span class="timestamp">
                                        [${formatTimestamp(new Date())}]
                                    </span>
                                    <span class="status-message">
                                        Self-learning system initialized
                                    </span>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-5">
                            <div class="optimization-container">
                                <h6 class="optimization-header">
                                    <i class="fas fa-cogs me-2"></i>
                                    Current Optimizations
                                </h6>
                                <div id="optimization-bars">
                                    <!-- Optimization bars will be added here -->
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-corners"></div>
            </div>
        </div>
    `;

    // Find the right position to insert the panel
    const container = document.querySelector('.container-fluid');
    if (container) {
        const lastRow = container.querySelector('.row:last-child');
        container.insertBefore(row, lastRow.nextSibling);
    }

    // Initialize optimization bars
    initOptimizationBars();

    // Set up learning toggle
    const learningToggle = document.getElementById('enable-learning');
    if (learningToggle) {
        learningToggle.addEventListener('change', function() {
            window.selfLearningEnabled = this.checked;
            updateSelfLearningStatus(
                window.selfLearningEnabled ? 'Self-learning enabled' : 'Self-learning paused',
                window.selfLearningEnabled
            );
        });
    }
}

function addVoiceProfileSelector() {
    // Create voice profile selector
    const voiceSelector = document.createElement('div');
    voiceSelector.className = 'voice-profile-selector mt-3';
    voiceSelector.innerHTML = `
        <label for="voice-profile" class="form-label d-flex justify-content-between align-items-center">
            <span>Voice Profile</span>
            <i class="fas fa-info-circle" data-bs-toggle="tooltip" title="Select different voice characteristics"></i>
        </label>
        <select class="form-select cyber-select" id="voice-profile">
            ${voiceProfiles.map(profile => `
                <option value="${profile.id}" ${profile.id === 'default' ? 'selected' : ''}>
                    ${profile.name}
                </option>
            `).join('')}
        </select>
        <div class="voice-description small text-muted mt-1" id="voice-description">
            ${voiceProfiles[0].description}
        </div>
    `;

    // Add the selector to the communication card
    const communicationCard = document.querySelector('.card:nth-child(1)');
    if (communicationCard) {
        const cardBody = communicationCard.querySelector('.card-body');
        cardBody.appendChild(voiceSelector);

        // Set up voice profile change handler
        const voiceProfileSelect = document.getElementById('voice-profile');
        if (voiceProfileSelect) {
            voiceProfileSelect.addEventListener('change', function() {
                currentVoiceProfile = this.value;

                // Update description
                const selectedProfile = voiceProfiles.find(p => p.id === currentVoiceProfile);
                if (selectedProfile) {
                    document.getElementById('voice-description').textContent = selectedProfile.description;
                }

                updateSelfLearningStatus(`Voice profile changed to: ${selectedProfile.name}`, true);
            });
        }
    }
}

function addMessageHistoryPanel() {
    // Create message history panel
    const historyPanel = document.createElement('div');
    historyPanel.className = 'message-history-panel mt-3';
    historyPanel.innerHTML = `
        <h6 class="d-flex justify-content-between align-items-center">
            <span>Message History</span>
            <button class="btn btn-sm btn-outline-danger" id="clear-history">
                <i class="fas fa-trash-alt"></i>
            </button>
        </h6>
        <div class="message-history-container" id="message-history-container">
            <div class="text-muted text-center py-3">No messages yet</div>
        </div>
    `;

    // Add the panel to the communication card
    const communicationCard = document.querySelector('.col-md-6:nth-child(2) .card:nth-child(1)');
    if (communicationCard) {
        const cardBody = communicationCard.querySelector('.card-body');
        cardBody.appendChild(historyPanel);

        // Setup clear history button
        const clearBtn = document.getElementById('clear-history');
        if (clearBtn) {
            clearBtn.addEventListener('click', function() {
                messageHistory = [];
                updateMessageHistory();
                updateSelfLearningStatus('Message history cleared', true);
            });
        }
    }
}

function addToMessageHistory(type, content) {
    // Add message to history
    messageHistory.push({
        type: type,
        content: content,
        timestamp: new Date()
    });

    // Keep only the last 10 messages
    if (messageHistory.length > 10) {
        messageHistory.shift();
    }

    // Update the display
    updateMessageHistory();
}

function updateMessageHistory() {
    const container = document.getElementById('message-history-container');
    if (!container) return;

    if (messageHistory.length === 0) {
        container.innerHTML = '<div class="text-muted text-center py-3">No messages yet</div>';
        return;
    }

    // Create HTML for messages
    const messagesHtml = messageHistory.map(msg => {
        let iconClass = 'fas fa-comment';
        let msgClass = '';

        switch (msg.type) {
            case 'user':
                iconClass = 'fas fa-user';
                msgClass = 'user-message';
                break;
            case 'alphavox':
                iconClass = 'fas fa-robot';
                msgClass = 'ai-message';
                break;
            case 'gesture':
                iconClass = 'fas fa-hand-paper';
                msgClass = 'gesture-message';
                break;
        }

        return `
            <div class="history-message ${msgClass}">
                <div class="message-icon">
                    <i class="${iconClass}"></i>
                </div>
                <div class="message-content">
                    <div class="message-text">${msg.content}</div>
                    <div class="message-time">${formatTimestamp(msg.timestamp)}</div>
                </div>
            </div>
        `;
    }).join('');

    container.innerHTML = messagesHtml;

    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
}

function initOptimizationBars() {
    const container = document.getElementById('optimization-bars');
    if (!container) return;

    // Create optimization bars for each area
    optimizationAreas.forEach((area, index) => {
        const progress = Math.random() * 0.5 + 0.3; // Random progress between 30% and 80%
        const barId = `opt-bar-${index}`;

        const barHtml = `
            <div class="optimization-item">
                <div class="d-flex justify-content-between">
                    <small>${area}</small>
                    <small id="${barId}-value">${Math.round(progress * 100)}%</small>
                </div>
                <div class="progress">
                    <div id="${barId}" class="progress-bar bg-info" role="progressbar"
                         style="width: ${progress * 100}%"></div>
                </div>
            </div>
        `;

        container.innerHTML += barHtml;
    });
}

function updateSelfLearningStatus(message, enabled) {
    const container = document.getElementById('learning-status-container');
    if (!container) return;

    // Add new status message
    const statusLine = document.createElement('div');
    statusLine.className = 'status-line';
    statusLine.innerHTML = `
        <span class="timestamp">[${formatTimestamp(new Date())}]</span>
        <span class="status-message ${enabled ? '' : 'status-disabled'}">${message}</span>
    `;

    container.appendChild(statusLine);

    // Keep only the last 10 status messages
    while (container.children.length > 10) {
        container.removeChild(container.firstChild);
    }

    // Scroll to bottom
    container.scrollTop = container.scrollHeight;

    // Update a random optimization bar
    if (enabled) {
        updateRandomOptimizationBar();
    }
}

function updateRandomOptimizationBar() {
    // Pick a random optimization area
    const index = Math.floor(Math.random() * optimizationAreas.length);
    const barId = `opt-bar-${index}`;

    const bar = document.getElementById(barId);
    const barValue = document.getElementById(`${barId}-value`);

    if (bar && barValue) {
        // Get current width and increase it slightly
        let currentWidth = parseFloat(bar.style.width);
        if (isNaN(currentWidth)) currentWidth = 50;

        // Increment by a small amount
        let newWidth = Math.min(currentWidth + Math.random() * 5, 100);

        // Animate the change
        bar.style.width = `${newWidth}%`;
        barValue.textContent = `${Math.round(newWidth)}%`;
    }
}

function formatTimestamp(date) {
    // Format: HH:MM:SS
    return date.toTimeString().split(' ')[0];
}

function playBeepSound(type) {
    // Create audio context if it doesn't exist
    if (!audioContext) {
        try {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.error('Web Audio API not supported:', e);
            return;
        }
    }

    // Different parameters for different sound types
    let frequency = 0, duration = 0, waveType = 'sine', volume = 0.2;

    switch(type) {
        case 'start':
            // Rising beep
            frequency = 880;
            duration = 0.15;
            volume = 0.15;
            break;
        case 'stop':
            // Falling beep
            frequency = 440;
            duration = 0.15;
            volume = 0.15;
            break;
        case 'error':
            // Error sound
            frequency = 220;
            duration = 0.3;
            volume = 0.25;
            waveType = 'sawtooth';
            break;
        default:
            frequency = 660;
            duration = 0.1;
    }

    // Create oscillator and gain node
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    // Configure oscillator
    oscillator.type = waveType;
    oscillator.frequency.value = frequency;

    // Configure gain (volume)
    gainNode.gain.value = volume;

    // Connect nodes
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    // Schedule automatic stop
    oscillator.start();
    oscillator.stop(audioContext.currentTime + duration);
}

function animationLoop(timestamp) {
    // Update matrix effect if desired

    // Schedule next frame
    requestAnimationFrame(animationLoop);
}

// Add the necessary CSS
document.head.insertAdjacentHTML('beforeend', `
<style>
/* Base styling */
body {
    font-family: 'Roboto', sans-serif;
    background-color: #000820;
    color: #fff;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}

.container-fluid {
    padding: 20px;
}

/* Cyber UI components */
.cyber-container {
    background-color: rgba(10, 20, 40, 0.8);
    border: 1px solid rgba(0, 125, 255, 0.4);
    border-radius: 4px;
    padding: 20px;
    position: relative;
}

.cyber-card {
    background: linear-gradient(to bottom, #0a1428, #061224);
    border: 1px solid rgba(0, 125, 255, 0.4);
    border-radius: 4px;
    box-shadow: 0 0 15px rgba(0, 98, 255, 0.15);
    transition: all 0.3s ease;
    overflow: hidden;
    position: relative;
}

.cyber-card:hover {
    box-shadow: 0 0 20px rgba(0, 98, 255, 0.25);
}

.card-corners {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    pointer-events: none;
}

.card-corners::before,
.card-corners::after {
    content: '';
    position: absolute;
    width: 10px;
    height: 10px;
    border: 2px solid rgba(0, 148, 255, 0.7);
}

.card-corners::before {
    top: -1px;
    left: -1px;
    border-right: none;
    border-bottom: none;
}

.card-corners::after {
    bottom: -1px;
    right: -1px;
    border-left: none;
    border-top: none;
}

.cyber-btn {
    background: linear-gradient(to bottom, #0066cc, #004c99);
    border: 1px solid rgba(0, 148, 255, 0.7);
    color: white;
    position: relative;
    overflow: hidden;
}

.cyber-btn::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -60%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        to right,
        rgba(255, 255, 255, 0) 0%,
        rgba(255, 255, 255, 0.1) 100%
    );
    transform: rotate(30deg);
    transition: transform 0.5s;
}

.cyber-btn:hover::after {
    transform: rotate(30deg) translate(10%, 10%);
}

.cyber-grid-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-image:
        linear-gradient(rgba(0, 30, 60, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 30, 60, 0.05) 1px, transparent 1px);
    background-size: 20px 20px;
    pointer-events: none;
    z-index: -1;
}

.cyber-response {
    background-color: rgba(15, 30, 50, 0.7);
    border-left: 3px solid rgba(0, 125, 255, 0.7);
    box-shadow: 0 0 10px rgba(0, 98, 255, 0.15);
}

/* Video feed styling */
.video-feed {
    width: 100%;
    border-radius: 4px;
    height: 300px;
    object-fit: cover;
}

.eye-tracking-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}

.eye-position-dot {
    position: absolute;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background-color: rgba(0, 255, 255, 0.7);
    border: 2px solid rgba(255, 255, 255, 0.7);
    transform: translate(-50%, -50%);
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
    pointer-events: none;
}

/* Gesture buttons */
.gesture-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
}

.gesture-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 80px;
    height: 80px;
    background-color: rgba(30, 40, 60, 0.7);
    border: 1px solid rgba(100, 150, 255, 0.4);
    transition: all 0.2s ease;
}

.gesture-button:hover {
    transform: translateY(-3px);
    background-color: rgba(40, 50, 80, 0.7);
    border-color: rgba(100, 150, 255, 0.8);
    box-shadow: 0 5px 15px rgba(0, 60, 120, 0.3);
}

.gesture-button i {
    font-size: 1.5rem;
    margin-bottom: 5px;
}

.gesture-button div {
    font-size: 0.7rem;
    text-align: center;
}

/* Self learning system styling */
.learning-status-container {
    background-color: rgba(0, 20, 40, 0.7);
    border: 1px solid rgba(0, 125, 255, 0.4);
    border-radius: 4px;
    padding: 10px;
    height: 150px;
    overflow-y: auto;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
}

.status-line {
    margin-bottom: 5px;
    line-height: 1.3;
    animation: fadeIn 0.3s ease;
}

.timestamp {
    color: #0094ff;
    margin-right: 8px;
}

.status-message {
    color: rgba(255, 255, 255, 0.9);
}

.status-disabled {
    color: rgba(255, 255, 255, 0.5);
}

.optimization-container {
    padding: 10px;
    background-color: rgba(0, 20, 40, 0.7);
    border: 1px solid rgba(0, 125, 255, 0.4);
    border-radius: 4px;
}

.optimization-header {
    margin-bottom: 15px;
    color: #0094ff;
}

.optimization-item {
    margin-bottom: 12px;
}

.progress {
    height: 8px;
    background-color: rgba(0, 20, 40, 0.5);
}

.progress-bar {
    transition: width 0.8s ease-in-out;
}

/* Voice profile selector */
.voice-profile-selector {
    background-color: rgba(0, 20, 40, 0.5);
    border-radius: 4px;
    padding: 10px;
    margin-top: 15px;
}

.cyber-select {
    background-color: rgba(10, 30, 50, 0.7);
    color: white;
    border: 1px solid rgba(0, 125, 255, 0.4);
}

.cyber-select:focus {
    box-shadow: 0 0 0 0.25rem rgba(0, 125, 255, 0.25);
    border-color: rgba(0, 125, 255, 0.7);
}

/* Message history styling */
.message-history-panel {
    background-color: rgba(0, 20, 40, 0.5);
    border-radius: 4px;
    padding: 10px;
}

.message-history-container {
    max-height: 150px;
    overflow-y: auto;
    margin-top: 10px;
}

.history-message {
    display: flex;
    margin-bottom: 8px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(0, 125, 255, 0.2);
}

.history-message:last-child {
    border-bottom: none;
}

.message-icon {
    margin-right: 10px;
    color: #0094ff;
}

.message-content {
    flex: 1;
}

.message-text {
    margin-bottom: 3px;
}

.message-time {
    font-size: 0.7rem;
    color: rgba(255, 255, 255, 0.5);
}

.user-message .message-icon {
    color: #00cc99;
}

.ai-message .message-icon {
    color: #0094ff;
}

.gesture-message .message-icon {
    color: #ff9900;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-5px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(0, 148, 255, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(0, 148, 255, 0); }
    100% { box-shadow: 0 0 0 0 rgba(0, 148, 255, 0); }
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
</style>
`);
