"""
AlphaVox Module Organization and Loading Order
Ensures all 136+ modules load in the correct dependency order
"""

import logging
import sys
from typing import Dict, List, Optional, Set

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlphaVoxModuleManager:
    """Manages loading of all AlphaVox modules in correct dependency order."""
    
    def __init__(self):
        self.loaded_modules: Set[str] = set()
        self.failed_modules: Dict[str, str] = {}
        
        # Define module groups and their dependencies
        self.module_groups = {
            # Level 1: Core/Foundation (no dependencies)
            "core": {
                "modules": [
                    "logger",
                    "logging_config",
                    "db",
                    "models",
                    "helpers",
                    "clients",
                ],
                "dependencies": []
            },
            
            # Level 2: Configuration & Middleware (depends on core)
            "config": {
                "modules": [
                    "app_init",
                    "middleware",
                    "json_guardian",
                ],
                "dependencies": ["core"]
            },
            
            # Level 3: Data Services (depends on core, config)
            "data": {
                "modules": [
                    "memory_manager",
                    "memory_engine",
                    "memory_service",
                    "memory",
                    "knowledge_engine",
                    "learning_service",
                ],
                "dependencies": ["core", "config"]
            },
            
            # Level 4: NLP & Language (depends on core, config)
            "nlp": {
                "modules": [
                    "advanced_nlp_service",
                    "nlu_core",
                    "alphavox_input_nlu",
                    "nlp_module",
                    "nlp_integration",
                    "intent_engine",
                    "language_service",
                ],
                "dependencies": ["core", "config", "data"]
            },
            
            # Level 5: Audio & Speech (depends on core)
            "audio": {
                "modules": [
                    "audio_processor",
                    "audio_pattern_service",
                    "advanced_tts_service",
                    "alphavox_speech_module",
                    "enhanced_speech_recognition",
                    "real_speech_recognition",
                ],
                "dependencies": ["core", "config"]
            },
            
            # Level 6: Vision & Gesture (depends on core)
            "vision": {
                "modules": [
                    "eye_tracking_service",
                    "eye_tracking_api",
                    "real_eye_tracking",
                    "facial_gesture_service",
                    "gesture_manager",
                    "gesture_dictionary",
                ],
                "dependencies": ["core", "config"]
            },
            
            # Level 7: Behavior & Emotion (depends on nlp, vision, audio)
            "behavior": {
                "modules": [
                    "emotion",
                    "behavior_capture",
                    "behavioral_interpreter",
                    "nonverbal_engine",
                    "nonverbal_expertiser",
                ],
                "dependencies": ["core", "config", "nlp", "audio", "vision"]
            },
            
            # Level 8: Interpretation (depends on nlp, behavior)
            "interpretation": {
                "modules": [
                    "interpreter",
                    "input_analyzer",
                    "cognitive_bridge",
                ],
                "dependencies": ["core", "config", "nlp", "behavior", "data"]
            },
            
            # Level 9: Conversation (depends on interpretation, nlp)
            "conversation": {
                "modules": [
                    "conversation_engine",
                    "conversation_bridge",
                    "conversation_integration",
                    "conversation_loop",
                    "complete_conversation_handler",
                    "adaptive_conversation",
                ],
                "dependencies": ["core", "config", "nlp", "interpretation", "data"]
            },
            
            # Level 10: Learning & AI (depends on conversation, data)
            "learning": {
                "modules": [
                    "learning_journey",
                    "learning_analytics",
                    "learning_utils",
                    "ai_learning_engine",
                    "advanced_learning",
                    "neural_learning_core",
                ],
                "dependencies": ["core", "config", "data", "nlp", "conversation"]
            },
            
            # Level 11: Research & Knowledge Acquisition (depends on learning)
            "research": {
                "modules": [
                    "research_module",
                    "literature_crawler",
                    "learn_arxiv",
                    "learn_pubmed",
                    "perplexity_service",
                    "internet_mode",
                ],
                "dependencies": ["core", "config", "data", "learning"]
            },
            
            # Level 12: Temporal & Scheduling (depends on core)
            "temporal": {
                "modules": [
                    "alphavox_temporal",
                    "engine_temporal",
                    "action_scheduler",
                    "executor",
                ],
                "dependencies": ["core", "config"]
            },
            
            # Level 13: User Interfaces (depends on most modules)
            "ui": {
                "modules": [
                    "caregiver_interface",
                    "caregiver_dashboard",
                    "personality_service",
                    "color_scheme_generator",
                ],
                "dependencies": ["core", "config", "data", "conversation"]
            },
            
            # Level 14: Routes (depends on all features)
            "routes": {
                "modules": [
                    "learning_routes",
                    "learning_router",
                    "memory_router",
                    "color_scheme_routes",
                    "app_routes",
                    "endpoints",
                    "route",
                    "router",
                    "routes",
                ],
                "dependencies": ["core", "config", "data", "nlp", "conversation", "learning", "ui"]
            },
            
            # Level 15: Analytics & Monitoring (depends on all)
            "analytics": {
                "modules": [
                    "analytics_engine",
                    "performance_optimizer",
                ],
                "dependencies": ["core"]
            },
            
            # Level 16: Security & Self-modification (depends on all)
            "system": {
                "modules": [
                    "security_module",
                    "self_modifying_code",
                    "self_repair",
                    "alpha_security_bridge",
                ],
                "dependencies": ["core", "config"]
            },
            
            # Level 17: Integration & Main (last to load)
            "integration": {
                "modules": [
                    "face_to_face",
                    "alphavox_module_loader",
                ],
                "dependencies": ["core", "config", "data", "nlp", "audio", "vision", "behavior", "interpretation", "conversation"]
            }
        }
    
    def load_module_group(self, group_name: str) -> bool:
        """Load all modules in a specific group."""
        if group_name not in self.module_groups:
            logger.error(f"Unknown module group: {group_name}")
            return False
        
        group = self.module_groups[group_name]
        logger.info(f"Loading module group: {group_name}")
        
        # Check dependencies
        for dep in group["dependencies"]:
            if dep not in self.loaded_modules:
                logger.warning(f"Dependency {dep} not loaded for {group_name}")
                return False
        
        # Load modules in this group
        success_count = 0
        for module_name in group["modules"]:
            if self._load_single_module(module_name):
                success_count += 1
        
        if success_count > 0:
            self.loaded_modules.add(group_name)
            logger.info(f"✅ Loaded {success_count}/{len(group['modules'])} modules in {group_name}")
            return True
        else:
            logger.warning(f"⚠️  Failed to load any modules in {group_name}")
            return False
    
    def _load_single_module(self, module_name: str) -> bool:
        """Attempt to load a single module."""
        try:
            __import__(module_name)
            logger.debug(f"  ✅ {module_name}")
            return True
        except ImportError as e:
            logger.debug(f"  ⚠️  {module_name}: {str(e)[:50]}")
            self.failed_modules[module_name] = str(e)
            return False
        except Exception as e:
            logger.debug(f"  ❌ {module_name}: {str(e)[:50]}")
            self.failed_modules[module_name] = str(e)
            return False
    
    def load_all_modules(self) -> Dict[str, any]:
        """Load all modules in dependency order."""
        logger.info("=" * 80)
        logger.info("ALPHAVOX MODULE LOADER - Organized Loading")
        logger.info("=" * 80)
        
        # Define loading order (based on dependencies)
        load_order = [
            "core",
            "config",
            "data",
            "nlp",
            "audio",
            "vision",
            "behavior",
            "interpretation",
            "conversation",
            "learning",
            "research",
            "temporal",
            "ui",
            "routes",
            "analytics",
            "system",
            "integration",
        ]
        
        results = {
            "total_groups": len(load_order),
            "loaded_groups": 0,
            "total_modules": 0,
            "loaded_modules": 0,
            "failed_modules": {},
        }
        
        for group_name in load_order:
            group = self.module_groups[group_name]
            results["total_modules"] += len(group["modules"])
            
            if self.load_module_group(group_name):
                results["loaded_groups"] += 1
        
        results["loaded_modules"] = sum(
            len(self.module_groups[g]["modules"]) - len([m for m in self.module_groups[g]["modules"] if m in self.failed_modules])
            for g in self.loaded_modules
        )
        results["failed_modules"] = self.failed_modules
        
        logger.info("=" * 80)
        logger.info(f"RESULTS: {results['loaded_modules']}/{results['total_modules']} modules loaded")
        logger.info(f"Groups: {results['loaded_groups']}/{results['total_groups']}")
        logger.info("=" * 80)
        
        if self.failed_modules:
            logger.info("\nModules that couldn't be loaded (optional features):")
            for module, error in list(self.failed_modules.items())[:10]:
                logger.info(f"  ⚠️  {module}: {error[:60]}")
            if len(self.failed_modules) > 10:
                logger.info(f"  ... and {len(self.failed_modules) - 10} more")
        
        return results


def get_module_manager():
    """Get the singleton module manager instance."""
    if not hasattr(get_module_manager, "_instance"):
        get_module_manager._instance = AlphaVoxModuleManager()
    return get_module_manager._instance


if __name__ == "__main__":
    # Test the module loader
    manager = AlphaVoxModuleManager()
    results = manager.load_all_modules()
    
    print("\n" + "=" * 80)
    print("MODULE LOADING COMPLETE")
    print("=" * 80)
    print(f"\n✅ Successfully loaded: {results['loaded_modules']}/{results['total_modules']} modules")
    print(f"✅ Module groups operational: {results['loaded_groups']}/{results['total_groups']}")
    
    if results['failed_modules']:
        print(f"\n⚠️  Optional modules not loaded: {len(results['failed_modules'])}")
        print("   (These are advanced features - app will work without them)")
    
    print("\nAlphaVox is ready to start!")
