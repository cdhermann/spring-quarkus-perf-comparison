# Benchmark Results: Quarkus 3.x vs .NET 10 — 2026-04-24 (Run 2, 9 iterations)

## Environment

| Property | Value |
|---|---|
| Date | 2026-04-24 |
| Host | Hetzner vServer CPX62 <https://www.hetzner.com/cloud/regular-performance/> |
| OS | Ubuntu 24.04.3 LTS (kernel 6.8.0-110-generic) |
| CPU | AMD EPYC-Genoa, 16 vCPUs |
| Memory | 30 GiB |
| Java (JVM runtimes) | OpenJDK 25.0.2 (Temurin) |
| GraalVM (native) | GraalVM CE 25.0.2+10.1 |
| .NET | 10.0.107 |
| Quarkus | 3.34.5 |
| Repo branch | `main` |
| Repo commit | `3267435` |
| Iterations | 9 per runtime |
| Duration | ~6 h 43 m |

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

- **JVM runtimes:** `-Xms512m -Xmx512m`, `-XX:ActiveProcessorCount=4`
- **dotnet10:** `DOTNET_GCHeapHardLimit=0x20000000` (512 MiB), `DOTNET_ProcessorCount=4`, `DOTNET_gcServer=1`
- **Load test:** wrk2, 2 threads, 100 connections, 2 min warmup + 30 sec measurement window
- **Endpoint:** `GET /fruits` (reads all fruits with store/address joins from PostgreSQL)

---

## Runtimes Tested

| Runtime | Description |
|---|---|
| `quarkus3-jvm` | Quarkus 3.34.5, standard threads, JVM |
| `quarkus3-leyden` | Quarkus 3.34.5, standard threads, JVM + Project Leyden AOT cache |
| `quarkus3-virtual` | Quarkus 3.34.5, virtual threads, JVM |
| `quarkus3-virtual-leyden` | Quarkus 3.34.5, virtual threads, JVM + Project Leyden AOT cache |
| `quarkus3-native` | Quarkus 3.34.5, GraalVM native image (x86-64-v3, Serial GC) |
| `dotnet10` | ASP.NET Core 10.0.107, server GC, 512 MiB heap limit |

---

## Raw Measurements

### Build Time (seconds)

| Runtime | I0 | I1 | I2 | I3 | I4 | I5 | I6 | I7 | I8 | Average |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| quarkus3-jvm | 8.36 | 7.87 | 8.17 | 8.00 | 7.97 | 7.93 | 8.16 | 8.01 | 7.82 | **8.03** |
| quarkus3-leyden | 53.71 | 52.32 | 51.45 | 67.35 ¹ | 51.86 | 51.91 | 51.94 | 52.13 | 51.93 | **53.84** |
| quarkus3-virtual | 8.13 | 8.10 | 8.10 | 7.96 | 8.17 | 8.32 | 8.17 | 8.15 | 8.10 | **8.13** |
| quarkus3-virtual-leyden | 52.70 | 52.08 | 52.25 | 50.95 | 52.69 | 52.72 | 52.61 | 52.40 | 52.76 | **52.35** |
| quarkus3-native | 153.87 | 152.21 | 155.10 | 152.75 | 151.91 | 153.81 | 152.88 | 156.49 | 154.54 | **153.73** |
| dotnet10 | 8.01 | 1.74 | 1.64 | 1.72 | 1.70 | 1.78 | 1.71 | 1.72 | 1.73 | **2.42** ² |

¹ quarkus3-leyden I3 (67.35 s) is a scheduling outlier — all other iterations are 51–54 s.  
² dotnet10 I0 is a full publish (8.01 s); I1–I8 are incremental cached rebuilds (~1.7 s). The representative cold-build time is **8.01 s**.

### Time to First Request (milliseconds)

| Runtime | I0 | I1 | I2 | I3 | I4 | I5 | I6 | I7 | I8 | Average |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| quarkus3-jvm | 2543.74 | 2750.22 | 2603.69 | 2596.34 | 2576.27 | 2553.46 | 2534.01 | 2527.34 | 2659.07 | **2593.79** |
| quarkus3-leyden | 982.06 | 992.81 | 1005.33 | 1016.08 | 989.48 | 946.91 | 966.23 | 965.08 | 939.22 | **978.14** |
| quarkus3-virtual | 2574.57 | 2547.57 | 2612.40 | 2529.06 | 2653.00 | 2565.81 | 2536.24 | 2618.50 | 2588.87 | **2580.67** |
| quarkus3-virtual-leyden | 855.62 | 894.36 | 871.97 | 905.11 | 903.61 | 912.65 | 901.07 | 909.60 | 863.43 | **890.83** |
| quarkus3-native | 119.23 | 117.83 | 121.08 | 85.09 ³ | 121.01 | 119.77 | 112.49 | 118.99 | 124.21 | **115.52** |
| dotnet10 | 1770.77 | 1740.16 | 1793.62 | 1618.46 | 1694.99 | 1732.54 | 1678.62 | 1695.04 | 1704.72 | **1714.33** |

