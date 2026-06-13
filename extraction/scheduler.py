from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DISCOVERY_CHECKPOINT = ROOT / "out" / "checkpoints" / "discovery_checkpoint.json"
DEFAULT_QUERY_FILE = ROOT / "query_rahul2026 copy.py"
DEFAULT_OUT_DIR = ROOT / "out" / "query_benchmark"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strategy",
        choices=["periodic", "interval"],
        default="interval",
    )
    parser.add_argument("--hours", type=float, default=3.0)
    parser.add_argument("--max-runtime-hours", type=float)
    parser.add_argument("--mode", choices=["agentic", "human", "all"])
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--max-pages", type=int)
    parser.add_argument("--include-related", action="store_true")
    parser.add_argument("--daily-hour", type=int, default=23)
    parser.add_argument("--daily-minute", type=int, default=0)
    parser.add_argument("--stop-after-date")
    parser.add_argument("--query-file", default=str(DEFAULT_QUERY_FILE))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--repo-filter", default="repo:microsoft/vscode")
    parser.add_argument(
        "--run-type",
        choices=["split", "original", "both"],
        default="split",
    )
    parser.add_argument("--first-prs", type=int)
    parser.add_argument("--max-pr-ids", type=int)
    parser.add_argument("--max-repo-ids", type=int)
    parser.add_argument("--max-user-ids", type=int)
    parser.add_argument(
        "--resume-until-complete",
        action="store_true",
        help="Keep rerunning the same periodic extraction command until the discovery checkpoint clears.",
    )
    parser.add_argument(
        "--checkpoint-path",
        default=str(DEFAULT_DISCOVERY_CHECKPOINT),
        help="Path to the discovery checkpoint used to report resume/completion state.",
    )
    return parser.parse_args()


def _load_checkpoint(path: Path) -> dict[str, Any]:
    """Load discovery checkpoint state when present."""
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except Exception:
        return {}
    return {}


def _checkpoint_matches_run(checkpoint: dict[str, Any], args: argparse.Namespace) -> bool:
    """Return True when the checkpoint appears to belong to the requested run range."""
    if not checkpoint:
        return False
    if args.start and checkpoint.get("start_date") != args.start:
        return False
    if args.end and checkpoint.get("end_date") != args.end:
        return False
    return True


def _print_resume_state(path: Path, args: argparse.Namespace) -> None:
    """Log whether a discovery checkpoint is present and appears to match the requested run range."""
    checkpoint = _load_checkpoint(path)
    if not checkpoint:
        print("[scheduler] No discovery checkpoint found; next run will start fresh.")
        return

    start_date = checkpoint.get("start_date") or "unknown"
    end_date = checkpoint.get("end_date") or "unknown"
    phase = checkpoint.get("phase") or "unknown"
    clause_index = checkpoint.get("clause_index")
    current_start = checkpoint.get("current_start") or "unknown"
    count_in_window = checkpoint.get("count_in_window")

    if _checkpoint_matches_run(checkpoint, args):
        print(
            "[scheduler] Discovery checkpoint found; next run will resume "
            f"phase={phase}, clause={clause_index}, start={current_start}, "
            f"window_count={count_in_window}, range={start_date}..{end_date}"
        )
        return

    print(
        "[scheduler] Discovery checkpoint exists for a different range "
        f"({start_date}..{end_date}); requested run may start fresh."
    )


def _build_command(args: argparse.Namespace) -> list[str]:
    """Build the extraction command for each scheduled run."""
    command = [
        sys.executable,
        "extraction/query_runner.py",
        "--query-file",
        args.query_file,
        "--out-dir",
        args.out_dir,
        "--repo-filter",
        args.repo_filter,
        "--run-type",
        args.run_type,
        "--checkpoint-path",
        args.checkpoint_path,
    ]
    if args.start is not None:
        command.extend(["--start", args.start])
    if args.end is not None:
        command.extend(["--end", args.end])
    first_prs = args.first_prs if args.first_prs is not None else args.max_pages
    if first_prs is not None:
        command.extend(["--first-prs", str(first_prs)])
    if args.max_pr_ids is not None:
        command.extend(["--max-pr-ids", str(args.max_pr_ids)])
    if args.max_repo_ids is not None:
        command.extend(["--max-repo-ids", str(args.max_repo_ids)])
    if args.max_user_ids is not None:
        command.extend(["--max-user-ids", str(args.max_user_ids)])
    return command


def _build_run_env(args: argparse.Namespace) -> dict[str, str]:
    """Build subprocess environment for extraction runs."""
    env = os.environ.copy()
    if args.strategy == "interval":
        env.setdefault(
            "EXTRACTION_RUN_LABEL",
            f"interval_{args.mode or 'query'}_{args.start}_to_{args.end}",
        )
    return env


def _run_once(
    args: argparse.Namespace,
    checkpoint_path: Path,
    env: dict[str, str],
) -> int:
    """Run the extraction command once and log the active checkpoint state."""
    print("[scheduler] Starting a new run...")
    _print_resume_state(checkpoint_path, args)
    command = _build_command(args)
    print(f"[scheduler] Command: {' '.join(command)}")
    if args.include_related:
        print("[scheduler] --include-related is accepted for compatibility and ignored by query_runner.py.")
    run_label = env.get("EXTRACTION_RUN_LABEL")
    if run_label:
        print(f"[scheduler] Run label: {run_label}")
    result = subprocess.run(command, check=False, env=env)
    if result.returncode != 0:
        print(f"[scheduler] Extraction run exited with code {result.returncode}.")
    return result.returncode


