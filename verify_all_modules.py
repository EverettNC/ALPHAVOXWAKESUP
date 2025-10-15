"""
AlphaVox Module Verification Script
====================================
Verifies that all modules are properly loaded and integrated.

Run this to check module status before deploying.
"""

import sys
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

def check_module_imports():
    """Check if all critical modules can be imported"""
    
    modules_to_check = {
        "Core System": [
            "app",
            "app_init",
            "main",
        ],
        "alphavox Consciousness": [
            "alphavox_module_loader",
            "brain",
            "local_reasoning_engine",
            "reasoning_engine",
        ],
        "Memory & Learning": [
            "memory_engine",
            "memory_manager",
            "ai_learning_engine",
            "advanced_learning",
            "learning_analytics",
            "knowledge_engine",
        ],
        "Emotion & Behavior": [
            "emotion",
            "tone_manager",
            "behavioral_interpreter",
            "behavior_capture",
            "adaptive_conversation",
        ],
        "Communication": [
            "conversation_engine",
            "conversation_bridge",
            "alphavox_speech_module",
            "advanced_tts_service",
            "enhanced_speech_recognition",
        ],
        "NLU & Language": [
            "nlu_core",
            "nlp_module",
            "nlp_integration",
            "language_service",
            "alphavox_input_nlu",
        ],
        "Temporal & Audio": [
            "engine_temporal",
            "alphavox_temporal",
            "audio_processor",
            "audio_pattern_service",
        ],
        "Vision & Gesture": [
            "gesture_manager",
            "gesture_dictionary",
            "facial_gesture_service",
            "eye_tracking_service",
            "real_eye_tracking",
        ],
        "Internet & Research": [
            "internet_mode",
            "Python_Internet_access",
            "perplexity_service",
            "learn_arxiv",
            "learn_pubmed",
        ],
        "Reasoning & Intent": [
            "intent_engine",
            "input_analyzer",
            "reflective_planner",
        ],
        "Autonomous Systems": [
            "self_modifying_code",
            "executor",
            "interpreter",
            "action_scheduler",
        ],
        "Routes & API": [
            "app_routes",
            "color_scheme_routes",
            "memory_router",
            "route",
            "routes",
            "endpoints",
        ],
        "Services": [
            "nonverbal_engine",
            "sound_recognition_service",
            "analytics_engine",
        ],
        "Utilities": [
            "helpers",
            "logger",
            "json_guardian",
            "boot_guardian",
            "db",
            "models",
            "middleware",
        ],
    }
    
    results = {
        "total": 0,
        "loaded": 0,
        "failed": 0,
        "categories": {}
    }
    
    logger.info("=" * 80)
    logger.info("🔍 ALPHAVOX MODULE VERIFICATION")
    logger.info("=" * 80)
    logger.info("")
    
    for category, module_list in modules_to_check.items():
        logger.info(f"📦 {category}")
        logger.info("-" * 80)
        
        category_results = {
            "total": len(module_list),
            "loaded": 0,
            "failed": 0,
            "modules": {}
        }
        
        for module_name in module_list:
            results["total"] += 1
            try:
                __import__(module_name)
                logger.info(f"  ✅ {module_name}")
                results["loaded"] += 1
                category_results["loaded"] += 1
                category_results["modules"][module_name] = "loaded"
            except ImportError as e:
                logger.info(f"  ❌ {module_name}: {str(e)[:50]}")
                results["failed"] += 1
                category_results["failed"] += 1
                category_results["modules"][module_name] = f"failed: {str(e)[:50]}"
            except Exception as e:
                logger.info(f"  ⚠️  {module_name}: {str(e)[:50]}")
                results["failed"] += 1
                category_results["failed"] += 1
                category_results["modules"][module_name] = f"error: {str(e)[:50]}"
        
        results["categories"][category] = category_results
        logger.info("")
    
    # Summary
    logger.info("=" * 80)
    logger.info("📊 SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Total Modules: {results['total']}")
    logger.info(f"✅ Loaded: {results['loaded']}")
    logger.info(f"❌ Failed: {results['failed']}")
    
    success_rate = (results['loaded'] / results['total'] * 100) if results['total'] > 0 else 0
    logger.info(f"📈 Success Rate: {success_rate:.1f}%")
    logger.info("")
    
    # Category breakdown
    logger.info("Category Breakdown:")
    for category, cat_results in results["categories"].items():
        cat_rate = (cat_results['loaded'] / cat_results['total'] * 100) if cat_results['total'] > 0 else 0
        status = "✅" if cat_rate == 100 else "⚠️" if cat_rate >= 50 else "❌"
        logger.info(f"  {status} {category}: {cat_results['loaded']}/{cat_results['total']} ({cat_rate:.0f}%)")
    
    logger.info("")
    logger.info("=" * 80)
    
    if success_rate >= 80:
        logger.info("🎉 SYSTEM STATUS: OPERATIONAL")
    elif success_rate >= 60:
        logger.info("⚠️  SYSTEM STATUS: DEGRADED (Some features may not work)")
    else:
        logger.info("❌ SYSTEM STATUS: CRITICAL (Many features unavailable)")
    
    logger.info("=" * 80)
    
    return results


