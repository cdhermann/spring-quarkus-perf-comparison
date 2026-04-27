# Benchmark Results: Quarkus 3.x vs .NET 10

## Environment

| Property            | Value                                                                      |
| ------------------- | -------------------------------------------------------------------------- |
| Date                | 2026-04-24                                                                 |
| Host                | Hetzner vServer CPX62 <https://www.hetzner.com/cloud/regular-performance/> |
| OS                  | Ubuntu 24.04.3 LTS (kernel 6.8.0-106-generic)                              |
| CPU                 | AMD EPYC-Genoa, 16 vCPUs                                                   |
| Memory              | 30 GiB                                                                     |
| Java (JVM runtimes) | OpenJDK 25.0.2 (Temurin)                                                   |
| GraalVM (native)    | GraalVM CE 25.0.2+10.1                                                     |
| .NET                | 10.0.107                                                                   |
| Quarkus             | 3.34.5                                                                     |
| Repo branch         | `main`                                                                     |
| Repo commit         | `6709abd`                                                                  |
| Iterations          | 3 per runtime                                                              |

### CPU Pinning

| Role                      | CPUs          |
| ------------------------- | ------------- |
| Application               | 0–3 (4 cores) |
| PostgreSQL                | 4–6           |
| OpenTelemetry stack       | 7–9           |
| Load generator (wrk2)     | 10–12         |
| First-request measurement | 10            |
| Monitoring (pidstat)      | 13            |

### Runtime Configuration

- **JVM runtimes:** `-Xms512m -Xmx512m`, `-XX:ActiveProcessorCount=4`
- **dotnet10:** `DOTNET_GCHeapHardLimit=0x20000000` (512 MiB), `DOTNET_ProcessorCount=4`, `DOTNET_gcServer=1`
- **Load test:** wrk2, 2 threads, 100 connections, 2 min warmup + 30 sec measurement window
- **Endpoint:** `GET /fruits` (reads all fruits with store/address joins from PostgreSQL)

---

## Runtimes Tested

| Runtime                   | Description                                                      |
| ------------------------- | ---------------------------------------------------------------- |
| `quarkus3-jvm`            | Quarkus 3.34.5, standard threads, JVM                            |
| `quarkus3-leyden`         | Quarkus 3.34.5, standard threads, JVM + Project Leyden AOT cache |
| `quarkus3-virtual`        | Quarkus 3.34.5, virtual threads, JVM                             |
| `quarkus3-virtual-leyden` | Quarkus 3.34.5, virtual threads, JVM + Project Leyden AOT cache  |
| `quarkus3-native`         | Quarkus 3.34.5, GraalVM native image (x86-64-v3, Serial GC)      |
| `dotnet10`                | ASP.NET Core 10.0.107, server GC, 512 MiB heap limit             |

---

## Raw Measurements

### Build Time (seconds)

| Runtime                 | Iter 0 | Iter 1 | Iter 2 |    Average |
| ----------------------- | -----: | -----: | -----: | ---------: |
| quarkus3-jvm            |   8.33 |   8.10 |   8.12 |   **8.18** |
| quarkus3-leyden         |  52.25 |  52.30 |  52.41 |  **52.32** |
| quarkus3-virtual        |   8.06 |   8.28 |   7.96 |   **8.10** |
| quarkus3-virtual-leyden |  52.03 |  52.54 |  52.54 |  **52.37** |
| quarkus3-native         | 153.16 | 154.59 | 153.85 | **153.87** |
| dotnet10                |   7.27 |   1.70 |   1.77 | **3.58** ¹ |

¹ dotnet10 iter 0 is a full publish (7.27 s); iters 1–2 are incremental rebuilds
of the same binary (~1.7 s). The representative cold-build time is **7.27 s**.

### Time to First Request (milliseconds)

| Runtime                 |  Iter 0 |  Iter 1 |  Iter 2 |     Average |
| ----------------------- | ------: | ------: | ------: | ----------: |
| quarkus3-jvm            | 2603.70 | 2660.54 | 2512.36 | **2592.20** |
| quarkus3-leyden         |  997.73 |  962.98 |  954.71 |  **971.81** |
| quarkus3-virtual        | 2616.92 | 2712.10 | 2637.00 | **2655.34** |
| quarkus3-virtual-leyden |  875.32 |  892.21 |  875.09 |  **880.87** |
| quarkus3-native         |  118.92 |  115.28 |  113.84 |  **116.01** |
| dotnet10                | 1597.72 | 1695.90 | 1755.33 | **1682.98** |

