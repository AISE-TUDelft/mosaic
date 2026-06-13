from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


GRAPHQL_URL = "https://api.github.com/graphql"
RATE_LIMIT_URL = "https://api.github.com/rate_limit"
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUERY_FILE = ROOT / "query_rahul2026 copy.py"
DEFAULT_OUT_DIR = ROOT / "out" / "query_benchmark"
DEFAULT_DISCOVERY_CHECKPOINT = ROOT / "out" / "checkpoints" / "discovery_checkpoint.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from extraction.utility.checkpoint_handler import CheckpointHandler


def get_token() -> str | None:
    token = os.environ.get("GITHUB_TOKEN")
    if token and token.strip():
        return token.strip()

    token = os.environ.get("GH_TOKEN")
    if token and token.strip():
        return token.strip()

    tokens = os.environ.get("GITHUB_TOKENS")
    if tokens and tokens.strip():
        first_token = tokens.split(",")[0].strip()
        if first_token:
            return first_token

    return None


def mask_token(token: str | None) -> str:
    if not token:
        return "NO TOKEN FOUND"
    if len(token) <= 10:
        return "***"
    return f"{token[:4]}...{token[-4:]}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the GraphQL query benchmark.")
    parser.add_argument(
        "--query-file",
        default=str(DEFAULT_QUERY_FILE),
        help="Python file containing the GraphQL query builder functions.",
    )
    parser.add_argument(
        "--out-dir",
        default=str(DEFAULT_OUT_DIR),
        help="Directory where query payloads and summary files are written.",
    )
    parser.add_argument(
        "--repo-filter",
        default="repo:microsoft/vscode",
        help="GitHub search filter used by backbone_pr_query.",
    )
    parser.add_argument(
        "--run-type",
        choices=["split", "original", "both"],
        default="split",
        help=(
            "Use 'original' for only the PR query functions, 'split' to also "
            "run the smaller follow-up queries, or 'both' to compare them."
        ),
    )
    parser.add_argument("--start", dest="start_date", default="2024-01-01")
    parser.add_argument("--end", dest="end_date", default="2024-01-31")
    parser.add_argument("--first-prs", type=int, default=5)
    parser.add_argument("--max-pr-ids", type=int, default=5)
    parser.add_argument("--max-repo-ids", type=int, default=5)
    parser.add_argument("--max-user-ids", type=int, default=5)
    parser.add_argument(
        "--checkpoint-path",
        default=str(DEFAULT_DISCOVERY_CHECKPOINT),
        help="Path to the checkpoint file used for resuming interrupted runs.",
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Ignore any existing checkpoint and start this query run from scratch.",
    )
    return parser.parse_args()


def _load_json(path: Path) -> Any | None:
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _load_checkpoint(path: Path) -> dict[str, Any]:
    """Load checkpoint state when present."""
    return CheckpointHandler(path).load()


def _run_settings(
    args: argparse.Namespace,
    query_file: Path,
    out_dir: Path,
) -> dict[str, Any]:
    return {
        "query_file": str(query_file.resolve()),
        "out_dir": str(out_dir.resolve()),
        "run_type": args.run_type,
        "repo_filter": args.repo_filter,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "first_prs": args.first_prs,
        "max_pr_ids": args.max_pr_ids,
        "max_repo_ids": args.max_repo_ids,
        "max_user_ids": args.max_user_ids,
    }


def _checkpoint_matches_run(
    checkpoint: dict[str, Any],
    settings: dict[str, Any],
) -> bool:
    """Return True when the checkpoint belongs to the requested run."""
    checkpoint_settings = checkpoint.get("run")
    if not isinstance(checkpoint_settings, dict):
        return False
    for key, value in settings.items():
        if checkpoint_settings.get(key) != value:
            return False
    return True


def _new_checkpoint(settings: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": 1,
        "run": settings,
        "start_date": settings["start_date"],
        "end_date": settings["end_date"],
        "phase": "start",
        "clause_index": None,
        "current_start": settings["start_date"],
        "count_in_window": 0,
        "completed_queries": [],
        "payload_files": {},
        "summary": [],
        "usage_rows": [],
        "pr_ids": [],
        "repository_ids": [],
        "user_ids": [],
    }


