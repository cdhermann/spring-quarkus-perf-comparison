#!/usr/bin/env python3
"""
Generate a markdown benchmark report from a qDup benchmark log file.

The log file contains a line:
    echo '{...}' > /tmp/metrics.json
This script extracts that JSON and renders it as a structured markdown report
following the pattern established in docs/benchmark-runs/.

Usage:
    python3 generate-report.py <path-to-log.txt> [output.md]

If output.md is omitted the report is written to stdout.
If output.md is a directory the report is written there with a name derived
from the input filename.
"""

import json
import math
import os
import re
import sys
from pathlib import Path


# ──────────────────────────────────────────────────────────────────────────────
# Extraction
# ──────────────────────────────────────────────────────────────────────────────

def extract_metrics(log_path: Path) -> dict:
    """Find the last echo '...' > /tmp/metrics.json line and parse the JSON.

    A log file may contain multiple such lines when a run was retried or
    preceded by a failed setup attempt.  The last occurrence is the one
    that contains the actual benchmark results.
    """
    pattern = re.compile(r"echo '(\{.*\})' > /tmp/metrics\.json")
    last_match = None
    with open(log_path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = pattern.search(line)
            if m:
                last_match = m
    if last_match:
        return json.loads(last_match.group(1))
    raise ValueError(
        f"Could not find 'echo ... > /tmp/metrics.json' in {log_path}.\n"
        "Make sure the file is a complete qDup benchmark log."
    )


def extract_java_versions(log_path: Path) -> dict[str, str]:
    """
    Scrape Java/GraalVM/Mandrel/dotnet version strings from the log.
    Returns a dict with keys: java, graalvm, mandrel, dotnet.
    """
    versions: dict[str, str] = {}
    graalvm_next = False
    mandrel_next = False

    java_re   = re.compile(r'openjdk version "([^"]+)"')
    vendor_re = re.compile(r"(GraalVM CE|Mandrel-[\d.]+[^\s]*)", re.IGNORECASE)
    dotnet_re = re.compile(r"\.NET\s+([\d.]+)")

    with open(log_path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if "Showing GraalVM version" in line or "Native image tool version" in line:
                graalvm_next = True
                mandrel_next = False
                continue
            if "Showing Mandrel version" in line:
                mandrel_next = True
                graalvm_next = False
                continue
            if "Showing Java version" in line:
                graalvm_next = False
                mandrel_next = False

            m = java_re.search(line)
            if m:
                ver = m.group(1)
                if graalvm_next and "graalvm" not in versions:
                    versions["graalvm_jdk"] = ver
                    vm = vendor_re.search(line)
                    if vm:
                        versions["graalvm"] = vm.group(1)
                    graalvm_next = False
                elif mandrel_next and "mandrel" not in versions:
                    versions["mandrel_jdk"] = ver
                    vm = vendor_re.search(line)
                    if vm:
                        versions["mandrel"] = vm.group(1)
                    mandrel_next = False
                elif "java" not in versions:
                    versions["java"] = ver

            m = dotnet_re.search(line)
            if m and "dotnet" not in versions:
                versions["dotnet"] = m.group(1)

    return versions


# ──────────────────────────────────────────────────────────────────────────────
# Formatting helpers
# ──────────────────────────────────────────────────────────────────────────────

def _safe(val, decimals=2, thousands=False):
    """Format a numeric value; return '—' for missing/empty."""
    if val is None or val == "" or (isinstance(val, float) and math.isnan(val)):
        return "—"
    if isinstance(val, str):
        return val if val.strip() else "—"
    if thousands:
        return f"{val:,.{decimals}f}"
    return f"{val:.{decimals}f}"


def _pct(new_val, base_val, invert=False):
    """
    Return a concise relative string.
    invert=True means smaller is better (e.g. latency, memory): show as Nx less/more.
    invert=False means larger is better (throughput): show as +X% or −X%.
    """
    if base_val is None or new_val is None or base_val == 0:
        return "—"
    try:
        bv = float(base_val)
        nv = float(new_val)
    except (TypeError, ValueError):
        return "—"
    if bv == 0:
        return "—"
    if invert:
        ratio = bv / nv if nv != 0 else float("inf")
        if abs(ratio - 1) < 0.03:
            return "~same"
        if ratio > 1:
            return f"{ratio:.1f}× less"
        return f"{1/ratio:.1f}× more"
    else:
        diff = (nv - bv) / bv * 100
        if abs(diff) < 0.5:
            return "~same"
        return f"+{diff:.0f}%" if diff > 0 else f"{diff:.0f}%"


def _header_row(cols):
    sep = "|".join("---" for _ in cols)
    return f"|{'|'.join(cols)}|\n|{sep}|"


def _table(headers, rows):
    """Render a markdown table."""
    lines = [_header_row(headers)]
    for row in rows:
        lines.append("|" + "|".join(str(c) for c in row) + "|")
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Runtime classification
# ──────────────────────────────────────────────────────────────────────────────

NATIVE_PATTERNS = ("native",)
DOTNET_PATTERNS = ("dotnet",)
LEYDEN_PATTERNS = ("leyden",)

def is_native(name: str) -> bool:
    return any(p in name for p in NATIVE_PATTERNS)

def is_dotnet(name: str) -> bool:
    return any(p in name for p in DOTNET_PATTERNS)

def is_leyden(name: str) -> bool:
    return any(p in name for p in LEYDEN_PATTERNS)

RUNTIME_DESCRIPTIONS = {
    "quarkus3-jvm":            "Quarkus, standard threads, JVM",
    "quarkus3-leyden":         "Quarkus, standard threads, JVM + Project Leyden AOT cache",
    "quarkus3-virtual":        "Quarkus, virtual threads, JVM",
    "quarkus3-virtual-leyden": "Quarkus, virtual threads, JVM + Project Leyden AOT cache",
    "quarkus3-native":         "Quarkus, GraalVM CE native image (x86-64-v3, Serial GC)",
    "quarkus3-native-mandrel": "Quarkus, Mandrel native image (x86-64-v3, Serial GC)",
    "spring3-jvm":             "Spring Boot 3.x, standard threads, JVM",
    "spring3-leyden":          "Spring Boot 3.x, standard threads, JVM + Project Leyden AOT cache",
    "spring3-virtual":         "Spring Boot 3.x, virtual threads, JVM",
    "spring3-virtual-leyden":  "Spring Boot 3.x, virtual threads, JVM + Project Leyden AOT cache",
    "spring3-native":          "Spring Boot 3.x, GraalVM CE native image",
    "spring3-jvm-aot":         "Spring Boot 3.x, Spring AOT processing, JVM",
    "spring4-jvm":             "Spring Boot 4.x, standard threads, JVM",
    "spring4-leyden":          "Spring Boot 4.x, standard threads, JVM + Project Leyden AOT cache",
    "spring4-virtual":         "Spring Boot 4.x, virtual threads, JVM",
    "spring4-virtual-leyden":  "Spring Boot 4.x, virtual threads, JVM + Project Leyden AOT cache",
    "spring4-native":          "Spring Boot 4.x, GraalVM CE native image",
    "spring4-jvm-aot":         "Spring Boot 4.x, Spring AOT processing, JVM",
    "dotnet10":                "ASP.NET Core 10, server GC",
}

def runtime_description(name: str, metrics: dict) -> str:
    if name in RUNTIME_DESCRIPTIONS:
        desc = RUNTIME_DESCRIPTIONS[name]
    else:
        desc = name
    # Annotate with version where known
    cfg = metrics.get("config", {})
    if "quarkus" in name:
        v = cfg.get("quarkus", {}).get("version", "")
        if v:
            desc = f"Quarkus {v}, " + desc.split("Quarkus, ", 1)[-1]
    elif "spring3" in name:
        v = cfg.get("springboot3", {}).get("version", "")
        if v:
            desc = f"Spring Boot {v}, " + desc.split("Spring Boot 3.x, ", 1)[-1]
    elif "spring4" in name:
        v = cfg.get("springboot4", {}).get("version", "")
        if v:
            desc = f"Spring Boot {v}, " + desc.split("Spring Boot 4.x, ", 1)[-1]
    elif "dotnet" in name:
        dotnet_limit = cfg.get("dotnet", {}).get("gcHeapHardLimit", "")
        if dotnet_limit:
            # convert hex to MiB
            try:
                mib = int(dotnet_limit, 16) // (1024 * 1024)
                desc += f", {mib} MiB heap limit"
            except ValueError:
                pass
    return desc


# ──────────────────────────────────────────────────────────────────────────────
# Baseline selection
# ──────────────────────────────────────────────────────────────────────────────

BASELINE_PREFERENCE = [
    "quarkus3-jvm",
    "quarkus3-virtual",
    "quarkus3-native",
    "spring3-jvm",
    "spring4-jvm",
    "dotnet10",
]

def pick_baseline(runtimes: list[str]) -> str:
    for candidate in BASELINE_PREFERENCE:
        if candidate in runtimes:
            return candidate
    return runtimes[0]

def pick_throughput_baseline(runtimes: list[str]) -> str:
    """For throughput tables use the lowest-throughput runtime as baseline."""
    # Prefer dotnet10 (established convention), else last in list
    if "dotnet10" in runtimes:
        return "dotnet10"
    return runtimes[-1]


# ──────────────────────────────────────────────────────────────────────────────
# Report sections
# ──────────────────────────────────────────────────────────────────────────────

def section_environment(metrics: dict, versions: dict) -> str:
    cfg  = metrics.get("config", {})
    env  = metrics.get("env", {})
    tim  = metrics.get("timing", {})
    host = env.get("host", {})
    repo = cfg.get("repo", {})
    jvm  = cfg.get("jvm", {})

    host_type = host.get("type", "")
    host_line = host_type
    if "Hetzner" in host_type:
        host_line = f"{host_type} CPX62 <https://www.hetzner.com/cloud/regular-performance/>"

    start = tim.get("start", "")
    date  = start[:10] if start else "—"

    graalvm_ver  = jvm.get("graalvm", {}).get("version", "")
    mandrel_ver  = jvm.get("mandrel", {}).get("version", "")
    java_sdk_ver = jvm.get("version", "")
    quarkus_ver  = cfg.get("quarkus", {}).get("version", "")
    sb3_ver      = cfg.get("springboot3", {}).get("version", "")
    sb4_ver      = cfg.get("springboot4", {}).get("version", "")
    dotnet_ver   = versions.get("dotnet", "")
    num_iter     = cfg.get("num_iterations", "")
    commit       = repo.get("short_commit", repo.get("commit", "")[:7])
    branch       = repo.get("branch", "")

    rows = [
        ("Date", date),
        ("Host", host_line),
        ("OS", f"{host.get('os','')} (kernel {host.get('kernel','')})"),
        ("CPU", host.get("cpu", "")),
        ("Memory", host.get("memory", "")),
    ]
    if java_sdk_ver:
        rows.append(("Java (JVM runtimes)", f"OpenJDK {java_sdk_ver.split('-')[0]} (Temurin)"))
    if graalvm_ver:
        rows.append(("GraalVM CE (native)", graalvm_ver))
    if mandrel_ver:
        rows.append(("Mandrel (native)", mandrel_ver))
    if dotnet_ver:
        rows.append((".NET", dotnet_ver))
    if quarkus_ver:
        rows.append(("Quarkus", quarkus_ver))
    if sb3_ver:
        rows.append(("Spring Boot 3.x", sb3_ver))
    if sb4_ver:
        rows.append(("Spring Boot 4.x", sb4_ver))
    rows += [
        ("Repo branch", f"`{branch}`"),
        ("Repo commit", f"`{commit}`"),
        ("Iterations", str(num_iter)),
    ]

    table = _table(["Property", "Value"],
                   [[f"**{k}**", v] for k, v in rows])

    # CPU pinning
    res = cfg.get("resources", {}).get("cpu", {})
    cpu_rows = [
        ["Application",               res.get("app",            "—")],
        ["PostgreSQL",                res.get("db",             "—")],
        ["OpenTelemetry stack",        res.get("otel",           "—")],
        ["Load generator (wrk2)",      res.get("load_generator", "—")],
        ["First-request measurement",  str(res.get("1st_request","—"))],
        ["Monitoring (pidstat)",       str(res.get("monitor",    "—"))],
    ]
    cpu_table = _table(["Role", "CPUs"], cpu_rows)

    # Runtime config
    mem   = jvm.get("memory", "")
    dnet  = cfg.get("dotnet", {}).get("gcHeapHardLimit", "")
    runtimes_in_run = list(metrics.get("results", {}).keys())
    has_jvm    = any(not is_native(r) and not is_dotnet(r) for r in runtimes_in_run)
    has_dotnet = any(is_dotnet(r) for r in runtimes_in_run)

    rt_config_lines = []
    if has_jvm and mem:
        active_count = cfg.get("resources", {}).get("app_cpus", "")
        rt_config_lines.append(
            f"- **JVM runtimes:** `{mem}`, `-XX:ActiveProcessorCount={active_count}`"
        )
    if has_dotnet and dnet:
        try:
            mib = int(dnet, 16) // (1024 * 1024)
        except ValueError:
            mib = "?"
        app_cpus = cfg.get("resources", {}).get("app_cpus", "?")
        rt_config_lines.append(
            f"- **dotnet10:** `DOTNET_GCHeapHardLimit={dnet}` ({mib} MiB), "
            f"`DOTNET_ProcessorCount={app_cpus}`, `DOTNET_gcServer=1`"
        )
    rt_config_lines += [
        "- **Load test:** wrk2, 2 threads, 100 connections, 2 min warmup + 30 sec measurement window",
        "- **Endpoint:** `GET /fruits` (reads all fruits with store/address joins from PostgreSQL)",
    ]

    return f"""\
## Environment

{table}

### CPU Pinning

{cpu_table}

### Runtime Configuration

{chr(10).join(rt_config_lines)}"""


def section_runtimes(metrics: dict) -> str:
    runtimes = list(metrics.get("results", {}).keys())
    rows = [[f"`{r}`", runtime_description(r, metrics)] for r in runtimes]
    return f"## Runtimes Tested\n\n{_table(['Runtime', 'Description'], rows)}"


def section_native_stats(metrics: dict) -> str:
    results  = metrics.get("results", {})
    natives  = [(r, results[r]) for r in results if is_native(r)]
    if not natives:
        return ""

    headers = ["Metric"] + [f"`{r}`" for r, _ in natives]
    stat_keys = [
        ("Total image size (MB)",     lambda b: _safe(b.get("native",{}).get("binarySize"),  2)),
        ("Reachable types",           lambda b: _safe(b.get("classCount"), 0)),
        ("Reachable fields",          lambda b: _safe(b.get("fieldCount"), 0)),
        ("Reachable methods",         lambda b: _safe(b.get("methodCount"), 0)),
        ("Reflection types",          lambda b: _safe(b.get("reflectionClassCount"), 0)),
        ("Reflection fields",         lambda b: _safe(b.get("reflectionFieldCount"), 0)),
        ("Reflection methods",        lambda b: _safe(b.get("reflectionMethodCount"), 0)),
        ("Peak build RSS (GB)",       lambda b: _safe(
            sum(b.get("native",{}).get("rss",[]))/len(b.get("native",{}).get("rss",[1]))
            if b.get("native",{}).get("rss") else None, 2)),
    ]

    rows = []
    for label, fn in stat_keys:
        row = [f"**{label}**"]
        for _, rd in natives:
            row.append(fn(rd.get("build", {})))
        rows.append(row)

    return f"## Native Image Statistics\n\n{_table(headers, rows)}"


def _raw_table(metric_name: str, runtimes: list[str], results: dict,
               extractor, unit: str, fmt_decimals: int = 2,
               max_not_avg: bool = False) -> str:
    """Generic raw measurement table with per-iteration columns + average/max."""
    num_iter = max(len(extractor(results[r]) or []) for r in runtimes)
    iter_cols = [f"I{i}" for i in range(num_iter)]
    agg_label = "Max" if max_not_avg else "Average"
    headers = ["Runtime"] + iter_cols + [agg_label]

    rows = []
    for r in runtimes:
        vals = extractor(results[r]) or []
        row = [f"`{r}`"]
        for v in vals:
            row.append(_safe(v, fmt_decimals, thousands=(fmt_decimals == 0 or v > 999)))
        # pad if fewer iterations
        while len(row) < 1 + num_iter:
            row.append("—")
        if vals:
            agg = max(vals) if max_not_avg else sum(vals) / len(vals)
            agg_str = _safe(agg, fmt_decimals, thousands=(fmt_decimals == 0 or agg > 999))
            row.append(f"**{agg_str}**")
        else:
            row.append("—")
        rows.append(row)

    return f"### {metric_name} ({unit})\n\n{_table(headers, rows)}"


def section_raw_measurements(metrics: dict) -> str:
    results  = metrics.get("results", {})
    runtimes = list(results.keys())
    has_native = any(is_native(r) for r in runtimes)

    parts = ["## Raw Measurements"]

    # Build time
    parts.append(_raw_table(
        "Build Time", runtimes, results,
        lambda rd: rd.get("build", {}).get("timings"),
        "seconds", fmt_decimals=2
    ))

    # TTFR
    parts.append(_raw_table(
        "Time to First Request", runtimes, results,
        lambda rd: rd.get("startup", {}).get("timings"),
        "milliseconds", fmt_decimals=2
    ))

    # RSS startup
    parts.append(_raw_table(
        "RSS at Startup — before any request", runtimes, results,
        lambda rd: rd.get("rss", {}).get("startup"),
        "MiB", fmt_decimals=2
    ))

    # RSS first request
    parts.append(_raw_table(
        "RSS after First Request", runtimes, results,
        lambda rd: rd.get("rss", {}).get("firstRequest"),
        "MiB", fmt_decimals=2
    ))

    # RSS under load
    parts.append(_raw_table(
        "RSS under Load", runtimes, results,
        lambda rd: rd.get("load", {}).get("rss"),
        "MiB", fmt_decimals=2
    ))

    # Throughput
    parts.append(_raw_table(
        "Throughput", runtimes, results,
        lambda rd: rd.get("load", {}).get("throughput"),
        "req/sec", fmt_decimals=0
    ))

    # Throughput density
    parts.append(_raw_table(
        "Throughput Density", runtimes, results,
        lambda rd: rd.get("load", {}).get("throughputDensity"),
        "req/sec per MiB of RSS under load", fmt_decimals=2,
        max_not_avg=True
    ))

    return "\n\n".join(parts)


def _avg(vals):
    if not vals:
        return None
    clean = [v for v in vals if v is not None and v != ""]
    return sum(clean) / len(clean) if clean else None


def section_summary(metrics: dict) -> str:
    results  = metrics.get("results", {})
    runtimes = list(results.keys())

    headers = ["Runtime", "Build (s)", "Startup (ms)",
               "RSS idle (MiB)", "RSS load (MiB)",
               "Throughput (tps)", "Density (tps/MiB)"]

    rows = []
    for r in runtimes:
        rd = results[r]
        build    = _avg(rd.get("build", {}).get("timings"))
        startup  = _avg(rd.get("startup", {}).get("timings"))
        rss_idle = _avg(rd.get("rss", {}).get("startup"))
        rss_load = _avg(rd.get("load", {}).get("rss"))
        tput     = _avg(rd.get("load", {}).get("throughput"))
        density  = rd.get("load", {}).get("maxThroughputDensity") or \
                   max(rd.get("load", {}).get("throughputDensity") or [0])
        rows.append([
            f"`{r}`",
            _safe(build,    2),
            _safe(startup,  1) if startup else "—",
            _safe(rss_idle, 1) if rss_idle else "—",
            _safe(rss_load, 1) if rss_load else "—",
            f"**{_safe(tput, 0, thousands=True)}**" if tput else "—",
            _safe(density,  2) if density else "—",
        ])

    return f"## Summary Comparison\n\n{_table(headers, rows)}"


def _analysis_table(title: str, runtimes: list[str], results: dict,
                    value_fn, unit: str, baseline: str,
                    smaller_is_better: bool = True,
                    fmt_d: int = 1,
                    thousands: bool = False) -> str:
    """Render a ranked analysis table with 'vs baseline' column."""
    # Collect averages
    vals = {}
    for r in runtimes:
        rd = results[r]
        v = value_fn(rd)
        vals[r] = v

    base_val = vals.get(baseline)

    # Sort: ascending if smaller_is_better, descending otherwise
    sorted_runtimes = sorted(
        runtimes,
        key=lambda r: (vals[r] is None, vals[r] or 0),
        reverse=not smaller_is_better
    )

    col_vs = f"vs `{baseline}`"
    headers = ["Runtime", f"Avg ({unit})" if not smaller_is_better or unit != "tps/MiB"
               else f"Max ({unit})", col_vs]

    rows = []
    for r in sorted_runtimes:
        v = vals[r]
        if v is None:
            val_str = "—"
            rel_str = "—"
        else:
            val_str = _safe(v, fmt_d, thousands=thousands)
            if r == baseline:
                val_str = f"**{val_str}**"
                rel_str = "baseline"
            else:
                rel_str = _pct(v, base_val, invert=smaller_is_better)
        rows.append([f"`{r}`", val_str, rel_str])

    return f"### {title}\n\n{_table(headers, rows)}"


def section_analysis(metrics: dict) -> str:
    results  = metrics.get("results", {})
    runtimes = list(results.keys())
    baseline = pick_baseline(runtimes)
    tp_baseline = pick_throughput_baseline(runtimes)

    parts = ["## Analysis"]

    # Build time
    parts.append(_analysis_table(
        "Build Time", runtimes, results,
        lambda rd: _avg(rd.get("build", {}).get("timings")),
        "s", baseline, smaller_is_better=True, fmt_d=1
    ))

    # Startup
    parts.append(_analysis_table(
        "Startup — Time to First Request", runtimes, results,
        lambda rd: _avg(rd.get("startup", {}).get("timings")),
        "ms", baseline, smaller_is_better=True, fmt_d=0
    ))

    # RSS idle
    parts.append(_analysis_table(
        "Memory at Idle (RSS at startup)", runtimes, results,
        lambda rd: _avg(rd.get("rss", {}).get("startup")),
        "MiB", baseline, smaller_is_better=True, fmt_d=1
    ))

    # RSS load
    parts.append(_analysis_table(
        "Memory under Load (RSS)", runtimes, results,
        lambda rd: _avg(rd.get("load", {}).get("rss")),
        "MiB", baseline, smaller_is_better=True, fmt_d=1
    ))

    # Throughput
    parts.append(_analysis_table(
        "Throughput", runtimes, results,
        lambda rd: _avg(rd.get("load", {}).get("throughput")),
        "tps", tp_baseline, smaller_is_better=False, fmt_d=0, thousands=True
    ))

    # Density
    parts.append(_analysis_table(
        "Throughput Density (tps per MiB of RAM under load)", runtimes, results,
        lambda rd: rd.get("load", {}).get("maxThroughputDensity") or
                   max(rd.get("load", {}).get("throughputDensity") or [0]),
        "tps/MiB", baseline, smaller_is_better=False, fmt_d=2
    ))

    return "\n\n".join(parts)


def section_key_tradeoffs(metrics: dict) -> str:
    results  = metrics.get("results", {})
    runtimes = list(results.keys())

    def best_by(fn, want_max=True):
        candidates = {r: fn(results[r]) for r in runtimes}
        candidates = {r: v for r, v in candidates.items() if v is not None}
        if not candidates:
            return "—"
        r = max(candidates, key=candidates.__getitem__) if want_max \
            else min(candidates, key=candidates.__getitem__)
        return f"`{r}` ({_safe(candidates[r], 1)})"

    startup_best  = best_by(lambda rd: _avg(rd.get("startup", {}).get("timings")), want_max=False)
    tput_best     = best_by(lambda rd: _avg(rd.get("load", {}).get("throughput")), want_max=True)
    mem_idle_best = best_by(lambda rd: _avg(rd.get("rss", {}).get("startup")), want_max=False)
    mem_load_best = best_by(lambda rd: _avg(rd.get("load", {}).get("rss")), want_max=False)
    density_best  = best_by(
        lambda rd: rd.get("load", {}).get("maxThroughputDensity") or
                   max(rd.get("load", {}).get("throughputDensity") or [0]),
        want_max=True
    )
    build_best    = best_by(lambda rd: _avg(rd.get("build", {}).get("timings")), want_max=False)

    rows = [
        ["Lowest startup latency",         startup_best],
        ["Highest raw throughput",          tput_best],
        ["Lowest memory footprint (idle)",  mem_idle_best],
        ["Lowest memory footprint (load)",  mem_load_best],
        ["Best throughput per MiB of RAM",  density_best],
        ["Fastest build",                   build_best],
    ]
    return f"## Key Trade-offs\n\n{_table(['Goal', 'Best choice'], rows)}"


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def generate_report(log_path: Path) -> str:
    metrics  = extract_metrics(log_path)
    versions = extract_java_versions(log_path)

    tim     = metrics.get("timing", {})
    cfg     = metrics.get("config", {})
    repo    = cfg.get("repo", {})
    results = metrics.get("results", {})

    runtimes     = list(results.keys())
    date         = tim.get("start", "")[:10]
    branch       = repo.get("branch", "")
    commit       = repo.get("short_commit", repo.get("commit", "")[:7])
    num_iter     = cfg.get("num_iterations", "")
    has_native   = any(is_native(r) for r in runtimes)

    runtime_names = ", ".join(runtimes)
    title = f"# Benchmark Results: {runtime_names} — {date}"

    header = f"""\
{title}

> **Branch:** `{branch}` · **Commit:** `{commit}` · **Iterations:** {num_iter}
"""

    footer = (
        "\n---\n\n"
        "*Generated by `scripts/perf-lab/generate-report.py` "
        "from the [spring-quarkus-perf-comparison](https://github.com/quarkusio/spring-quarkus-perf-comparison) "
        "perf-lab tooling.*"
    )

    sections = [
        header,
        section_environment(metrics, versions),
        "---",
        section_runtimes(metrics),
    ]

    if has_native:
        sections += ["---", section_native_stats(metrics)]

    sections += [
        "---",
        section_raw_measurements(metrics),
        "---",
        section_summary(metrics),
        "---",
        section_analysis(metrics),
        "---",
        section_key_tradeoffs(metrics),
        footer,
    ]

    return "\n\n".join(sections)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    log_path = Path(sys.argv[1])
    if not log_path.exists():
        print(f"Error: file not found: {log_path}", file=sys.stderr)
        sys.exit(1)

    report = generate_report(log_path)

    if len(sys.argv) >= 3:
        out = Path(sys.argv[2])
        if out.is_dir():
            stem = log_path.stem
            out = out / f"{stem}.md"
        out.write_text(report, encoding="utf-8")
        print(f"Report written to {out}")
    else:
        print(report)


if __name__ == "__main__":
    main()
