"""NightmareNet 4-Phase Adaption Pipeline.

Creates adversarial robustness training datasets using Adaption Labs' adaptive data
platform. Each phase of NightmareNet's sleep cycle maps to distinct Adaption recipes
and brand controls:

  Wake    -> Grounded, deduplicated data with reasoning traces
  Dream   -> Creative paraphrases preserving semantics
  Nightmare -> Adversarially challenging variants
  Compress -> Chain-of-thought teacher outputs for distillation

Usage:
    python pipeline/run_adaption_pipeline.py --phase all
    python pipeline/run_adaption_pipeline.py --phase wake
    python pipeline/run_adaption_pipeline.py --phase dream nightmare
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
import time
import tempfile
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("nightmarenet.adaption_pipeline")

from adaption import Adaption, DatasetTimeout


# ---------------------------------------------------------------------------
# Phase configuration
# ---------------------------------------------------------------------------

PHASE_CONFIGS: Dict[str, Dict[str, Any]] = {
    "wake": {
        "description": "Clean, grounded data with reasoning traces and deduplication",
        "column_mapping": {"prompt": "text", "completion": "label"},
        "brand_controls": {
            "hallucination_mitigation": True,
            "length": "detailed",
            "blueprint": (
                "You are preparing training data for NightmareNet, an AI robustness "
                "system. Ensure completions are factually accurate, well-grounded, "
                "and free of hallucination. Preserve the original intent and domain "
                "knowledge of each example. Focus on clarity, precision, and "
                "verifiable information."
            ),
        },
        "recipe_specification": {
            "recipes": {
                "reasoning_traces": True,
                "deduplication": True,
            },
        },
    },
    "dream": {
        "description": "Creative paraphrases preserving core semantic meaning",
        "column_mapping": {"prompt": "text"},
        "brand_controls": {
            "length": "concise",
            "blueprint": (
                "Generate creative paraphrases that preserve the core semantic "
                "meaning while introducing novel phrasings, sentence structures, "
                "and perspectives. The goal is linguistic diversity without "
                "factual drift. Maintain the same sentiment and intent as the "
                "original."
            ),
        },
        "recipe_specification": {
            "recipes": {
                "prompt_rephrase": True,
                "deduplication": True,
            },
        },
    },
    "nightmare": {
        "description": "Adversarially challenging examples for stress-testing robustness",
        "column_mapping": {"prompt": "text", "completion": "label"},
        "brand_controls": {
            "length": "detailed",
            "safety_categories": ["harassment", "hate"],
            "blueprint": (
                "Generate adversarially challenging examples that stress-test "
                "model robustness. Introduce subtle contradictions, ambiguous "
                "phrasings, misleading contexts, and edge-case formulations "
                "while staying within safety boundaries. The goal is to create "
                "hard negatives that force the model to be precise and not "
                "fooled by superficial cues."
            ),
        },
        "recipe_specification": {
            "recipes": {
                "reasoning_traces": True,
            },
        },
    },
    "compress": {
        "description": "High-quality teacher outputs with chain-of-thought for distillation",
        "column_mapping": {"prompt": "text", "completion": "label"},
        "brand_controls": {
            "hallucination_mitigation": True,
            "length": "extensive",
            "blueprint": (
                "Generate high-quality teacher outputs with explicit "
                "chain-of-thought reasoning. These will be used as distillation "
                "targets for model compression. Be thorough, accurate, and logical. "
                "Show your reasoning step by step before giving the final answer."
            ),
        },
        "recipe_specification": {
            "recipes": {
                "reasoning_traces": True,
            },
        },
    },
}


@dataclass
class PhaseResult:
    phase: str
    dataset_id: str
    run_id: Optional[str] = None
    status: str = "pending"
    estimated_credits: Optional[float] = None
    quality_before: Optional[float] = None
    quality_after: Optional[float] = None
    improvement_percent: Optional[float] = None
    download_url: Optional[str] = None
    error: Optional[str] = None
    duration_seconds: float = 0.0


@dataclass
class PipelineReport:
    phases: List[PhaseResult] = field(default_factory=list)
    total_duration_seconds: float = 0.0
    base_dataset: str = ""
    total_credits_consumed: float = 0.0

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


# ---------------------------------------------------------------------------
# Base dataset creation (SST-2 sentiment subset for NLP robustness)
# ---------------------------------------------------------------------------

SST2_SAMPLES = [
    ("a stirring , funny and finally transporting re-imagining of beauty and the beast and 1930s horror films", "positive"),
    ("apparently reassembled from the cutting-room floor of any given daytime soap", "negative"),
    ("they presume their audience wo n't sit still for a nice story about good people", "negative"),
    ("this is a visually stunning rumination on love , memory , history and the bonds between mothers and daughters", "positive"),
    ("a sometimes tedious film", "negative"),
    ("the rock is destined to be the 21st century 's new conan and that he 's going to make a splash even greater than arnold schwarzenegger", "positive"),
    ("an absurdist comedy about a city that has been reduced to rubble by an earthquake", "negative"),
    ("effective but too-tepid biopic", "negative"),
    ("if you sometimes like to go to the movies to have fun , wasabi is a good place to start", "positive"),
    ("emerges as something rare , an issue movie that 's so honest and keenly observed that it does n't feel like one", "positive"),
    ("the film provides some great insight into the mindset of paranoid ,�, gun-loving separatists", "positive"),
    ("offers that rare combination of entertainment and education", "positive"),
    ("perhaps no picture ever made has more literally showed that the road to hell is paved with good intentions", "negative"),
    ("steers turns in a snappy screenplay that curls at the edges ; it 's so clever you want to hate it", "positive"),
    ("but he somehow pulls it off", "positive"),
    ("take care of my cat offers a refreshingly different slice of asian cinema", "positive"),
    ("a film really about nothing at all", "negative"),
    ("demonstrates that the director of such hollywood blockbusters as patriot games can still turn out a small , personal film with an emotional wallop", "positive"),
    ("the entire movie is filled with deja vu moments", "negative"),
    ("this overlong infomercial is an utterly charming film with a life-affirming message", "positive"),
    ("it 's a charming and often affecting journey", "positive"),
    ("unflinchingly bleak and desperate", "negative"),
    ("allows us to hope that nollywood invasion is on the rise", "positive"),
    ("the survey course removes the documentary from its usual ghetto", "positive"),
    ("a decent entry into the sentimental-dog-movie genre", "positive"),
    ("a badly edited waste of cellulose", "negative"),
    ("while the ensemble players are excellent , it 's really clooney 's film", "positive"),
    ("pretty much sucks", "negative"),
    ("if this movie were a person , i 'd say it had terminal depression and no will to live", "negative"),
    ("does a 180 on its subject and083 concludes by pulling every heartstring it 's tweaked so far", "positive"),
    ("the acting , costumes , music , cinematography and sound are all astounding given the production 's low budget", "positive"),
    ("it is not a mass-audience entertainment but an uncompromising piece of art", "positive"),
    ("a slow , non-eventful ride that only tests your patience", "negative"),
    ("the film 's center will not hold", "negative"),
    ("a quiet , pure , elliptical film", "positive"),
    ("a thoughtful , provocative , insistently humanizing film", "positive"),
    ("there 's a lot to recommend this movie", "positive"),
    ("the script is badly crafted and the ending is a letdown", "negative"),
    ("you will emerge with a greater knowledge of the history of the(nft movement", "positive"),
    ("a movie of ideas that manages to be just as thrilling as a movie of action", "positive"),
    ("the production qualities are first-rate , everything looking as it should", "positive"),
    ("too slow for a younger audience , and too routine for an older one", "negative"),
    ("it 's rare to find a film that manages to be both brutally honest and darkly funny", "positive"),
    ("a celebration of queli quirkiness , visual wit , and the magic of silent-era filmmaking", "positive"),
    ("overly long and boring adaptation of a stephen king novel", "negative"),
    ("you 'll forget it by the time you get to the parking lot", "negative"),
    ("a perfect movie for those who like their films with unexpected twists", "positive"),
    ("the most hopelessly monotonous film of the year , noteworthy only for the depths of its aesthetic failure", "negative"),
    ("succeeds because it trusts its characters to tell the story", "positive"),
    ("evokes the wistful spirit of a lazy , sun-drenched summer afternoon", "positive"),
]

# Hindi sentiment samples — demonstrating multilingual capability (Adaption supports 242 languages)
HINDI_SAMPLES = [
    ("यह फिल्म बहुत ही प्रेरणादायक और मनोरंजक है", "positive"),
    ("कहानी बहुत धीमी और उबाऊ थी, समय की बर्बादी", "negative"),
    ("अभिनय शानदार था और संगीत ने दिल जीत लिया", "positive"),
    ("इस फिल्म में कोई नई बात नहीं है, पुरानी कहानी का दोहराव", "negative"),
    ("निर्देशन कमाल का है, हर दृश्य बहुत सोच-समझकर बनाया गया है", "positive"),
    ("पटकथा कमजोर है और अंत निराशाजनक", "negative"),
    ("भारतीय सिनेमा के लिए एक मील का पत्थर, बहुत गर्व की बात", "positive"),
    ("बजट बहुत खर्च किया लेकिन कहानी में दम नहीं", "negative"),
    ("इस तरह की फिल्में बहुत कम बनती हैं, अद्भुत अनुभव", "positive"),
    ("पूरी फिल्म में एक भी ऐसा दृश्य नहीं जो याद रहे", "negative"),
    ("हर किरदार ने अपनी भूमिका में जान डाल दी", "positive"),
    ("तीन घंटे की फिल्म जो दस मिनट में बताई जा सकती थी", "negative"),
    ("संवाद बहुत प्रभावशाली हैं और सोचने पर मजबूर करते हैं", "positive"),
    ("एक शानदार प्रयास जो भारतीय फिल्म उद्योग को नई दिशा देता है", "positive"),
    ("बिल्कुल बेकार फिल्म, पैसे और समय दोनों बर्बाद", "negative"),
]


def create_base_dataset_csv(output_path: Path) -> Path:
    """Create the multilingual sentiment dataset for Adaption ingestion.
    
    Uses the standalone generator for a 184-sample bilingual corpus.
    """
    import importlib
    import sys
    # Ensure pipeline package is importable
    pipeline_dir = str(Path(__file__).parent)
    if pipeline_dir not in sys.path:
        sys.path.insert(0, pipeline_dir)
    from generate_dataset import generate_dataset
    csv_path = generate_dataset(str(output_path / "nightmarenet_base_sst2.csv"))
    return Path(csv_path)


# ---------------------------------------------------------------------------
# Retry helper for 503 outages
# ---------------------------------------------------------------------------

def _retry_with_backoff(fn, max_retries=5, initial_delay=10.0, description="API call"):
    """Retry a function with exponential backoff, handling 503 outages."""
    last_exc = None
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            last_exc = e
            err_str = str(e)
            if "503" in err_str or "502" in err_str or "500" in err_str:
                delay = initial_delay * (2 ** attempt)
                logger.warning(
                    f"{description} got server error (attempt {attempt+1}/{max_retries}), "
                    f"retrying in {delay:.0f}s..."
                )
                time.sleep(delay)
            else:
                raise
    raise last_exc

class AdaptionPipeline:
    """Orchestrates the 4-phase NightmareNet dataset creation via Adaption."""

    def __init__(self, api_key: Optional[str] = None, output_dir: str = "datasets"):
        self.api_key = api_key or os.environ.get("ADAPTION_API_KEY")
        if not self.api_key:
            raise ValueError("ADAPTION_API_KEY must be set")
        self.client = Adaption(api_key=self.api_key)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.report = PipelineReport()

    def upload_base_dataset(self, csv_path: Path) -> str:
        """Upload the base dataset to Adaption and return dataset_id."""
        logger.info(f"Uploading base dataset: {csv_path}")

        result = _retry_with_backoff(
            lambda: self.client.datasets.upload_file(str(csv_path), name="nightmarenet-robustness-corpus"),
            description="upload_file",
        )
        dataset_id = result.dataset_id
        logger.info(f"Upload initiated, dataset_id={dataset_id}")

        # Wait for file processing to complete
        logger.info("Waiting for ingestion to complete...")
        for i in range(60):
            status = self.client.datasets.get_status(dataset_id)
            if getattr(status, "row_count", None) is not None:
                logger.info(f"Ingestion complete: {status.row_count} rows detected")
                break
            time.sleep(2)
        else:
            raise TimeoutError("Dataset ingestion did not complete within 120s")

        self.report.base_dataset = str(csv_path)
        return dataset_id

    def estimate_phase(self, dataset_id: str, phase: str) -> Optional[float]:
        """Estimate credits for a phase without starting the run."""
        config = PHASE_CONFIGS[phase]
        try:
            estimate = self.client.datasets.run(
                dataset_id,
                column_mapping=config["column_mapping"],
                brand_controls=config.get("brand_controls"),
                recipe_specification=config.get("recipe_specification"),
                estimate=True,
            )
            credits = getattr(estimate, "estimated_credits_consumed", None)
            logger.info(f"Phase '{phase}' estimated at {credits} credits")
            return credits
        except Exception as e:
            logger.warning(f"Could not estimate phase '{phase}': {e}")
            return None

    def run_phase(self, dataset_id: str, phase: str) -> PhaseResult:
        """Execute a single Adaption phase and wait for completion."""
        config = PHASE_CONFIGS[phase]
        result = PhaseResult(phase=phase, dataset_id=dataset_id)
        start_time = time.time()

        logger.info(f"{'='*60}")
        logger.info(f"PHASE: {phase.upper()} — {config['description']}")
        logger.info(f"{'='*60}")

        try:
            # Upload a fresh copy for this phase (each phase gets its own dataset)
            csv_path = self.output_dir / "nightmarenet_base_sst2.csv"
            upload = _retry_with_backoff(
                lambda: self.client.datasets.upload_file(str(csv_path), name=f"nightmarenet-{phase}-phase"),
                description=f"upload ({phase})",
            )
            phase_dataset_id = upload.dataset_id
            result.dataset_id = phase_dataset_id
            logger.info(f"Uploaded phase dataset: {phase_dataset_id}")

            # Wait for ingestion
            for _ in range(60):
                status = self.client.datasets.get_status(phase_dataset_id)
                if getattr(status, "row_count", None) is not None:
                    break
                time.sleep(2)

            # Estimate
            credits = self.estimate_phase(phase_dataset_id, phase)
            result.estimated_credits = credits

            # Run adaptation
            logger.info(f"Starting {phase} adaptation run...")
            run = self.client.datasets.run(
                phase_dataset_id,
                column_mapping=config["column_mapping"],
                brand_controls=config.get("brand_controls"),
                recipe_specification=config.get("recipe_specification"),
            )
            result.run_id = getattr(run, "run_id", None)
            logger.info(f"Run started: {result.run_id}")

            # Wait for completion
            logger.info("Waiting for adaptation to complete...")
            try:
                final = self.client.datasets.wait_for_completion(
                    phase_dataset_id, timeout=1800
                )
                result.status = getattr(final, "status", "unknown")
                if getattr(final, "error", None):
                    result.error = str(final.error)
                    logger.error(f"Phase '{phase}' failed: {result.error}")
                else:
                    logger.info(f"Phase '{phase}' completed: {result.status}")
            except DatasetTimeout:
                result.status = "timeout"
                result.error = "Timed out after 1800s"
                logger.warning(f"Phase '{phase}' timed out")

            # Get quality evaluation
            if result.status in ("succeeded", "ready"):
                self._fetch_quality(phase_dataset_id, result)
                self._download_result(phase_dataset_id, phase, result)

        except Exception as e:
            result.status = "error"
            result.error = str(e)
            logger.error(f"Phase '{phase}' error: {e}")

        result.duration_seconds = time.time() - start_time
        self.report.phases.append(result)
        return result

    def _fetch_quality(self, dataset_id: str, result: PhaseResult) -> None:
        """Poll evaluation metrics after a successful run."""
        logger.info("Fetching quality evaluation...")
        for _ in range(30):
            try:
                evaluation = self.client.datasets.get_evaluation(dataset_id)
                eval_status = getattr(evaluation, "status", "pending")
                if eval_status in ("succeeded", "failed", "skipped"):
                    if eval_status == "succeeded" and getattr(evaluation, "quality", None):
                        q = evaluation.quality
                        result.quality_before = getattr(q, "score_before", None)
                        result.quality_after = getattr(q, "score_after", None)
                        result.improvement_percent = getattr(q, "improvement_percent", None)
                        logger.info(
                            f"Quality: {result.quality_before} -> {result.quality_after} "
                            f"({result.improvement_percent}% improvement)"
                        )
                    break
                time.sleep(5)
            except Exception as e:
                logger.debug(f"Evaluation poll error: {e}")
                time.sleep(5)

    def _download_result(self, dataset_id: str, phase: str, result: PhaseResult) -> None:
        """Download the adapted dataset."""
        try:
            url = self.client.datasets.download(dataset_id, file_format="jsonl")
            result.download_url = url
            logger.info(f"Download URL ready for phase '{phase}'")

            # Download to local file
            import httpx
            output_file = self.output_dir / f"nightmarenet_{phase}_adapted.jsonl"
            response = httpx.get(url)
            output_file.write_bytes(response.content)
            logger.info(f"Downloaded to {output_file} ({len(response.content)} bytes)")
        except Exception as e:
            logger.warning(f"Download failed for '{phase}': {e}")

    def run_all_phases(self, phases: Optional[List[str]] = None) -> PipelineReport:
        """Run all (or selected) phases of the pipeline."""
        phases = phases or ["wake", "dream", "nightmare", "compress"]
        start = time.time()

        # Create base dataset
        csv_path = create_base_dataset_csv(self.output_dir)

        for phase in phases:
            if phase not in PHASE_CONFIGS:
                logger.warning(f"Unknown phase: {phase}, skipping")
                continue
            self.run_phase("", phase)

        self.report.total_duration_seconds = time.time() - start
        self.report.total_credits_consumed = sum(
            r.estimated_credits or 0 for r in self.report.phases
        )

        # Save report
        report_path = self.output_dir / "pipeline_report.json"
        report_path.write_text(self.report.to_json(), encoding="utf-8")
        logger.info(f"Pipeline report saved to {report_path}")

        self._print_summary()
        return self.report

    def _print_summary(self) -> None:
        """Print a formatted summary of all phases."""
        print("\n" + "=" * 70)
        print("  NIGHTMARENET ADAPTION PIPELINE — SUMMARY")
        print("=" * 70)
        print(f"  Base dataset: {self.report.base_dataset}")
        print(f"  Total duration: {self.report.total_duration_seconds:.1f}s")
        print(f"  Total credits: ~{self.report.total_credits_consumed:.1f}")
        print("-" * 70)
        for r in self.report.phases:
            status_icon = "OK" if r.status in ("succeeded", "ready") else "FAIL"
            quality = ""
            if r.improvement_percent is not None:
                quality = f" | Quality: +{r.improvement_percent:.1f}%"
            print(
                f"  [{status_icon}] {r.phase.upper():10} "
                f"| {r.duration_seconds:.0f}s "
                f"| ~{r.estimated_credits or 0:.1f} credits"
                f"{quality}"
            )
        print("=" * 70 + "\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="NightmareNet 4-Phase Adaption Pipeline"
    )
    parser.add_argument(
        "--phase",
        nargs="+",
        default=["all"],
        choices=["all", "wake", "dream", "nightmare", "compress"],
        help="Which phases to run (default: all)",
    )
    parser.add_argument(
        "--output-dir",
        default="datasets",
        help="Output directory for adapted datasets",
    )
    parser.add_argument(
        "--estimate-only",
        action="store_true",
        help="Only estimate credits without running",
    )
    args = parser.parse_args()

    phases = None if "all" in args.phase else args.phase

    pipeline = AdaptionPipeline(output_dir=args.output_dir)

    if args.estimate_only:
        csv_path = create_base_dataset_csv(Path(args.output_dir))
        # Upload once to get dataset_id
        dataset_id = pipeline.upload_base_dataset(csv_path)
        total = 0.0
        for phase in (phases or ["wake", "dream", "nightmare", "compress"]):
            cost = pipeline.estimate_phase(dataset_id, phase)
            total += cost or 0
        print(f"\nEstimated total: ~{total:.1f} credits")
    else:
        pipeline.run_all_phases(phases)


if __name__ == "__main__":
    main()
