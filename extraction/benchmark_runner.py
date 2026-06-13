from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


API_BASE = "https://api.github.com"
GRAPHQL_URL = "https://api.github.com/graphql"


@dataclass(frozen=True)
class ResourceSpec:
    name: str
    path: str
    paginated: bool = True
    description: str = ""


@dataclass
class RateLimitState:
    resource: str | None = None
    limit: int | None = None
    remaining: int | None = None
    used: int | None = None
    reset: int | None = None
    retry_after: int | None = None


@dataclass
class PageBenchmark:
    page: int
    url: str
    status: int
    elapsed_ms: float
    response_bytes: int
    item_count: int
    has_next: bool
    last_page: int | None
    rate_limit: RateLimitState
    error: str | None = None


@dataclass
class ResourceBenchmark:
    repo: str
    resource: str
    pages: list[PageBenchmark]
    total_items: int
    total_bytes: int
    avg_elapsed_ms: float
    max_elapsed_ms: float
    complete: bool
    estimated_pages: int | None
    warnings: list[str] = field(default_factory=list)


@dataclass
class GraphQLBenchmark:
    repo: str
    query_name: str
    status: int
    elapsed_ms: float
    response_bytes: int
    cost: int | None
    error_count: int
    error_messages: list[str]
    rate_limit: RateLimitState
    warnings: list[str] = field(default_factory=list)


RESOURCE_SPECS = {
    "repo": ResourceSpec(
        name="repo",
        path="/repos/{owner}/{repo}",
        paginated=False,
        description="Repository metadata.",
    ),
    "issues": ResourceSpec(
        name="issues",
        path="/repos/{owner}/{repo}/issues?state=all&sort=created&direction=desc",
        description="Issues API; GitHub includes pull requests in this listing.",
    ),
    "pulls": ResourceSpec(
        name="pulls",
        path="/repos/{owner}/{repo}/pulls?state=all&sort=created&direction=desc",
        description="Pull request listing.",
    ),
    "commits": ResourceSpec(
        name="commits",
        path="/repos/{owner}/{repo}/commits",
        description="Commit listing.",
    ),
    "issue-comments": ResourceSpec(
        name="issue-comments",
        path="/repos/{owner}/{repo}/issues/comments?sort=created&direction=desc",
        description="All issue comments for the repository.",
    ),
    "pull-comments": ResourceSpec(
        name="pull-comments",
        path="/repos/{owner}/{repo}/pulls/comments?sort=created&direction=desc",
        description="All pull request review comments for the repository.",
    ),
    "releases": ResourceSpec(
        name="releases",
        path="/repos/{owner}/{repo}/releases",
        description="Release listing.",
    ),
    "tags": ResourceSpec(
        name="tags",
        path="/repos/{owner}/{repo}/tags",
        description="Tag listing.",
    ),
    "contributors": ResourceSpec(
        name="contributors",
        path="/repos/{owner}/{repo}/contributors?anon=true",
        description="Contributor listing.",
    ),
    "branches": ResourceSpec(
        name="branches",
        path="/repos/{owner}/{repo}/branches",
        description="Branch listing.",
    ),
    "labels": ResourceSpec(
        name="labels",
        path="/repos/{owner}/{repo}/labels",
        description="Issue labels.",
    ),
    "milestones": ResourceSpec(
        name="milestones",
        path="/repos/{owner}/{repo}/milestones?state=all",
        description="Milestones.",
    ),
    "languages": ResourceSpec(
        name="languages",
        path="/repos/{owner}/{repo}/languages",
        paginated=False,
        description="Language byte totals.",
    ),
    "workflows": ResourceSpec(
        name="workflows",
        path="/repos/{owner}/{repo}/actions/workflows",
        paginated=False,
        description="GitHub Actions workflows.",
    ),
}

DEFAULT_RESOURCES = [
    "repo",
    "issues",
    "pulls",
    "commits",
    "issue-comments",
    "pull-comments",
    "releases",
    "tags",
    "contributors",
    "branches",
    "labels",
    "milestones",
    "languages",
]


