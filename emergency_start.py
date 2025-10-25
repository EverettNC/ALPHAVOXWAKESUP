#!/usr/bin/env python3
"""
Emergency AlphaVox Startup - Stable Voice Mode
"""

import sys
import os
sys.path.insert(0, '.')

# Set environment for stability
os.environ['DISABLE_API_WARNINGS'] = 'true'
os.environ['VOICE_LOCK'] = 'matthew'
os.environ['PREVENT_VOICE_SWITCHING'] = 'true'

print("🎤 Starting AlphaVox in STABLE VOICE MODE")
print("   Voice locked: matthew")
print("   API warnings: disabled") 
print("   Switching prevention: enabled")
print()

try:
    # Import voice override first
    from voice_stability_override import VOICE_OVERRIDE
    
    # Import and patch main app
    import app
    
    # Override voice functions in app
    if hasattr(app, 'ultimate_voice'):
        app.ultimate_voice.speak = VOICE_OVERRIDE.speak
        print("✅ Voice override applied to ultimate_voice")
    
    print("✅ AlphaVox starting with stable voice...")
    print("   Navigate to: http://localhost:5000")
    print()
    
    # Start the app
    if __name__ == "__main__":
        app.app.run(host='0.0.0.0', port=5000, debug=False)
        
except Exception as e:
    print(f"❌ Startup error: {e}")
    print("\nTrying basic mode...")
    
    # Basic fallback
    print("\n[AlphaVox Emergency Mode]")
    print("Voice: matthew (locked)")
    print("Status: Ready for communication")
    
    # Simple loop
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit']:
                break
            print(f"alphavox (matthew): I hear you saying '{user_input}'. I'm in stable voice mode.")
        except KeyboardInterrupt:
            break
    
    print("\nGoodbye!")
