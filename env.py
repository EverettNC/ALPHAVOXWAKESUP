"""
Simplified env loader for AlphaVox
"""

import os
from dotenv import load_dotenv

def LoadEnv():
    """Load environment variables from .env files."""
    # Load from .env.production if it exists, otherwise .env
    if os.path.exists('.env.production'):
        load_dotenv('.env.production')
    elif os.path.exists('.env'):
        load_dotenv('.env')
    return True