#!/usr/bin/env python3
"""
Quick module tester - Test import of all core modules
"""
import sys

modules_to_test = [
    'app_init',
    'models', 
    'nonverbal_engine',
    'eye_tracking_service',
    'sound_recognition_service',
    'learning_analytics',
    'behavior_capture',
    'alphavox_input_nlu',
    'advanced_tts_service',
    'conversation_engine',
    'memory_engine',
    'ai_learning_engine',
    'neural_learning_core',
]

print("Testing module imports...")
failed = []
for module in modules_to_test:
    try:
        __import__(module)
        print(f"✓ {module}")
    except Exception as e:
        print(f"✗ {module}: {e}")
        failed.append(module)

print(f"\n{len(modules_to_test) - len(failed)}/{len(modules_to_test)} modules loaded successfully")
sys.exit(len(failed))
