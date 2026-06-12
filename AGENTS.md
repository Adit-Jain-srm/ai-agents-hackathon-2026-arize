## Learned User Preferences

- Prefers a "winner mindset" — work both smartly and hard; optimize for hackathon judging criteria
- Self-evaluates tool usage before proceeding (e.g., "are you using Adaption correctly?")
- Wants end-to-end automation: generate dataset → adapt via API → publish to HuggingFace + Kaggle
- Concerned about dataset size — prefers larger, more impressive datasets over minimal examples
- Expects the agent to understand hackathon submission rules and comply automatically
- Prefers using Adaption's direct export (Share > HuggingFace/Kaggle) for strongest verifiable proof
- Wants all information stored, updated, and synced across project docs/md files

## Learned Workspace Facts

- Project: "NightmareNet x Adaption" for AI Agents Hackathon 2026 (Team Arize, Adaptive Data Track)
- Tech stack: Python 3.13, Adaption Labs API, HuggingFace Hub, Kaggle API
- 4-phase pipeline concept: Wake → Dream → Nightmare → Compress (biologically-grounded adversarial robustness)
- Base dataset: `datasets/nightmarenet_base_sst2.csv` (SST-2 sentiment + Hindi multilingual examples)
- Pipeline scripts in `pipeline/` (generate_dataset.py, run_adaption_pipeline.py)
- Publishing scripts in `scripts/` (publish_to_hf.py, publish_to_kaggle.py, run_all.py)
- Submission requirement: dataset MUST be created through Adaption platform, not just uploaded externally
- Must publish to both HuggingFace and Kaggle, credit Adaption in description
- Hackathon deadlines: form submission by June 14; final project deadline June 15, 5:30 PM IST
- Two mandatory submission steps: Discord post (#hackindia-hackathon) + official HubSpot form
- All 4 Adaption runs completed: quality D→B (4.0→8.3), 107.5% improvement, ~4 credits each
- Adaption has direct export buttons (Share > HuggingFace / Kaggle) — preferred over manual download
