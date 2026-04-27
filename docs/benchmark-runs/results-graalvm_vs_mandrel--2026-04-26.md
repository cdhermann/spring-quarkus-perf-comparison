# Benchmark Results: quarkus3-native, quarkus3-native-mandrel — 2026-04-26

> **Branch:** `native-mandrel` · **Commit:** `c0bd332` · **Iterations:** 1


## Environment

|Property|Value|
|---|---|
|**Date**|2026-04-26|
|**Host**|Hetzner vServer CPX62 <https://www.hetzner.com/cloud/regular-performance/>|
|**OS**|Ubuntu 24.04.3 LTS (kernel 6.8.0-110-generic)|
|**CPU**|AMD EPYC-Genoa Processor (16 cpus)|
|**Memory**|30Gi|
|**Java (JVM runtimes)**|OpenJDK 25.0.2 (Temurin)|
|**GraalVM CE (native)**|25.0.2-graalce|
|**Mandrel (native)**|25.0.0.1.r25-mandrel|
|**Quarkus**|3.34.5|
|**Repo branch**|`native-mandrel`|
|**Repo commit**|`c0bd332`|
|**Iterations**|1|

### CPU Pinning

|Role|CPUs|
|---|---|
|Application|0-3|
|PostgreSQL|4-6|
|OpenTelemetry stack|7-9|
|Load generator (wrk2)|10-12|
|First-request measurement|10|
|Monitoring (pidstat)|13|

### Runtime Configuration

- **Load test:** wrk2, 2 threads, 100 connections, 2 min warmup + 30 sec measurement window
- **Endpoint:** `GET /fruits` (reads all fruits with store/address joins from PostgreSQL)

---

## Runtimes Tested

|Runtime|Description|
|---|---|
|`quarkus3-native`|Quarkus 3.34.5, GraalVM CE native image (x86-64-v3, Serial GC)|
|`quarkus3-native-mandrel`|Quarkus 3.34.5, Mandrel native image (x86-64-v3, Serial GC)|

---

## Native Image Statistics

|Metric|`quarkus3-native`|`quarkus3-native-mandrel`|
|---|---|---|
|**Total image size (MB)**|121.82|122.34|
|**Reachable types**|27,587|27,587|
|**Reachable fields**|37,248|37,246|
|**Reachable methods**|135,482|135,469|
|**Reflection types**|9,051|9,050|
|**Reflection fields**|1,816|1,815|
|**Reflection methods**|17,176|17,176|
|**Peak build RSS (GB)**|5.08|5.13|

---

## Raw Measurements

### Build Time (seconds)

|Runtime|I0|Average|Std|CV%|
|---|---|---|---|---|
|`quarkus3-native`|155.63|**155.63**|—|—|
|`quarkus3-native-mandrel`|151.28|**151.28**|—|—|

### Time to First Request (milliseconds)

|Runtime|I0|Average|Std|CV%|
|---|---|---|---|---|
|`quarkus3-native`|121.85|**121.85**|—|—|
|`quarkus3-native-mandrel`|111.38|**111.38**|—|—|

### RSS at Startup — before any request (MiB)

|Runtime|I0|Average|Std|CV%|
|---|---|---|---|---|
|`quarkus3-native`|89.65|**89.65**|—|—|
|`quarkus3-native-mandrel`|89.73|**89.73**|—|—|

### RSS after First Request (MiB)

|Runtime|I0|Average|Std|CV%|
|---|---|---|---|---|
|`quarkus3-native`|95.66|**95.66**|—|—|
|`quarkus3-native-mandrel`|95.66|**95.66**|—|—|

### RSS under Load (MiB)

|Runtime|I0|Average|Std|CV%|
|---|---|---|---|---|
|`quarkus3-native`|291.77|**291.77**|—|—|
|`quarkus3-native-mandrel`|291.14|**291.14**|—|—|

### Throughput (req/sec)

|Runtime|I0|Average|Std|CV%|
|---|---|---|---|---|
|`quarkus3-native`|8,550|**8,550**|—|—|
|`quarkus3-native-mandrel`|8,741|**8,741**|—|—|

### Throughput Density (req/sec per MiB of RSS under load)

