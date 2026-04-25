# Benchmark Results: GraalVM CE vs Mandrel — 2026-04-25

## Environment

| Property | Value |
|---|---|
| Date | 2026-04-25 |
| Host | Hetzner vServer CPX62 <https://www.hetzner.com/cloud/regular-performance/> |
| OS | Ubuntu 24.04.3 LTS (kernel 6.8.0-110-generic) |
| CPU | AMD EPYC-Genoa, 16 vCPUs |
| Memory | 30 GiB |
| Java (build/runtime) | OpenJDK 25.0.2 (Temurin) |
| GraalVM CE | 25.0.2+10.1 (JDK 25) |
| Mandrel | 24.1.2.0-Final (JDK 23.0.2+7) |
| Quarkus | 3.34.5 |
| Repo branch | `native-mandrel` |
| Repo commit | `c0bd332` |
| Iterations | 3 per runtime |
| Duration | ~56 min |

### CPU Pinning

| Role | CPUs |
|---|---|
| Application | 0–3 (4 cores) |
| PostgreSQL | 4–6 |
| OpenTelemetry stack | 7–9 |
| Load generator (wrk2) | 10–12 |
| First-request measurement | 10 |
| Monitoring (pidstat) | 13 |

### Runtime Configuration

- **Native binary memory:** `-Xms512m -Xmx512m`
- **Load test:** wrk2, 2 threads, 100 connections, 2 min warmup + 30 sec measurement window
- **Endpoint:** `GET /fruits` (reads all fruits with store/address joins from PostgreSQL)

---

## ⚠️ Important Caveat: Different JDK Versions

This is **not a pure toolchain comparison**. The two native image tools embed different JDK versions in the produced binary:

| Tool | Version | Embedded JDK |
|---|---|---|
| GraalVM CE | 25.0.2 | JDK 25 |
| Mandrel | 24.1.2.0-Final | JDK 23 |

Mandrel's latest release at the time of this run was 24.1.2, which is based on JDK 23. A Mandrel release tracking JDK 25 would be required for a fully equivalent comparison. Performance differences observed here may be partially attributable to JDK 23 vs JDK 25 runtime differences rather than toolchain differences alone.

---

## Runtimes Tested

| Runtime | Description |
|---|---|
| `quarkus3-native` | Quarkus 3.34.5, GraalVM CE 25.0.2 native image (JDK 25, x86-64-v3, Serial GC) |
| `quarkus3-native-mandrel` | Quarkus 3.34.5, Mandrel 24.1.2 native image (JDK 23, x86-64-v3, Serial GC) |

---

## Native Image Statistics

| Metric | GraalVM CE 25.0.2 | Mandrel 24.1.2 |
|---|---:|---:|
| Total image size | 121.82 MB | 122.78 MB |
| Code area | 52.61 MB (43.19%) | 52.17 MB (42.49%) |
| Compilation units | 93,039 | 96,672 |
| Image heap | 60.82 MB (49.92%) | 62.31 MB (50.75%) |
| Objects in heap | 657,963 | ~726,800 |
| Reachable types | 27,587 | 27,734 |
| Reachable fields | 37,248 | 38,504 |
| Reachable methods | 135,481 | 141,116 |
| Reflection types | 9,051 | 8,939 |
| Reflection fields | 1,816 | 229 ⁴ |
| Reflection methods | 17,176 | 2,299 ⁴ |
| Peak build RSS | 4.95 GB | 4.62 GB |

⁴ Mandrel's significantly lower reflection field/method counts vs GraalVM CE suggest a different metadata processing path between toolchain versions, likely due to deprecation handling differences in GraalVM 25 vs Mandrel 24 regarding `DynamicProxyConfigurationResources`.

---

## Raw Measurements

### Build Time (seconds)

| Runtime | Iter 0 | Iter 1 | Iter 2 | Average |
|---|---:|---:|---:|---:|
| quarkus3-native | 152.68 | 154.55 | 154.55 | **153.93** |
| quarkus3-native-mandrel | 155.77 | 154.69 | 154.84 | **155.10** |