³ quarkus3-native I3 (85.09 ms) is an outlier — all other iterations are 112–124 ms.

### RSS at Startup — before any request (MiB)

| Runtime | I0 | I1 | I2 | I3 | I4 | I5 | I6 | I7 | I8 | Average |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| quarkus3-jvm | 275.12 | 280.83 | 275.09 | 269.72 | 270.17 | 270.21 | 276.31 | 271.38 | 276.33 | **273.91** |
| quarkus3-leyden | 239.99 | 219.53 | 248.22 | 230.64 | 219.38 | 227.47 | 229.64 | 232.19 | 245.86 | **232.55** |
| quarkus3-virtual | 274.41 | 275.29 | 273.22 | 273.82 | 276.18 | 277.70 | 274.59 | 277.93 | 274.77 | **275.32** |
| quarkus3-virtual-leyden | 236.91 | 234.38 | 233.70 | 238.79 | 236.98 | 233.23 | 238.65 | 234.77 | 234.86 | **235.81** |
| quarkus3-native | 89.31 | 89.31 | 89.33 | 89.30 | 89.32 | 89.30 | 89.29 | 89.29 | 89.31 | **89.31** |
| dotnet10 | 68.94 | 69.11 | 69.00 | 69.07 | 68.88 | 69.19 | 68.86 | 68.93 | 68.66 | **68.96** |

### RSS after First Request (MiB)

| Runtime | I0 | I1 | I2 | I3 | I4 | I5 | I6 | I7 | I8 | Average |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| quarkus3-jvm | 292.84 | 297.93 | 292.94 | 287.02 | 287.91 | 285.56 | 291.61 | 288.45 | 294.26 | **290.95** |
| quarkus3-leyden | 248.25 | 246.24 | 256.25 | 246.92 | 244.26 | 242.63 | 243.88 | 242.21 | 254.78 | **247.27** |
| quarkus3-virtual | 293.21 | 293.65 | 295.88 | 294.27 | 306.68 | 296.66 | 295.92 | 297.40 | 304.09 | **297.53** |
| quarkus3-virtual-leyden | 249.65 | 245.57 | 244.00 | 244.76 | 249.35 | 247.74 | 246.31 | 247.45 | 245.85 | **246.74** |
| quarkus3-native | 95.32 | 95.32 | 95.34 | 95.32 | 95.32 | 95.32 | 95.32 | 95.32 | 95.33 | **95.32** |
| dotnet10 | 128.64 | 128.85 | 128.72 | 128.83 | 128.59 | 128.79 | 128.62 | 128.65 | 128.22 | **128.65** |

### RSS under Load (MiB)

| Runtime | I0 | I1 | I2 | I3 | I4 | I5 | I6 | I7 | I8 | Average |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| quarkus3-jvm | 780.90 | 763.42 | 746.83 | 779.34 | 760.59 | 765.95 | 757.56 | 750.45 | 775.74 | **764.53** |
| quarkus3-leyden | 720.62 | 727.75 | 731.75 | 700.90 | 725.78 | 703.71 | 705.66 | 717.45 | 743.40 | **719.67** |
| quarkus3-virtual | 714.03 | 708.81 | 690.36 | 706.57 | 695.24 | 707.22 | 710.26 | 708.58 | 683.60 | **702.74** |
| quarkus3-virtual-leyden | 679.20 | 653.30 | 659.79 | 669.99 | 647.72 | 663.78 | 643.28 | 670.87 | 672.54 | **662.27** |
| quarkus3-native | 289.00 | 285.25 | 295.55 | 289.14 | 285.94 | 289.28 | 293.17 | 293.32 | 292.13 | **290.31** |
| dotnet10 | 225.30 | 219.65 | 220.06 | 215.84 | 221.17 | 219.40 | 202.68 | 223.06 | 218.26 | **218.38** |

### Throughput (req/sec)

| Runtime | I0 | I1 | I2 | I3 | I4 | I5 | I6 | I7 | I8 | Average |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| quarkus3-jvm | 18,252 | 18,477 | 18,057 | 18,012 | 18,142 | 17,764 | 18,218 | 17,581 | 18,070 | **18,064** |
| quarkus3-leyden | 16,741 | 16,130 | 16,601 | 16,722 | 16,198 | 16,338 | 16,510 | 16,549 | 16,755 | **16,505** |
| quarkus3-virtual | 17,062 | 17,322 | 16,869 | 16,727 | 17,079 | 16,463 | 16,505 | 16,591 | 17,065 | **16,854** |
| quarkus3-virtual-leyden | 15,474 | 15,950 | 15,838 | 15,992 | 15,407 | 15,768 | 15,733 | 15,147 | 16,056 | **15,707** |
| quarkus3-native | 8,535 | 8,585 | 8,613 | 8,887 | 8,669 | 8,552 | 8,578 | 8,605 | 8,714 | **8,637** |
| dotnet10 | 6,632 | 6,483 | 6,694 | 6,568 | 6,725 | 6,473 | 6,482 | 6,407 | 6,521 | **6,554** |

