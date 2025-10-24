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
AlphaVox System Operational Check
This script verifies all modules and dependencies are properly configured
"""

import sys
import os
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SystemCheck:
    def __init__(self):
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        self.start_time = datetime.now()
        
    def log_pass(self, message):
        """Log a passed check"""
        logger.info(f"✓ {message}")
        self.results['passed'].append(message)
        
    def log_fail(self, message, error=None):
        """Log a failed check"""
        error_msg = f"{message}: {error}" if error else message
        logger.error(f"✗ {error_msg}")
        self.results['failed'].append(error_msg)
        
    def log_warning(self, message):
        """Log a warning"""
        logger.warning(f"⚠ {message}")
        self.results['warnings'].append(message)
    
    def check_python_version(self):
        """Check Python version"""
        logger.info("=" * 60)
        logger.info("Checking Python Version")
        logger.info("=" * 60)
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        
        if version.major == 3 and version.minor >= 10:
            self.log_pass(f"Python version {version_str}")
        else:
            self.log_warning(f"Python {version_str} - recommended 3.10+")
    
    def check_core_dependencies(self):
        """Check core Python package dependencies"""
        logger.info("\n" + "=" * 60)
        logger.info("Checking Core Dependencies")
        logger.info("=" * 60)
        
        critical_packages = [
            'flask',
            'numpy',
            'pandas',
            'sqlalchemy',
            'cv2',  # opencv-python
            'pygame',
            'gtts',
            'anthropic',
            'openai',
            'requests',
            'scipy',
            'sklearn',  # scikit-learn
            'bs4',  # beautifulsoup4
        ]
        
        for package in critical_packages:
            try:
                __import__(package)
                self.log_pass(f"Package '{package}' installed")
            except ImportError as e:
                self.log_fail(f"Package '{package}' missing", e)
    
    def check_database_setup(self):
        """Check database configuration"""
        logger.info("\n" + "=" * 60)
        logger.info("Checking Database Setup")
        logger.info("=" * 60)
        
        try:
            from app_init import app, db
            
            with app.app_context():
                # Try to create tables
                db.create_all()
                self.log_pass("Database initialized successfully")
                
                # Check if tables exist
                from sqlalchemy import inspect
                inspector = inspect(db.engine)
                tables = inspector.get_table_names()
                
                if tables:
                    self.log_pass(f"Found {len(tables)} database tables: {', '.join(tables)}")
                else:
                    self.log_warning("No database tables found")
                    
        except Exception as e:
            self.log_fail("Database setup", e)
    
    def check_core_modules(self):
        """Check AlphaVox core modules"""
        logger.info("\n" + "=" * 60)
        logger.info("Checking AlphaVox Core Modules")
        logger.info("=" * 60)
        
        core_modules = [
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
        
        for module_name in core_modules:
            try:
                __import__(module_name)
                self.log_pass(f"Module '{module_name}' loads successfully")
            except ImportError as e:
                self.log_fail(f"Module '{module_name}' failed to load", e)
            except Exception as e:
                self.log_warning(f"Module '{module_name}' loaded with warnings: {e}")
    
    def check_directories(self):
        """Check required directories"""
        logger.info("\n" + "=" * 60)
        logger.info("Checking Directory Structure")
        logger.info("=" * 60)
        
        required_dirs = [
            'data',
            'static',
            'static/audio',
            'templates',
            'logs',
            'memory',
        ]
        
        for dir_path in required_dirs:
            full_path = Path(dir_path)
            if full_path.exists():
                self.log_pass(f"Directory '{dir_path}' exists")
            else:
                try:
                    full_path.mkdir(parents=True, exist_ok=True)
                    self.log_pass(f"Created directory '{dir_path}'")
                except Exception as e:
                    self.log_fail(f"Failed to create directory '{dir_path}'", e)
    
    def check_environment(self):
        """Check environment variables"""
        logger.info("\n" + "=" * 60)
        logger.info("Checking Environment Variables")
        logger.info("=" * 60)
        
        env_vars = {
            'DATABASE_URL': 'sqlite:///alphavox.db',  # default
            'SESSION_SECRET': None,  # optional
            'ANTHROPIC_API_KEY': None,  # optional
            'OPENAI_API_KEY': None,  # optional
        }
        
        for var, default in env_vars.items():
            value = os.environ.get(var)
            if value:
                # Mask sensitive data
                if 'KEY' in var or 'SECRET' in var:
                    masked = value[:8] + '...' if len(value) > 8 else '***'
                    self.log_pass(f"Environment variable '{var}' set ({masked})")
                else:
                    self.log_pass(f"Environment variable '{var}' set")
            elif default:
                self.log_pass(f"Environment variable '{var}' using default: {default}")
            else:
                self.log_warning(f"Environment variable '{var}' not set (optional)")
    
    def test_basic_functionality(self):
        """Test basic system functionality"""
        logger.info("\n" + "=" * 60)
        logger.info("Testing Basic Functionality")
        logger.info("=" * 60)
        
        # Test database operations
        try:
            from app_init import app, db
            from models import User
            
            with app.app_context():
                # Try to create a test user
                test_user = User.query.filter_by(name='system_check_test').first()
                if not test_user:
                    test_user = User(name='system_check_test')
                    db.session.add(test_user)
                    db.session.commit()
                    self.log_pass("Database write operation successful")
                else:
                    self.log_pass("Database read operation successful")
                    
                # Cleanup
                db.session.delete(test_user)
                db.session.commit()
                
        except Exception as e:
            self.log_fail("Database operations", e)
        
        # Test TTS capability
        try:
            from gtts import gTTS
            import tempfile
            
            test_text = "System check"
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=True) as tmp:
                tts = gTTS(text=test_text, lang='en')
                tts.save(tmp.name)
                self.log_pass("Text-to-speech generation working")
        except Exception as e:
            self.log_fail("Text-to-speech generation", e)
        
        # Test nonverbal engine
        try:
            from nonverbal_engine import NonverbalEngine
            engine = NonverbalEngine()
            result = engine.classify_gesture('test')
            self.log_pass("Nonverbal engine initialized")
        except Exception as e:
            self.log_warning(f"Nonverbal engine initialization: {e}")
    
    def generate_report(self):
        """Generate final report"""
        logger.info("\n" + "=" * 60)
        logger.info("SYSTEM CHECK REPORT")
        logger.info("=" * 60)
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        logger.info(f"\n📊 Summary:")
        logger.info(f"  ✓ Passed:   {len(self.results['passed'])}")
        logger.info(f"  ✗ Failed:   {len(self.results['failed'])}")
        logger.info(f"  ⚠ Warnings: {len(self.results['warnings'])}")
        logger.info(f"  ⏱ Duration: {elapsed:.2f}s")
        
        if self.results['failed']:
            logger.info(f"\n❌ Failed Checks:")
            for fail in self.results['failed']:
                logger.info(f"  • {fail}")
        
        if self.results['warnings']:
            logger.info(f"\n⚠️  Warnings:")
            for warning in self.results['warnings']:
                logger.info(f"  • {warning}")
        
        logger.info("\n" + "=" * 60)
        
        if not self.results['failed']:
            logger.info("✅ SYSTEM IS OPERATIONAL")
            logger.info("All critical checks passed!")
            return 0
        else:
            logger.info("⚠️  SYSTEM HAS ISSUES")
            logger.info("Some critical checks failed. Review the report above.")
            return 1
    
    def run_all_checks(self):
        """Run all system checks"""
        logger.info("\n🚀 AlphaVox System Check")
        logger.info(f"Starting at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Run all checks
        self.check_python_version()
        self.check_core_dependencies()
        self.check_database_setup()
        self.check_directories()
        self.check_environment()
        self.check_core_modules()
        self.test_basic_functionality()
        
        # Generate report
        return self.generate_report()

def main():
    """Main entry point"""
    checker = SystemCheck()
    exit_code = checker.run_all_checks()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