def _save_checkpoint(path: Path, checkpoint: dict[str, Any]) -> None:
    checkpoint["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    CheckpointHandler(path).save(checkpoint)


def _clear_checkpoint(path: Path) -> None:
    CheckpointHandler(path).clear()


def _print_resume_state(path: Path, checkpoint: dict[str, Any]) -> None:
    if not checkpoint:
        print("[checkpoint] No checkpoint found; starting fresh.")
        return

    phase = checkpoint.get("phase") or "unknown"
    completed = checkpoint.get("completed_queries") or []
    start_date = checkpoint.get("start_date") or "unknown"
    end_date = checkpoint.get("end_date") or "unknown"
    print(
        "[checkpoint] Resuming from "
        f"{path}: phase={phase}, completed={len(completed)}, "
        f"range={start_date}..{end_date}"
    )


def _restore_list(checkpoint: dict[str, Any], key: str) -> list[Any]:
    value = checkpoint.get(key)
    if isinstance(value, list):
        return value
    return []


def _load_completed_payload(
    query_name: str,
    out_dir: Path,
    checkpoint: dict[str, Any],
) -> dict[str, Any] | None:
    payload_files = checkpoint.get("payload_files")
    if not isinstance(payload_files, dict):
        payload_files = {}
    payload_name = payload_files.get(query_name) or f"{query_name}.json"
    payload = _load_json(out_dir / str(payload_name))
    if isinstance(payload, dict):
        print(f"[checkpoint] Skipping completed query: {query_name}")
        return payload
    print(f"[checkpoint] Missing payload for {query_name}; rerunning it.")
    return None


def _mark_query_complete(
    checkpoint: dict[str, Any],
    query_name: str,
    summary: list[dict[str, Any]],
    usage_rows: list[dict[str, Any]],
    *,
    phase: str | None = None,
    clause_index: int | None = None,
) -> None:
    completed = [
        item
        for item in checkpoint.get("completed_queries", [])
        if isinstance(item, str)
    ]
    if query_name not in completed:
        completed.append(query_name)

    payload_files = checkpoint.get("payload_files")
    if not isinstance(payload_files, dict):
        payload_files = {}
    payload_files[query_name] = f"{query_name}.json"

    checkpoint["completed_queries"] = completed
    checkpoint["payload_files"] = payload_files
    checkpoint["summary"] = summary
    checkpoint["usage_rows"] = usage_rows
    checkpoint["phase"] = phase or query_name
    checkpoint["clause_index"] = clause_index
    checkpoint["count_in_window"] = len(completed)


def _drop_query_records(
    query_name: str,
    summary: list[dict[str, Any]],
    usage_rows: list[dict[str, Any]],
) -> None:
    summary[:] = [row for row in summary if row.get("query") != query_name]
    usage_rows[:] = [row for row in usage_rows if row.get("query") != query_name]


def _failure_payload(message: str) -> dict[str, Any]:
    return {
        "errors": [{"message": message}],
        "_benchmark": {
            "elapsed_ms": None,
            "response_bytes": None,
            "http_status": 0,
        },
    }


def _sync_checkpoint_ids(
    checkpoint: dict[str, Any],
    pr_ids: list[str],
    repository_ids: list[str],
    user_ids: list[str],
) -> None:
    checkpoint["pr_ids"] = pr_ids
    checkpoint["repository_ids"] = repository_ids
    checkpoint["user_ids"] = user_ids


def _mode_out_dir(base_out_dir: str, run_type: str) -> Path:
    return Path(base_out_dir) / run_type


def _mode_checkpoint_path(base_checkpoint_path: str, run_type: str) -> Path:
    checkpoint_path = Path(base_checkpoint_path)
    suffix = checkpoint_path.suffix or ".json"
    return checkpoint_path.with_name(f"{checkpoint_path.stem}_{run_type}{suffix}")


def _run_child_mode(args: argparse.Namespace, run_type: str) -> int:
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--run-type",
        run_type,
        "--query-file",
        args.query_file,
        "--out-dir",
        str(_mode_out_dir(args.out_dir, run_type)),
        "--repo-filter",
        args.repo_filter,
        "--start",
        args.start_date,
        "--end",
        args.end_date,
        "--first-prs",
        str(args.first_prs),
        "--max-pr-ids",
        str(args.max_pr_ids),
        "--max-repo-ids",
        str(args.max_repo_ids),
        "--max-user-ids",
        str(args.max_user_ids),
        "--checkpoint-path",
        str(_mode_checkpoint_path(args.checkpoint_path, run_type)),
    ]
    if args.fresh:
        command.append("--fresh")
    print(f"[run] Starting {run_type} comparison run...")
    result = subprocess.run(command, check=False)
    return result.returncode