### Throughput Density (req/sec per MiB of RSS under load)

| Runtime | I0 | I1 | I2 | I3 | I4 | I5 | I6 | I7 | I8 | Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| quarkus3-jvm | 23.37 | 24.20 | 24.18 | 23.11 | 23.85 | 23.19 | 24.05 | 23.43 | 23.30 | **24.20** |
| quarkus3-leyden | 23.23 | 22.17 | 22.69 | 23.86 | 22.32 | 23.22 | 23.40 | 23.07 | 22.54 | **23.86** |
| quarkus3-virtual | 23.90 | 24.44 | 24.44 | 23.67 | 24.57 | 23.28 | 23.24 | 23.42 | 24.96 | **24.96** |
| quarkus3-virtual-leyden | 22.78 | 24.41 | 24.00 | 23.87 | 23.79 | 23.76 | 24.46 | 22.58 | 23.87 | **24.46** |
| quarkus3-native | 29.53 | 30.10 | 29.14 | 30.74 | 30.32 | 29.56 | 29.26 | 29.34 | 29.83 | **30.74** |
| dotnet10 | 29.44 | 29.51 | 30.42 | 30.43 | 30.40 | 29.50 | 31.98 | 28.72 | 29.88 | **31.98** |

---

## Summary Comparison

| Runtime | Build (s) | Startup (ms) | RSS idle (MiB) | RSS load (MiB) | Throughput (tps) | Density (tps/MiB) |
|---|---:|---:|---:|---:|---:|---:|
| quarkus3-jvm | 8.0 | 2,594 | 274 | 765 | **18,064** | 24.2 |
| quarkus3-leyden | 53.8 | 978 | 233 | 720 | 16,505 | 23.9 |
| quarkus3-virtual | 8.1 | 2,581 | 275 | 703 | 16,854 | 25.0 |
| quarkus3-virtual-leyden | 52.4 | 891 | 236 | 662 | 15,707 | 24.5 |
| quarkus3-native | 153.7 | **116** | 89 | 290 | 8,637 | 30.7 |
| dotnet10 | **8.0** | 1,714 | **69** | **218** | 6,554 | **32.0** |

---

## Analysis

### Build Time

| Runtime | Build (s) | vs quarkus3-jvm | Notes |
|---|---:|---:|---|
| quarkus3-jvm | 8.0 | baseline | Standard Maven build |
| dotnet10 | **8.0** | ~same | Cold publish; I1–I8 are ~1.7 s incremental rebuilds |
| quarkus3-virtual | 8.1 | ~same | Standard Maven build |
| quarkus3-virtual-leyden | 52.4 | 6.5× slower | Includes AOT cache generation |
| quarkus3-leyden | 53.8 | 6.7× slower | Same; I3 outlier at 67 s excluded from practical estimate |
| quarkus3-native | **153.7** | 19.1× slower | ~2m 34s GraalVM native-image, ~5 GB peak build RSS |

In this run dotnet10's cold publish time (8.01 s) is virtually identical to a JVM Quarkus build. The Leyden AOT cache adds ~44 s to the build. Native Quarkus remains the most expensive at ~154 s.

### Startup Speed

| Runtime | Avg (ms) | vs quarkus3-jvm |
|---|---:|---:|
| quarkus3-native | **116** | 22.4× faster |
| quarkus3-virtual-leyden | 891 | 2.9× faster |
| quarkus3-leyden | 978 | 2.7× faster |
| dotnet10 | 1,714 | 1.5× faster |
| quarkus3-virtual | 2,581 | ~same |
| quarkus3-jvm | 2,594 | baseline |

The startup ranking is identical to Run 1. Native Quarkus starts in ~116 ms; the two Leyden variants are under 1 second; dotnet10 is 1.7 s; plain JVM Quarkus variants are ~2.6 s. Virtual threads offer no startup benefit.

### Memory at Idle

| Runtime | Avg (MiB) | vs quarkus3-jvm |
|---|---:|---:|
| dotnet10 | **69** | 4.0× less |
| quarkus3-native | 89 | 3.1× less |
| quarkus3-leyden | 233 | 1.2× less |
| quarkus3-virtual-leyden | 236 | 1.2× less |
| quarkus3-jvm | 274 | baseline |
| quarkus3-virtual | 275 | ~same |

