"""Check HuggingFace and Kaggle auth status."""
from dotenv import load_dotenv
load_dotenv()

from huggingface_hub import HfApi
import os

# HuggingFace
try:
    token = os.environ.get("HF_TOKEN")
    api = HfApi(token=token)
    info = api.whoami()
    name = info.get("name", "unknown")
    print(f"HuggingFace: Logged in as '{name}'")
except Exception as e:
    print(f"HuggingFace: NOT authenticated ({type(e).__name__})")
    print("  Fix: run 'huggingface-cli login' or set HF_TOKEN in .env")

# Kaggle
kaggle_user = os.environ.get("KAGGLE_USERNAME")
kaggle_key = os.environ.get("KAGGLE_KEY")
if kaggle_user and kaggle_key:
    print(f"Kaggle: Configured (user={kaggle_user})")
else:
    print("Kaggle: NOT configured")
    print("  Fix: set KAGGLE_USERNAME and KAGGLE_KEY in .env")
