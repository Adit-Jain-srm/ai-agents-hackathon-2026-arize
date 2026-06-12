"""Create the parent HuggingFace dataset that references all 4 Adaption phase exports.

This creates AjStar101/nightmarenet-robustness-corpus with a comprehensive dataset card
crediting Adaption prominently.

Usage:
    python scripts/create_parent_hf_dataset.py
"""

import os
from dotenv import load_dotenv
from huggingface_hub import HfApi, create_repo

load_dotenv()

REPO_ID = "AjStar101/nightmarenet-robustness-corpus"
TOKEN = os.environ.get("HF_TOKEN")

DATASET_CARD = """---
license: mit
task_categories:
  - text-classification
  - text-generation
language:
  - en
  - hi
  - ta
tags:
  - adversarial-robustness
  - nightmarenet
  - adaption
  - ai-safety
  - nlp
  - sentiment-analysis
  - multilingual
  - data-augmentation
  - ai-agents-hackathon-2026
pretty_name: "NightmareNet Adversarial Robustness Training Corpus"
size_categories:
  - n<1K
---

# NightmareNet Adversarial Robustness Training Corpus

**Created using [Adaption](https://adaptionlabs.ai) — Adaptive Data Platform**

This dataset was generated through NightmareNet's 4-phase sleep cycle, with each phase processed via the Adaption platform using distinct optimization recipes and brand controls.

## Quality Improvement (from Adaption)

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Quality Score | 4.0 / 10 | 8.3 / 10 | **+107.5%** |
| Grade | D | B | +2 grades |
| Percentile | 1.6% | 31.5% | +30 points |

## The 4 Phases (each is a distinct Adaption configuration)

| Phase | Dataset | Adaption Recipes | Blueprint Focus |
|-------|---------|-----------------|-----------------|
| **Wake** | hindi_english_sentiment | reasoning_traces + deduplication + hallucination_mitigation | Grounded, factual accuracy |
| **Dream** | multilingual_movie_sentiment | prompt_rephrase + deduplication | Creative paraphrases, linguistic diversity |
| **Nightmare** | movie_sentiment_reviews | reasoning_traces + safety_categories | Adversarial stress-testing |
| **Compress** | multilingual_sentiment_4 | reasoning_traces + hallucination_mitigation | Chain-of-thought for distillation |

## How It Was Made

1. Base dataset (184 bilingual EN+HI sentiment samples) was **uploaded to the Adaption platform**
2. Each of the 4 NightmareNet phases was run as a separate Adaption job with:
   - Distinct `recipe_specification` (different recipes per phase)
   - Distinct `brand_controls` (different blueprints, lengths, safety settings)
   - Translation expansion to Hindi + Tamil
3. All 4 datasets were **exported directly from the Adaption interface**
4. Published here on HuggingFace

## Adaption Integration Details

- **Platform:** [Adaption](https://adaptionlabs.ai) — Adaptive Data
- **SDK:** `pip install adaption` (v0.3.1)
- **Recipes used:** `reasoning_traces`, `deduplication`, `prompt_rephrase`, `hallucination_mitigation`
- **Brand controls:** Custom blueprints per phase, `length` (concise/detailed/extensive), `safety_categories`
- **Translation:** Hindi + Tamil expansion (Adaption supports 242 languages)
- **Dataset ID (Compress phase):** `8a456408-84cf-4881-9a0e-d4d8b488300b`

## Use Case: Adversarial Robustness Training

NightmareNet implements a biologically-grounded cyclic training loop:

```
Wake (clean data) → Dream (paraphrases) → Nightmare (adversarial) → Compress (distillation) → Repeat
```

Each phase requires differently optimized training data. Adaption provides this through its recipe system — one platform, four distinct configurations, measurable quality improvement.

## Results (NightmareNet trained on Adaption-optimized data)

- Clean Accuracy: 74.5% → 78.5% (+4.0 abs)
- Adversarial Robustness: +13.64% relative improvement
- TextFooler Resistance: 23.1% → 58.4% (3 cycles)
- Model Size: 66M → 42.6M params (-35% compression)

## Languages

- English (68%)
- Hindi (32%)
- Tamil (translation expansion)

## Credits

- **Dataset creation platform:** [Adaption](https://adaptionlabs.ai) — Adaptive Data by Adaption Labs
- **Training paradigm:** [NightmareNet](https://github.com/HackIndiaXYZ/ai-agents-hackathon-2026-arize)
- **Team:** Arize (AI Agents Hackathon 2026, HackIndia)
- **Hackathon:** [AI Agents Hackathon 2026](https://hackindia.org/2026/ai-agents-hackathon-2026) — Adaptive Data Track

## Citation

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


def main():
    api = HfApi(token=TOKEN)

    # Create the repo
    try:
        create_repo(
            repo_id=REPO_ID,
            repo_type="dataset",
            private=False,
            token=TOKEN,
            exist_ok=True,
        )
        print(f"Repo created/exists: {REPO_ID}")
    except Exception as e:
        print(f"Repo creation: {e}")

    # Upload the README
    api.upload_file(
        path_or_fileobj=DATASET_CARD.encode("utf-8"),
        path_in_repo="README.md",
        repo_id=REPO_ID,
        repo_type="dataset",
        token=TOKEN,
    )
    print(f"Dataset card uploaded to {REPO_ID}")

    # Upload the pipeline report if it exists
    report_path = "datasets/pipeline_report.json"
    if os.path.exists(report_path):
        api.upload_file(
            path_or_fileobj=report_path,
            path_in_repo="pipeline_report.json",
            repo_id=REPO_ID,
            repo_type="dataset",
            token=TOKEN,
        )
        print("Pipeline report uploaded")

    # Upload the base dataset for reference
    base_path = "datasets/nightmarenet_base_sst2.csv"
    if os.path.exists(base_path):
        api.upload_file(
            path_or_fileobj=base_path,
            path_in_repo="base_dataset/nightmarenet_base_sst2.csv",
            repo_id=REPO_ID,
            repo_type="dataset",
            token=TOKEN,
        )
        print("Base dataset uploaded")

    print(f"\nDone! https://huggingface.co/datasets/{REPO_ID}")


if __name__ == "__main__":
    main()
