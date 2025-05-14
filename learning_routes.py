"""
Routes for the Learning Journey feature
"""

import logging
from flask import Blueprint, render_template, request, jsonify, session
from learning_journey import get_learning_journey

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug print statement
print("LEARNING_ROUTES MODULE LOADED SUCCESSFULLY")

# Create blueprint
learning_bp = Blueprint("learning", __name__, url_prefix="/learning")
learning_journey = get_learning_journey()


@learning_bp.route("/")
def learning_hub():
    """Main learning hub page."""
    user_id = session.get("user_id", "default_user")
    topics = learning_journey.get_topics()
    stats = learning_journey.get_learning_statistics(user_id)

    return render_template("learning/hub.html", topics=topics, stats=stats)


@learning_bp.route("/topics")
def view_topics():
    """View all available learning topics."""
    topics = learning_journey.get_topics()

    return render_template("learning/topics.html", topics=topics)


@learning_bp.route("/facts")
def view_facts():
    """View all available facts across topics."""
    facts = learning_journey.get_all_facts()
    topics = learning_journey.get_topics()

    return render_template("learning/facts.html", facts=facts, topics=topics)


@learning_bp.route("/topics/<topic_name>")
def view_topic(topic_name):
    """View a specific topic and related facts."""
    user_id = session.get("user_id", "default_user")

    # Get topic information
    topic = learning_journey.get_topic_by_name(topic_name)
    if not topic:
        return (
            render_template("error.html", message=f"Topic '{topic_name}' not found"),
            404,
        )

    # Get related facts
    facts = learning_journey.get_facts_by_topic(topic_name)

    # Find related topics (topics that have this topic as a prerequisite)
    all_topics = learning_journey.get_topics()
    related_topics = [t for t in all_topics if topic_name in t.get("prerequisites", [])]

    # Get user's learning statistics
    stats = learning_journey.get_learning_statistics(user_id)

    # Calculate progress
    topic_progress = stats.get("topic_progress", {})
    progress = int(topic_progress.get(topic_name, 0) * 100)  # Convert to percentage

    # Calculate facts learned
    fact_mastery = stats.get("fact_mastery", {})
    facts_learned = sum(
        1
        for fact_id, mastery in fact_mastery.items()
        if mastery > 0 and learning_journey.get_fact(fact_id).get("topic") == topic_name
    )
    facts_learned_percent = int((facts_learned / max(1, len(facts))) * 100)

    # Log this topic exploration
    learning_journey.log_event(
        user_id=user_id, event_type="topic_explored", details={"topic": topic_name}
    )

    return render_template(
        "learning/topic_detail.html",
        topic=topic,
        facts=facts,
        related_topics=related_topics,
        progress=progress,
        facts_learned=facts_learned,
        facts_learned_percent=facts_learned_percent,
    )


@learning_bp.route("/facts/<fact_id>")
def view_fact(fact_id):
    """View a specific fact."""
    user_id = session.get("user_id", "default_user")

    # Get fact information
    fact = learning_journey.get_fact(fact_id)
    if not fact:
        return render_template("error.html", message=f"Fact '{fact_id}' not found"), 404

    # Get related facts (other facts on the same topic)
    related_facts = learning_journey.get_facts_by_topic(fact["topic"])
    # Remove the current fact from related facts
    related_facts = [f for f in related_facts if f["id"] != fact_id]

    # Log this fact exploration
    learning_journey.log_event(
        user_id=user_id, event_type="fact_learned", details={"fact_id": fact_id}
    )

    return render_template(
        "learning/fact_detail.html", fact=fact, related_facts=related_facts
    )


@learning_bp.route("/graph")
def view_graph():
    """View the knowledge graph visualization."""
    graph = learning_journey.get_knowledge_graph()

    return render_template("learning/graph.html", graph=graph)


@learning_bp.route("/journey")
def view_journey():
    """View personal learning journey and progress."""
    user_id = session.get("user_id", "default_user")
    stats = learning_journey.get_learning_statistics(user_id)

    return render_template("learning/journey.html", stats=stats)


@learning_bp.route("/api/topics", methods=["GET"])
def api_get_topics():
    """API endpoint to get all topics."""
    topics = learning_journey.get_topics()
    return jsonify(topics)


@learning_bp.route("/api/facts", methods=["GET"])
def api_get_facts():
    """API endpoint to get facts, optionally filtered by topic."""
    topic = request.args.get("topic")
    if topic:
        facts = learning_journey.get_facts_by_topic(topic)
    else:
        facts = learning_journey.get_all_facts()

    return jsonify(facts)


