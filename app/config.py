import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

NVIDIA_MODEL = os.getenv(
    "NVIDIA_MODEL",
    "nvidia/nemotron-3-ultra-550b-a55b"
)

NVIDIA_BASE_URL = os.getenv(
    "NVIDIA_BASE_URL",
    "https://integrate.api.nvidia.com/v1"
)

# Persistent project registry
DATA_DIR = BASE_DIR / "data"
PROJECTS_REGISTRY_FILE = DATA_DIR / "projects.json"

# Existing default project
DEFAULT_PROJECT_ID = "sample_project"

# Scanner configuration
MAX_FILE_SIZE = 100_000

SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".html", ".css",
    ".json", ".md", ".txt", ".sql",
}

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
}