"""End-to-end pipeline: Adaption -> NightmareNet -> Publish.

Single command to run the full hackathon submission workflow:
1. Create base dataset
2. Run 4-phase Adaption optimization
3. Download adapted data
4. (Optional) Publish to HuggingFace + Kaggle

Usage:
    python scripts/run_all.py
    python scripts/run_all.py --publish --hf-repo arize-team/nightmarenet-robustness-corpus
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def run_cmd(cmd: list, cwd: str = ".") -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"  Running: {' '.join(cmd)}")
    print(f"{'='*60}\n")
    result = subprocess.run(cmd, cwd=cwd)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="NightmareNet Full Pipeline")
    parser.add_argument("--publish", action="store_true", help="Publish to HF/Kaggle after pipeline")
    parser.add_argument("--hf-repo", default=None, help="HuggingFace repo ID for publishing")
    parser.add_argument("--kaggle-slug", default="nightmarenet-robustness-corpus")
    parser.add_argument("--phases", nargs="+", default=["all"])
    parser.add_argument("--estimate-only", action="store_true")
    args = parser.parse_args()

    python = sys.executable
    root = Path(__file__).parent.parent

    # Verify API key
    if not os.environ.get("ADAPTION_API_KEY"):
        print("ERROR: ADAPTION_API_KEY not set. Check your .env file.")
        sys.exit(1)

    # Step 1: Run Adaption pipeline
    pipeline_cmd = [python, str(root / "pipeline" / "run_adaption_pipeline.py")]
    pipeline_cmd.extend(["--phase"] + args.phases)
    pipeline_cmd.extend(["--output-dir", str(root / "datasets")])
    if args.estimate_only:
        pipeline_cmd.append("--estimate-only")

    if not run_cmd(pipeline_cmd, cwd=str(root)):
        print("\nPipeline FAILED. Check logs above.")
        sys.exit(1)

    if args.estimate_only:
        return

    # Step 2: Publish (optional)
    if args.publish:
        if args.hf_repo:
            hf_cmd = [
                python, str(root / "scripts" / "publish_to_hf.py"),
                "--repo-id", args.hf_repo,
                "--datasets-dir", str(root / "datasets"),
            ]
            run_cmd(hf_cmd, cwd=str(root))

        kaggle_cmd = [
            python, str(root / "scripts" / "publish_to_kaggle.py"),
            "--slug", args.kaggle_slug,
            "--datasets-dir", str(root / "datasets"),
        ]
        run_cmd(kaggle_cmd, cwd=str(root))

    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE")
    print("=" * 60)
    print(f"  Datasets: {root / 'datasets'}")
    print(f"  Report:   {root / 'datasets' / 'pipeline_report.json'}")
    if args.publish:
        if args.hf_repo:
            print(f"  HF:       https://huggingface.co/datasets/{args.hf_repo}")
        print(f"  Kaggle:   https://kaggle.com/datasets/YOUR_USER/{args.kaggle_slug}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