class TokenCycler:
    def __init__(self, tokens: list[str]) -> None:
        self._tokens = tokens
        self._index = 0

    def next(self) -> str | None:
        if not self._tokens:
            return None
        token = self._tokens[self._index]
        self._index = (self._index + 1) % len(self._tokens)
        return token


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Benchmark GitHub REST resources and GraphQL queries before adding them "
            "to the scheduler."
        )
    )
    parser.add_argument(
        "--repo",
        action="append",
        help="Repository as owner/name or https://github.com/owner/name. Can be repeated.",
    )
    parser.add_argument(
        "--repos-file",
        help="Optional file with one owner/name repository per line. Lines starting with # are ignored.",
    )
    parser.add_argument(
        "--resources",
        default=",".join(DEFAULT_RESOURCES),
        help=(
            "Comma-separated resources, 'all', or 'default'. Available: "
            + ", ".join(sorted(RESOURCE_SPECS))
        ),
    )
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help=(
            "Custom paginated REST path as name=/repos/{owner}/{repo}/... . "
            "Use {owner} and {repo} placeholders. Can be repeated."
        ),
    )
    parser.add_argument("--per-page", type=int, default=100)
    parser.add_argument("--max-pages", type=int, default=1)
    parser.add_argument(
        "--graphql-query",
        action="append",
        default=[],
        help="Path to a GraphQL query file. Can be repeated.",
    )
    parser.add_argument(
    "--graphql-dir",
    help="Folder containing .graphql files. All .graphql files in the folder will be benchmarked.",
    )
    parser.add_argument(
        "--graphql-variables",
        help="GraphQL variables as JSON, or @path/to/variables.json.",
    )
    parser.add_argument(
        "--warn-graphql-cost",
        type=int,
        default=50,
        help="Warn when a GraphQL query reports a cost above this value.",
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--page-sleep", type=float, default=0.0)
    parser.add_argument(
        "--tokens-env",
        default="GITHUB_TOKENS",
        help="Environment variable containing comma-separated tokens. Falls back to GITHUB_TOKEN.",
    )
    parser.add_argument("--out", help="Optional JSON report path.")
    parser.add_argument("--fail-on-warning", action="store_true")
    parser.add_argument("--warn-seconds", type=float, default=10.0)
    parser.add_argument("--warn-bytes", type=int, default=5_000_000)
    parser.add_argument("--warn-items", type=int, default=1_000)
    parser.add_argument("--warn-pages", type=int, default=10)
    return parser.parse_args()


def load_tokens(tokens_env: str) -> list[str]:
    raw = os.environ.get(tokens_env) or os.environ.get("GITHUB_TOKEN") or ""
    tokens: list[str] = []
    for chunk in raw.replace(";", ",").replace("\n", ",").split(","):
        token = chunk.strip()
        if token:
            tokens.append(token)
    return tokens


def load_repos(args: argparse.Namespace) -> list[str]:
    repos = list(args.repo or [])
    if args.repos_file:
        path = Path(args.repos_file)
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                repos.append(line)
    parsed = [parse_repo(repo) for repo in repos]
    return list(dict.fromkeys(parsed))


def parse_repo(repo: str) -> str:
    value = repo.strip().removesuffix(".git").strip("/")
    if value.startswith("https://github.com/"):
        value = value.removeprefix("https://github.com/")
    parts = [part for part in value.split("/") if part]
    if len(parts) < 2:
        raise ValueError(f"Invalid repo '{repo}'. Expected owner/name.")
    return f"{parts[0]}/{parts[1]}"


def parse_resource_specs(args: argparse.Namespace) -> list[ResourceSpec]:
    specs = dict(RESOURCE_SPECS)
    for custom in args.path:
        if "=" not in custom:
            raise ValueError("--path must use name=/repos/{owner}/{repo}/...")
        name, path = custom.split("=", 1)
        name = name.strip()
        path = path.strip()
        if not name or not path:
            raise ValueError("--path requires both name and path.")
        specs[name] = ResourceSpec(name=name, path=path, description="Custom REST path.")

    requested = [item.strip() for item in args.resources.split(",") if item.strip()]
    if not requested or requested == ["default"]:
        requested = DEFAULT_RESOURCES
    elif requested == ["all"]:
        requested = sorted(specs)
    elif requested == ["none"]:
        return []

    missing = [name for name in requested if name not in specs]
    if missing:
        raise ValueError(f"Unknown resources: {', '.join(missing)}")
    return [specs[name] for name in requested]


def build_url(spec: ResourceSpec, repo: str, page: int, per_page: int) -> str:
    owner, repo_name = repo.split("/", 1)
    path = spec.path.format(
        owner=urllib.parse.quote(owner, safe=""),
        repo=urllib.parse.quote(repo_name, safe=""),
    )
    if path.startswith("https://"):
        url = path
    else:
        url = API_BASE + path

    if not spec.paginated:
        return url

    parts = urllib.parse.urlsplit(url)
    query = dict(urllib.parse.parse_qsl(parts.query, keep_blank_values=True))
    query["per_page"] = str(per_page)
    query["page"] = str(page)
    return urllib.parse.urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            parts.path,
            urllib.parse.urlencode(query),
            parts.fragment,
        )
    )


