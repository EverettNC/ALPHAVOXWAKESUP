import sys
import logging
import time
import os
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from perplexity_service import PerplexityService
from memory_engine import MemoryEngine
from conversation_engine import ConversationEngine
from brain import alphavox
from derek import DerekUltimateVoice, POLLY_VOICES, playsound
from memory_mesh_bridge import MemoryMeshBridge
import boto3
from datetime import datetime
import tempfile
import uuid

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Create logs directory
os.makedirs("logs", exist_ok=True)

# Configure logging for HIPAA audit trails
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/alphavox_dashboard.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AlphaVox Dashboard", description="Voice for the voiceless")

# Initialize Derek for voice synthesis
try:
    derek = DerekUltimateVoice(ai_provider="auto", voice_id="matthew", use_web_search=True)
    logger.info("✅ DerekUltimateVoice initialized for AlphaVox")
except Exception as e:
    logger.error(f"❌ Failed to initialize DerekUltimateVoice: {str(e)}")
    raise RuntimeError(f"Derek initialization failed: {str(e)}")

# Initialize MemoryMeshBridge for Derek's memory
try:
    memory = MemoryMeshBridge(memory_dir="./derek_memory")
    logger.info("🧠 MemoryMeshBridge initialized for AlphaVox")
except Exception as e:
    logger.error(f"❌ Failed to initialize MemoryMeshBridge: {str(e)}")
    raise RuntimeError(f"Memory initialization failed: {str(e)}")

# TTS Request Model
class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "matthew"
    speed: Optional[float] = 1.0

class AlphaVoxDashboard:
    def __init__(self):
        logger.info("=" * 60)
        logger.info("🚀 Initializing AlphaVox Dashboard")
        logger.info("The Christman AI Project - AI That Empowers")
        logger.info("=" * 60)

        # Initialize components
        self.memory_engine: Optional[MemoryEngine] = None
        self.conversation_engine: Optional[ConversationEngine] = None
        self.perplexity_service: Optional[PerplexityService] = None
        self.alphavox: Optional[alphavox] = None
        self.derek = derek
        self.memory = memory

        try:
            self.alphavox = alphavox.AlphaVox(file_path="./memory/memory_store.json")
            logger.info("AlphaVox instance initialized and linked to dashboard.")
        except Exception as e:
            logger.error(f"❌ Failed to initialize AlphaVox: {str(e)}")
            raise

        self.api_host = "127.0.0.1"
        self.api_port = 8000

        self._initialize_components()

    def _initialize_components(self):
        logger.info("Loading memory engine...")
        memory_path = "./memory/memory_store.json"
        os.makedirs(os.path.dirname(memory_path), exist_ok=True)

        try:
            self.memory_engine = MemoryEngine(file_path=memory_path)
            logger.info(f"Memory engine initialized with file: {memory_path}")
            self.conversation_engine = ConversationEngine()
            logger.info("Conversation engine initialized")
            try:
                self.perplexity_service = PerplexityService()
                logger.info("Perplexity service initialized")
            except Exception as e:
                logger.warning(f"Perplexity service not available: {str(e)}")
                self.perplexity_service = None
            logger.info("✓ All components initialized successfully")
        except Exception as e:
            logger.error(f"❌ Component initialization failed: {str(e)}")
            raise

    def start(self):
        logger.info("")
        logger.info("=" * 60)
        logger.info("🚀 Starting AlphaVox Dashboard Services")
        logger.info("=" * 60)
        logger.info("")

        try:
            logger.info("→ Starting AlphaVox learning system...")
            if self.alphavox:
                self.alphavox.start_learning()
            logger.info("→ Loading memory context...")
            if self.memory_engine:
                recent_events = self.memory_engine.get_recent_events()
                logger.info(f"Loaded {len(recent_events)} recent memory events")
            logger.info("")
            logger.info("=" * 60)
            logger.info("✓ AlphaVox Dashboard is RUNNING")
            logger.info("✓ Ready for conversation processing")
            logger.info("=" * 60)
            logger.info("")
            self._display_greeting()
        except Exception as e:
            logger.error(f"❌ Failed to start dashboard: {str(e)}")
            self.stop()
            sys.exit(1)

    def _display_greeting(self):
        if self.alphavox:
            greeting = self.alphavox.generate_greeting()
            logger.info(f"🗣️ AlphaVox says: {greeting}")
            # Speak the greeting using Derek's voice
            self.derek.speak(greeting)

    def process_message(self, message: str):
        if not self.alphavox:
            logger.warning("AlphaVox is not initialized yet.")
            return "System not ready."
        try:
            response = self.alphavox.think(message)
            self.derek.speak(response.get("response", "[No output]"))
            self.memory.store(
                content=f"Conversation: {message[:50]} -> {response.get('response', '')[:50]}",
                category="conversation",
                importance=0.7,
                metadata={"timestamp": datetime.now().isoformat()}
            )
            return response.get("response", "[No output]")
        except Exception as e:
            logger.error(f"Error during message processing: {str(e)}")
            return "Error processing message."

    def stop(self):
        logger.info("🧠 Shutting down AlphaVox Dashboard services...")
        try:
            if self.memory_engine:
                self.memory_engine.save()
                logger.info("Memory engine saved successfully.")
            if self.memory:
                self.memory.save()
                logger.info("MemoryMeshBridge saved successfully.")
        except Exception as e:
            logger.error(f"Error saving memory on shutdown: {str(e)}")
        logger.info("🛑 AlphaVox Dashboard stopped cleanly.")