### RSS at Startup — before any request (MiB)

| Runtime                 | Iter 0 | Iter 1 | Iter 2 |    Average |
| ----------------------- | -----: | -----: | -----: | ---------: |
| quarkus3-jvm            | 274.28 | 276.98 | 275.75 | **275.67** |
| quarkus3-leyden         | 242.44 | 241.61 | 240.84 | **241.63** |
| quarkus3-virtual        | 278.03 | 274.93 | 276.54 | **276.50** |
| quarkus3-virtual-leyden | 236.77 | 216.49 | 235.18 | **229.48** |
| quarkus3-native         |  89.35 |  89.37 |  89.35 |  **89.36** |
| dotnet10                |  69.08 |  69.40 |  69.39 |  **69.29** |

### RSS after First Request (MiB)

| Runtime                 | Iter 0 | Iter 1 | Iter 2 |    Average |
| ----------------------- | -----: | -----: | -----: | ---------: |
| quarkus3-jvm            | 289.60 | 292.57 | 291.11 | **291.09** |
| quarkus3-leyden         | 260.90 | 250.41 | 249.32 | **253.54** |
| quarkus3-virtual        | 308.43 | 305.38 | 304.48 | **306.10** |
| quarkus3-virtual-leyden | 250.21 | 228.79 | 249.31 | **242.77** |
| quarkus3-native         |  95.33 |  95.34 |  95.32 |  **95.33** |
| dotnet10                | 128.99 | 129.36 | 129.32 | **129.22** |

### RSS under Load (MiB)

| Runtime                 | Iter 0 | Iter 1 | Iter 2 |    Average |
| ----------------------- | -----: | -----: | -----: | ---------: |
| quarkus3-jvm            | 756.30 | 781.03 | 774.43 | **770.59** |
| quarkus3-leyden         | 722.68 | 728.04 | 716.82 | **722.51** |
| quarkus3-virtual        | 701.56 | 705.19 | 699.70 | **702.15** |
| quarkus3-virtual-leyden | 643.32 | 649.51 | 650.10 | **647.64** |
| quarkus3-native         | 285.57 | 295.59 | 292.03 | **291.06** |
| dotnet10                | 237.88 | 231.13 | 224.36 | **231.13** |

### Throughput (req/sec)

| Runtime                 |    Iter 0 |    Iter 1 |    Iter 2 |       Average |
| ----------------------- | --------: | --------: | --------: | ------------: |
| quarkus3-jvm            | 18,149.45 | 17,794.56 | 18,427.60 | **18,123.87** |
| quarkus3-leyden         | 16,085.51 | 16,620.18 | 16,419.21 | **16,374.97** |
| quarkus3-virtual        | 17,265.29 | 16,893.69 | 17,013.52 | **17,057.50** |
| quarkus3-virtual-leyden | 15,734.07 | 15,028.13 | 15,946.95 | **15,569.72** |
| quarkus3-native         |  8,697.93 |  8,780.91 |  8,766.07 |  **8,748.30** |
| dotnet10                |  6,646.00 |  6,617.42 |  6,400.74 |  **6,554.72** |

### Throughput Density (req/sec per MiB of RSS under load)

| Runtime                 | Iter 0 | Iter 1 | Iter 2 |       Max |
| ----------------------- | -----: | -----: | -----: | --------: |
| quarkus3-jvm            |  24.00 |  22.78 |  23.79 | **24.00** |
| quarkus3-leyden         |  22.26 |  22.83 |  22.91 | **22.91** |
| quarkus3-virtual        |  24.61 |  23.96 |  24.32 | **24.61** |
| quarkus3-virtual-leyden |  24.46 |  23.14 |  24.53 | **24.53** |
| quarkus3-native         |  30.46 |  29.71 |  30.02 | **30.46** |
| dotnet10                |  27.94 |  28.63 |  28.53 | **28.63** |

---

## Summary Comparison

