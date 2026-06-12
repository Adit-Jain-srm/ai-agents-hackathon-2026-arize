"""Publish adapted datasets to Kaggle.

Takes the JSONL outputs from the Adaption pipeline and publishes them as a Kaggle dataset.

Usage:
    python scripts/publish_to_kaggle.py --slug nightmarenet-robustness-corpus
"""

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


DATASET_METADATA = {
    "title": "NightmareNet Adversarial Robustness Training Corpus",
    "id": "{username}/nightmarenet-robustness-corpus",
    "licenses": [{"name": "Apache-2.0"}],
    "keywords": [
        "adversarial-robustness",
        "nightmarenet",
        "adaption",
        "ai-safety",
        "nlp",
        "sentiment-analysis",
    ],
    "resources": [],
}


DESCRIPTION = """# NightmareNet Adversarial Robustness Training Corpus

**Created using [Adaption](https://adaptionlabs.ai) — Adaptive Data Platform**

This dataset was generated through NightmareNet's 4-phase sleep cycle, with each phase
processed via the Adaption platform's AI-powered data optimization pipeline.

## Phases

- **wake** — Clean, grounded data with reasoning traces (Adaption: hallucination_mitigation + deduplication)
- **dream** — Creative paraphrases preserving semantics (Adaption: prompt_rephrase + deduplication)
- **nightmare** — Adversarially challenging examples (Adaption: reasoning_traces + safety controls)
- **compress** — Chain-of-thought teacher outputs (Adaption: reasoning_traces + hallucination_mitigation)

## Credits

- **Dataset creation platform:** [Adaption](https://adaptionlabs.ai) — Adaptive Data
- **Training paradigm:** NightmareNet
- **Team:** Arize (AI Agents Hackathon 2026, HackIndia)
"""


def main():
    parser = argparse.ArgumentParser(description="Publish adapted datasets to Kaggle")
    parser.add_argument("--slug", default="nightmarenet-robustness-corpus")
    parser.add_argument("--datasets-dir", default="datasets")
    parser.add_argument("--username", default=None)
    args = parser.parse_args()

    username = args.username or os.environ.get("KAGGLE_USERNAME")
    if not username:
        print("ERROR: Set KAGGLE_USERNAME env var or pass --username")
        return

    datasets_dir = Path(args.datasets_dir)
    staging_dir = Path("kaggle_staging")
    staging_dir.mkdir(exist_ok=True)

    # Copy adapted files to staging
    for phase in ["wake", "dream", "nightmare", "compress"]:
        src = datasets_dir / f"nightmarenet_{phase}_adapted.jsonl"
        if src.exists():
            shutil.copy2(src, staging_dir / f"{phase}.jsonl")
            print(f"  Staged: {phase}.jsonl")

    # Copy pipeline report
    report = datasets_dir / "pipeline_report.json"
    if report.exists():
        shutil.copy2(report, staging_dir / "pipeline_report.json")

    # Write metadata
    metadata = DATASET_METADATA.copy()
    metadata["id"] = f"{username}/{args.slug}"
    (staging_dir / "dataset-metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )

    # Write description
    (staging_dir / "description.md").write_text(DESCRIPTION, encoding="utf-8")

    print(f"\nStaging directory ready at: {staging_dir}")
    print("To publish, run:")
    print(f"  kaggle datasets create -p {staging_dir}")
    print(f"  # or: kaggle datasets version -p {staging_dir} -m 'Initial upload'")

    # Try auto-publish if kaggle CLI is available
    try:
        result = subprocess.run(
            ["kaggle", "datasets", "create", "-p", str(staging_dir)],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print(f"\nPublished to Kaggle: https://kaggle.com/datasets/{username}/{args.slug}")
        else:
            print(f"\nKaggle CLI error: {result.stderr}")
            print("Manual upload may be required.")
    except FileNotFoundError:
        print("\nKaggle CLI not found. Install with: pip install kaggle")
        print("Then run the command above manually.")
    except Exception as e:
        print(f"\nKaggle publish error: {e}")


if __name__ == "__main__":
    main()