@learning_bp.route("/api/graph", methods=["GET"])
def api_get_graph():
    """API endpoint to get the knowledge graph data."""
    graph = learning_journey.get_knowledge_graph()
    return jsonify(graph)


@learning_bp.route("/api/stats", methods=["GET"])
def api_get_stats():
    """API endpoint to get learning statistics."""
    user_id = session.get("user_id", "default_user")
    stats = learning_journey.get_learning_statistics(user_id)
    return jsonify(stats)


@learning_bp.route("/api/recommend", methods=["GET"])
def api_recommend_topics():
    """API endpoint to get topic recommendations."""
    user_id = session.get("user_id", "default_user")
    count = request.args.get("count", 3, type=int)
    recommendations = learning_journey.get_recommended_topics(user_id, limit=count)
    return jsonify(recommendations)


@learning_bp.route("/api/explore", methods=["POST"])
def api_explore_topic():
    """API endpoint to mark a topic as explored."""
    user_id = session.get("user_id", "default_user")
    data = request.json or {}

    # Extract data
    topic_name = data.get("topic")

    # Validate
    if not topic_name:
        return jsonify({"success": False, "message": "Topic name is required"}), 400

    # Check if topic exists
    topic = learning_journey.get_topic_by_name(topic_name)
    if not topic:
        return (
            jsonify({"success": False, "message": f"Topic '{topic_name}' not found"}),
            404,
        )

    # Log the exploration
    event = learning_journey.log_event(
        user_id=user_id, event_type="topic_explored", details={"topic": topic_name}
    )

    return jsonify(
        {
            "success": True,
            "message": f"Topic '{topic_name}' marked as explored",
            "event": event,
        }
    )


@learning_bp.route("/api/learn", methods=["POST"])
def api_learn_fact():
    """API endpoint to mark a fact as learned."""
    user_id = session.get("user_id", "default_user")
    data = request.json or {}

    # Extract data
    fact_id = data.get("fact_id")

    # Validate
    if not fact_id:
        return jsonify({"success": False, "message": "Fact ID is required"}), 400

    # Check if fact exists
    fact = learning_journey.get_fact(fact_id)
    if not fact:
        return (
            jsonify({"success": False, "message": f"Fact '{fact_id}' not found"}),
            404,
        )

    # Log the learning
    event = learning_journey.log_event(
        user_id=user_id,
        event_type="fact_learned",
        details={"fact_id": fact_id, "topic": fact["topic"]},
    )

    return jsonify(
        {
            "success": True,
            "message": f"Fact '{fact_id}' marked as learned",
            "event": event,
        }
    )


# Admin routes
@learning_bp.route("/admin")
def admin_dashboard():
    """Admin dashboard for managing learning content."""
    return render_template("learning/admin.html")


@learning_bp.route("/admin/add-topic", methods=["POST"])
def admin_add_topic():
    """Add a new topic."""
    data = request.json or {}

    # Extract data
    name = data.get("name")
    description = data.get("description")
    difficulty = data.get("difficulty")
    prerequisites = data.get("prerequisites", [])

    # Validate required fields
    if not all([name, description, difficulty]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    # Add the topic
    try:
        topic = learning_journey.add_topic(
            name=name,
            description=description,
            difficulty=difficulty,
            prerequisites=prerequisites,
        )

        return jsonify({"status": "success", "topic": topic})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@learning_bp.route("/admin/add-fact", methods=["POST"])
def admin_add_fact():
    """Add a new fact."""
    data = request.json or {}

    # Extract data
    topic = data.get("topic")
    content = data.get("content")
    source = data.get("source")

    # Validate required fields
    if not all([topic, content]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    # Add the fact
    try:
        fact = learning_journey.add_fact(topic=topic, content=content, source=source)

        return jsonify({"status": "success", "fact": fact})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@learning_bp.route("/admin/connect-concepts", methods=["POST"])
def admin_connect_concepts():
    """Connect concepts in the knowledge graph."""
    data = request.json or {}

    # Extract data
    concepts = data.get("concepts", [])

    # Validate
    if len(concepts) < 2:
        return (
            jsonify(
                {"status": "error", "message": "Need at least 2 concepts to connect"}
            ),
            400,
        )

    # Log the connection
    user_id = session.get("user_id", "default_user")
    learning_journey.log_event(
        user_id=user_id, event_type="concept_connected", details={"concepts": concepts}
    )

    return jsonify({"status": "success", "message": "Concepts connected successfully"})


def register_learning_routes(app):
    """Register the learning blueprint with the Flask app."""
    app.register_blueprint(learning_bp)
    logger.info("Learning routes registered")
