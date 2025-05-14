/**
 * AlphaVox Cyber UI System
 * This script applies futuristic UI enhancements to any AlphaVox page
 */

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing AlphaVox Cyber UI...');

    // Apply cyber UI elements
    initCyberUI();

    // Add self-learning visualization if needed
    if (document.querySelector('.add-self-learning')) {
        addSelfLearningPanel();
    }

    // Initialize voice profile selector if needed
    if (document.querySelector('.add-voice-profile')) {
        addVoiceProfileSelector();
    }

    // Initialize message history if needed
    if (document.querySelector('.add-message-history')) {
        addMessageHistoryPanel();
    }

    // Start animation loop for dynamic elements
    requestAnimationFrame(animationLoop);
});

// Global state
window.selfLearningEnabled = true;
let messageHistory = [];
let currentVoiceProfile = 'default';

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

// Self-learning optimizations (example areas)
const optimizationAreas = [
    'Intent Recognition', 'Eye Tracking', 'Speech Analysis',
    'Gesture Detection', 'Message Generation', 'Voice Synthesis',
    'Behavior Analysis', 'Context Modeling', 'Emotion Detection'
];

/**
 * Initialize the cyber UI elements
 */
function initCyberUI() {
    // Add cyber grid background if not already present
    if (!document.querySelector('.cyber-grid-overlay')) {
        const gridOverlay = document.createElement('div');
        gridOverlay.className = 'cyber-grid-overlay';
        document.body.appendChild(gridOverlay);
    }

    // Add hexagonal background if not already present
    if (!document.querySelector('.hex-bg')) {
        const hexBg = document.createElement('div');
        hexBg.className = 'hex-bg';
        document.body.appendChild(hexBg);
    }

    // Update standard elements with cyber styling
    convertStandardElementsToCyber();

    // Add pulsing effect to status indicators
    document.querySelectorAll('.badge').forEach(badge => {
        if (badge.classList.contains('bg-success')) {
            badge.style.animation = 'pulse 2s infinite';
        }
    });
}

/**
 * Convert standard Bootstrap elements to cyber-styled versions
 */
function convertStandardElementsToCyber() {
    // Convert all cards to cyber-cards
    document.querySelectorAll('.card').forEach(card => {
        if (!card.classList.contains('cyber-card')) {
            card.classList.add('cyber-card');

            // Add corner accents if not already present
            if (!card.querySelector('.card-corners')) {
                const corners = document.createElement('div');
                corners.className = 'card-corners';
                card.appendChild(corners);
            }
        }
    });

    // Convert all primary buttons to cyber-buttons
    document.querySelectorAll('.btn-primary').forEach(btn => {
        if (!btn.classList.contains('cyber-btn')) {
            btn.classList.add('cyber-btn');
        }
    });

    // Convert standard inputs to cyber-inputs
    document.querySelectorAll('input.form-control').forEach(input => {
        if (!input.classList.contains('cyber-input')) {
            input.classList.add('cyber-input');
        }
    });

    // Convert standard selects to cyber-selects
    document.querySelectorAll('select.form-select').forEach(select => {
        if (!select.classList.contains('cyber-select')) {
            select.classList.add('cyber-select');
        }
    });

    // Convert standard progress bars to cyber-progress
    document.querySelectorAll('.progress').forEach(progress => {
        if (!progress.classList.contains('cyber-progress')) {
            progress.classList.add('cyber-progress');
        }
    });

    // Apply cyber-text class to monospace elements
    document.querySelectorAll('code, .text-monospace').forEach(el => {
        if (!el.classList.contains('cyber-text')) {
            el.classList.add('cyber-text');
        }
    });

    // Apply cyber-title class to card headers
    document.querySelectorAll('.card-header h5').forEach(title => {
        if (!title.classList.contains('cyber-title')) {
            title.classList.add('cyber-title');
        }
    });

    // Convert container to cyber-container if needed
    const container = document.querySelector('.container');
    if (container && !container.classList.contains('cyber-container')) {
        container.classList.add('cyber-container');
        container.classList.remove('container');
        container.classList.add('container-fluid');
    }

    // Convert symbol-card elements
    document.querySelectorAll('.symbol-card').forEach(card => {
        // Add glow effect to icons inside symbol cards
        const icon = card.querySelector('i');
        if (icon) {
            icon.style.filter = 'drop-shadow(0 0 5px rgba(0, 148, 255, 0.5))';
        }
    });
}

/**
 * Add a self-learning status panel
 */