dotnet10 and native Quarkus remain the clear winners for idle memory. Leyden variants save ~15% vs their non-Leyden counterparts.

### Memory under Load

| Runtime | Avg (MiB) | vs quarkus3-jvm |
|---|---:|---:|
| dotnet10 | **218** | 3.5× less |
| quarkus3-native | 290 | 2.6× less |
| quarkus3-virtual-leyden | 662 | 1.2× less |
| quarkus3-virtual | 703 | 1.1× less |
| quarkus3-leyden | 720 | 1.1× less |
| quarkus3-jvm | 765 | baseline |

dotnet10's under-load RSS dropped to **218 MiB** in this run (vs 231 MiB in Run 1), widening its lead over native Quarkus (290 MiB). The `DOTNET_GCHeapHardLimit` of 512 MiB is clearly not a bottleneck at this load level.

### Throughput

| Runtime | Avg (req/sec) | vs dotnet10 |
|---|---:|---:|
| quarkus3-jvm | **18,064** | +176% |
| quarkus3-virtual | 16,854 | +157% |
| quarkus3-leyden | 16,505 | +152% |
| quarkus3-virtual-leyden | 15,707 | +140% |
| quarkus3-native | 8,637 | +32% |
| dotnet10 | 6,554 | baseline |

Throughput results are highly consistent with Run 1. The JVM's JIT advantage is unchanged: plain JVM Quarkus delivers ~2.75× the throughput of dotnet10 and even native Quarkus beats it by a third.

### Throughput Density (throughput per MiB of RAM)

| Runtime | Max (tps/MiB) | vs quarkus3-jvm |
|---|---:|---:|
| dotnet10 | **32.0** | +32% |
| quarkus3-native | 30.7 | +27% |
| quarkus3-virtual | 25.0 | +3% |
| quarkus3-virtual-leyden | 24.5 | +1% |
| quarkus3-jvm | 24.2 | baseline |
| quarkus3-leyden | 23.9 | −1% |

A notable result: in this run dotnet10 achieves the **highest throughput density of all runtimes** (32.0 tps/MiB), marginally ahead of native Quarkus (30.7 tps/MiB). This is driven by its lower under-load RSS (218 MiB vs 290 MiB). If memory is the primary constraint — e.g. when running many instances on a fixed-size host — dotnet10 is the strongest choice.

---

## Key Trade-offs

| Goal | Best choice |
|---|---|
| Lowest startup latency | `quarkus3-native` (116 ms) |
| Fastest startup without native build | `quarkus3-virtual-leyden` (891 ms) |
| Highest raw throughput | `quarkus3-jvm` (18,064 tps) |
| Lowest memory footprint (idle) | `dotnet10` (69 MiB) |
| Lowest memory footprint (under load) | `dotnet10` (218 MiB) |
| Best throughput per MiB of RAM | `dotnet10` (32.0 tps/MiB) |
| Fastest build | tie: `quarkus3-jvm` / `dotnet10` (~8 s cold) |
| Balanced startup + throughput (JVM) | `quarkus3-jvm` or `quarkus3-virtual` |
| Balanced startup + memory (JVM) | `quarkus3-virtual-leyden` |

### dotnet10 in Context

dotnet10's position strengthened in this run: its under-load RSS of 218 MiB (vs 231 MiB in Run 1) pushed its throughput density to 32.0 tps/MiB — the highest of any runtime, just ahead of native Quarkus. Raw throughput remains its main weakness, at roughly one-third of JVM Quarkus. For memory-constrained or cost-sensitive deployments where packing density matters more than per-instance peak throughput, dotnet10 and native Quarkus are the two strongest options.

---

## Comparison with Run 1 (3 iterations)

| Metric | Run 1 (3 iter) | Run 2 (9 iter) | Delta |
|---|---:|---:|---:|
| **quarkus3-jvm throughput** | 18,124 tps | 18,064 tps | −0.3% |
| **quarkus3-native TTFR** | 116.0 ms | 115.5 ms | −0.4% |
| **quarkus3-native throughput** | 8,748 tps | 8,637 tps | −1.3% |
| **dotnet10 TTFR** | 1,683 ms | 1,714 ms | +1.9% |
| **dotnet10 throughput** | 6,555 tps | 6,554 tps | ~0% |
| **dotnet10 RSS under load** | 231 MiB | 218 MiB | −5.6% |
| **dotnet10 density** | 28.6 tps/MiB | 32.0 tps/MiB | +11.9% |

Results are highly reproducible across all runtimes. The main difference is dotnet10's lower under-load RSS in Run 2, which boosted its throughput density to first place. This is likely due to natural GC heap variation rather than a systematic change.

---

*Benchmark run by [cdhermann](https://github.com/cdhermann) using the [spring-quarkus-perf-comparison](https://github.com/quarkusio/spring-quarkus-perf-comparison) perf-lab tooling.*