### Time to First Request (milliseconds)

| Runtime | Iter 0 | Iter 1 | Iter 2 | Average |
|---|---:|---:|---:|---:|
| quarkus3-native | 117.47 | 89.87 ⁵ | 119.84 | **109.06** |
| quarkus3-native-mandrel | 172.05 | 163.15 | 144.24 | **159.82** |

⁵ quarkus3-native Iter 1 (89.87 ms) is an outlier — likely a warm OS cache effect. Iters 0 and 2 are 117–120 ms.

### RSS at Startup — before any request (MiB)

| Runtime | Iter 0 | Iter 1 | Iter 2 | Average |
|---|---:|---:|---:|---:|
| quarkus3-native | 89.79 | 89.75 | 89.78 | **89.77** |
| quarkus3-native-mandrel | 115.98 | 116.00 | 115.96 | **115.98** |

### RSS after First Request (MiB)

| Runtime | Iter 0 | Iter 1 | Iter 2 | Average |
|---|---:|---:|---:|---:|
| quarkus3-native | 95.82 | 95.76 | 95.81 | **95.80** |
| quarkus3-native-mandrel | 122.20 | 122.22 | 122.18 | **122.20** |

### RSS under Load (MiB)

| Runtime | Iter 0 | Iter 1 | Iter 2 | Average |
|---|---:|---:|---:|---:|
| quarkus3-native | 295.57 | 286.04 | 287.31 | **289.64** |
| quarkus3-native-mandrel | 270.16 | 293.05 | 300.32 | **287.84** |

### Throughput (req/sec)

| Runtime | Iter 0 | Iter 1 | Iter 2 | Average |
|---|---:|---:|---:|---:|
| quarkus3-native | 8,367 | 8,401 | 8,298 | **8,356** |
| quarkus3-native-mandrel | 7,789 | 7,735 | 7,739 | **7,754** |

### Throughput Density (req/sec per MiB of RSS under load)

| Runtime | Iter 0 | Iter 1 | Iter 2 | Max |
|---|---:|---:|---:|---:|
| quarkus3-native | 28.31 | 29.37 | 28.88 | **29.37** |
| quarkus3-native-mandrel | 28.83 | 26.40 | 25.77 | **28.83** |

---

## Summary Comparison

| Metric | GraalVM CE 25.0.2 | Mandrel 24.1.2 | Mandrel vs GraalVM |
|---|---:|---:|---:|
| Build time (s) | 153.93 | 155.10 | +0.8% |
| Peak build RSS (GB) | 4.95 | 4.62 | −6.7% |
| Binary size (MB) | 121.82 | 122.78 | +0.8% |
| Startup / TTFR (ms) | **109.1** | 159.8 | +46.5% slower |
| RSS at startup (MiB) | **89.8** | 116.0 | +29.2% more |
| RSS after 1st req (MiB) | **95.8** | 122.2 | +27.6% more |
| RSS under load (MiB) | 289.6 | **287.8** | −0.6% |
| Throughput (tps) | **8,356** | 7,754 | −7.2% |
| Throughput density (tps/MiB) | **29.37** | 28.83 | −1.8% |

---

## Analysis

### Build Time

Both tools take virtually the same time to build: **153.9 s** (GraalVM) vs **155.1 s** (Mandrel), a difference of ~1.2 s or 0.8%. This is within normal run-to-run variation. From a CI perspective, the two toolchains are equivalent.

Mandrel requires notably less memory during the build: **4.62 GB** peak RSS vs **4.95 GB** for GraalVM CE — a 6.7% reduction. On memory-constrained build machines this could matter.

### Startup — Time to First Request

| Runtime | Avg TTFR | vs GraalVM CE |
|---|---:|---:|
| quarkus3-native (GraalVM CE) | **109.1 ms** | baseline |
| quarkus3-native-mandrel | 159.8 ms | +46.5% slower |

