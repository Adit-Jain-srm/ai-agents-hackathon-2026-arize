"""Health check for Adaption API connection.

Usage:
    python scripts/check_adaption.py
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("ADAPTION_API_KEY")
if not api_key:
    print("FAIL: ADAPTION_API_KEY not set in environment or .env")
    sys.exit(1)

print(f"API Key: {api_key[:12]}...{api_key[-4:]}")

from adaption import Adaption

client = Adaption(api_key=api_key)

try:
    datasets = list(client.datasets.list(limit=3))
    print(f"OK: Connection successful! Found {len(datasets)} dataset(s).")
    for ds in datasets:
        did = getattr(ds, "dataset_id", "?")
        name = getattr(ds, "name", "unnamed")
        status = getattr(ds, "status", "?")
        print(f"  - {did}: {name} ({status})")
    sys.exit(0)
except Exception as e:
    error_str = str(e)
    if "503" in error_str:
        print("WARN: Adaption API is temporarily unavailable (503). Try again later.")
    elif "401" in error_str or "403" in error_str:
        print("FAIL: Authentication error. Check your API key.")
    else:
        print(f"FAIL: {type(e).__name__}: {error_str[:200]}")
    sys.exit(1)