| Runtime                 | Build (s) | Startup (ms) | RSS idle (MiB) | RSS load (MiB) | Throughput (tps) | Density (tps/MiB) |
| ----------------------- | --------: | -----------: | -------------: | -------------: | ---------------: | ----------------: |
| quarkus3-jvm            |       8.2 |        2,592 |            276 |            771 |       **18,124** |              24.0 |
| quarkus3-leyden         |      52.3 |          972 |            242 |            723 |           16,375 |              22.9 |
| quarkus3-virtual        |       8.1 |        2,655 |            277 |            702 |           17,058 |              24.6 |
| quarkus3-virtual-leyden |      52.4 |          881 |            229 |            648 |           15,570 |              24.5 |
| quarkus3-native         |     153.9 |      **116** |             89 |            291 |            8,748 |          **30.5** |
| dotnet10                |   **7.3** |        1,683 |         **69** |        **231** |            6,555 |              28.6 |

---

## Analysis

### Build Time

| Runtime                 | Build (s) | vs quarkus3-jvm | Notes                                                         |
| ----------------------- | --------: | --------------: | ------------------------------------------------------------- |
| dotnet10                |   **7.3** |     1.1× faster | Cold publish; iters 1–2 are ~1.7 s (incremental, same binary) |
| quarkus3-virtual        |       8.1 |           ~same | Standard Maven build                                          |
| quarkus3-jvm            |       8.2 |        baseline | Standard Maven build                                          |
| quarkus3-leyden         |      52.3 |     6.4× slower | Includes AOT cache generation                                 |
| quarkus3-virtual-leyden |      52.4 |     6.4× slower | Same                                                          |
| quarkus3-native         | **153.9** |    18.8× slower | ~2m 34s GraalVM native-image, 5 GB peak build RSS             |

dotnet10 builds fastest at **7.3 s** (cold publish). JVM Quarkus variants build
in ~8 s. Leyden variants take ~52 s due to the additional AOT cache training
run. Native Quarkus is the most expensive at **154 s** (~2.5 min) with a peak
build-time RSS of 5 GB — a meaningful infrastructure cost in CI.

### Startup Speed

| Runtime                 | Avg (ms) | vs quarkus3-jvm |
| ----------------------- | -------: | --------------: |
| quarkus3-native         |  **116** |      22× faster |
| quarkus3-virtual-leyden |      881 |     2.9× faster |
| quarkus3-leyden         |      972 |     2.7× faster |
| dotnet10                |    1,683 |     1.5× faster |
| quarkus3-jvm            |    2,592 |        baseline |
| quarkus3-virtual        |    2,655 |           ~same |

Native Quarkus is in a league of its own at **116 ms**, roughly 22× faster than
JVM Quarkus. The Leyden AOT cache variants bring JVM startup down to under 1
second — **881 ms** for virtual-leyden and **972 ms** for standard-leyden —
making them competitive with dotnet10's **1,683 ms**. Plain JVM Quarkus
(standard and virtual threads) sits at ~2,600 ms. Virtual threads add no startup
benefit. dotnet10 starts faster than plain JVM Quarkus but slower than either
Leyden variant.

### Memory at Idle

| Runtime                 | Avg (MiB) | vs quarkus3-jvm |
| ----------------------- | --------: | --------------: |
| dotnet10                |    **69** |       4.0× less |
| quarkus3-native         |        89 |       3.1× less |
| quarkus3-virtual-leyden |       229 |       1.2× less |
| quarkus3-leyden         |       242 |       1.1× less |
| quarkus3-jvm            |       276 |        baseline |
| quarkus3-virtual        |       277 |           ~same |

dotnet10 has the smallest idle footprint at **69 MiB** — 20 MiB less than native
Quarkus. All JVM variants sit in the 230–277 MiB range, with Leyden variants
consistently lower (229–242 MiB) than their non-Leyden counterparts (276–277
MiB) — the AOT cache appears to reduce class metadata overhead at startup.

### Memory under Load

| Runtime                 | Avg (MiB) | vs quarkus3-jvm |
| ----------------------- | --------: | --------------: |
| dotnet10                |   **231** |       3.3× less |
| quarkus3-native         |       291 |       2.6× less |
| quarkus3-virtual-leyden |       648 |       1.2× less |
| quarkus3-virtual        |       702 |       1.1× less |
| quarkus3-leyden         |       723 |       1.1× less |
| quarkus3-jvm            |       771 |        baseline |

