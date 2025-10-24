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

from flask import Flask, render_template
import sys

# 🔧 Add path to ensure ai_learning_engine can be found
sys.path.append("alphavox-v9/alphavox-v9")  # Adjust this if needed

from ai_learning_engine import get_self_improvement_engine

app = Flask(__name__)

@app.route("/learning/hub")
def learning_hub():
    # Initialize and start the AI Learning Engine
    engine = get_self_improvement_engine()
    engine.start_learning()

    # Load statistics and suggestions
    stats = engine.model_optimizer._load_stats()
    suggestions = engine.get_improvement_suggestions()

    # Render them in the learning hub template
    return render_template("learning_hub.html", stats=stats, suggestions=suggestions)

if __name__ == "__main__":
    app.run(debug=True)