def _comparison_entry(out_dir: Path) -> dict[str, Any]:
    summary = _load_json(out_dir / "summary.json")
    usage_rows = _load_json(out_dir / "usage_summary.json")
    if not isinstance(summary, list):
        summary = []
    if not isinstance(usage_rows, list):
        usage_rows = []

    total_consumed = 0
    for row in usage_rows:
        if isinstance(row, dict) and isinstance(row.get("graphql_consumed"), int):
            total_consumed += row["graphql_consumed"]

    queries: dict[str, dict[str, Any]] = {}
    for row in summary:
        if not isinstance(row, dict):
            continue
        query_name = row.get("query")
        if not isinstance(query_name, str):
            continue
        usage = next(
            (
                usage_row
                for usage_row in usage_rows
                if isinstance(usage_row, dict) and usage_row.get("query") == query_name
            ),
            {},
        )
        queries[query_name] = {
            "http_status": row.get("http_status"),
            "error_count": row.get("error_count"),
            "response_bytes": row.get("response_bytes"),
            "elapsed_ms": row.get("elapsed_ms"),
            "graphql_consumed": usage.get("graphql_consumed") if isinstance(usage, dict) else None,
        }

    return {
        "out_dir": str(out_dir),
        "query_count": len(queries),
        "total_graphql_consumed": total_consumed,
        "queries": queries,
    }


def _write_comparison_summary(base_out_dir: Path) -> None:
    comparison = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "runs": {
            "original": _comparison_entry(base_out_dir / "original"),
            "split": _comparison_entry(base_out_dir / "split"),
        },
    }
    save_json(base_out_dir / "comparison_summary.json", comparison)
    print(f"[run] Comparison summary written: {base_out_dir / 'comparison_summary.json'}")


def _run_both(args: argparse.Namespace) -> int:
    base_out_dir = Path(args.out_dir)
    original_code = _run_child_mode(args, "original")
    split_code = _run_child_mode(args, "split")
    _write_comparison_summary(base_out_dir)
    return 1 if original_code or split_code else 0


