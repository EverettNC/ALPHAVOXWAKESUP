# Enable AlphaVox AI Features

AlphaVox has powerful AI capabilities, but they require API keys to function. Here's how to enable them:

## 🧠 Available AI Features

### 1. **Anthropic Claude** (Advanced NLP & Conversation)
- **What it does:** Powers advanced conversational AI, natural language understanding, academic responses
- **Used by:** `conversation_engine.py`, `advanced_nlp_service.py`, `clients.py`
- **Cost:** Paid API (pay-per-use)
- **Get API Key:** https://console.anthropic.com/

### 2. **Perplexity AI** (Internet Search & Knowledge)
- **What it does:** Real-time internet search, current information, research queries
- **Used by:** `perplexity_service.py`, `internet_mode.py`, `language_service.py`
- **Cost:** Paid API (pay-per-use)
- **Get API Key:** https://www.perplexity.ai/settings/api

### 3. **OpenAI** (Optional - Alternative NLP)
- **What it does:** Alternative to Anthropic for some features
- **Used by:** Some optional modules
- **Cost:** Paid API (pay-per-use)
- **Get API Key:** https://platform.openai.com/api-keys

## 🔧 Setup Instructions

### Method 1: Environment Variables (Recommended for Mac)

Create a `.env` file in your project root:

```bash
cd ~/Downloads/ALPHAVOXWAKESUP-main

# Create .env file
cat > .env << 'EOF'
# Anthropic API Key (for advanced conversation)
ANTHROPIC_API_KEY=your_anthropic_key_here

# Perplexity API Key (for internet search)
PERPLEXITY_API_KEY=your_perplexity_key_here

# OpenAI API Key (optional)
OPENAI_API_KEY=your_openai_key_here

# Enable internet mode
ENABLE_INTERNET_MODE=true
EOF

# Make sure .env is in .gitignore (don't commit API keys!)
echo ".env" >> .gitignore
```

Then install python-dotenv and load environment variables:

```bash
pip install python-dotenv
```

Update `app.py` to load .env file (add at the top):

```python
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
```

### Method 2: Export in Terminal (Temporary)

```bash
# For current session only
export ANTHROPIC_API_KEY="your_key_here"
export PERPLEXITY_API_KEY="your_key_here"
export ENABLE_INTERNET_MODE=true

# Start AlphaVox
python app.py --port 5001
```

### Method 3: Add to Shell Profile (Permanent)

```bash
# Add to ~/.zshrc (Mac default shell)
echo 'export ANTHROPIC_API_KEY="your_key_here"' >> ~/.zshrc
echo 'export PERPLEXITY_API_KEY="your_key_here"' >> ~/.zshrc
echo 'export ENABLE_INTERNET_MODE=true' >> ~/.zshrc

# Reload shell
source ~/.zshrc
```

## 📊 Current Status Check

Run this to see what's available:

```bash
python3 << 'EOF'
import os

print("🔍 AlphaVox AI Features Status:\n")

# Check Anthropic
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
if anthropic_key:
    print("✅ Anthropic Claude: ENABLED")
    print(f"   Key: {anthropic_key[:10]}...{anthropic_key[-4:]}")
else:
    print("❌ Anthropic Claude: DISABLED (no API key)")
    print("   → Advanced conversation features unavailable")

# Check Perplexity
perplexity_key = os.getenv("PERPLEXITY_API_KEY")
if perplexity_key:
    print("✅ Perplexity AI: ENABLED")
    print(f"   Key: {perplexity_key[:10]}...{perplexity_key[-4:]}")
else:
    print("❌ Perplexity AI: DISABLED (no API key)")
    print("   → Internet search features unavailable")

# Check Internet Mode
internet_mode = os.getenv("ENABLE_INTERNET_MODE", "false").lower() == "true"
if internet_mode:
    print("✅ Internet Mode: ENABLED")
else:
    print("⚠️  Internet Mode: DISABLED")
    print("   → Set ENABLE_INTERNET_MODE=true to enable")

print("\n📝 To enable features:")
print("   1. Get API keys from providers")
print("   2. Create .env file or export environment variables")
print("   3. Restart AlphaVox")
EOF
```

## 💡 Free Alternative: Local Mode

AlphaVox can work WITHOUT API keys in limited mode:

1. **Basic conversation:** Uses rule-based responses
2. **Learning Hub:** Works fully (no API needed)
3. **Memory:** Works fully (local storage)
4. **Eye tracking:** Works fully (local processing)
5. **Gestures:** Work fully (local recognition)

**What requires API keys:**
- Advanced natural language understanding
- Internet search and current information
- PhD-level academic responses
- Real-time research queries

## 🚀 Quick Start for Testing

Want to test AlphaVox without paying for APIs? You can:

1. **Use Learning Hub** (no APIs needed):
   ```
   http://localhost:5001/learning
   ```

2. **Enable free tier APIs** (limited):
   - Anthropic: $5 free credit for new accounts
   - Perplexity: Free tier available
   - OpenAI: $5 free credit for new accounts

3. **Mock Mode** (coming soon):
   - Will simulate AI responses for testing
   - No API keys required

## 📞 Need Help?

Check logs to see what features are loading:

```bash
# Check what loaded successfully
python alphavox_module_loader.py

# Look for these lines:
# "Anthropic API available for advanced conversational capabilities"
# "Perplexity service initialized"
```

If you see warnings about missing API keys, that's normal - just means those features are disabled.

---

## 🎯 Recommended Setup for Full Features

```bash
# 1. Get API keys
# - Anthropic: https://console.anthropic.com/
# - Perplexity: https://www.perplexity.ai/settings/api

# 2. Install dotenv
pip install python-dotenv

# 3. Create .env file with your keys
cat > .env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-xxxxx
PERPLEXITY_API_KEY=pplx-xxxxx
ENABLE_INTERNET_MODE=true
EOF

# 4. Update app.py (add at top)
# from dotenv import load_dotenv
# load_dotenv()

# 5. Start AlphaVox
python app.py --port 5001
```

**Cost estimate for moderate use:**
- Anthropic Claude: ~$10-20/month
- Perplexity AI: ~$5-10/month
- Total: ~$15-30/month for full AI features

---

© 2025 The Christman AI Project
