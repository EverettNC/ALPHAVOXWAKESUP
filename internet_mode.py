"""
Internet Mode Module
--------------------
Handles alphavox's secure connection to online knowledge sources.

Phase 1: Controlled Internet Mode
Author: Everett Christman & The Christman AI Project
"""

import os
import sys
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional

# -------------------------------------------------------------
# Ensure project root is available for imports
# -------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# -------------------------------------------------------------
# Internal module imports
# -------------------------------------------------------------
from perplexity_service import PerplexityService
from memory_engine import MemoryEngine
from brain import alphavox

# -------------------------------------------------------------
# Logging setup
# -------------------------------------------------------------
os.makedirs("logs/internet_activity", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [InternetMode] - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/internet_activity/internet_log.txt"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("InternetMode")

# -------------------------------------------------------------
# Configuration
# -------------------------------------------------------------
ENABLE_INTERNET_MODE = os.getenv("ENABLE_INTERNET_MODE", "false").lower() == "true"

# Initialize key systems (global for legacy, but prefer instance)
perplexity = PerplexityService() if os.getenv("PERPLEXITY_API_KEY") else None
memory_engine = MemoryEngine()


class InternetMode:
    """Main class for InternetMode - Secure web search integration for alphavox."""
    
    def __init__(self):
        """Initialize InternetMode with Perplexity and memory engine."""
        self.perplexity = PerplexityService() if os.getenv("PERPLEXITY_API_KEY") else None
        self.memory = MemoryEngine()
        self.enabled = ENABLE_INTERNET_MODE
        logger.info(f"InternetMode initialized - Enabled: {self.enabled}")
    
    def search(self, query: str) -> str:
        """Perform internet search via Perplexity, log, and save to memory."""
        if not self.enabled:
            logger.warning("Internet Mode is disabled — returning local fallback.")
            return "Internet Mode is currently disabled."
        
        if not self.perplexity:
            return "No knowledge sources available (check PERPLEXITY_API_KEY)."
        
        try:
            logger.info(f"🌐 Querying Perplexity for: {query}")
            result = self.perplexity.generate_content(query)
            summary = result.get("content", "") if isinstance(result, dict) else str(result)
            self._log_search(query, summary)
            self.memory.save({
                "query": query,
                "summary": summary,
                "status": "success",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return summary
        except Exception as e:
            logger.error(f"❌ Internet query failed: {e}")
            return f"Error querying knowledge source: {e}"
    
    def _log_search(self, query: str, summary: str):
        """Log internet search interactions to JSONL."""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query": query,
            "summary": summary,
        }
        log_path = "logs/internet_activity/internet_log.jsonl"
        with open(log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        logger.info(f"✅ Logged: {query}")


class KnowledgeGateway:
    """Gateway for accessing external knowledge sources (legacy/alt interface)."""
    
    def __init__(self):
        self.perplexity = PerplexityService() if os.getenv("PERPLEXITY_API_KEY") else None
        self.memory = MemoryEngine()
        logger.info("KnowledgeGateway initialized")
    
    def query(self, question: str) -> str:
        """Query external knowledge sources (uses InternetMode under hood)."""
        if not ENABLE_INTERNET_MODE:
            return "Internet mode is disabled"
        
        if self.perplexity:
            try:
                response = self.perplexity.generate_content(question)
                if isinstance(response, dict):
                    return response.get('content', response.get('answer', str(response)))
                return str(response)
            except Exception as e:
                logger.error(f"Perplexity query failed: {e}")
                return f"Error querying knowledge source: {e}"
        
        return "No knowledge sources available"


# -------------------------------------------------------------
# Query the Internet (legacy function - redirect to class)
# -------------------------------------------------------------
def query_internet(query: str) -> Dict[str, Any]:
    """Legacy function - Use InternetMode.search() for new code."""
    if not ENABLE_INTERNET_MODE:
        logger.warning("Internet Mode is disabled — returning local fallback.")
        return {"response": "Internet Mode is currently disabled."}
    
    # Instantiate for legacy use
    mode = InternetMode()
    summary = mode.search(query)
    return {
        "query": query,
        "summary": summary,
        "status": "success",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# -------------------------------------------------------------
# Logging Helper (moved to class, but keep for legacy)
# -------------------------------------------------------------
def _log_search(query: str, summary: str):
    """Log internet search interactions (legacy)."""
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "summary": summary,
    }
    log_path = "logs/internet_activity/internet_log.jsonl"
    with open(log_path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    logger.info(f"✅ Logged: {query}")


# -------------------------------------------------------------
# Interactive Test
# -------------------------------------------------------------
def main():
    print(f"\n🌍 Internet Mode Test — ENABLED? {ENABLE_INTERNET_MODE}\n")
    if not ENABLE_INTERNET_MODE:
        print("💡 To enable, run this first in your terminal:")
        print("   export ENABLE_INTERNET_MODE=True\n")

    # Use class for test
    mode = InternetMode()
    
    while True:
        query = input("🔎 Ask alphavox something (or 'exit'): ").strip()
        if query.lower() in ("exit", "quit"):
            print("👋 Exiting Internet Mode.")
            break

        result = mode.search(query)
        print(f"\n🧠 alphavox (Internet): {result}\n")


# -------------------------------------------------------------
if __name__ == "__main__":
    main()


# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training 
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?" 
# Autonomy & Alignment Protocol v3.0
# ==============================================================================
