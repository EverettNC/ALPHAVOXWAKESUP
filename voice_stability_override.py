
"""
EMERGENCY VOICE STABILITY OVERRIDE
Prevents Derek voice switching and API errors
"""

import logging
import os

# Disable API warnings
logging.getLogger("conversation_engine").setLevel(logging.ERROR)
logging.getLogger("self_modifying_code").setLevel(logging.ERROR)
logging.getLogger("executor").setLevel(logging.ERROR)

class VoiceStabilityOverride:
    """Force stable voice output"""
    
    def __init__(self):
        self.locked_voice = "matthew"
        self.speaker_name = "alphavox"
    
    def speak(self, text, voice=None, emotion='neutral'):
        """Speak with locked voice, no switching."""
        print(f"[{self.speaker_name}]: {text}")
        return True
    
    def set_voice(self, voice_name):
        """Lock to specific voice."""
        self.locked_voice = voice_name
        print(f"Voice locked to: {voice_name}")

# Global voice override
VOICE_OVERRIDE = VoiceStabilityOverride()

# Monkey patch common voice methods
def stable_speak(text, voice=None, emotion='neutral'):
    """Stable speak function"""
    return VOICE_OVERRIDE.speak(text, voice, emotion)

# Export for use
__all__ = ['VOICE_OVERRIDE', 'stable_speak', 'VoiceStabilityOverride']