This is the most striking difference. Mandrel-built binaries start ~50 ms slower than GraalVM CE (159 ms vs 109 ms). However, note that:
- The GraalVM average is pulled down by an outlier (Iter 1: 89.9 ms). Excluding it, GraalVM iters 0 and 2 average ~118 ms — still ~35% faster than Mandrel.
- The JDK 23 vs JDK 25 difference could contribute; JDK 25 may have startup optimisations not yet in JDK 23.

### Memory at Idle

| Runtime | RSS idle (MiB) | vs GraalVM CE |
|---|---:|---:|
| quarkus3-native (GraalVM CE) | **89.8** | baseline |
| quarkus3-native-mandrel | 116.0 | +29.2% more |

Mandrel binaries use ~26 MiB more RSS at startup. This corresponds directly to the larger image heap (62.31 MB vs 60.82 MB) and more objects (726,800 vs 657,963). The Mandrel binary's larger reachability surface (38,504 fields vs 37,248; 141,116 methods vs 135,481) also contributes.

Memory after the first request follows the same pattern: 122.2 MiB (Mandrel) vs 95.8 MiB (GraalVM), a 27.6% difference.

### Memory under Load

| Runtime | RSS load (MiB) | vs GraalVM CE |
|---|---:|---:|
| quarkus3-native (GraalVM CE) | 289.6 | baseline |
| quarkus3-native-mandrel | **287.8** | −0.6% |

Interestingly, under load the two are essentially identical. The additional ~26 MiB of startup RSS in Mandrel is absorbed into the same working set under concurrent request handling. Database connection pools, HTTP threads, and heap pressure dominate at load, making the toolchain-level binary differences negligible.

### Throughput

| Runtime | Avg (tps) | vs GraalVM CE |
|---|---:|---:|
| quarkus3-native (GraalVM CE) | **8,356** | baseline |
| quarkus3-native-mandrel | 7,754 | −7.2% |

GraalVM CE delivers ~600 more req/sec than Mandrel. With only 3 iterations it is difficult to fully attribute this to the toolchain vs the JDK version: JDK 25 contains JIT and runtime improvements over JDK 23 that could account for part of this gap, even in native (no-JIT) mode where things like Serial GC implementation, intrinsics, and compiler-backend optimisations still differ between JDK releases.

### Throughput Density

| Runtime | Max (tps/MiB) | vs GraalVM CE |
|---|---:|---:|
| quarkus3-native (GraalVM CE) | **29.37** | baseline |
| quarkus3-native-mandrel | 28.83 | −1.8% |

Because under-load RSS is nearly identical, the density difference mirrors the throughput difference. Both are in the same range and both outperform all JVM variants (which peak around 25 tps/MiB).

---

## Key Findings

| Metric | Winner | Margin |
|---|---|---|
| Build time | Tie | <1% |
| Build memory | Mandrel | −6.7% |
| Startup speed | GraalVM CE | ~35–46% faster |
| Idle RSS | GraalVM CE | −29% |
| Under-load RSS | Tie | <1% |
| Throughput | GraalVM CE | +7.2% |
| Throughput density | GraalVM CE | +1.8% |
| Binary size | Tie | <1% |

### Conclusion

GraalVM CE 25.0.2 outperforms Mandrel 24.1.2 on every runtime metric in this run: faster startup, lower idle memory, and higher throughput. Build time and binary size are effectively identical.

**However, this comparison is not fully equivalent.** Mandrel 24.1.2 is based on JDK 23, while GraalVM CE 25.0.2 is based on JDK 25 — a two-major-version gap. A meaningful toolchain comparison would require Mandrel and GraalVM CE built on the same JDK version. A Mandrel release tracking JDK 25 should be used for a conclusive result.

---

*Benchmark run by [cdhermann](https://github.com/cdhermann) using the [spring-quarkus-perf-comparison](https://github.com/quarkusio/spring-quarkus-perf-comparison) perf-lab tooling.*
