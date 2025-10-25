
"""
Stable Voice Wrapper - Prevents voice switching
"""
import json
from pathlib import Path

class StableVoiceWrapper:
    def __init__(self, voice_system):
        self.voice_system = voice_system
        self.locked_voice = None
        self.load_config()
    
    def load_config(self):
        config_file = Path("voice_config.json")
        if config_file.exists():
            with open(config_file) as f:
                self.config = json.load(f)
            self.locked_voice = self.config.get("default_voice", "matthew")
    
    def speak(self, text, voice=None, emotion='neutral'):
        """Speak with locked voice to prevent switching."""
        # Always use the locked voice, ignore voice parameter if set
        if self.config.get("voice_stability_mode", True):
            voice = self.locked_voice
        
        return self.voice_system.speak(text, voice=voice, emotion=emotion)
    
    def set_voice(self, voice_name):
        """Safely change voice and lock it."""
        if voice_name in self.voice_system.NEURAL_VOICES:
            self.locked_voice = voice_name
            self.voice_system.default_voice = voice_name
            print(f"Voice locked to: {voice_name}")
            return True
        return False
