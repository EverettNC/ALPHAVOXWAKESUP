#!/usr/bin/env python3
"""
Comprehensive AlphaVox Module Scanner
Scans and tests ALL Python modules in the system
"""

import sys
import os
import importlib
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveModuleScanner:
    def __init__(self):
        self.all_modules = []
        self.loaded = []
        self.failed = []
        self.skipped = []
        
    def discover_modules(self):
        """Discover all Python modules in the project"""
        logger.info("🔍 Discovering all Python modules...")
        
        # Get all .py files in root directory
        root_path = Path('.')
        py_files = sorted(root_path.glob('*.py'))
        
        # Filter out test files, setup files, and our scanner itself
        skip_patterns = ['test_', 'setup.py', 'system_check.py', 'integration_test.py', 
                        'comprehensive_module_scan.py', 'create_test', 'train_', 
                        'generate_', 'simplified_']
        
        for py_file in py_files:
            module_name = py_file.stem
            
            # Skip certain patterns
            if any(pattern in module_name for pattern in skip_patterns):
                self.skipped.append(module_name)
                continue
                
            self.all_modules.append(module_name)
        
        logger.info(f"Found {len(self.all_modules)} modules to test")
        logger.info(f"Skipped {len(self.skipped)} test/setup files\n")
    
    def test_module(self, module_name):
        """Test if a module can be imported"""
        try:
            importlib.import_module(module_name)
            return True, None
        except Exception as e:
            return False, str(e)
    
    def scan_all_modules(self):
        """Scan and test all modules"""
        logger.info("=" * 70)
        logger.info("COMPREHENSIVE MODULE SCAN - AlphaVox v7")
        logger.info("=" * 70)
        logger.info("")
        
        # Test each module
        for i, module_name in enumerate(self.all_modules, 1):
            success, error = self.test_module(module_name)
            
            if success:
                logger.info(f"✓ [{i:3d}] {module_name}")
                self.loaded.append(module_name)
            else:
                # Truncate long error messages
                error_msg = error.split('\n')[0][:60]
                logger.error(f"✗ [{i:3d}] {module_name}: {error_msg}")
                self.failed.append((module_name, error))
        
        logger.info("")
        logger.info("=" * 70)
        logger.info("SCAN RESULTS")
        logger.info("=" * 70)
        logger.info(f"✓ Successfully Loaded: {len(self.loaded)}")
        logger.info(f"✗ Failed to Load:     {len(self.failed)}")
        logger.info(f"⊘ Skipped (test/gen): {len(self.skipped)}")
        logger.info(f"━ Total Modules:      {len(self.all_modules)}")
        logger.info("")
        
        if self.failed:
            logger.info("=" * 70)
            logger.info("FAILED MODULES DETAILS")
            logger.info("=" * 70)
            for module_name, error in self.failed:
                logger.info(f"\n✗ {module_name}")
                # Show first 3 lines of error
                error_lines = error.split('\n')[:3]
                for line in error_lines:
                    logger.info(f"  {line}")
        
        logger.info("")
        logger.info("=" * 70)
        
        if self.failed:
            logger.info("⚠️  SOME MODULES FAILED TO LOAD")
            logger.info(f"Success Rate: {len(self.loaded)}/{len(self.all_modules)} ({len(self.loaded)*100//len(self.all_modules)}%)")
            return 1
        else:
            logger.info("✅ ALL MODULES LOADED SUCCESSFULLY")
            logger.info(f"Success Rate: 100% ({len(self.loaded)}/{len(self.all_modules)})")
            return 0

def main():
    scanner = ComprehensiveModuleScanner()
    scanner.discover_modules()
    exit_code = scanner.scan_all_modules()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