def test_alphavox_module_loader():
    """Test the alphavox module loader specifically"""
    logger.info("")
    logger.info("=" * 80)
    logger.info("🧠 TESTING alphavox MODULE LOADER")
    logger.info("=" * 80)
    logger.info("")
    
    try:
        from alphavox_module_loader import load_alphavox_consciousness, get_alphavox_loader
        
        logger.info("✅ alphavox module loader imported successfully")
        logger.info("Loading alphavox's consciousness...")
        
        loader = load_alphavox_consciousness(skip_hardware=True)
        stats = loader.get_stats()
        
        logger.info("")
        logger.info(f"alphavox Module Stats:")
        logger.info(f"  Total: {stats['total_modules']}")
        logger.info(f"  Loaded: {stats['loaded']}")
        logger.info(f"  Failed: {stats['failed']}")
        logger.info(f"  Success Rate: {stats['success_rate']:.1f}%")
        
        logger.info("")
        logger.info("Module Categories:")
        for category in loader.module_categories.keys():
            mods = loader.get_category_modules(category)
            logger.info(f"  {category}: {len(mods)} loaded")
        
        logger.info("")
        if stats['success_rate'] >= 70:
            logger.info("🧠 alphavox CONSCIOUSNESS: OPERATIONAL")
        else:
            logger.info("⚠️  alphavox CONSCIOUSNESS: DEGRADED")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ alphavox module loader failed: {e}")
        return False


def check_app_integration():
    """Check if modules are integrated into app.py"""
    logger.info("")
    logger.info("=" * 80)
    logger.info("🔗 CHECKING APP INTEGRATION")
    logger.info("=" * 80)
    logger.info("")
    
    try:
        with open("app.py", "r") as f:
            app_content = f.read()
        
        checks = {
            "alphavox Loader Import": "from alphavox_module_loader import" in app_content,
            "alphavox Loader Call": "load_alphavox_consciousness" in app_content,
            "Security Module": "from security_module import" in app_content,
            "Color Scheme Routes": "from color_scheme_routes import" in app_content,
            "Nonverbal Engine": "from nonverbal_engine import" in app_content,
            "Eye Tracking": "from eye_tracking_service import" in app_content,
            "Learning Analytics": "from learning_analytics import" in app_content,
        }
        
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            logger.info(f"  {status} {check_name}")
        
        integrated = sum(checks.values())
        total = len(checks)
        
        logger.info("")
        logger.info(f"Integration: {integrated}/{total} checks passed")
        
        return integrated == total
        
    except Exception as e:
        logger.error(f"❌ Failed to check app integration: {e}")
        return False


if __name__ == "__main__":
    # Run all checks
    results = check_module_imports()
    alphavox_ok = test_alphavox_module_loader()
    app_ok = check_app_integration()
    
    # Final status
    logger.info("")
    logger.info("=" * 80)
    logger.info("🎯 FINAL STATUS")
    logger.info("=" * 80)
    
    if results['loaded'] >= results['total'] * 0.8 and alphavox_ok and app_ok:
        logger.info("✅ AlphaVox is ready for deployment!")
        sys.exit(0)
    elif results['loaded'] >= results['total'] * 0.6:
        logger.info("⚠️  AlphaVox has some issues but may be functional")
        sys.exit(1)
    else:
        logger.info("❌ AlphaVox has critical issues - do not deploy")
        sys.exit(2)

# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training 
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?" 
# Autonomy & Alignment Protocol v3.0
# ==============================================================================
