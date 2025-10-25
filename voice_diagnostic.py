#!/usr/bin/env python3
"""
Voice Configuration Test and Fix Script
Diagnose and fix AlphaVox voice switching issues
"""

import os
import sys
import json
import boto3
from pathlib import Path

def check_aws_credentials():
    """Check if AWS credentials are properly configured."""
    print("🔍 Checking AWS credentials...")
    
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY') 
    region = os.getenv('AWS_REGION', 'us-east-1')
    
    if not access_key or not secret_key:
        print("❌ AWS credentials not found in environment variables")
        print("   Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        return False
    
    try:
        polly = boto3.client('polly', region_name=region)
        response = polly.describe_voices(Engine='neural', LanguageCode='en-US')
        print(f"✅ AWS Polly connection successful - {len(response['Voices'])} neural voices available")
        return True
    except Exception as e:
        print(f"❌ AWS Polly connection failed: {e}")
        return False

def check_voice_configuration():
    """Check current voice configuration."""
    print("\n🎤 Checking voice configuration...")
    
    # Check if alphavox_ultimate_voice.py exists and is valid
    voice_file = Path("alphavox_ultimate_voice.py")
    if not voice_file.exists():
        print("❌ alphavox_ultimate_voice.py not found")
        return False
    
    print("✅ Voice module file found")
    
    # Try to import and check configuration
    try:
        sys.path.insert(0, '.')
        from alphavox_ultimate_voice import alphavoxUltimateVoice
        
        voice_system = alphavoxUltimateVoice()
        print(f"✅ Voice system initialized")
        print(f"   Default voice: {voice_system.default_voice}")
        print(f"   Available voices: {list(voice_system.NEURAL_VOICES.keys())}")
        
        return voice_system
    except Exception as e:
        print(f"❌ Failed to initialize voice system: {e}")
        return False

def test_voice_stability(voice_system):
    """Test if voice switching is happening."""
    print("\n🧪 Testing voice stability...")
    
    test_text = "This is a voice stability test. I should speak in one consistent voice."
    
    print(f"Testing with default voice: {voice_system.default_voice}")
    
    # Test multiple speak calls
    for i in range(3):
        print(f"   Test {i+1}/3...")
        success = voice_system.speak(test_text)
        if success:
            print(f"   ✅ Speech {i+1} successful")
        else:
            print(f"   ❌ Speech {i+1} failed")

def fix_voice_configuration():
    """Apply fixes for common voice switching issues."""
    print("\n🔧 Applying voice configuration fixes...")
    
    # Create/update voice configuration file
    config = {
        "default_voice": "matthew",
        "voice_stability_mode": True,
        "fallback_chain": {
            "prefer_neural": True,
            "stick_to_voice": True,
            "avoid_switching": True
        },
        "aws_config": {
            "region": os.getenv('AWS_REGION', 'us-east-1'),
            "engine_preference": "neural"
        }
    }
    
    config_file = Path("voice_config.json")
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Voice configuration saved to {config_file}")
    
    # Create a stable voice wrapper
    wrapper_code = '''
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
'''
    
    wrapper_file = Path("stable_voice_wrapper.py")
    with open(wrapper_file, 'w') as f:
        f.write(wrapper_code)
    
    print(f"✅ Stable voice wrapper created: {wrapper_file}")

def main():
    print("🎯 AlphaVox Voice Configuration Diagnostic & Fix")
    print("=" * 50)
    
    # Step 1: Check AWS credentials
    aws_ok = check_aws_credentials()
    
    # Step 2: Check voice configuration
    voice_system = check_voice_configuration()
    
    if voice_system and aws_ok:
        # Step 3: Test voice stability
        test_voice_stability(voice_system)
    
    # Step 4: Apply fixes
    fix_voice_configuration()
    
    print("\n🎉 Voice diagnostic complete!")
    print("\n📝 Next steps to fix voice switching:")
    print("   1. Make sure AWS credentials are set correctly")
    print("   2. Use the stable_voice_wrapper.py for consistent voice")
    print("   3. Check voice_config.json for settings")
    print("   4. Restart AlphaVox after applying fixes")

if __name__ == "__main__":
    main()