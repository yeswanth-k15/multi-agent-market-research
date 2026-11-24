import os
from pathlib import Path

from dotenv import load_dotenv

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the project root
load_dotenv(BASE_DIR / ".env")

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# LLM configuration
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
MANAGER_MODEL = os.getenv("MANAGER_MODEL", "gpt-4o")

# Output directories
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = BASE_DIR / "data"

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)


def validate_required_settings():
    """Check whether required API keys are configured."""

    missing_keys = []

    if not OPENAI_API_KEY:
        missing_keys.append("OPENAI_API_KEY")

    if not TAVILY_API_KEY:
        missing_keys.append("TAVILY_API_KEY")

    if missing_keys:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_keys)}"
        )