def get_graphql_remaining(token: str | None) -> tuple[int | None, int | None]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "query-runner",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(RATE_LIMIT_URL, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()

        payload = json.loads(body.decode("utf-8"))
        graphql = payload.get("resources", {}).get("graphql", {})

        remaining = graphql.get("remaining")
        limit = graphql.get("limit")

        if isinstance(remaining, int) and isinstance(limit, int):
            return remaining, limit

        return None, None

    except Exception:
        return None, None


def print_graphql_consumption(
    query_name: str,
    before_remaining: int | None,
    after_remaining: int | None,
    limit: int | None,
) -> dict[str, Any]:
    if isinstance(before_remaining, int) and isinstance(after_remaining, int):
        consumed = before_remaining - after_remaining
    else:
        consumed = None

    consumed_display = "-" if consumed is None else str(consumed)
    before_display = "-" if before_remaining is None else str(before_remaining)
    after_display = "-" if after_remaining is None else str(after_remaining)
    limit_display = "-" if limit is None else str(limit)

    print(
        f"[GitHub GraphQL] {query_name}: "
        f"consumed={consumed_display}, "
        f"before={before_display}, "
        f"after={after_display}, "
        f"limit={limit_display}"
    )

    return {
        "query": query_name,
        "graphql_before": before_remaining,
        "graphql_after": after_remaining,
        "graphql_consumed": consumed,
        "graphql_limit": limit,
    }


def load_module_from_path(path: str):
    module_path = Path(path)

    if not module_path.exists():
        raise FileNotFoundError(f"Query file not found: {module_path}")

    spec = importlib.util.spec_from_file_location("query_module", module_path)

    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def github_graphql(query: str, token: str | None) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "query-runner",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = json.dumps({"query": query}).encode("utf-8")

    request = urllib.request.Request(
        GRAPHQL_URL,
        data=body,
        headers=headers,
        method="POST",
    )

    started = time.perf_counter()

    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            raw = response.read()
            elapsed_ms = (time.perf_counter() - started) * 1000
            http_status = response.status

        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            payload = {"errors": [{"message": raw.decode("utf-8", errors="replace")}]}

        payload["_benchmark"] = {
            "elapsed_ms": elapsed_ms,
            "response_bytes": len(raw),
            "http_status": http_status,
        }

        return payload

    except urllib.error.HTTPError as exc:
        raw = exc.read()
        elapsed_ms = (time.perf_counter() - started) * 1000

        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            payload = {"errors": [{"message": raw.decode("utf-8", errors="replace")}]}

        payload.setdefault("errors", [])
        payload["errors"].insert(
            0,
            {"message": f"HTTP Error {exc.code}: {exc.reason}"},
        )

        payload["_benchmark"] = {
            "elapsed_ms": elapsed_ms,
            "response_bytes": len(raw),
            "http_status": exc.code,
        }

        return payload

    except Exception as exc:
        elapsed_ms = (time.perf_counter() - started) * 1000

        return {
            "errors": [{"message": str(exc)}],
            "_benchmark": {
                "elapsed_ms": elapsed_ms,
                "response_bytes": 0,
                "http_status": 0,
            },
        }


def run_measured_graphql(
    query_name: str,
    query: str,
    token: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    before_remaining, before_limit = get_graphql_remaining(token)

    payload = github_graphql(query, token)

    after_remaining, after_limit = get_graphql_remaining(token)
    limit = after_limit if after_limit is not None else before_limit

    usage_row = print_graphql_consumption(
        query_name=query_name,
        before_remaining=before_remaining,
        after_remaining=after_remaining,
        limit=limit,
    )

    return payload, usage_row


def quote_ids(ids: list[str]) -> str:
    return ", ".join(json.dumps(item) for item in ids)


def ids_arg(ids: list[str], max_ids: int = 5) -> str:
    return quote_ids(ids[:max_ids])


def extract_pr_ids(backbone_payload: dict[str, Any], max_ids: int) -> list[str]:
    nodes = (
        backbone_payload
        .get("data", {})
        .get("search", {})
        .get("nodes", [])
    )

    ids: list[str] = []

    for node in nodes:
        if isinstance(node, dict) and node.get("id"):
            ids.append(node["id"])

        if len(ids) >= max_ids:
            break

    return ids


def collect_ids_by_typename(obj: Any, typenames: set[str]) -> list[str]:
    found: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            typename = value.get("__typename")
            node_id = value.get("id")

            if isinstance(typename, str) and typename in typenames and isinstance(node_id, str):
                found.add(node_id)

            for child in value.values():
                walk(child)

        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(obj)
    return sorted(found)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def summarize_payload(function_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    benchmark = payload.get("_benchmark", {})
    errors = payload.get("errors", [])

    return {
        "query": function_name,
        "http_status": benchmark.get("http_status"),
        "elapsed_ms": benchmark.get("elapsed_ms"),
        "response_bytes": benchmark.get("response_bytes"),
        "error_count": len(errors),
        "errors": [
            error.get("message", str(error))
            if isinstance(error, dict)
            else str(error)
            for error in errors
        ],
    }


def print_final_usage_table(usage_rows: list[dict[str, Any]]) -> None:
    if not usage_rows:
        return

    print()
    print("GitHub GraphQL consumption by query type")
    print()

    headers = ["query", "before", "after", "consumed", "limit"]
    rows: list[list[str]] = []

    total_consumed = 0

    for row in usage_rows:
        consumed = row.get("graphql_consumed")
        if isinstance(consumed, int):
            total_consumed += consumed

        rows.append(
            [
                str(row.get("query", "-")),
                "-" if row.get("graphql_before") is None else str(row["graphql_before"]),
                "-" if row.get("graphql_after") is None else str(row["graphql_after"]),
                "-" if consumed is None else str(consumed),
                "-" if row.get("graphql_limit") is None else str(row["graphql_limit"]),
            ]
        )

    widths = [
        max(len(headers[i]), *(len(row[i]) for row in rows))
        for i in range(len(headers))
    ]

    fmt = "  ".join("{:<" + str(width) + "}" for width in widths)

    print(fmt.format(*headers))
    print(fmt.format(*["-" * width for width in widths]))

    for row in rows:
        print(fmt.format(*row))

    print()
    print(f"Total measured GraphQL consumed: {total_consumed}")


def run_and_record_query(
    query_name: str,
    query: str,
    token: str,
    out_dir: Path,
    summary: list[dict[str, Any]],
    usage_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    print(f"Running {query_name}...")

    payload, usage_row = run_measured_graphql(
        query_name=query_name,
        query=query,
        token=token,
    )

    usage_rows.append(usage_row)
    save_json(out_dir / f"{query_name}.json", payload)

    row = summarize_payload(query_name, payload)
    summary.append(row)

    if row["error_count"]:
        print(f"{query_name} returned {row['error_count']} error(s):")
        for error in row["errors"]:
            print("-", error)

    return payload


def main() -> int:
    args = parse_args()
    if args.run_type == "both":
        return _run_both(args)

    query_file = Path(args.query_file)
    out_dir = Path(args.out_dir)
    checkpoint_path = Path(args.checkpoint_path)
    settings = _run_settings(args, query_file, out_dir)

    token = get_token()

    print(f"Using token: {mask_token(token)}")

    if not token:
        print()
        print("No GitHub token found.")
        print("Set it in PowerShell like this:")
        print('$env:GITHUB_TOKEN="your_token_here"')
        return 1

    module = load_module_from_path(str(query_file))

    checkpoint = _load_checkpoint(checkpoint_path)
    if args.fresh or not _checkpoint_matches_run(checkpoint, settings):
        if checkpoint and not args.fresh:
            print("[checkpoint] Existing checkpoint belongs to different run settings; starting fresh.")
        checkpoint = _new_checkpoint(settings)
    _print_resume_state(checkpoint_path, checkpoint if checkpoint.get("completed_queries") else {})

    summary: list[dict[str, Any]] = [
        row for row in _restore_list(checkpoint, "summary") if isinstance(row, dict)
    ]
    usage_rows: list[dict[str, Any]] = [
        row for row in _restore_list(checkpoint, "usage_rows") if isinstance(row, dict)
    ]
    payloads_for_id_collection: list[dict[str, Any]] = []
    completed_queries = {
        item
        for item in checkpoint.get("completed_queries", [])
        if isinstance(item, str)
    }

    backbone_payload = None
    if "backbone_pr_query" in completed_queries:
        backbone_payload = _load_completed_payload("backbone_pr_query", out_dir, checkpoint)
        if backbone_payload is not None:
            payloads_for_id_collection.append(backbone_payload)
        else:
            completed_queries.discard("backbone_pr_query")

    if backbone_payload is None:
        print("Running backbone_pr_query...")
        _drop_query_records("backbone_pr_query", summary, usage_rows)

        backbone_query = module.backbone_pr_query(
            filter=args.repo_filter,
            start_date=args.start_date,
            end_date=args.end_date,
            first=args.first_prs,
            after=None,
        )

        backbone_payload, usage_row = run_measured_graphql(
            "backbone_pr_query",
            backbone_query,
            token,
        )
        usage_rows.append(usage_row)
        payloads_for_id_collection.append(backbone_payload)

        save_json(out_dir / "backbone_pr_query.json", backbone_payload)

        backbone_summary = summarize_payload("backbone_pr_query", backbone_payload)
        summary.append(backbone_summary)

        if backbone_payload.get("errors"):
            print("backbone_pr_query returned errors:")
            for error in backbone_summary["errors"]:
                print("-", error)

            checkpoint["summary"] = summary
            checkpoint["usage_rows"] = usage_rows
            checkpoint["phase"] = "backbone_pr_query"
            _save_checkpoint(checkpoint_path, checkpoint)
            save_json(out_dir / "summary.json", summary)
            save_json(out_dir / "usage_summary.json", usage_rows)
            print_final_usage_table(usage_rows)
            return 1

        _mark_query_complete(
            checkpoint,
            "backbone_pr_query",
            summary,
            usage_rows,
            phase="backbone_pr_query",
            clause_index=0,
        )
        _save_checkpoint(checkpoint_path, checkpoint)
        completed_queries.add("backbone_pr_query")

    checkpoint_pr_ids = [
        item for item in _restore_list(checkpoint, "pr_ids") if isinstance(item, str)
    ]
    pr_ids = checkpoint_pr_ids or extract_pr_ids(backbone_payload, args.max_pr_ids)
    print(f"Extracted {len(pr_ids)} PR ids")
    _sync_checkpoint_ids(
        checkpoint,
        pr_ids,
        [item for item in _restore_list(checkpoint, "repository_ids") if isinstance(item, str)],
        [item for item in _restore_list(checkpoint, "user_ids") if isinstance(item, str)],
    )
    _save_checkpoint(checkpoint_path, checkpoint)

    if not pr_ids:
        print("No PR ids found, cannot run PR-detail queries.")

        checkpoint["phase"] = "no_pr_ids"
        _save_checkpoint(checkpoint_path, checkpoint)
        save_json(out_dir / "summary.json", summary)
        save_json(out_dir / "usage_summary.json", usage_rows)
        print_final_usage_table(usage_rows)
        return 1

    pr_ids_arg = quote_ids(pr_ids)

    pr_query_functions = [
        "pr_review_query",
        "pr_commit_query",
        "pr_comment_query",
        "pr_closing_issue_query",
        "pr_repository_query",
        "pr_user_query",
    ]

    for index, function_name in enumerate(pr_query_functions, start=1):
        if not hasattr(module, function_name):
            print(f"Skipping missing function: {function_name}")
            continue

        if function_name in completed_queries:
            payload = _load_completed_payload(function_name, out_dir, checkpoint)
            if payload is not None:
                payloads_for_id_collection.append(payload)
                continue
            completed_queries.discard(function_name)

        fn = getattr(module, function_name)

        try:
            _drop_query_records(function_name, summary, usage_rows)
            query = fn(None, pr_ids_arg)

            payload = run_and_record_query(
                query_name=function_name,
                query=query,
                token=token,
                out_dir=out_dir,
                summary=summary,
                usage_rows=usage_rows,
            )

            payloads_for_id_collection.append(payload)
            _mark_query_complete(
                checkpoint,
                function_name,
                summary,
                usage_rows,
                phase=function_name,
                clause_index=index,
            )
            _save_checkpoint(checkpoint_path, checkpoint)
            completed_queries.add(function_name)

        except Exception as exc:
            print(f"Failed {function_name}: {exc}")
            save_json(out_dir / f"{function_name}.json", _failure_payload(str(exc)))
            summary.append(
                {
                    "query": function_name,
                    "http_status": 0,
                    "elapsed_ms": None,
                    "response_bytes": None,
                    "error_count": 1,
                    "errors": [str(exc)],
                }
            )
            _mark_query_complete(
                checkpoint,
                function_name,
                summary,
                usage_rows,
                phase=function_name,
                clause_index=index,
            )
            _save_checkpoint(checkpoint_path, checkpoint)
            completed_queries.add(function_name)

    checkpoint_repository_ids = [
        item
        for item in _restore_list(checkpoint, "repository_ids")
        if isinstance(item, str)
    ]
    checkpoint_user_ids = [
        item for item in _restore_list(checkpoint, "user_ids") if isinstance(item, str)
    ]

    if checkpoint_repository_ids or checkpoint_user_ids:
        repository_ids_list = checkpoint_repository_ids
        user_ids_list = checkpoint_user_ids
    else:
        repository_ids: set[str] = set()
        user_ids: set[str] = set()

        for payload in payloads_for_id_collection:
            repository_ids.update(collect_ids_by_typename(payload, {"Repository"}))
            user_ids.update(collect_ids_by_typename(payload, {"User"}))

        repository_ids_list = sorted(repository_ids)
        user_ids_list = sorted(user_ids)
        _sync_checkpoint_ids(checkpoint, pr_ids, repository_ids_list, user_ids_list)
        checkpoint["phase"] = "collected_followup_ids"
        _save_checkpoint(checkpoint_path, checkpoint)

    print(f"Collected {len(repository_ids_list)} repository ids")
    print(f"Collected {len(user_ids_list)} user ids")

    followup_queries: list[tuple[str, str]] = []

    if args.run_type == "original":
        print("[run] Original mode: skipping split follow-up queries.")
    elif repository_ids_list:
        repo_ids_arg = ids_arg(repository_ids_list, max_ids=args.max_repo_ids)

        if hasattr(module, "repository_labels_query"):
            followup_queries.append(
                (
                    "repository_labels_query",
                    module.repository_labels_query(None, repo_ids_arg),
                )
            )

        if hasattr(module, "repository_languages_query"):
            followup_queries.append(
                (
                    "repository_languages_query",
                    module.repository_languages_query(None, repo_ids_arg),
                )
            )

    elif not repository_ids_list:
        print("Skipping repository follow-up queries: no Repository ids found.")

    if args.run_type == "original":
        pass
    elif user_ids_list:
        user_ids_arg = ids_arg(user_ids_list, max_ids=args.max_user_ids)

        if hasattr(module, "user_top_repositories_query"):
            followup_queries.append(
                (
                    "user_top_repositories_query",
                    module.user_top_repositories_query(None, user_ids_arg),
                )
            )

        if hasattr(module, "user_contributions_by_repository_query"):
            followup_queries.append(
                (
                    "user_contributions_by_repository_query",
                    module.user_contributions_by_repository_query(None, user_ids_arg),
                )
            )

    elif not user_ids_list:
        print("Skipping user follow-up queries: no User ids found.")

    for index, (query_name, query) in enumerate(
        followup_queries,
        start=len(pr_query_functions) + 1,
    ):
        if query_name in completed_queries:
            payload = _load_completed_payload(query_name, out_dir, checkpoint)
            if payload is not None:
                payloads_for_id_collection.append(payload)
                continue
            completed_queries.discard(query_name)

        try:
            _drop_query_records(query_name, summary, usage_rows)
            payload = run_and_record_query(
                query_name=query_name,
                query=query,
                token=token,
                out_dir=out_dir,
                summary=summary,
                usage_rows=usage_rows,
            )
            payloads_for_id_collection.append(payload)
            _mark_query_complete(
                checkpoint,
                query_name,
                summary,
                usage_rows,
                phase=query_name,
                clause_index=index,
            )
            _save_checkpoint(checkpoint_path, checkpoint)
            completed_queries.add(query_name)

        except Exception as exc:
            print(f"Failed {query_name}: {exc}")
            save_json(out_dir / f"{query_name}.json", _failure_payload(str(exc)))
            summary.append(
                {
                    "query": query_name,
                    "http_status": 0,
                    "elapsed_ms": None,
                    "response_bytes": None,
                    "error_count": 1,
                    "errors": [str(exc)],
                }
            )
            _mark_query_complete(
                checkpoint,
                query_name,
                summary,
                usage_rows,
                phase=query_name,
                clause_index=index,
            )
            _save_checkpoint(checkpoint_path, checkpoint)
            completed_queries.add(query_name)

    save_json(out_dir / "summary.json", summary)
    save_json(out_dir / "usage_summary.json", usage_rows)
    _clear_checkpoint(checkpoint_path)

    print()
    print("Done. Results saved to:")
    print(out_dir)

    print_final_usage_table(usage_rows)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
