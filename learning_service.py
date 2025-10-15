"""Learning services for alphavox Dashboard."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class LearningService:
    """Tracks learner progress and recommends actions."""

    def __init__(self):
        self.progress: Dict[str, Any] = {}

    def update_progress(self, user_id: str, metrics: Dict[str, Any]) -> None:
        """Update stored progress for a user."""
        logger.debug("Updating progress for %s: %s", user_id, metrics)
        self.progress[user_id] = metrics

    def get_progress(self, user_id: str) -> Dict[str, Any]:
        """Return stored progress for a user."""
        return self.progress.get(user_id, {})
