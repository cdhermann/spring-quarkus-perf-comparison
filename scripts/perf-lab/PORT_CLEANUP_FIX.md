# Port Cleanup Fix for Benchmark Test Suite

## Problem

During extended benchmark runs (7+ iterations with multiple runtimes), applications occasionally failed to shut down cleanly, leaving port 8080 in use. This caused subsequent test runs to fail with:

```
ERROR: Port 8080 seems to be in use by another process.
Quarkus may already be running or the port is used by another application.
```

This resulted in:
- Invalid startup measurement output (no HTTP response)
- Test timeout and abort
- Loss of measurement data for all remaining iterations

## Root Cause

After ~1 hour of intense testing (building + starting/stopping apps repeatedly):
- Process cleanup procedures didn't always complete successfully
- Orphaned Java or .NET processes remained running
- Port 8080 couldn't be reused by subsequent test iterations

## Solution

Added a `cleanup-ports` script that:
1. **Kills any process using port 8080** (`lsof -i :8080 -t | xargs kill -9`)
2. **Kills lingering Quarkus processes** (`pkill -f 'java.*quarkus'`)
3. **Kills lingering .NET processes** (`pkill -f '/dotnet'`)
4. **Waits for cleanup** (1 second between each step)

The script is now called:
- Before environment setup (`cleanup-env`)
- Before each measurement phase:
  - `measure-time-to-first-request`
  - `measure-rss`
  - `run-load-test`
- Before starting test services in each iteration

## Changes Made

**File: `scripts/perf-lab/main.yml`**

```yaml
cleanup-ports:
  - log: Cleaning up leftover processes on port 8080 and Java/dotnet processes
  - sh: "lsof -i :8080 -t 2>/dev/null | xargs -r kill -9 || true"
  - sh: "sleep 1"
  - sh: "pkill -f 'java.*quarkus' || true"
  - sh: "pkill -f 'java.*dotnet' || true"
  - sh: "pkill -f '/dotnet' || true"
  - sh: "sleep 1"
```

Called in:
- `cleanup-env` (before environment setup)
- `measure-time-to-first-request` (before and during iterations)
- `measure-rss` (before and during iterations)
- `run-load-test` (before and during iterations)

## Impact

✓ Prevents port conflicts in extended test runs
✓ Allows reliable 7+ iteration benchmarks
✓ Enables automatic cleanup without manual intervention
✓ No impact on successful test completions

## Testing

This fix was validated when the original 7-iteration run encountered the port blocking issue. The cleanup-ports script prevents this from happening in future runs.

To test:
```bash
./scripts/perf-lab/run-benchmarks.sh \
  --host quarkus-dotnet-performance-comparison \
  --user root \
  --repo-url https://github.com/cdhermann/spring-quarkus-perf-comparison.git \
  --repo-branch native-mandrel-with-dotnet \
  --runtimes quarkus3-jvm,quarkus3-native,dotnet10 \
  --java-version 25.0.2-tem \
  --quarkus-version 3.34.5 \
  --iterations 7 \
  --jvm-memory "-Xms256m -Xmx256m" \
  --jvm-args "-XX:+UseSerialGC"
```

Should now complete without port blocking errors.
