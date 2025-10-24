# © 2025 The Christman AI Project. All rights reserved.
#
# This code is released as part of a trauma-informed, dignity-first AI ecosystem
# designed to protect, empower, and elevate vulnerable populations.
#
# By using, modifying, or distributing this software, you agree to uphold the following:
# 1. Truth — No deception, no manipulation.
# 2. Dignity — Respect the autonomy and humanity of all users.
# 3. Protection — Never use this to exploit or harm vulnerable individuals.
# 4. Transparency — Disclose all modifications and contributions clearly.
# 5. No Erasure — Preserve the mission and ethical origin of this work.
#
# This is not just code. This is redemption in code.
# Contact: lumacognify@thechristmanaiproject.com
# https://thechristmanaiproject.com

#!/usr/bin/env python3
"""
AlphaVox Integration Test
Tests that all vital modules work together correctly
"""

import sys
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class IntegrationTest:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        
    def test(self, name, func):
        """Run a test and track results"""
        try:
            func()
            logger.info(f"✓ {name}")
            self.passed += 1
            return True
        except Exception as e:
            logger.error(f"✗ {name}: {e}")
            self.failed += 1
            return False
    
    def test_database_integration(self):
        """Test database layer"""
        from app_init import app, db
        from models import User, UserInteraction
        
        with app.app_context():
            # Test user creation
            test_user = User(name='integration_test_user')
            db.session.add(test_user)
            db.session.commit()
            
            # Test interaction storage
            interaction = UserInteraction(
                user_id=test_user.id,
                text='test',
                intent='test',
                confidence=0.9
            )
            db.session.add(interaction)
            db.session.commit()
            
            # Cleanup
            db.session.delete(interaction)
            db.session.delete(test_user)
            db.session.commit()
    
    def test_nonverbal_engine(self):
        """Test nonverbal processing"""
        from nonverbal_engine import NonverbalEngine
        
        engine = NonverbalEngine()
        result = engine.classify_gesture('nod')
        assert 'intent' in result
        assert 'confidence' in result
    
    def test_nlu_processing(self):
        """Test NLU module"""
        from alphavox_input_nlu import get_input_processor
        
        processor = get_input_processor()
        result = processor.process_interaction(
            {'type': 'text', 'input': 'I need help'},
            'test_user'
        )
        assert result.get('confidence', 0) > 0
    
    def test_neural_core(self):
        """Test neural learning core"""
        from neural_learning_core import get_neural_learning_core
        
        nlc = get_neural_learning_core()
        # Core should initialize without errors
        assert nlc is not None
    
    def test_tts_generation(self):
        """Test text-to-speech"""
        from gtts import gTTS
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=True) as tmp:
            tts = gTTS(text='Integration test', lang='en')
            tts.save(tmp.name)
            assert os.path.exists(tmp.name)
    
    def test_conversation_engine(self):
        """Test conversation engine"""
        from conversation_engine import get_conversation_engine
        from nonverbal_engine import NonverbalEngine
        
        engine = NonverbalEngine()
        conv = get_conversation_engine(engine)
        assert conv is not None
    
    def test_memory_engine(self):
        """Test memory persistence"""
        from memory_engine import MemoryEngine
        import tempfile
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=True) as tmp:
            mem = MemoryEngine(file_path=tmp.name)
            # Should initialize without errors
            assert mem is not None
    
    def test_learning_analytics(self):
        """Test analytics module"""
        from learning_analytics import LearningAnalytics
        
        analytics = LearningAnalytics(user_id=1)
        assert analytics is not None
    
    def test_ai_learning_engine(self):
        """Test self-learning system"""
        from ai_learning_engine import get_self_improvement_engine
        
        engine = get_self_improvement_engine()
        assert engine is not None
    
    def test_behavior_capture(self):
        """Test behavior analysis"""
        from behavior_capture import get_behavior_capture
        
        capture = get_behavior_capture()
        assert capture is not None
    
    def test_eye_tracking(self):
        """Test eye tracking service"""
        from eye_tracking_service import EyeTrackingService
        
        service = EyeTrackingService()
        assert service is not None
    
    def test_sound_recognition(self):
        """Test sound recognition"""
        from sound_recognition_service import SoundRecognitionService
        
        service = SoundRecognitionService()
        assert service is not None
    
    def test_full_pipeline(self):
        """Test complete input-to-output pipeline"""
        from app_init import app, db
        from models import User
        from alphavox_input_nlu import get_input_processor
        from advanced_tts_service import text_to_speech_with_emotion
        import os
        
        with app.app_context():
            # Create test user
            user = User.query.filter_by(name='pipeline_test').first()
            if not user:
                user = User(name='pipeline_test')
                db.session.add(user)
                db.session.commit()
            
            # Process input
            processor = get_input_processor()
            result = processor.process_interaction(
                {'type': 'text', 'input': 'Hello'},
                str(user.id)
            )
            
            # Generate speech
            audio_path = text_to_speech_with_emotion(
                text='Hello response',
                emotion='positive',
                emotion_tier='moderate'
            )
            
            # Verify audio created
            assert os.path.exists(audio_path)
            
            # Cleanup
            os.remove(audio_path)
    
    def run_all_tests(self):
        """Run all integration tests"""
        logger.info("=" * 60)
        logger.info("AlphaVox Integration Test Suite")
        logger.info("=" * 60)
        logger.info("")
        
        tests = [
            ("Database Integration", self.test_database_integration),
            ("Nonverbal Engine", self.test_nonverbal_engine),
            ("NLU Processing", self.test_nlu_processing),
            ("Neural Core", self.test_neural_core),
            ("TTS Generation", self.test_tts_generation),
            ("Conversation Engine", self.test_conversation_engine),
            ("Memory Engine", self.test_memory_engine),
            ("Learning Analytics", self.test_learning_analytics),
            ("AI Learning Engine", self.test_ai_learning_engine),
            ("Behavior Capture", self.test_behavior_capture),
            ("Eye Tracking", self.test_eye_tracking),
            ("Sound Recognition", self.test_sound_recognition),
            ("Full Pipeline", self.test_full_pipeline),
        ]
        
        for name, test_func in tests:
            self.test(name, test_func)
        
        logger.info("")
        logger.info("=" * 60)
        logger.info("Test Results")
        logger.info("=" * 60)
        logger.info(f"Passed: {self.passed}")
        logger.info(f"Failed: {self.failed}")
        logger.info(f"Total:  {self.passed + self.failed}")
        
        if self.failed == 0:
            logger.info("")
            logger.info("✅ ALL INTEGRATION TESTS PASSED")
            logger.info("System is fully operational and integrated")
            return 0
        else:
            logger.info("")
            logger.info("⚠️  SOME INTEGRATION TESTS FAILED")
            logger.info("Review errors above")
            return 1

if __name__ == '__main__':
    tester = IntegrationTest()
    sys.exit(tester.run_all_tests())