function addSelfLearningPanel() {
    // Create the self-learning panel
    const row = document.createElement('div');
    row.className = 'row mt-4';
    row.innerHTML = `
        <div class="col-md-12">
            <div class="card bg-dark text-white cyber-card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0 cyber-title">
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
    const targetElement = document.querySelector('.add-self-learning');
    if (targetElement) {
        const parent = targetElement.parentNode;
        parent.insertBefore(row, targetElement.nextSibling);
    } else {
        // Fallback to adding at the end of the container
        const container = document.querySelector('.container-fluid');
        if (container) {
            container.appendChild(row);
        }
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

    // Add initial status messages
    updateSelfLearningStatus('AlphaVox neural core online', true);
    updateSelfLearningStatus('Initializing adaptive learning systems', true);
    updateSelfLearningStatus('Loading behavioral models', true);
    updateSelfLearningStatus('System ready for interaction', true);
}

/**
 * Add voice profile selector
 */
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

    // Add the selector to the target element
    const targetElement = document.querySelector('.add-voice-profile');
    if (targetElement) {
        targetElement.appendChild(voiceSelector);

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

                // Update status
                if (document.getElementById('learning-status-container')) {
                    updateSelfLearningStatus(`Voice profile changed to: ${selectedProfile.name}`, true);
                }
            });
        }
    }
}

/**
 * Add message history panel
 */
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

    // Add the panel to the target element
    const targetElement = document.querySelector('.add-message-history');
    if (targetElement) {
        targetElement.appendChild(historyPanel);

        // Setup clear history button
        const clearBtn = document.getElementById('clear-history');
        if (clearBtn) {
            clearBtn.addEventListener('click', function() {
                messageHistory = [];
                updateMessageHistory();
                if (document.getElementById('learning-status-container')) {
                    updateSelfLearningStatus('Message history cleared', true);
                }
            });
        }
    }
}

/**
 * Initialize optimization bars
 */
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
                <div class="progress cyber-progress">
                    <div id="${barId}" class="progress-bar bg-info" role="progressbar"
                         style="width: ${progress * 100}%"></div>
                </div>
            </div>
        `;

        container.innerHTML += barHtml;
    });
}

/**
 * Update self-learning status
 */
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

/**
 * Update a random optimization bar
 */
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

/**
 * Add to message history
 */
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

/**
 * Update message history display
 */
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
            case 'symbol':
                iconClass = 'fas fa-th-large';
                msgClass = 'symbol-message';
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

/**
 * Format timestamp
 */
function formatTimestamp(date) {
    // Format: HH:MM:SS
    return date.toTimeString().split(' ')[0];
}

/**
 * Animation loop
 */
function animationLoop(timestamp) {
    // Update eye tracking dot position if it exists
    updateEyeTrackingDot();

    // Update self-learning status periodically if enabled
    if (window.selfLearningEnabled && Math.random() < 0.001) {
        const container = document.getElementById('learning-status-container');
        if (container) {
            const messages = [
                'Optimizing speech patterns',
                'Analyzing user behavior patterns',
                'Updating contextual awareness',
                'Refining gesture recognition',
                'Enhancing response generation',
                'Updating temporal models',
                'Improving emotional recognition',
                'Adjusting adaptive parameters'
            ];

            const randomMessage = messages[Math.floor(Math.random() * messages.length)];
            updateSelfLearningStatus(randomMessage, true);
        }
    }

    // Schedule next frame
    requestAnimationFrame(animationLoop);
}

/**
 * Update eye tracking dot position
 */
function updateEyeTrackingDot() {
    const dot = document.getElementById('eye-position-dot');
    if (!dot) return;

    const overlay = document.getElementById('eye-tracking-overlay');
    if (!overlay) return;

    // Simulate eye movement with sine waves
    const t = Date.now() / 1000;
    const width = overlay.clientWidth;
    const height = overlay.clientHeight;

    const x = width * 0.5 + Math.sin(t) * width * 0.3;
    const y = height * 0.5 + Math.cos(t * 1.3) * height * 0.3;

    dot.style.left = `${x}px`;
    dot.style.top = `${y}px`;
}

/**
 * Process text input
 */
