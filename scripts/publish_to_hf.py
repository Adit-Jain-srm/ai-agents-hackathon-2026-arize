"""Publish adapted datasets to HuggingFace Hub.

Takes the JSONL outputs from the Adaption pipeline and publishes them
as a single HuggingFace dataset with splits for each NightmareNet phase.

Usage:
    python scripts/publish_to_hf.py --repo-id YOUR_USERNAME/nightmarenet-robustness-corpus
"""

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from datasets import Dataset, DatasetDict
from huggingface_hub import HfApi

load_dotenv()

DATASET_CARD = """---
license: apache-2.0
task_categories:
  - text-classification
  - text-generation
language:
  - en
tags:
  - adversarial-robustness
  - nightmarenet
  - adaption
  - ai-safety
  - nlp
  - sentiment-analysis
  - data-augmentation
pretty_name: "NightmareNet Adversarial Robustness Training Corpus"
size_categories:
  - n<1K
---

# NightmareNet Adversarial Robustness Training Corpus

**Created using [Adaption](https://adaptionlabs.ai) — Adaptive Data Platform**

This dataset was generated through NightmareNet's 4-phase sleep cycle, with each phase
processed via the Adaption platform's AI-powered data optimization pipeline.

## Dataset Description

NightmareNet implements a biologically-grounded cyclic training loop inspired by
sleep-mediated memory consolidation. This dataset contains the training data for
each phase, optimized through Adaption's recipes:

| Split | Phase | Adaption Recipe | Purpose |
|-------|-------|-----------------|---------|
| `wake` | Wake | Hallucination mitigation + Reasoning traces + Deduplication | Establish clean-data competence |
| `dream` | Dream | Prompt rephrase + Deduplication | Build invariance to plausible distribution shift |
| `nightmare` | Nightmare | Reasoning traces + Safety controls | Harden against worst-case perturbations |
| `compress` | Compress | Reasoning traces + Hallucination mitigation | Chain-of-thought teacher outputs for distillation |

## How It Was Made

1. Base dataset (SST-2 sentiment classification samples) was **created on the Adaption platform**
2. Each phase was processed through Adaption with phase-specific `brand_controls` and `recipe_specification`
3. Datasets were **exported from the Adaption interface** via the SDK
4. Published here for open-source access

## Adaption Integration

This dataset demonstrates deep integration with [Adaption Labs](https://adaptionlabs.ai):
- **Platform:** Adaptive Data by Adaption
- **SDK:** `pip install adaption` (v0.3.1)
- **Recipes used:** `reasoning_traces`, `deduplication`, `prompt_rephrase`
- **Brand controls:** `hallucination_mitigation`, `blueprint`, `safety_categories`, `length`

## Credits

- **Dataset creation platform:** [Adaption](https://adaptionlabs.ai) — Adaptive Data
- **Training paradigm:** [NightmareNet](https://github.com/HackIndiaXYZ/ai-agents-hackathon-2026-arize)
- **Hackathon:** AI Agents Hackathon 2026 (HackIndia) — Adaptive Data Track

## Quality Metrics (from Adaption)

Quality improvement scores are recorded in the pipeline report included in this repository.

## Usage

```python
from datasets import load_dataset

ds = load_dataset("YOUR_USERNAME/nightmarenet-robustness-corpus")

# Access individual phases
wake_data = ds["wake"]
dream_data = ds["dream"]
nightmare_data = ds["nightmare"]
compress_data = ds["compress"]
```

## Citation

If you use this dataset, please credit Adaption:

```
@misc{nightmarenet-robustness-corpus-2026,
  title={NightmareNet Adversarial Robustness Training Corpus},
  author={Team Arize},
  year={2026},
  publisher={Hugging Face},
  note={Created using Adaption (adaptionlabs.ai) Adaptive Data platform}
}
```
"""


def load_adapted_jsonl(path: Path) -> list:
    """Load a JSONL file into a list of dicts."""
    records = []
    if not path.exists():
        print(f"Warning: {path} not found, skipping")
        return records
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def build_dataset_dict(datasets_dir: Path) -> DatasetDict:
    """Build a DatasetDict from the adapted JSONL files."""
    splits = {}
    for phase in ["wake", "dream", "nightmare", "compress"]:
        jsonl_path = datasets_dir / f"nightmarenet_{phase}_adapted.jsonl"
        records = load_adapted_jsonl(jsonl_path)
        if records:
            splits[phase] = Dataset.from_list(records)
            print(f"  {phase}: {len(records)} rows")
        else:
            print(f"  {phase}: NO DATA (file missing or empty)")

    if not splits:
        raise ValueError("No adapted data found in any phase!")

    return DatasetDict(splits)


def publish(repo_id: str, datasets_dir: Path, token: Optional[str] = None):
    """Publish the dataset to HuggingFace Hub."""
    print(f"Building dataset from {datasets_dir}...")
    dataset_dict = build_dataset_dict(datasets_dir)

    print(f"\nPushing to HuggingFace: {repo_id}")
    dataset_dict.push_to_hub(
        repo_id,
        token=token,
        private=False,
    )

    # Upload the dataset card
    api = HfApi(token=token)
    api.upload_file(
        path_or_fileobj=DATASET_CARD.encode("utf-8"),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="dataset",
    )

    # Upload pipeline report if available
    report_path = datasets_dir / "pipeline_report.json"
    if report_path.exists():
        api.upload_file(
            path_or_fileobj=str(report_path),
            path_in_repo="pipeline_report.json",
            repo_id=repo_id,
            repo_type="dataset",
        )

    print(f"\nPublished! https://huggingface.co/datasets/{repo_id}")


Optional = type(None) | type  # Fix for forward reference


def main():
    parser = argparse.ArgumentParser(description="Publish adapted datasets to HuggingFace")
    parser.add_argument("--repo-id", required=True, help="HuggingFace repo ID (user/name)")
    parser.add_argument("--datasets-dir", default="datasets", help="Directory with adapted JSONL files")
    parser.add_argument("--token", default=None, help="HF token (or set HF_TOKEN env var)")
    args = parser.parse_args()

    token = args.token or os.environ.get("HF_TOKEN")
    publish(args.repo_id, Path(args.datasets_dir), token)


if __name__ == "__main__":
    main()
