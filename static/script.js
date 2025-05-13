/**
 * AlphaVox - Main JavaScript
 * Handles client-side interactions for the AlphaVox communication system
 */

// Global response update function to ensure it's available before DOM content is loaded
/**
 * Update the response display with a message
 * @param {object} response - The response object containing message, intent, etc.
 */
function updateResponse(response) {
    const responseContainer = document.getElementById('response-container');
    if (!responseContainer) return;
    
    // Create message element
    const messageElement = document.createElement('div');
    messageElement.className = 'alert alert-info feedback-message';
    
    // Show the intent and confidence if available
    let messageText = response.message || "Response received";
    
    // Add technical details in small text
    if (response.intent && response.confidence) {
        messageText += `<br><small class="text-muted">Intent: ${response.intent} (Confidence: ${(response.confidence * 100).toFixed(1)}%)</small>`;
    }
    
    // Add advanced AI badge if applicable
    if (response.advanced_ai) {
        messageText += `<br><span class="badge bg-info">Advanced AI</span>`;
    }
    
    messageElement.innerHTML = messageText;
    
    // Add to response container
    responseContainer.innerHTML = '';
    responseContainer.appendChild(messageElement);
    
    // Play audio if a speech URL is provided
    if (response.speech_url) {
        playAudio(response.speech_url);
    }
}

/**
 * Play audio from a URL
 * @param {string} url - The URL of the audio file to play
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
    
    // Create the audio element with controls (helps with debugging)
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
    
    // Play the audio with a button click simulation for mobile
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
 
// Auto-greeting functionality
document.addEventListener('DOMContentLoaded', function() {
    // Check if we should play the welcome greeting
    setTimeout(function() {
        // Play welcome greeting on home page
        if (window.location.pathname.includes('/home')) {
            playWelcomeGreeting();
        }
    }, 1000); // Slight delay to ensure page is fully loaded
});

/**
 * Play welcome greeting based on time of day and user history
 */
function playWelcomeGreeting() {
    const currentHour = new Date().getHours();
    let greeting = "";
    
    // Get time-appropriate greeting
    if (currentHour >= 5 && currentHour < 12) {
        greeting = "Good morning! Welcome to AlphaVox. I'm ready to help you communicate.";
    } else if (currentHour >= 12 && currentHour < 18) {
        greeting = "Good afternoon! Welcome to AlphaVox. How can I assist with your communication today?";
    } else {
        greeting = "Good evening! Welcome to AlphaVox. I'm here to help you express yourself.";
    }
    
    // Get username if available
    const username = document.querySelector('.navbar-text')?.textContent?.trim() || 
                    document.getElementById('user-greeting')?.getAttribute('data-username') || '';
    
    if (username) {
        greeting = greeting.replace('Welcome to AlphaVox.', `Welcome back, ${username}.`);
    }
    
    // Update UI with greeting
    updateResponse({
        message: greeting,
        intent: 'greet',
        confidence: 0.95,
        expression: 'positive',
        emotion_tier: 'moderate'
    });
    
    // Check if text-to-speech should be used
    speakGreeting(greeting);
}

/**
 * Speak the greeting using text-to-speech
 */
function speakGreeting(greeting) {
    // Use our API endpoint to generate speech
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

document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    let aiRunning = false;
    let lastResponse = null;
    
    // DOM elements
    const responseContainer = document.getElementById('response-container');
    const startAiButton = document.getElementById('start-ai');
    const stopAiButton = document.getElementById('stop-ai');
    const gestureButtons = document.querySelectorAll('.gesture-button');
    const inputForm = document.getElementById('input-form');
    const aiStatusIndicator = document.getElementById('ai-status');
    
    // Initialize the UI
    if (stopAiButton) stopAiButton.style.display = 'none';
    
    // Use the global updateResponse function defined earlier
    
    // Setup gesture buttons
    if (gestureButtons) {
        gestureButtons.forEach(button => {
            button.addEventListener('click', function() {
                const gesture = this.dataset.gesture;
                
                // Provide visual feedback
                this.classList.add('active');
                setTimeout(() => this.classList.remove('active'), 200);
                
                // Send gesture to server
                fetch(`/speak/${gesture}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    updateResponse(data);
                })
                .catch(error => {
                    console.error('Error:', error);
                    responseContainer.innerHTML = '<div class="alert alert-danger">Error communicating with server</div>';
                });
            });
        });
    }
    
    // Setup input form
    if (inputForm) {
        inputForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(inputForm);
            
            fetch('/process-input', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                updateResponse(data);
                // Clear the input field
                document.getElementById('input_text').value = '';
            })
            .catch(error => {
                console.error('Error:', error);
                responseContainer.innerHTML = '<div class="alert alert-danger">Error communicating with server</div>';
            });
        });
    }
    
    // Setup AI control buttons
    if (startAiButton) {
        startAiButton.addEventListener('click', function() {
            fetch('/start-ai', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'started' || data.status === 'already_running') {
                    aiRunning = true;
                    startAiButton.style.display = 'none';
                    stopAiButton.style.display = 'inline-block';
                    aiStatusIndicator.innerHTML = '<span class="badge bg-success">Active</span>';
                    
                    responseContainer.innerHTML = '<div class="alert alert-success">AI assistance activated</div>';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                responseContainer.innerHTML = '<div class="alert alert-danger">Error starting AI</div>';
            });
        });
    }
    
    if (stopAiButton) {
        stopAiButton.addEventListener('click', function() {
            fetch('/stop-ai', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'stopped') {
                    aiRunning = false;
                    stopAiButton.style.display = 'none';
                    startAiButton.style.display = 'inline-block';
                    aiStatusIndicator.innerHTML = '<span class="badge bg-secondary">Inactive</span>';
                    
                    responseContainer.innerHTML = '<div class="alert alert-warning">AI assistance deactivated</div>';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                responseContainer.innerHTML = '<div class="alert alert-danger">Error stopping AI</div>';
            });
        });
    }
    
    // Simulate eye tracking visualization in the browser
    const eyeTrackingOverlay = document.getElementById('eye-tracking-overlay');
    const eyePositionDot = document.getElementById('eye-position-dot');
    
    if (eyeTrackingOverlay && eyePositionDot) {
        // Initialize with center position
        let eyePosition = { x: 0.5, y: 0.5 };
        
        // Function to update eye position randomly (for simulation)
        function updateEyePosition() {
            // Move towards a random target with some inertia
            const targetX = Math.random();
            const targetY = Math.random();
            
            eyePosition.x += (targetX - eyePosition.x) * 0.2;
            eyePosition.y += (targetY - eyePosition.y) * 0.2;
            
            // Update dot position
            eyePositionDot.style.left = `${eyePosition.x * 100}%`;
            eyePositionDot.style.top = `${eyePosition.y * 100}%`;
            
            // Call again after random delay (slower than real eye tracking)
            setTimeout(updateEyePosition, 1000 + Math.random() * 1000);
        }
        
        // Start simulation if we're on the home page
        if (window.location.pathname.includes('/home')) {
            updateEyePosition();
        }
    }
});