function processTextInput(text) {
    // Show processing state
    const responseContainer = document.getElementById('response-container');
    if (!responseContainer) return;

    responseContainer.innerHTML = `
        <div class="alert alert-info cyber-response">
            <div class="d-flex align-items-center">
                <div class="me-3">
                    <i class="fas fa-cog fa-spin fa-2x"></i>
                </div>
                <div>
                    <div class="mb-2">Processing: "${text}"</div>
                    <div class="progress cyber-progress" style="height: 5px;">
                        <div class="progress-bar bg-info progress-bar-striped progress-bar-animated" style="width: 100%"></div>
                    </div>
                </div>
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
            'input_text': text,
            'voice_profile': currentVoiceProfile  // Send current voice profile
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

        // Update self-learning status
        if (document.getElementById('learning-status-container')) {
            updateSelfLearningStatus(`Processing text input: "${text}"`, true);
        }
    })
    .catch(error => {
        console.error('Error processing input:', error);
        responseContainer.innerHTML = `
            <div class="alert alert-danger cyber-response">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Error processing your input. Please try again.
            </div>
        `;
    });
}

/**
 * Process a gesture
 */
function processGesture(gesture) {
    // Show processing state
    const responseContainer = document.getElementById('response-container');
    if (!responseContainer) return;

    responseContainer.innerHTML = `
        <div class="alert alert-info cyber-response">
            <div class="d-flex align-items-center">
                <div class="me-3">
                    <i class="fas fa-hand-paper fa-2x fa-pulse"></i>
                </div>
                <div>
                    <div class="mb-2">Processing gesture: ${gesture}</div>
                    <div class="progress cyber-progress" style="height: 5px;">
                        <div class="progress-bar bg-info progress-bar-striped progress-bar-animated" style="width: 100%"></div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Call the API
    fetch(`/speak/${gesture}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            voice_profile: currentVoiceProfile  // Send current voice profile
        })
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

        // Update self-learning status
        if (document.getElementById('learning-status-container')) {
            updateSelfLearningStatus(`Processing gesture: "${gesture}"`, true);
        }
    })
    .catch(error => {
        console.error('Error processing gesture:', error);
        responseContainer.innerHTML = `
            <div class="alert alert-danger cyber-response">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Error processing your gesture. Please try again.
            </div>
        `;
    });
}

/**
 * Process a symbol
 */
function processSymbol(symbol) {
    // Show processing state
    const responseContainer = document.getElementById('symbol-response-container') ||
                             document.getElementById('response-container');
    if (!responseContainer) return;

    responseContainer.innerHTML = `
        <div class="alert alert-info cyber-response">
            <div class="d-flex align-items-center">
                <div class="me-3">
                    <i class="fas fa-th-large fa-2x fa-pulse"></i>
                </div>
                <div>
                    <div class="mb-2">Processing symbol: ${symbol}</div>
                    <div class="progress cyber-progress" style="height: 5px;">
                        <div class="progress-bar bg-info progress-bar-striped progress-bar-animated" style="width: 100%"></div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Call the API
    fetch(`/symbol/${symbol}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            voice_profile: currentVoiceProfile  // Send current voice profile
        })
    })
    .then(response => response.json())
    .then(data => {
        // Add to message history if panel exists
        if (document.getElementById('message-history-container')) {
            addToMessageHistory('symbol', `<i class="fas fa-th-large me-2"></i> ${symbol}`);
            addToMessageHistory('alphavox', data.message);
        }

        // Update recent symbols list if it exists
        updateRecentSymbols(symbol);

        // Update UI with response
        displayResponse(data, responseContainer);

        // Play audio if available
        if (data.speech_url) {
            playAudio(data.speech_url);
        }

        // Update self-learning status if panel exists
        if (document.getElementById('learning-status-container')) {
            updateSelfLearningStatus(`Processing symbol: "${symbol}"`, true);
        }
    })
    .catch(error => {
        console.error('Error processing symbol:', error);
        responseContainer.innerHTML = `
            <div class="alert alert-danger cyber-response">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Error processing your symbol. Please try again.
            </div>
        `;
    });
}

/**
 * Update recent symbols display
 */
function updateRecentSymbols(symbol) {
    const recentSymbols = document.getElementById('recent-symbols');
    if (!recentSymbols) return;

    const container = recentSymbols.querySelector('.d-flex');
    if (!container) return;

    // Symbol to icon mapping
    const symbolIcons = {
        'food': '<i class="fas fa-utensils text-warning"></i>',
        'drink': '<i class="fas fa-glass-water text-info"></i>',
        'bathroom': '<i class="fas fa-toilet text-primary"></i>',
        'medicine': '<i class="fas fa-pills text-danger"></i>',
        'happy': '<i class="fas fa-smile-beam text-warning"></i>',
        'sad': '<i class="fas fa-sad-tear text-info"></i>',
        'pain': '<i class="fas fa-head-side-virus text-danger"></i>',
        'tired': '<i class="fas fa-bed text-secondary"></i>',
        'yes': '<i class="fas fa-check-circle text-success"></i>',
        'no': '<i class="fas fa-times-circle text-danger"></i>',
        'help': '<i class="fas fa-hands-helping text-warning"></i>',
        'question': '<i class="fas fa-question-circle text-info"></i>',
        'play': '<i class="fas fa-gamepad text-success"></i>',
        'music': '<i class="fas fa-music text-primary"></i>',
        'book': '<i class="fas fa-book text-secondary"></i>',
        'outside': '<i class="fas fa-tree text-success"></i>'
    };

    // Create symbol element
    const symbolElement = document.createElement('div');
    symbolElement.className = 'recent-symbol';
    symbolElement.setAttribute('data-symbol', symbol);
    symbolElement.innerHTML = `
        ${symbolIcons[symbol] || `<i class="fas fa-square text-info"></i>`}
        <span>${symbol}</span>
    `;

    // Add click handler
    symbolElement.addEventListener('click', function() {
        processSymbol(symbol);
    });

    // Add to container (at the beginning)
    container.insertBefore(symbolElement, container.firstChild);

    // Keep only the last 5 symbols
    while (container.children.length > 5) {
        container.removeChild(container.lastChild);
    }
}

/**
 * Display a response in the UI
 */
function displayResponse(data, container = null) {
    const responseContainer = container || document.getElementById('response-container');
    if (!responseContainer) return;

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

/**
 * Play audio from a URL
 */
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

    // Create the audio element
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
