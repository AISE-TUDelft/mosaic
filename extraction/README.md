# Extraction Benchmarks

Use the benchmark runner to test GitHub resource queries separately before adding
them to the scheduler. This helps catch resources that are too large, too slow,
or too expensive for the current rate-limit budget.

Set one token:

```powershell
$env:GITHUB_TOKEN = "ghp_..."
```

Or set several tokens:

```powershell
$env:GITHUB_TOKENS = "ghp_1,ghp_2,ghp_3"
```

Run a small benchmark:

```powershell
python extraction/benchmark_runner.py --repo owner/name --resources repo,issues,pulls,commits --max-pages 1
```

Run the default resource set and save a JSON report:

```powershell
python extraction/benchmark_runner.py --repo owner/name --max-pages 2 --out out/benchmarks/owner-name.json
```

Useful knobs:

```powershell
python extraction/benchmark_runner.py `
  --repo owner/name `
  --resources all `
  --per-page 100 `
  --max-pages 3 `
  --warn-pages 20 `
  --warn-items 1000 `
  --warn-seconds 10 `
  --warn-bytes 5000000
```

You can also benchmark a custom REST path:

```powershell
python extraction/benchmark_runner.py `
  --repo owner/name `
  --resources custom-events `
  --path "custom-events=/repos/{owner}/{repo}/events"
```

Benchmark a GraphQL query before putting it in the scheduler:

```powershell
python extraction/benchmark_runner.py `
  --repo owner/name `
  --resources none `
  --graphql-query extraction/examples/repo_summary.graphql `
  --warn-graphql-cost 50
```

GraphQL variables are auto-filled for repo queries:

```json
{
  "owner": "owner",
  "repo": "name",
  "name": "name",
  "repoName": "name",
  "repository": "owner/name"
}
```

You can pass additional variables as JSON:

```powershell
python extraction/benchmark_runner.py `
  --repo owner/name `
  --resources none `
  --graphql-query extraction/examples/repo_summary.graphql `
  --graphql-variables '{"pageSize": 25}'
```

Include this in GraphQL queries to see the query cost:

```graphql
rateLimit {
  cost
  limit
  remaining
  used
  resetAt
}
```
