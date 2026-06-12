# Adaption Pipeline Runs — Record of All 4 Phases

## Execution Date: June 6, 2026 ~8:15 PM IST
## Platform: adaptionlabs.ai (Web UI)
## Credits Used: ~16 out of 450 remaining
## Base Dataset: nightmarenet_base_sst2.csv (184 rows, 134 EN + 50 HI)

---

## Phase 1: WAKE — `hindi_english_sentiment`

| Setting | Value |
|---------|-------|
| **Adaption Name** | hindi_english_sentiment |
| **Dataset Type** | Instruction dataset |
| **Prompt Column** | text |
| **Completion Column** | label |
| **Expand** | Translate (Hindi + Tamil, ~10-50%) |
| **Recipes ON** | Reasoning traces, Hallucination mitigation, Prompt Deduplication |
| **Recipes OFF** | Prompt Rephrase, Metadata Injection, House Special |
| **Blueprint** | "You are preparing training data for NightmareNet, an AI robustness system designed to harden language models against adversarial attacks. Ensure all completions are factually accurate, well-grounded, and free of hallucination. Preserve the original sentiment intent and domain knowledge of each example. Focus on clarity, precision, and verifiable information. Each completion should provide clear reasoning for why the sentiment is positive or negative, citing specific linguistic cues from the prompt." |
| **Length** | Detailed |
| **Safety** | Harassment, Hate |
| **Hallucination Mitigation** | ON |
| **Status** | Job Launched |
| **Estimated Time** | ~13 minutes |

---

## Phase 2: DREAM — `multilingual_movie_sentiment`

| Setting | Value |
|---------|-------|
| **Adaption Name** | multilingual_movie_sentiment |
| **Dataset Type** | Instruction dataset |
| **Prompt Column** | text |
| **Completion Column** | label |
| **Expand** | Translate (Hindi + Tamil) |
| **Recipes ON** | Prompt Rephrase, Prompt Deduplication |
| **Recipes OFF** | Reasoning traces, Hallucination mitigation, Metadata Injection, House Special |
| **Blueprint** | "Generate creative paraphrases that preserve the core semantic meaning while introducing novel phrasings, sentence structures, and perspectives. The goal is linguistic diversity without factual drift. Maintain the same sentiment and intent as the original. Vary vocabulary, syntax, and tone while keeping the underlying opinion unchanged." |
| **Length** | Concise |
| **Safety** | None |
| **Hallucination Mitigation** | OFF |
| **Status** | Job Launched |
| **Estimated Time** | ~13 minutes |

---

## Phase 3: NIGHTMARE — `movie_sentiment_reviews`

| Setting | Value |
|---------|-------|
| **Adaption Name** | movie_sentiment_reviews |
| **Dataset Type** | Instruction dataset |
| **Prompt Column** | text |
| **Completion Column** | label |
| **Expand** | Translate (Hindi + Tamil) |
| **Recipes ON** | Reasoning traces |
| **Recipes OFF** | Prompt Rephrase, Deduplication, Hallucination mitigation, Metadata Injection, House Special |
| **Blueprint** | "Generate adversarially challenging examples that stress-test model robustness. Introduce subtle contradictions, ambiguous phrasings, misleading contexts, and edge-case formulations while staying within safety boundaries. Create hard negatives that force the model to be precise and not be fooled by superficial sentiment cues. The goal is to produce examples where surface-level features conflict with the true underlying sentiment." |
| **Length** | Detailed |
| **Safety** | Harassment, Hate |
| **Hallucination Mitigation** | OFF |
| **Status** | Job Launched |
| **Estimated Time** | ~13 minutes |

---

## Phase 4: COMPRESS — `multilingual_sentiment_4`

| Setting | Value |
|---------|-------|
| **Adaption Name** | multilingual_sentiment_4 |
| **Dataset Type** | Instruction dataset |
| **Prompt Column** | text |
| **Completion Column** | label |
| **Expand** | Translate (Hindi + Tamil) |
| **Recipes ON** | Reasoning traces, Hallucination mitigation |
| **Recipes OFF** | Prompt Rephrase, Deduplication, Metadata Injection, House Special |
| **Blueprint** | "Generate high-quality teacher outputs with explicit chain-of-thought reasoning. These will be used as distillation targets for model compression. For each review, provide thorough step-by-step reasoning that identifies sentiment indicators, analyzes tone, examines word choice, considers context, and arrives at a well-justified final sentiment classification. Be exhaustive in your reasoning chain." |
| **Length** | Extensive |
| **Safety** | None |
| **Hallucination Mitigation** | ON |
| **Status** | Job Launched |
| **Estimated Time** | ~13 minutes |

---

## Differentiation Summary (for judges)

| Dimension | Wake | Dream | Nightmare | Compress |
|-----------|------|-------|-----------|----------|
| **Primary Recipe** | Reasoning + Dedup | Rephrase + Dedup | Reasoning | Reasoning + Anti-hal |
| **Blueprint Focus** | Grounding/accuracy | Diversity/creativity | Adversarial challenge | Chain-of-thought |
| **Length Setting** | Detailed | Concise | Detailed | Extensive |
| **Safety Filters** | Harassment, Hate | None | Harassment, Hate | None |
| **Hallucination Mit.** | ON | OFF | OFF | ON |

Each phase uses a DISTINCT configuration. No two phases share the same recipe + blueprint + length combination. This is verifiable on Adaption's backend.

---

## Next Steps (after jobs complete)

1. [ ] View each completed dataset in Adaption dashboard
2. [ ] Screenshot quality scores (before/after) for each
3. [ ] Export/Download all 4 datasets (JSONL or CSV)
4. [ ] Save to `datasets/` folder with phase names
5. [ ] Publish to HuggingFace as 4-split dataset
6. [ ] Publish to Kaggle
7. [ ] Update README with real quality metrics
8. [ ] Record demo video
9. [ ] Submit via form + Discord