# FastAPI TTS Endpoint
@app.post("/tts/synthesize")
async def synthesize_tts(request: TTSRequest = Body(...)):
    try:
        if len(request.text) > 1000:
            raise HTTPException(status_code=400, detail="Text too long for real-time TTS")
        if not 0.5 <= request.speed <= 2.0:
            raise HTTPException(status_code=400, detail="Speed must be between 0.5 and 2.0")
        if request.voice not in POLLY_VOICES:
            raise HTTPException(status_code=400, detail=f"Invalid voice: {request.voice}. Choose from {list(POLLY_VOICES.keys())}")

        polly = boto3.client('polly')
        response = polly.synthesize_speech(
            Text=request.text,
            OutputFormat='mp3',
            VoiceId=request.voice.capitalize(),
            Engine=POLLY_VOICES[request.voice].get('engine', 'neural'),
            SampleRate='22050'
        )

        temp_dir = tempfile.gettempdir()
        audio_file = os.path.join(temp_dir, f"alphavox_{uuid.uuid4()}.mp3")
        with open(audio_file, 'wb') as f:
            f.write(response['AudioStream'].read())

        playsound(audio_file)
        os.remove(audio_file)

        memory.store(
            content=f"TTS Interaction: {request.text[:50]}... (voice: {request.voice}, speed: {request.speed})",
            category="conversation",
            importance=0.7,
            metadata={"endpoint": "tts/synthesize", "timestamp": datetime.now().isoformat()}
        )

        logger.info(f"TTS synthesized: {request.text[:50]}... (voice: {request.voice}, speed: {request.speed})")
        return {"status": "success", "text": request.text, "voice": request.voice}
    except Exception as e:
        logger.error(f"TTS error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {str(e)}")

@app.get("/health")
async def health_check():
    try:
        stats = memory.get_memory_stats()
        return {
            "status": "healthy",
            "memory_stats": stats,
            "message": "AlphaVox is ready to speak for the voiceless"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}

def main():
    dashboard = None
    try:
        dashboard = AlphaVoxDashboard()
        dashboard.start()
        logger.info("Testing conversation system...")
        response = dashboard.process_message("Hello AlphaVox, how are you?")
        logger.info(f"Test response: {response}")
        logger.info("Dashboard running. Press Ctrl+C to stop.")
        import uvicorn
        uvicorn.run(app, host="0.0.0.1", port=8000)
    except KeyboardInterrupt:
        logger.info("⌨️ Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
    finally:
        if dashboard:
            dashboard.stop()

if __name__ == "__main__":
    main()
