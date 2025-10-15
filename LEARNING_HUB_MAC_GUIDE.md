# Learning Hub - Mac Setup Guide

## Quick Fix (After Doctor's Appointment)

If the Learning Hub isn't working on your Mac, follow these steps:

### 1. Pull Latest Code
```bash
cd ~/Downloads/ALPHAVOXWAKESUP-main
git pull origin main
```

### 2. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 3. Run Quick Fix Script
```bash
python fix_learning_hub.py
```

This will:
- Install all required packages
- Verify Learning Hub components
- Confirm everything is ready

### 4. Start AlphaVox
```bash
python app.py --port 5001
```

### 5. Access Learning Hub
Open your browser to: **http://localhost:5001/learning**

---

## What You'll See

The Learning Hub includes:

### Main Sections
- **📚 Browse Topics** - Explore communication topics (PECS, AAC, Social Interaction, etc.)
- **🎯 Learning Journey** - Track your progress and achievements
- **💡 Facts Database** - Discover interesting facts about communication
- **🕸️ Knowledge Graph** - Visualize connections between concepts

### Stats Dashboard
- Topics Explored
- Facts Learned
- Active Days
- Learning Streak

### Featured Topics
- **PECS** (Beginner) - Picture Exchange Communication System
- **AAC** (Intermediate) - Augmentative and Alternative Communication
- **Social Interaction** (Intermediate) - Engaging with others socially

---

## Troubleshooting

### If you get "404 Not Found" at /learning:

**Option A: Use the fix script**
```bash
python fix_learning_hub.py
```

**Option B: Manual fix**
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt

# Test imports
python -c "from learning_routes import learning_bp; print('SUCCESS')"

# Restart app
python app.py --port 5001
```

### If imports fail:

```bash
# Check which Python you're using
which python

# Should show: ~/Downloads/ALPHAVOXWAKESUP-main/venv/bin/python
# If not, activate venv again:
source venv/bin/activate
```

### If Flask isn't found:

```bash
pip install Flask==3.0.0
```

---

## Understanding the Learning Hub

### Routes Available:
- `/learning` - Main hub page
- `/learning/topics` - Browse all topics
- `/learning/facts` - Explore facts database
- `/learning/journey` - View your learning progress
- `/learning/graph` - Interactive knowledge graph
- `/learning/topics/<name>` - Details for specific topic
- `/learning/facts/<id>` - Details for specific fact

### Data Files:
- `data/knowledge/topics.json` - 15 communication topics
- `data/knowledge/facts.json` - Growing database of facts
- `data/knowledge_graph.json` - Connections between topics
- `data/knowledge/learning_log.json` - Your learning history

### Templates:
All located in `templates/learning/`:
- `hub.html` - Main dashboard
- `topics.html` - Topics browser
- `facts.html` - Facts explorer
- `journey.html` - Progress tracker
- `graph.html` - Interactive visualization
- `topic_detail.html` - Individual topic view
- `fact_detail.html` - Individual fact view

---

## Why This Matters

The Learning Hub is a **core AlphaVox feature** that:

1. **Personalizes Learning** - Tracks user progress and adapts content
2. **Builds Knowledge** - Connects communication concepts systematically
3. **Supports Caregivers** - Provides educational resources
4. **Demonstrates AI** - Shows machine learning in action
5. **Improves Communication** - Teaches AAC principles progressively

This is **valuable IP** that showcases AlphaVox as more than just a voice assistant - it's an intelligent learning companion.

---

## After Setup

Once the Learning Hub is working:

1. ✅ Test all routes (/learning, /learning/topics, etc.)
2. ✅ Verify data loads correctly
3. ✅ Check that templates render properly
4. ✅ Confirm stats update as you explore

Then you're ready to:
- Continue development
- Demonstrate to investors
- Document for patent applications
- Prepare for funding submissions

---

## Support Files Created

These diagnostic tools are available to help:

1. **fix_learning_hub.py** - One-command fix for common issues
2. **diagnose_learning_hub_mac.py** - Detailed diagnostic report
3. **compare_environments.py** - Compare Mac vs codespace setup

Run any of these if you encounter problems!

---

**Remember:** The Learning Hub WAS working before. This guide ensures it works again after syncing from GitHub.

Good luck at the doctor! 🏥