The ordering is preserved under load. dotnet10 uses only **231 MiB** under 100
concurrent connections — less than native Quarkus (**291 MiB**) and dramatically
less than any JVM variant (648–771 MiB). The `DOTNET_GCHeapHardLimit` of 512 MiB
is clearly not the bottleneck at this load level. The JVM's higher load-time RSS
reflects its larger heap, JIT compiler data structures, and thread stacks.
Virtual threads reduce JVM load-RSS modestly (702 MiB vs 771 MiB for standard
threads), and Leyden reduces it further (648 MiB for virtual-leyden).

### Throughput

| Runtime                 | Avg (req/sec) | vs dotnet10 |
| ----------------------- | ------------: | ----------: |
| quarkus3-jvm            |    **18,124** |       +176% |
| quarkus3-virtual        |        17,058 |       +160% |
| quarkus3-leyden         |        16,375 |       +150% |
| quarkus3-virtual-leyden |        15,570 |       +137% |
| quarkus3-native         |         8,748 |        +33% |
| dotnet10                |         6,555 |    baseline |

This is where the JVM's JIT compilation advantage is most visible. JVM Quarkus
peaks at **18,124 req/sec** — nearly **3× dotnet10's 6,555 req/sec**. Even
native Quarkus (no JIT after startup) delivers **8,748 req/sec**, a 33%
advantage over dotnet10. The Leyden variants trade roughly 10–14% throughput for
faster startup, which is an expected trade-off from class-sharing optimisations
influencing JIT profiling. Virtual threads underperform standard threads
slightly (~6%) on this workload, which is typical for low-latency database-bound
endpoints where platform threads are not the bottleneck.

### Throughput Density (throughput per MiB of RAM)

| Runtime                 | Max (tps/MiB) | vs quarkus3-jvm |
| ----------------------- | ------------: | --------------: |
| quarkus3-native         |      **30.5** |            +27% |
| dotnet10                |          28.6 |            +19% |
| quarkus3-virtual        |          24.6 |             +3% |
| quarkus3-virtual-leyden |          24.5 |             +2% |
| quarkus3-jvm            |          24.0 |        baseline |
| quarkus3-leyden         |          22.9 |             −5% |

Throughput density reveals dotnet10's competitive position more clearly: at
**28.6 tps/MiB** it ranks second overall, just behind native Quarkus (**30.5
tps/MiB**) and ahead of all JVM variants (22.9–24.6 tps/MiB). This means that if
memory is the limiting resource — for example when running many instances on a
single host — dotnet10 and native Quarkus are the strongest choices. JVM Quarkus
delivers more raw throughput per instance but requires proportionally more RAM
to do so.

---

## Key Trade-offs

| Goal                                 | Best choice                          |
| ------------------------------------ | ------------------------------------ |
| Lowest startup latency               | `quarkus3-native` (116 ms)           |
| Fastest startup without native build | `quarkus3-virtual-leyden` (881 ms)   |
| Highest raw throughput               | `quarkus3-jvm` (18,124 tps)          |
| Lowest memory footprint (idle)       | `dotnet10` (69 MiB)                  |
| Lowest memory footprint (under load) | `dotnet10` (231 MiB)                 |
| Best throughput per MiB of RAM       | `quarkus3-native` (30.5 tps/MiB)     |
| Fastest build                        | `dotnet10` (7.3 s)                   |
| Balanced startup + throughput (JVM)  | `quarkus3-jvm` or `quarkus3-virtual` |
| Balanced startup + memory (JVM)      | `quarkus3-virtual-leyden`            |

### dotnet10 in Context

.NET 10 occupies a distinct position: it offers the smallest memory footprint of
all runtimes tested (both at idle and under load), competitive startup speed
(faster than plain JVM Quarkus, slower than Leyden), and strong throughput
density. Its raw throughput is significantly lower than any Quarkus variant. For
memory-constrained deployments or serverless/edge scenarios where cold-start and
RAM cost matter more than peak req/sec, dotnet10 is a strong contender. For
maximum throughput on a fixed-size server, JVM Quarkus remains the clear winner.

---

*Benchmark run by [cdhermann](https://github.com/cdhermann) using the
[spring-quarkus-perf-comparison](https://github.com/quarkusio/spring-quarkus-perf-comparison)
perf-lab tooling.*