|Runtime|I0|Max|Std|CV%|
|---|---|---|---|---|
|`quarkus3-native`|29.31|**29.31**|—|—|
|`quarkus3-native-mandrel`|30.02|**30.02**|—|—|

---

## Summary Comparison

|Runtime|Build (s)|Startup (ms)|RSS idle (MiB)|RSS load (MiB)|Throughput (tps)|Density (tps/MiB)|
|---|---|---|---|---|---|---|
|`quarkus3-native`|155.63|121.8|89.6|291.8|**8,550**|29.31|
|`quarkus3-native-mandrel`|151.28|111.4|89.7|291.1|**8,741**|30.02|

---

## Analysis

### Build Time

|Runtime|Avg (s)|vs `quarkus3-native`|
|---|---|---|
|`quarkus3-native-mandrel`|151.3|~same|
|`quarkus3-native`|**155.6**|baseline|

### Startup — Time to First Request

|Runtime|Avg (ms)|vs `quarkus3-native`|
|---|---|---|
|`quarkus3-native-mandrel`|111|1.1× less|
|`quarkus3-native`|**122**|baseline|

### Memory at Idle (RSS at startup)

|Runtime|Avg (MiB)|vs `quarkus3-native`|
|---|---|---|
|`quarkus3-native`|**89.6**|baseline|
|`quarkus3-native-mandrel`|89.7|~same|

### Memory under Load (RSS)

|Runtime|Avg (MiB)|vs `quarkus3-native`|
|---|---|---|
|`quarkus3-native-mandrel`|291.1|~same|
|`quarkus3-native`|**291.8**|baseline|

### Throughput

|Runtime|Avg (tps)|vs `quarkus3-native-mandrel`|
|---|---|---|
|`quarkus3-native-mandrel`|**8,741**|baseline|
|`quarkus3-native`|8,550|-2%|

### Throughput Density (tps per MiB of RAM under load)

|Runtime|Avg (tps/MiB)|vs `quarkus3-native`|
|---|---|---|
|`quarkus3-native-mandrel`|30.02|+2%|
|`quarkus3-native`|**29.31**|baseline|

---

## Key Trade-offs

|Goal|Best choice|
|---|---|
|Lowest startup latency|`quarkus3-native-mandrel` (111.4)|
|Highest raw throughput|`quarkus3-native-mandrel` (8741.5)|
|Lowest memory footprint (idle)|`quarkus3-native` (89.6)|
|Lowest memory footprint (load)|`quarkus3-native-mandrel` (291.1)|
|Best throughput per MiB of RAM|`quarkus3-native-mandrel` (30.0)|
|Fastest build|`quarkus3-native-mandrel` (151.3)|

---

## Statistical Significance

> ⚠️ **n = 1:** Standard deviation, confidence intervals, and significance tests require at least 2 observations. Run more iterations (`--iterations 3` or more) for robust statistics.

---

## Statistical Notes

|Measure|Meaning|
|---|---|
|**[CV%](https://en.wikipedia.org/wiki/Coefficient_of_variation)** (Coefficient of Variation)|Standard deviation expressed as a percentage of the mean. Measures run-to-run consistency. CV% < 5% → very stable · 5–15% → moderate · > 15% → noisy.|
|**[95% CI](https://en.wikipedia.org/wiki/Confidence_interval)** (Confidence Interval)|Range that would contain the true mean in 95% of repeated experiments (t-distribution, two-tailed). Wider CI = more uncertainty.|
|**[Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)** (Effect Size)|Standardised difference between two means using pooled standard deviation. Magnitude: < 0.2 negligible · 0.2–0.5 small · 0.5–0.8 medium · ≥ 0.8 large. Tells you *how big* a difference is, not just whether it's real.|
|**[Welch p-value](https://en.wikipedia.org/wiki/Welch%27s_t-test)** (Two-tailed Welch's t-test)|Probability of observing a difference at least this large by chance alone, assuming the two runtimes perform identically. p < 0.05 → statistically significant at the 95% confidence level. Does not assume equal variances.|

> Statistical tests require **n ≥ 2** iterations. With n < 5 the results are directionally informative but unreliable — prefer **n ≥ 5** for robust conclusions.


---

*Generated by `scripts/perf-lab/generate-report.py` from the [spring-quarkus-perf-comparison](https://github.com/quarkusio/spring-quarkus-perf-comparison) perf-lab tooling.*