def get_json(url: str, token: str | None, timeout: float) -> tuple[int, dict[str, str], bytes, Any, str | None]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "mosaic-benchmark-runner",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            return response.status, normalize_headers(response.headers), body, decode_json(body), None
    except urllib.error.HTTPError as exc:
        body = exc.read()
        payload = decode_json(body)
        message = extract_error_message(payload) or exc.reason
        return exc.code, normalize_headers(exc.headers), body, payload, str(message)
    except urllib.error.URLError as exc:
        return 0, {}, b"", None, str(exc.reason)
    except TimeoutError:
        return 0, {}, b"", None, "request timed out"


def post_json(
    url: str,
    token: str | None,
    payload: dict[str, Any],
    timeout: float,
) -> tuple[int, dict[str, str], bytes, Any, str | None]:
    headers = {
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "mosaic-benchmark-runner",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response_body = response.read()
            return response.status, normalize_headers(response.headers), response_body, decode_json(response_body), None
    except urllib.error.HTTPError as exc:
        response_body = exc.read()
        response_payload = decode_json(response_body)
        message = extract_error_message(response_payload) or exc.reason
        return exc.code, normalize_headers(exc.headers), response_body, response_payload, str(message)
    except urllib.error.URLError as exc:
        return 0, {}, b"", None, str(exc.reason)
    except TimeoutError:
        return 0, {}, b"", None, "request timed out"


def decode_json(body: bytes) -> Any:
    if not body:
        return None
    try:
        return json.loads(body.decode("utf-8"))
    except json.JSONDecodeError:
        return None


def extract_error_message(payload: Any) -> str | None:
    if isinstance(payload, dict):
        message = payload.get("message")
        if isinstance(message, str):
            return message
    return None


def normalize_headers(headers: Any) -> dict[str, str]:
    return {key.lower(): value for key, value in headers.items()}


def count_items(payload: Any) -> int:
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        if isinstance(payload.get("items"), list):
            return len(payload["items"])
        if isinstance(payload.get("workflows"), list):
            return len(payload["workflows"])
        if "id" in payload or "node_id" in payload or "full_name" in payload:
            return 1
        return len(payload)
    return 0


def parse_link_header(header: str | None) -> dict[str, str]:
    if not header:
        return {}
    links: dict[str, str] = {}
    for part in header.split(","):
        section = part.strip()
        if not section.startswith("<") or ">;" not in section:
            continue
        url_part, rel_part = section.split(">;", 1)
        url = url_part[1:]
        rel = None
        for token in rel_part.split(";"):
            token = token.strip()
            if token.startswith("rel="):
                rel = token.removeprefix("rel=").strip('"')
                break
        if rel:
            links[rel] = url
    return links


def page_number_from_url(url: str | None) -> int | None:
    if not url:
        return None
    parts = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qs(parts.query)
    values = query.get("page")
    if not values:
        return None
    try:
        return int(values[0])
    except ValueError:
        return None


def rate_limit_from_headers(headers: dict[str, str]) -> RateLimitState:
    return RateLimitState(
        resource=headers.get("x-ratelimit-resource"),
        limit=parse_int(headers.get("x-ratelimit-limit")),
        remaining=parse_int(headers.get("x-ratelimit-remaining")),
        used=parse_int(headers.get("x-ratelimit-used")),
        reset=parse_int(headers.get("x-ratelimit-reset")),
        retry_after=parse_int(headers.get("retry-after")),
    )


def parse_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def benchmark_resource(
    repo: str,
    spec: ResourceSpec,
    args: argparse.Namespace,
    tokens: TokenCycler,
) -> ResourceBenchmark:
    pages: list[PageBenchmark] = []
    next_url: str | None = None
    last_page: int | None = None

    for page in range(1, args.max_pages + 1):
        url = next_url or build_url(spec, repo, page, args.per_page)
        token = tokens.next()
        started = time.perf_counter()
        status, headers, body, payload, error = get_json(url, token, args.timeout)
        elapsed_ms = (time.perf_counter() - started) * 1000
        links = parse_link_header(headers.get("link"))
        next_url = links.get("next")
        last_page = page_number_from_url(links.get("last")) or last_page

        pages.append(
            PageBenchmark(
                page=page,
                url=url,
                status=status,
                elapsed_ms=elapsed_ms,
                response_bytes=len(body),
                item_count=count_items(payload),
                has_next=next_url is not None,
                last_page=last_page,
                rate_limit=rate_limit_from_headers(headers),
                error=error,
            )
        )

        if status < 200 or status >= 300 or error:
            break
        if not spec.paginated or not next_url:
            break
        if args.page_sleep > 0:
            time.sleep(args.page_sleep)

    total_items = sum(page.item_count for page in pages)
    total_bytes = sum(page.response_bytes for page in pages)
    timings = [page.elapsed_ms for page in pages]
    complete = bool(pages) and not pages[-1].has_next
    estimated_pages = last_page
    summary = ResourceBenchmark(
        repo=repo,
        resource=spec.name,
        pages=pages,
        total_items=total_items,
        total_bytes=total_bytes,
        avg_elapsed_ms=sum(timings) / len(timings) if timings else 0.0,
        max_elapsed_ms=max(timings) if timings else 0.0,
        complete=complete,
        estimated_pages=estimated_pages,
    )
    summary.warnings = build_warnings(summary, args)
    return summary


def load_graphql_query(path: str) -> tuple[str, str]:
    query_path = Path(path)
    return query_path.stem, query_path.read_text(encoding="utf-8")


def load_graphql_variables(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    if raw.startswith("@"):
        raw = Path(raw[1:]).read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("--graphql-variables must decode to a JSON object.")
    return data


def repo_variables(repo: str) -> dict[str, str]:
    if repo == "-":
        return {}
    owner, repo_name = repo.split("/", 1)
    return {
        "owner": owner,
        "repo": repo_name,
        "name": repo_name,
        "repoName": repo_name,
        "repository": repo,
    }


def benchmark_graphql_query(
    repo: str,
    query_name: str,
    query: str,
    base_variables: dict[str, Any],
    args: argparse.Namespace,
    tokens: TokenCycler,
) -> GraphQLBenchmark:
    variables = repo_variables(repo)
    variables.update(base_variables)
    token = tokens.next()
    request_payload = {
        "query": query,
        "variables": variables,
    }

    started = time.perf_counter()
    status, headers, body, payload, transport_error = post_json(
        GRAPHQL_URL,
        token,
        request_payload,
        args.timeout,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000
    messages = graphql_error_messages(payload)
    if transport_error:
        messages.insert(0, transport_error)

    result = GraphQLBenchmark(
        repo=repo,
        query_name=query_name,
        status=status,
        elapsed_ms=elapsed_ms,
        response_bytes=len(body),
        cost=extract_graphql_cost(payload),
        error_count=len(messages),
        error_messages=messages,
        rate_limit=rate_limit_from_headers(headers),
    )
    result.warnings = build_graphql_warnings(result, args)
    return result


def graphql_error_messages(payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return []
    errors = payload.get("errors")
    if not isinstance(errors, list):
        return []
    messages: list[str] = []
    for error in errors:
        if isinstance(error, dict) and isinstance(error.get("message"), str):
            messages.append(error["message"])
        else:
            messages.append(str(error))
    return messages


def extract_graphql_cost(payload: Any) -> int | None:
    if not isinstance(payload, dict):
        return None
    data = payload.get("data")
    if not isinstance(data, dict):
        return None
    rate_limit = data.get("rateLimit")
    if not isinstance(rate_limit, dict):
        return None
    cost = rate_limit.get("cost")
    if isinstance(cost, int):
        return cost
    return None


def build_graphql_warnings(result: GraphQLBenchmark, args: argparse.Namespace) -> list[str]:
    warnings: list[str] = []
    if result.status in {403, 429}:
        warnings.append("rate limited or forbidden")
    elif result.status >= 400 or result.status == 0:
        warnings.append(f"HTTP status {result.status}")

    if result.error_messages:
        warnings.append("GraphQL returned errors")
    if result.cost is None:
        warnings.append("query does not return rateLimit.cost")
    elif result.cost > args.warn_graphql_cost:
        warnings.append(f"GraphQL cost > {args.warn_graphql_cost}")

    if result.elapsed_ms / 1000 > args.warn_seconds:
        warnings.append(f"slow query > {args.warn_seconds:.1f}s")
    if result.response_bytes > args.warn_bytes:
        warnings.append(f"large response > {format_bytes(args.warn_bytes)}")

    rate = result.rate_limit
    if rate.retry_after is not None:
        warnings.append(f"retry-after={rate.retry_after}s")
    if rate.remaining is not None and rate.remaining <= 5:
        warnings.append(f"low remaining quota: {rate.remaining}")

    for message in result.error_messages:
        lowered = message.lower()
        if "resource" in lowered or "timeout" in lowered or "rate limit" in lowered:
            warnings.append(f"limit-related error: {message}")
    return warnings


def build_warnings(summary: ResourceBenchmark, args: argparse.Namespace) -> list[str]:
    warnings: list[str] = []
    if not summary.pages:
        warnings.append("no pages fetched")
        return warnings

    last = summary.pages[-1]
    if last.error:
        warnings.append(f"request error: {last.error}")
    if last.status in {403, 429}:
        warnings.append("rate limited or forbidden")
    elif last.status >= 400 or last.status == 0:
        warnings.append(f"HTTP status {last.status}")

    if summary.max_elapsed_ms / 1000 > args.warn_seconds:
        warnings.append(f"slow page > {args.warn_seconds:.1f}s")
    if summary.total_bytes > args.warn_bytes:
        warnings.append(f"large sampled payload > {format_bytes(args.warn_bytes)}")
    if summary.total_items > args.warn_items:
        warnings.append(f"large sampled item count > {args.warn_items}")

    if not summary.complete:
        if summary.estimated_pages:
            estimated_items = summary.estimated_pages * args.per_page
            warnings.append(
                f"more pages: estimated {summary.estimated_pages} pages / up to {estimated_items} rows"
            )
            if summary.estimated_pages > args.warn_pages:
                warnings.append(f"page count > {args.warn_pages}")
        else:
            warnings.append("more pages available; no last-page estimate")

    rate = last.rate_limit
    if rate.retry_after is not None:
        warnings.append(f"retry-after={rate.retry_after}s")
    if rate.remaining is not None and rate.remaining <= 5:
        warnings.append(f"low remaining quota: {rate.remaining}")
    return warnings


def print_report(results: list[ResourceBenchmark], token_count: int) -> None:
    print()
    print("MOSAIC GitHub query benchmark")
    print(f"Tokens loaded: {token_count} ({'authenticated' if token_count else 'unauthenticated'})")
    print()

    if not results:
        print("No REST resources requested.")
        return

    rows = []
    for result in results:
        last = result.pages[-1] if result.pages else None
        rows.append(
            [
                result.repo,
                result.resource,
                str(len(result.pages)),
                str(result.total_items),
                format_bytes(result.total_bytes),
                f"{result.avg_elapsed_ms:.0f}",
                f"{result.max_elapsed_ms:.0f}",
                "yes" if result.complete else "no",
                format_rate(last.rate_limit if last else None),
                str(len(result.warnings)),
            ]
        )

    print_table(
        [
            "repo",
            "resource",
            "pages",
            "items",
            "bytes",
            "avg_ms",
            "max_ms",
            "done",
            "rate",
            "warn",
        ],
        rows,
    )

    warning_lines = [
        (result.repo, result.resource, warning)
        for result in results
        for warning in result.warnings
    ]
    if warning_lines:
        print()
        print("Warnings")
        for repo, resource, warning in warning_lines:
            print(f"- {repo} {resource}: {warning}")
    else:
        print()
        print("No warnings.")


def print_graphql_report(results: list[GraphQLBenchmark]) -> None:
    if not results:
        return

    print()
    print("GraphQL query benchmarks")
    print()

    rows = []
    known_total_cost = 0
    unknown_cost_count = 0

    for result in results:
        if result.cost is None:
            cost_display = "-"
            unknown_cost_count += 1
        else:
            cost_display = str(result.cost)
            known_total_cost += result.cost

        rows.append(
            [
                result.repo,
                result.query_name,
                str(result.status),
                format_bytes(result.response_bytes),
                f"{result.elapsed_ms:.0f}",
                cost_display,
                str(result.error_count),
                format_rate(result.rate_limit),
                str(len(result.warnings)),
            ]
        )

    print_table(
        [
            "repo",
            "query",
            "status",
            "bytes",
            "ms",
            "cost",
            "errors",
            "rate",
            "warn",
        ],
        rows,
    )

    print()
    print("GraphQL resource usage")
    print(f"- Known consumed cost: {known_total_cost}")

    if unknown_cost_count:
        print(
            f"- Queries with unknown cost: {unknown_cost_count} "
            "(add rateLimit { cost remaining limit resetAt } to those queries)"
        )

    last_result = results[-1]
    rate = last_result.rate_limit
    if rate is not None:
        print(f"- Last rate state: {format_rate(rate)}")
        if rate.remaining is not None and rate.limit is not None:
            consumed_window = rate.limit - rate.remaining
            print(f"- Used in current GitHub rate-limit window: {consumed_window}/{rate.limit}")

    warning_lines = [
        (result.repo, result.query_name, warning)
        for result in results
        for warning in result.warnings
    ]

    if warning_lines:
        print()
        print("GraphQL warnings")
        for repo, query_name, warning in warning_lines:
            print(f"- {repo} {query_name}: {warning}")

    error_lines = [
        (result.repo, result.query_name, message)
        for result in results
        for message in result.error_messages
    ]

    if error_lines:
        print()
        print("GraphQL errors")
        for repo, query_name, message in error_lines:
            print(f"- {repo} {query_name}: {message}")


def print_table(headers: list[str], rows: list[list[str]]) -> None:
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in rows)) if rows else len(headers[index])
        for index in range(len(headers))
    ]
    fmt = "  ".join("{:<" + str(width) + "}" for width in widths)
    print(fmt.format(*headers))
    print(fmt.format(*["-" * width for width in widths]))
    for row in rows:
        print(fmt.format(*row))


def format_bytes(value: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    size = float(value)
    unit = units[0]
    for unit in units:
        if size < 1024 or unit == units[-1]:
            break
        size /= 1024
    if unit == "B":
        return f"{int(size)}{unit}"
    return f"{size:.1f}{unit}"


def format_rate(rate: RateLimitState | None) -> str:
    if rate is None:
        return "-"
    resource = rate.resource or "?"
    remaining = "?" if rate.remaining is None else str(rate.remaining)
    limit = "?" if rate.limit is None else str(rate.limit)
    return f"{resource}:{remaining}/{limit}"


def write_report(
    path: str,
    results: list[ResourceBenchmark],
    graphql_results: list[GraphQLBenchmark],
) -> None:
    data = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "rest_results": [asdict(result) for result in results],
        "graphql_results": [asdict(result) for result in graphql_results],
    }
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> int:
    args = parse_args()

    if args.per_page < 1 or args.per_page > 100:
        print("--per-page must be between 1 and 100.", file=sys.stderr)
        return 2

    if args.max_pages < 1:
        print("--max-pages must be at least 1.", file=sys.stderr)
        return 2

    try:
        repos = load_repos(args)
        specs = parse_resource_specs(args)

        # Load GraphQL query paths from --graphql-query and --graphql-dir
        graphql_query_paths = list(args.graphql_query)

        if args.graphql_dir:
            graphql_dir = Path(args.graphql_dir)
            if not graphql_dir.exists():
                print(f"GraphQL dir does not exist: {graphql_dir}", file=sys.stderr)
                return 2

            graphql_query_paths.extend(
                str(path)
                for path in sorted(graphql_dir.glob("*.graphql"))
            )

        # Remove duplicates while preserving order
        graphql_query_paths = list(dict.fromkeys(graphql_query_paths))

        graphql_queries = [load_graphql_query(path) for path in graphql_query_paths]
        graphql_variables = load_graphql_variables(args.graphql_variables)

    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if not repos:
        print("Provide at least one --repo or --repos-file.", file=sys.stderr)
        return 2

    tokens_list = load_tokens(args.tokens_env)
    tokens = TokenCycler(tokens_list)

    results: list[ResourceBenchmark] = []
    for repo in repos:
        for spec in specs:
            results.append(benchmark_resource(repo, spec, args, tokens))

    graphql_results: list[GraphQLBenchmark] = []
    for repo in repos:
        for query_name, query in graphql_queries:
            graphql_results.append(
                benchmark_graphql_query(
                    repo,
                    query_name,
                    query,
                    graphql_variables,
                    args,
                    tokens,
                )
            )

    print_report(results, len(tokens_list))
    print_graphql_report(graphql_results)

    if args.out:
        write_report(args.out, results, graphql_results)
        print()
        print(f"Wrote JSON report to {args.out}")

    all_results = [*results, *graphql_results]
    if args.fail_on_warning and any(result.warnings for result in all_results):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