def _resume_interval_until_complete(
    args: argparse.Namespace,
    checkpoint_path: Path,
    env: dict[str, str],
) -> int:
    """Keep rerunning the interval command until its discovery checkpoint clears."""
    while True:
        result_code = _run_once(args, checkpoint_path, env)
        checkpoint = _load_checkpoint(checkpoint_path)
        if result_code != 0:
            return result_code
        if checkpoint and _checkpoint_matches_run(checkpoint, args):
            print(
                "[scheduler] Discovery checkpoint still present for the requested "
                "interval; resuming immediately."
            )
            continue
        if checkpoint:
            print(
                "[scheduler] Discovery checkpoint remains, but it belongs to a "
                "different range; treating this interval run as complete."
            )
        else:
            print("[scheduler] Discovery checkpoint cleared; interval catch-up is complete.")
        return 0


def _next_daily_run(now_local: datetime, hour: int, minute: int) -> datetime:
    """Return the next local daily run time."""
    scheduled = now_local.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if scheduled <= now_local:
        scheduled += timedelta(days=1)
    return scheduled


def _should_continue_interval(end_date_iso: str | None, next_run_local: datetime) -> bool:
    """Return True when the next scheduled run is within the end date."""
    if end_date_iso is None:
        return False
    next_run_utc_date = next_run_local.astimezone(timezone.utc).date().isoformat()
    return next_run_utc_date <= end_date_iso


def _run_interval(args: argparse.Namespace, checkpoint_path: Path) -> None:
    """Run extraction keeping the discovery checkpoint in mind to determine when to stop or resume."""
    env = _build_run_env(args)

    while True:
        result_code = _resume_interval_until_complete(args, checkpoint_path, env)
        if result_code != 0:
            retry_seconds = args.hours * 3600
            print(
                "[scheduler] Interval run failed; retrying in "
                f"{retry_seconds / 3600:.2f} hours..."
            )
            time.sleep(retry_seconds)
            continue

        now_local = datetime.now().astimezone()
        next_run = _next_daily_run(now_local, args.daily_hour, args.daily_minute)
        if not _should_continue_interval(args.end, next_run):
            current_utc_date = datetime.now(timezone.utc).date().isoformat()
            print(
                "[scheduler] Interval completed and no further refresh is needed. "
                f"End date={args.end}, current UTC date={current_utc_date}."
            )
            break

        sleep_seconds = max(0.0, (next_run - now_local).total_seconds())
        print(
            "[scheduler] Interval completed; next refresh scheduled for "
            f"{next_run.isoformat()} (local time)."
        )
        time.sleep(sleep_seconds)


def _run_periodic(args: argparse.Namespace, checkpoint_path: Path) -> None:
    """Run extraction until completion / resume, then sleep."""
    env = _build_run_env(args)
    started_at = time.time()
    max_runtime_seconds = None
    if args.max_runtime_hours is not None:
        max_runtime_seconds = args.max_runtime_hours * 3600

    while True:
        if args.stop_after_date is not None:
            today = datetime.now().strftime("%Y-%m-%d")
            if today > args.stop_after_date:
                print("[scheduler] Stop-after date reached. No new runs will be started.")
                break

        if max_runtime_seconds is not None:
            elapsed = time.time() - started_at
            if elapsed >= max_runtime_seconds:
                print("[scheduler] Maximum scheduler runtime reached. Stopping before a new run.")
                break

        result_code = _run_once(args, checkpoint_path, env)

        if args.resume_until_complete:
            checkpoint = _load_checkpoint(checkpoint_path)
            if result_code == 0 and not checkpoint:
                print("[scheduler] Discovery checkpoint cleared; requested run appears complete.")
                break
            if checkpoint:
                print("[scheduler] Discovery checkpoint still present; next run will resume from it.")

        if max_runtime_seconds is not None:
            elapsed = time.time() - started_at
            remaining = max_runtime_seconds - elapsed
            if remaining <= 0:
                print("[scheduler] Maximum scheduler runtime reached after the run completed.")
                break
            sleep_seconds = min(args.hours * 3600, remaining)
            print(f"[scheduler] Run complete. Sleeping for {sleep_seconds / 3600:.2f} hours...")
            time.sleep(sleep_seconds)
            continue

        print(f"[scheduler] Run complete. Sleeping for {args.hours:.2f} hours...")
        time.sleep(args.hours * 3600)


def main() -> None:
    """Run the selected scheduler."""
    args = parse_args()
    checkpoint_path = Path(args.checkpoint_path)

    if args.strategy == "interval":
        _run_interval(args, checkpoint_path)
        return

    _run_periodic(args, checkpoint_path)


if __name__ == "__main__":
    main()


# python extraction/scheduler.py --strategy interval --hours 0.0167 --start 2026-03-16 --end 2026-03-17 --max-pages 1 --daily-hour 23 --daily-minute 15
# Dont change the strategy
# Hours is the sleep time between failed runs.
# Start and end are the discovery date range for the runs. Max pages is kept as a compatibility alias for query_runner.py --first-prs.
# Daily hour and minute are the local time for the next run in interval strategy. For periodic strategy, it will just sleep for the specified hours after each run.
