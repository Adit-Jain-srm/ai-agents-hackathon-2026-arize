# Adaption Integration — Technical Configuration

This document details the 4 distinct Adaption platform configurations used in the NightmareNet pipeline. Each phase maps to a unique combination of recipes, brand controls, and blueprints — demonstrating deep, meaningful integration with Adaption's adaptive data capabilities.

---

## Configuration Matrix

| Parameter | Wake | Dream | Nightmare | Compress |
|-----------|------|-------|-----------|----------|
| **Adaption Name** | hindi_english_sentiment | multilingual_movie_sentiment | movie_sentiment_reviews | multilingual_sentiment_4 |
| **Recipes** | reasoning_traces, deduplication, hallucination_mitigation | prompt_rephrase, deduplication | reasoning_traces | reasoning_traces, hallucination_mitigation |
| **Length** | Detailed | Concise | Detailed | Extensive |
| **Safety** | Harassment, Hate | None | Harassment, Hate | None |
| **Hallucination Mit.** | ON | OFF | OFF | ON |
| **Translation** | Hindi + Tamil | Hindi + Tamil | Hindi + Tamil | Hindi + Tamil |
| **Output Rows** | 378 | 378 | 386 | 376 |
| **Quality Improvement** | +102.5% | +153.3% | +170.0% | +107.5% |
| **Final Grade** | B | B | B | B |

---

## Phase Blueprints

### Wake — Grounding & Factual Accuracy

> You are preparing training data for NightmareNet, an AI robustness system designed to harden language models against adversarial attacks. Ensure all completions are factually accurate, well-grounded, and free of hallucination. Preserve the original sentiment intent and domain knowledge of each example. Focus on clarity, precision, and verifiable information. Each completion should provide clear reasoning for why the sentiment is positive or negative, citing specific linguistic cues from the prompt.

### Dream — Creative Diversity & Linguistic Invariance

> Generate creative paraphrases that preserve the core semantic meaning while introducing novel phrasings, sentence structures, and perspectives. The goal is linguistic diversity without factual drift. Maintain the same sentiment and intent as the original. Vary vocabulary, syntax, and tone while keeping the underlying opinion unchanged.

### Nightmare — Adversarial Stress-Testing

> Generate adversarially challenging examples that stress-test model robustness. Introduce subtle contradictions, ambiguous phrasings, misleading contexts, and edge-case formulations while staying within safety boundaries. Create hard negatives that force the model to be precise and not be fooled by superficial sentiment cues. The goal is to produce examples where surface-level features conflict with the true underlying sentiment.

### Compress — Chain-of-Thought Distillation

> Generate high-quality teacher outputs with explicit chain-of-thought reasoning. These will be used as distillation targets for model compression. For each review, provide thorough step-by-step reasoning that identifies sentiment indicators, analyzes tone, examines word choice, considers context, and arrives at a well-justified final sentiment classification. Be exhaustive in your reasoning chain.

---

## Adaption SDK Equivalent

Each phase can also be reproduced programmatically via the Adaption Python SDK:

```python
from adaption import Adaption

client = Adaption(api_key="pt_live_...")

# Example: Compress phase configuration
job = client.datasets.run(
    dataset_id,
    column_mapping={"prompt": "text", "completion": "label"},
    recipe_specification={
        "recipes": {
            "reasoning_traces": True,
            "deduplication": False,
            "prompt_rephrase": False,
        },
    },
    brand_controls={
        "length": "extensive",
        "hallucination_mitigation": True,
        "blueprint": "Generate high-quality teacher outputs with explicit chain-of-thought reasoning...",
    },
    training_type="instruction_dataset",
    job_specification={"max_rows": 184},
)
```

---

## Verification

All datasets were exported directly from the Adaption platform via the **Share > Hugging Face** feature, creating a verifiable audit trail on Adaption's backend. Each exported dataset includes Adaption's auto-generated branding, quality metrics charts, and evaluation results.

- Dataset ID (Compress): `8a456408-84cf-4881-9a0e-d4d8b488300b`
- Platform: adaptionlabs.ai
- Export method: Share > Hugging Face (direct integration)
- Credits consumed: ~16 out of 450 available
