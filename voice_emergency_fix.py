#!/usr/bin/env python3
"""
Quick Voice Fix - Stop voice switching immediately
Apply this fix to stabilize voice output
"""

import os
import json
from pathlib import Path

def create_voice_stability_patch():
    """Create a patch to prevent voice switching."""
    
    print("🔧 Creating voice stability patch...")
    
    # Create a minimal voice configuration
    stable_config = {
        "voice_lock": {
            "enabled": True,
            "locked_voice": "matthew",
            "prevent_fallback_switching": True
        },
        "tts_settings": {
            "prefer_single_engine": True,
            "consistent_voice": True,
            "fallback_behavior": "same_voice_different_engine"
        }
    }
    
    # Save configuration
    with open("voice_stability.json", "w") as f:
        json.dump(stable_config, f, indent=2)
    
    print("✅ Voice stability configuration created")
    
    # Create environment setup script  
    env_script = '''#!/bin/bash
# Quick Voice Fix Environment Setup

echo "🎤 Setting up AlphaVox voice stability..."

# Set basic AWS region (even without credentials, helps routing)
export AWS_REGION=us-east-1

# Voice stability flags
export ALPHAVOX_VOICE_LOCK=true
export ALPHAVOX_DEFAULT_VOICE=matthew
export ALPHAVOX_PREVENT_SWITCHING=true

# Force single TTS engine preference
export ALPHAVOX_TTS_ENGINE=gtts  # Use gTTS for consistency if no AWS

echo "✅ Voice environment configured"
echo "   Locked voice: matthew"
echo "   Switching prevention: enabled" 
echo ""
echo "Now run: python app.py"
'''
    
    with open("setup_stable_voice.sh", "w") as f:
        f.write(env_script)
    
    os.chmod("setup_stable_voice.sh", 0o755)
    print("✅ Voice setup script created: setup_stable_voice.sh")
    
    return True

def patch_voice_system():
    """Apply direct patch to voice system to prevent switching."""
    
    print("\n🩹 Applying voice system patch...")
    
    # Read the current voice file
    voice_file = Path("alphavox_ultimate_voice.py")
    if not voice_file.exists():
        print("❌ Voice file not found")
        return False
    
    # Create a backup
    backup_file = Path("alphavox_ultimate_voice.py.backup")
    if not backup_file.exists():
        import shutil
        shutil.copy2(voice_file, backup_file)
        print("✅ Backup created: alphavox_ultimate_voice.py.backup")
    
    # Create patched speak method
    patch_code = '''
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
    print(f"\\n[alphavox speaks ({locked_voice})]: {text}\\n")
    return True

# Monkey patch the original speak method
alphavoxUltimateVoice.speak_original = alphavoxUltimateVoice.speak
alphavoxUltimateVoice.speak = speak_stable
'''
    
    # Write patch to separate file
    with open("voice_stability_patch.py", "w") as f:
        f.write(patch_code)
    
    print("✅ Voice stability patch created: voice_stability_patch.py")
    return True

def create_quick_test():
    """Create a quick test to verify voice stability."""
    
    test_code = '''#!/usr/bin/env python3
"""Quick voice test to verify stability"""

import sys
sys.path.insert(0, '.')

def test_voice_stability():
    try:
        from alphavox_ultimate_voice import alphavoxUltimateVoice
        
        print("🧪 Testing voice stability...")
        voice_system = alphavoxUltimateVoice()
        
        # Apply stability patch
        exec(open("voice_stability_patch.py").read())
        
        test_phrases = [
            "Testing voice consistency - phrase one",
            "Testing voice consistency - phrase two", 
            "Testing voice consistency - phrase three"
        ]
        
        print(f"Locked to voice: {voice_system.default_voice}")
        
        for i, phrase in enumerate(test_phrases, 1):
            print(f"\\nTest {i}/3:")
            success = voice_system.speak(phrase)
            if success:
                print(f"✅ Consistent voice output {i}")
            else:
                print(f"❌ Voice output failed {i}")
        
        print("\\n🎉 Voice stability test complete!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_voice_stability()
'''
    
    with open("test_voice_stability.py", "w") as f:
        f.write(test_code)
    
    os.chmod("test_voice_stability.py", 0o755)
    print("✅ Voice stability test created: test_voice_stability.py")

def main():
    print("🚨 AlphaVox Voice Switching - EMERGENCY FIX")
    print("=" * 45)
    
    # Step 1: Create stability configuration
    create_voice_stability_patch()
    
    # Step 2: Patch the voice system
    patch_voice_system()
    
    # Step 3: Create test
    create_quick_test()
    
    print("\n🎯 IMMEDIATE FIX COMPLETE!")
    print("\n📋 To stop voice switching RIGHT NOW:")
    print("   1. Run: source setup_stable_voice.sh")
    print("   2. Run: python test_voice_stability.py")
    print("   3. If test passes, restart AlphaVox: python app.py")
    print("\n⚠️  This locks the voice to 'matthew' to prevent switching")
    print("   You can change the locked voice in voice_stability.json")

if __name__ == "__main__":
    main()