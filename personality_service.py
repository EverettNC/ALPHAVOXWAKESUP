"""Personality management for alphavox Dashboard."""

import logging
from typing import Dict, Any

from config import Settings

logger = logging.getLogger(__name__)


class PersonalityService:
    """Provides access to alphavox's personality profile."""

    def __init__(self):
        self.settings = Settings()
        self.profile: Dict[str, Any] = {}

    def load_profile(self) -> Dict[str, Any]:
        """Load the personality profile from settings."""
        self.profile = self.settings.identity
        logger.info(
            "Personality profile loaded for %s", self.profile.get("name", "alphavox")
        )
        return self.profile

        # In start():
        self.personality.load_profile()  # ← LOADS alphavox's character config

    def get_trait(self, trait_name: str) -> Any:
        """Retrieve a specific trait from the profile."""
        if not self.profile:
            self.load_profile()

        traits = self.profile.get("personality", {}).get("core_traits", [])
        return trait_name in traits
