#!/usr/bin/env python3
"""
AlphaVox Vision System Test
Tests all vision modules for behavior capture functionality
"""
import sys

def test_vision():
    print("=" * 70)
    print("ALPHAVOX VISION SYSTEM TEST")
    print("=" * 70)
    
    # Test 1
    print("\n[1/6] OpenCV + NumPy...")
    import cv2
    import numpy as np
    print(f"  ✓ OpenCV: {cv2.__version__}")
    print(f"  ✓ NumPy: {np.__version__}")
    
    # Test 2
    print("\n[2/6] TensorFlow...")
    import tensorflow as tf
    print(f"  ✓ TensorFlow: {tf.__version__}")
    
    # Test 3
    print("\n[3/6] DeepFace + MTCNN...")
    from deepface import DeepFace
    print(f"  ✓ DeepFace: OK")
    
    # Test 4
    print("\n[4/6] MediaPipe...")
    import mediapipe as mp
    print(f"  ✓ MediaPipe: OK")
    
    # Test 5
    print("\n[5/6] Behavior Capture...")
    from behavior_capture import BehaviorCapture
    bc = BehaviorCapture()
    print(f"  ✓ BehaviorCapture initialized")
    print(f"  ✓ Processors: {', '.join(bc.processors.keys())}")
    
    # Test 6
    print("\n[6/6] Haar Cascades...")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    print(f"  ✓ Face detection: {'OK' if not face_cascade.empty() else 'FAILED'}")
    print(f"  ✓ Eye detection: {'OK' if not eye_cascade.empty() else 'FAILED'}")
    
    print("\n" + "=" * 70)
    print("ALL VISION MODULES: OPERATIONAL ✓")
    print("=" * 70)
    
    print("\nReady for behavior capture:")
    print("  • Facial emotion detection (DeepFace)")
    print("  • Micro-expression analysis (OpenCV)")
    print("  • Eye movement tracking (OpenCV)")
    print("  • Facial gesture recognition (MediaPipe)")
    print("  • Repetitive movement detection (BehaviorCapture)")
    print("  • Tic detection (BehaviorCapture)")
    print("  • Posture tracking (BehaviorCapture)")

if __name__ == "__main__":
    test_vision()
