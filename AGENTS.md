## Learned User Preferences

- Prefers a "winner mindset" — work both smartly and hard; optimize for hackathon judging criteria
- Solo participant — uses "I" not "we"; correct all references to first person singular
- Self-evaluates tool usage before proceeding (e.g., "are you using Adaption correctly?")
- Wants end-to-end automation: generate dataset → adapt via API → publish to HuggingFace + Kaggle
- Concerned about dataset size — prefers larger, more impressive datasets over minimal examples
- Expects the agent to understand hackathon submission rules and comply automatically
- Prefers using Adaption's direct export (Share > HuggingFace/Kaggle) for strongest verifiable proof
- Wants all information stored, updated, and synced across project docs/md files
- Prefers short, concise outputs — asks for one-liners and condensed formats

## Learned Workspace Facts

- Project: "NightmareNet x Adaption" for AI Agents Hackathon 2026 (Team Arize, Adaptive Data Track)
- Tech stack: Python 3.13, Adaption Labs API, HuggingFace Hub, PyTorch, HuggingFace Transformers, DistilBERT, FastAPI, Next.js
- 4-phase pipeline concept: Wake → Dream → Nightmare → Compress (biologically-grounded adversarial robustness)
- Base dataset: `datasets/nightmarenet_base_sst2.csv` (SST-2 sentiment + Hindi multilingual examples)
- Pipeline scripts in `pipeline/` (generate_dataset.py, run_adaption_pipeline.py)
- Publishing scripts in `scripts/` (publish_to_hf.py, publish_to_kaggle.py, run_all.py, create_parent_hf_dataset.py)
- Submission requirement: dataset MUST be created through Adaption platform, not just uploaded externally
- Must publish to both HuggingFace and Kaggle, credit Adaption in description
- Hackathon deadlines: form submission by June 14; final project deadline June 15, 5:30 PM IST
- Two mandatory submission steps: Discord post (#hackindia-hackathon) + official HubSpot form
- All 4 Adaption runs completed: Wake +102.5%, Dream +153.3%, Nightmare +170.0%, Compress +107.5%
- GitHub repo: https://github.com/HackIndiaXYZ/ai-agents-hackathon-2026-arize
- HuggingFace account: AjStar101; parent dataset: AjStar101/nightmarenet-robustness-corpus
