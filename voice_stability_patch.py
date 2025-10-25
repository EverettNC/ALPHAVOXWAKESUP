
# VOICE STABILITY PATCH - Prevents voice switching
def speak_stable(self, text: str, voice: str = None, emotion: str = 'neutral') -> bool:
    """
    Stable speak method that prevents voice switching.
    Uses consistent voice across all fallback layers.
    """
    if not text:
        return False
    
    # Lock to default voice to prevent switching
    locked_voice = self.default_voice
    
    # Try each layer but maintain the same voice concept
    print(f"[alphavox stable voice: {locked_voice}] {text}")
    
    # Layer 1: AWS Polly Neural (if available)
    if self.polly_client:
        try:
            if self._speak_polly_neural(text, locked_voice):
                return True
        except:
            pass
    
    # Layer 2: gTTS (consistent fallback)
    if self._speak_gtts_pygame(text):
        return True
    
    # Layer 3: Console output (always works, maintains consistency)
    print(f"\n[alphavox speaks ({locked_voice})]: {text}\n")
    return True

# Monkey patch the original speak method
alphavoxUltimateVoice.speak_original = alphavoxUltimateVoice.speak
alphavoxUltimateVoice.speak = speak_stable
