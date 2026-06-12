# Submission Requirements — Critical Checklist

## Adaption Track Rules (MUST follow exactly)

### Valid Submission Flow
```
Adaption Platform → Export Dataset → Publish to HF/Kaggle → Submit
```

### Requirements (ALL mandatory)
- [ ] Dataset MUST be **created using the Adaption platform** (SDK or web UI — same lifecycle)
- [ ] Dataset MUST be **exported directly from Adaption** (via `client.datasets.download()`)
- [ ] Published to **HuggingFace** (open-source, public)
- [ ] Published to **Kaggle** (open-source, public)
- [ ] Credit **Adaption** in dataset description/README prominently
- [ ] Share dataset links in **Discord channel**
- [ ] Submit through **form**: https://uc9yb.share.hsforms.com/2VyQDViA5RQOCS3ydhGF6mA
- [ ] 2-minute **demo video** explaining product and technical implementation
- [ ] **Functional prototype** or working AI workflow demonstrated
- [ ] Complete **project code** on GitHub (hackathon repo)

### What WILL NOT qualify
- Taking an existing dataset and uploading it
- Creating a dataset using external tools only
- Uploading a non-Adaption dataset to HF/Kaggle
- Dataset with no meaningful Adaption platform usage

### Key fact: Adaption team CAN VERIFY which datasets were exported from their platform

### Our approach (VALID because):
- We use `pip install adaption` SDK (docs say: "The API and Python SDK expose the same lifecycle you use in the web app")
- We call `client.datasets.upload_file()` → `client.datasets.run()` → `client.datasets.download()`
- This IS "creating on Adaption platform" and "exporting from Adaption"
- Quality metrics from `get_evaluation()` prove platform usage

---

## Submission Deadlines
- **Project Submission**: June 15, 2026 • 5:30 PM IST
- **Finalists Announcement**: Via email
- **Final Showdown**: June 25, 2026
- **Results**: June 30, 2026

## Judging Criteria
- Innovation and originality
- Technical implementation quality
- Real-world usefulness and scalability
- AI agent capabilities and execution
- Product thinking and user experience
- Quality of presentation and demonstration

## Adaption Track Prizes
- 1st: $1,000 USD
- 2nd: $600 USD
- 3rd: $400 USD

---

## API Keys
- Key Name: A_KEY
- Stored in `.env` (gitignored)

## Publishing Accounts Needed
- HuggingFace account + token (HF_TOKEN)
- Kaggle account + API credentials (KAGGLE_USERNAME, KAGGLE_KEY)
