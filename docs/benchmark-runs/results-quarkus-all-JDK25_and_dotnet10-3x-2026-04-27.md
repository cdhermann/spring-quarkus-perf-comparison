# Benchmark Results: dotnet10, quarkus3-jvm, quarkus3-leyden, quarkus3-virtual, quarkus3-virtual-leyden, quarkus3-native, quarkus3-native-mandrel — 2026-04-27

> **Branch:** `native-mandrel-with-dotnet` · **Commit:** `ca9c1cd` · **Iterations:** 3


## Environment

|Property|Value|
|---|---|
|**Date**|2026-04-27|
|**Host**|Hetzner vServer CPX62 <https://www.hetzner.com/cloud/regular-performance/>|
|**OS**|Ubuntu 24.04.3 LTS (kernel 6.8.0-110-generic)|
|**CPU**|AMD EPYC-Genoa Processor (16 cpus)|
|**Memory**|30Gi|
|**Java (JVM runtimes)**|OpenJDK 25.0.2 (Temurin)|
|**GraalVM CE (native)**|25.0.2-graalce|
|**Mandrel (native)**|25.0.0.1.r25-mandrel|
|**Quarkus**|3.34.5|
|**Repo branch**|`native-mandrel-with-dotnet`|
|**Repo commit**|`ca9c1cd`|
|**Iterations**|3|

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

- **JVM runtimes:** `-Xms512m -Xmx512m`, `-XX:ActiveProcessorCount=4`
- **dotnet10:** `DOTNET_GCHeapHardLimit=0x20000000` (512 MiB), `DOTNET_ProcessorCount=4`, `DOTNET_gcServer=1`
- **Load test:** wrk2, 2 threads, 100 connections, 2 min warmup + 30 sec measurement window
- **Endpoint:** `GET /fruits` (reads all fruits with store/address joins from PostgreSQL)

---

## Runtimes Tested

|Runtime|Description|
|---|---|
|`dotnet10`|ASP.NET Core 10, server GC, 512 MiB heap limit|
|`quarkus3-jvm`|Quarkus 3.34.5, standard threads, JVM|
|`quarkus3-leyden`|Quarkus 3.34.5, standard threads, JVM + Project Leyden AOT cache|
|`quarkus3-virtual`|Quarkus 3.34.5, virtual threads, JVM|
|`quarkus3-virtual-leyden`|Quarkus 3.34.5, virtual threads, JVM + Project Leyden AOT cache|
|`quarkus3-native`|Quarkus 3.34.5, GraalVM CE native image (x86-64-v3, Serial GC)|
|`quarkus3-native-mandrel`|Quarkus 3.34.5, Mandrel native image (x86-64-v3, Serial GC)|

---

## Native Image Statistics

|Metric|`quarkus3-native`|`quarkus3-native-mandrel`|
|---|---|---|
|**Total image size (MB)**|121.82|122.34|
|**Reachable types**|27,587|27,587|
|**Reachable fields**|37,248|37,246|
|**Reachable methods**|135,482|135,470|
|**Reflection types**|9,051|9,050|
|**Reflection fields**|1,816|1,815|
|**Reflection methods**|17,176|17,176|
|**Peak build RSS (GB)**|4.93|5.18|

---

## Raw Measurements

### Build Time (seconds)

|Runtime|I0|I1|I2|Average|Std|CV%|
|---|---|---|---|---|---|---|
|`dotnet10`|7.06|1.67|1.70|**3.48**|3.10|89.3%|
|`quarkus3-jvm`|8.04|8.17|8.01|**8.07**|0.09|1.1%|
|`quarkus3-leyden`|52.24|52.73|52.04|**52.34**|0.36|0.7%|
|`quarkus3-virtual`|8.06|8.11|8.00|**8.06**|0.06|0.7%|
|`quarkus3-virtual-leyden`|52.57|52.43|53.03|**52.68**|0.31|0.6%|
|`quarkus3-native`|152.89|152.88|155.11|**153.63**|1.28|0.8%|
|`quarkus3-native-mandrel`|151.63|149.48|149.89|**150.33**|1.14|0.8%|

### Time to First Request (milliseconds)

|Runtime|I0|I1|I2|Average|Std|CV%|
|---|---|---|---|---|---|---|
|`dotnet10`|1,697.60|1,668.92|1,691.68|**1,686.07**|15.14|0.9%|
|`quarkus3-jvm`|2,630.82|2,586.57|2,646.54|**2,621.31**|31.09|1.2%|
|`quarkus3-leyden`|944.00|1,009.37|1,027.64|**993.67**|43.97|4.4%|
|`quarkus3-virtual`|2,581.31|2,752.57|2,599.14|**2,644.34**|94.16|3.6%|
|`quarkus3-virtual-leyden`|823.72|916.97|847.02|**862.57**|48.53|5.6%|
|`quarkus3-native`|102.61|119.81|122.04|**114.82**|10.63|9.3%|
|`quarkus3-native-mandrel`|108.40|113.29|103.54|**108.41**|4.88|4.5%|

### RSS at Startup — before any request (MiB)

|Runtime|I0|I1|I2|Average|Std|CV%|
|---|---|---|---|---|---|---|
|`dotnet10`|68.84|68.96|69.09|**68.97**|0.13|0.2%|
|`quarkus3-jvm`|273.62|274.23|264.22|**270.69**|5.61|2.1%|
|`quarkus3-leyden`|223.29|223.30|225.50|**224.03**|1.27|0.6%|
|`quarkus3-virtual`|276.06|273.84|277.74|**275.88**|1.96|0.7%|
|`quarkus3-virtual-leyden`|220.20|218.78|235.30|**224.76**|9.15|4.1%|
|`quarkus3-native`|89.86|89.88|89.87|**89.87**|0.01|0.0%|
|`quarkus3-native-mandrel`|89.91|89.89|89.88|**89.89**|0.01|0.0%|

### RSS after First Request (MiB)

|Runtime|I0|I1|I2|Average|Std|CV%|
|---|---|---|---|---|---|---|
|`dotnet10`|128.58|128.67|128.84|**128.70**|0.13|0.1%|
|`quarkus3-jvm`|289.95|290.68|285.35|**288.66**|2.89|1.0%|
|`quarkus3-leyden`|240.75|248.08|256.92|**248.58**|8.10|3.3%|
|`quarkus3-virtual`|300.27|302.45|294.66|**299.13**|4.02|1.3%|
|`quarkus3-virtual-leyden`|238.11|234.83|245.95|**239.63**|5.71|2.4%|
|`quarkus3-native`|95.81|95.84|95.83|**95.83**|0.02|0.0%|
|`quarkus3-native-mandrel`|95.93|95.89|95.89|**95.90**|0.02|0.0%|

### RSS under Load (MiB)

|Runtime|I0|I1|I2|Average|Std|CV%|
|---|---|---|---|---|---|---|
|`dotnet10`|225.14|200.33|234.54|**220.00**|17.68|8.0%|
|`quarkus3-jvm`|797.77|755.56|775.02|**776.11**|21.13|2.7%|
|`quarkus3-leyden`|740.20|710.46|703.91|**718.19**|19.34|2.7%|
|`quarkus3-virtual`|704.19|704.35|720.68|**709.74**|9.48|1.3%|
|`quarkus3-virtual-leyden`|634.28|627.75|655.50|**639.18**|14.51|2.3%|
|`quarkus3-native`|289.14|286.30|295.33|**290.25**|4.62|1.6%|
|`quarkus3-native-mandrel`|296.48|294.48|286.21|**292.39**|5.44|1.9%|

### Throughput (req/sec)

|Runtime|I0|I1|I2|Average|Std|CV%|
|---|---|---|---|---|---|---|
|`dotnet10`|6,549|6,525|6,638|**6,571**|60|0.9%|
|`quarkus3-jvm`|18,082|17,915|17,532|**17,843**|282|1.6%|
|`quarkus3-leyden`|16,208|16,940|17,092|**16,746**|473|2.8%|
|`quarkus3-virtual`|16,701|16,969|17,381|**17,017**|342|2.0%|
|`quarkus3-virtual-leyden`|16,237|15,864|16,056|**16,052**|186|1.2%|
|`quarkus3-native`|8,452|8,397|8,364|**8,405**|45|0.5%|
|`quarkus3-native-mandrel`|8,491|8,718|8,685|**8,631**|123|1.4%|

### Throughput Density (req/sec per MiB of RSS under load)

|Runtime|I0|I1|I2|Max|Std|CV%|
|---|---|---|---|---|---|---|
|`dotnet10`|29.09|32.57|28.30|**32.57**|2.27|7.6%|
|`quarkus3-jvm`|22.67|23.71|22.62|**23.71**|0.62|2.7%|
|`quarkus3-leyden`|21.90|23.84|24.28|**24.28**|1.27|5.4%|
|`quarkus3-virtual`|23.72|24.09|24.12|**24.12**|0.22|0.9%|
|`quarkus3-virtual-leyden`|25.60|25.27|24.49|**25.60**|0.57|2.3%|
|`quarkus3-native`|29.23|29.33|28.32|**29.33**|0.56|1.9%|
|`quarkus3-native-mandrel`|28.64|29.60|30.34|**30.34**|0.86|2.9%|

---

## Summary Comparison

|Runtime|Build (s)|Startup (ms)|RSS idle (MiB)|RSS load (MiB)|Throughput (tps)|Density (tps/MiB)|
|---|---|---|---|---|---|---|
|`dotnet10`|3.48|1686.1|69.0|220.0|**6,571**|32.57|
|`quarkus3-jvm`|8.07|2621.3|270.7|776.1|**17,843**|23.71|
|`quarkus3-leyden`|52.34|993.7|224.0|718.2|**16,746**|24.28|
|`quarkus3-virtual`|8.06|2644.3|275.9|709.7|**17,017**|24.12|
|`quarkus3-virtual-leyden`|52.68|862.6|224.8|639.2|**16,052**|25.60|
|`quarkus3-native`|153.63|114.8|89.9|290.3|**8,405**|29.33|
|`quarkus3-native-mandrel`|150.33|108.4|89.9|292.4|**8,631**|30.34|

---

## Analysis

### Build Time

|Runtime|Avg (s)|vs `quarkus3-jvm`|
|---|---|---|
|`dotnet10`|3.5|2.3× less|
|`quarkus3-virtual`|8.1|~same|
|`quarkus3-jvm`|**8.1**|baseline|
|`quarkus3-leyden`|52.3|6.5× more|
|`quarkus3-virtual-leyden`|52.7|6.5× more|
|`quarkus3-native-mandrel`|150.3|18.6× more|
|`quarkus3-native`|153.6|19.0× more|

### Startup — Time to First Request

|Runtime|Avg (ms)|vs `quarkus3-jvm`|
|---|---|---|
|`quarkus3-native-mandrel`|108|24.2× less|
|`quarkus3-native`|115|22.8× less|
|`quarkus3-virtual-leyden`|863|3.0× less|
|`quarkus3-leyden`|994|2.6× less|
|`dotnet10`|1686|1.6× less|
|`quarkus3-jvm`|**2621**|baseline|
|`quarkus3-virtual`|2644|~same|

### Memory at Idle (RSS at startup)

|Runtime|Avg (MiB)|vs `quarkus3-jvm`|
|---|---|---|
|`dotnet10`|69.0|3.9× less|
|`quarkus3-native`|89.9|3.0× less|
|`quarkus3-native-mandrel`|89.9|3.0× less|
|`quarkus3-leyden`|224.0|1.2× less|
|`quarkus3-virtual-leyden`|224.8|1.2× less|
|`quarkus3-jvm`|**270.7**|baseline|
|`quarkus3-virtual`|275.9|~same|

### Memory under Load (RSS)

|Runtime|Avg (MiB)|vs `quarkus3-jvm`|
|---|---|---|
|`dotnet10`|220.0|3.5× less|
|`quarkus3-native`|290.3|2.7× less|
|`quarkus3-native-mandrel`|292.4|2.7× less|
|`quarkus3-virtual-leyden`|639.2|1.2× less|
|`quarkus3-virtual`|709.7|1.1× less|
|`quarkus3-leyden`|718.2|1.1× less|
|`quarkus3-jvm`|**776.1**|baseline|

### Throughput

|Runtime|Avg (tps)|vs `dotnet10`|
|---|---|---|
|`quarkus3-jvm`|17,843|+172%|
|`quarkus3-virtual`|17,017|+159%|
|`quarkus3-leyden`|16,746|+155%|
|`quarkus3-virtual-leyden`|16,052|+144%|
|`quarkus3-native-mandrel`|8,631|+31%|
|`quarkus3-native`|8,405|+28%|
|`dotnet10`|**6,571**|baseline|

### Throughput Density (tps per MiB of RAM under load)

|Runtime|Avg (tps/MiB)|vs `quarkus3-jvm`|
|---|---|---|
|`dotnet10`|32.57|+37%|
|`quarkus3-native-mandrel`|30.34|+28%|
|`quarkus3-native`|29.33|+24%|
|`quarkus3-virtual-leyden`|25.60|+8%|
|`quarkus3-leyden`|24.28|+2%|
|`quarkus3-virtual`|24.12|+2%|
|`quarkus3-jvm`|**23.71**|baseline|

---

## Key Trade-offs

|Goal|Best choice|
|---|---|
|Lowest startup latency|`quarkus3-native-mandrel` (108.4)|
|Highest raw throughput|`quarkus3-jvm` (17843.3)|
|Lowest memory footprint (idle)|`dotnet10` (69.0)|
|Lowest memory footprint (load)|`dotnet10` (220.0)|
|Best throughput per MiB of RAM|`dotnet10` (32.6)|
|Fastest build|`dotnet10` (3.5)|

---

## Statistical Significance

> ⚠️ **Low sample size (n ≤ 3):** Tests have limited statistical power. Treat p-values and effect sizes as directional indicators only — run ≥ 5 iterations for reliable conclusions.

### Build Time (s)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`dotnet10`|3|3.48|3.10|89.3%|[-4.23, 11.19]|
|`quarkus3-jvm`|3|8.07|0.09|1.1%|[7.86, 8.28]|
|`quarkus3-leyden`|3|52.34|0.36|0.7%|[51.45, 53.22]|
|`quarkus3-virtual`|3|8.06|0.06|0.7%|[7.92, 8.19]|
|`quarkus3-virtual-leyden`|3|52.68|0.31|0.6%|[51.90, 53.46]|
|`quarkus3-native`|3|153.63|1.28|0.8%|[150.44, 156.82]|
|`quarkus3-native-mandrel`|3|150.33|1.14|0.8%|[147.50, 153.17]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`dotnet10` vs `quarkus3-jvm`|-2.09 (large)|0.124 (✗ not significant)|
|`dotnet10` vs `quarkus3-leyden`|-22.12 (large)|0.001 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual`|-2.09 (large)|0.125 (✗ not significant)|
|`dotnet10` vs `quarkus3-virtual-leyden`|-22.31 (large)|0.001 (✓ significant)|
|`dotnet10` vs `quarkus3-native`|-63.22 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native-mandrel`|-62.81 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-leyden`|-171.47 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|0.23 (small)|0.792 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|-193.96 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|-159.89 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|-175.76 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|174.31 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|-1.01 (large)|0.283 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-native`|-107.48 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|-115.93 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|-198.00 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|-160.11 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|-176.06 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|-107.96 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|-116.66 (large)|0.000 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|2.71 (large)|0.030 (✓ significant)|

### Startup — TTFR (ms)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`dotnet10`|3|1686.07|15.14|0.9%|[1648.45, 1723.68]|
|`quarkus3-jvm`|3|2621.31|31.09|1.2%|[2544.07, 2698.55]|
|`quarkus3-leyden`|3|993.67|43.97|4.4%|[884.43, 1102.92]|
|`quarkus3-virtual`|3|2644.34|94.16|3.6%|[2410.42, 2878.25]|
|`quarkus3-virtual-leyden`|3|862.57|48.53|5.6%|[742.00, 983.14]|
|`quarkus3-native`|3|114.82|10.63|9.3%|[88.40, 141.24]|
|`quarkus3-native-mandrel`|3|108.41|4.88|4.5%|[96.29, 120.52]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`dotnet10` vs `quarkus3-jvm`|-38.25 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-leyden`|21.05 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual`|-14.21 (large)|0.003 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual-leyden`|22.91 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native`|120.10 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native-mandrel`|140.27 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-leyden`|42.74 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|-0.33 (small)|0.720 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|43.15 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|107.88 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|112.92 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-22.46 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|2.83 (large)|0.026 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native`|27.47 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|28.30 (large)|0.001 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|23.79 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|37.75 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|38.04 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|21.28 (large)|0.001 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|21.87 (large)|0.001 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|0.77 (medium)|0.417 (✗ not significant)|

### RSS at startup (MiB)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`dotnet10`|3|68.97|0.13|0.2%|[68.65, 69.28]|
|`quarkus3-jvm`|3|270.69|5.61|2.1%|[256.75, 284.63]|
|`quarkus3-leyden`|3|224.03|1.27|0.6%|[220.86, 227.19]|
|`quarkus3-virtual`|3|275.88|1.96|0.7%|[271.02, 280.74]|
|`quarkus3-virtual-leyden`|3|224.76|9.15|4.1%|[202.02, 247.50]|
|`quarkus3-native`|3|89.87|0.01|0.0%|[89.84, 89.90]|
|`quarkus3-native-mandrel`|3|89.89|0.01|0.0%|[89.86, 89.93]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`dotnet10` vs `quarkus3-jvm`|-50.84 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-leyden`|-171.39 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual`|-149.32 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual-leyden`|-24.07 (large)|0.001 (✓ significant)|
|`dotnet10` vs `quarkus3-native`|-231.88 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native-mandrel`|-231.70 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-leyden`|11.47 (large)|0.003 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|-1.24 (large)|0.246 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|6.05 (large)|0.004 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|45.59 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|45.58 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-31.43 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|-0.11 (negligible)|0.903 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-native`|149.02 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|148.99 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|7.72 (large)|0.008 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|134.51 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|134.49 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|20.84 (large)|0.002 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|20.84 (large)|0.002 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|-1.81 (large)|0.093 (✗ not significant)|

### RSS after 1st req (MiB)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`dotnet10`|3|128.70|0.13|0.1%|[128.36, 129.03]|
|`quarkus3-jvm`|3|288.66|2.89|1.0%|[281.48, 295.84]|
|`quarkus3-leyden`|3|248.58|8.10|3.3%|[228.47, 268.69]|
|`quarkus3-virtual`|3|299.13|4.02|1.3%|[289.15, 309.10]|
|`quarkus3-virtual-leyden`|3|239.63|5.71|2.4%|[225.44, 253.83]|
|`quarkus3-native`|3|95.83|0.02|0.0%|[95.78, 95.87]|
|`quarkus3-native-mandrel`|3|95.90|0.02|0.0%|[95.84, 95.97]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`dotnet10` vs `quarkus3-jvm`|-78.21 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-leyden`|-20.94 (large)|0.002 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual`|-60.00 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual-leyden`|-27.45 (large)|0.001 (✓ significant)|
|`dotnet10` vs `quarkus3-native`|346.40 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native-mandrel`|342.79 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-leyden`|6.59 (large)|0.007 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|-2.99 (large)|0.025 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|10.83 (large)|0.001 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|94.38 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|94.34 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-7.91 (large)|0.003 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|1.28 (large)|0.201 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-native`|26.68 (large)|0.001 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|26.67 (large)|0.001 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|12.05 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|71.60 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|71.58 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|35.59 (large)|0.001 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|35.57 (large)|0.001 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|-3.55 (large)|0.015 (✓ significant)|

### RSS under load (MiB)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`dotnet10`|3|220.00|17.68|8.0%|[176.09, 263.92]|
|`quarkus3-jvm`|3|776.11|21.13|2.7%|[723.63, 828.60]|
|`quarkus3-leyden`|3|718.19|19.34|2.7%|[670.15, 766.24]|
|`quarkus3-virtual`|3|709.74|9.48|1.3%|[686.19, 733.29]|
|`quarkus3-virtual-leyden`|3|639.18|14.51|2.3%|[603.14, 675.22]|
|`quarkus3-native`|3|290.25|4.62|1.6%|[278.78, 301.73]|
|`quarkus3-native-mandrel`|3|292.39|5.44|1.9%|[278.87, 305.92]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`dotnet10` vs `quarkus3-jvm`|-28.55 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-leyden`|-26.89 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual`|-34.53 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual-leyden`|-25.92 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native`|-5.44 (large)|0.016 (✓ significant)|
|`dotnet10` vs `quarkus3-native-mandrel`|-5.54 (large)|0.013 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-leyden`|2.86 (large)|0.025 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|4.05 (large)|0.019 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|7.56 (large)|0.001 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|31.77 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|31.36 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|0.55 (medium)|0.547 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|4.62 (large)|0.006 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native`|30.44 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|29.97 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|5.76 (large)|0.004 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|56.27 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|54.00 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|32.41 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|31.65 (large)|0.000 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|-0.42 (small)|0.632 (✗ not significant)|

### Throughput (req/s)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`dotnet10`|3|6570.79|59.57|0.9%|[6422.79, 6718.79]|
|`quarkus3-jvm`|3|17843.32|282.18|1.6%|[17142.29, 18544.34]|
|`quarkus3-leyden`|3|16746.44|472.93|2.8%|[15571.53, 17921.35]|
|`quarkus3-virtual`|3|17016.75|342.22|2.0%|[16166.57, 17866.94]|
|`quarkus3-virtual-leyden`|3|16052.32|186.43|1.2%|[15589.16, 16515.48]|
|`quarkus3-native`|3|8404.54|44.67|0.5%|[8293.55, 8515.53]|
|`quarkus3-native-mandrel`|3|8631.28|122.80|1.4%|[8326.20, 8936.36]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`dotnet10` vs `quarkus3-jvm`|-55.28 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-leyden`|-30.19 (large)|0.001 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual`|-42.53 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual-leyden`|-68.51 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native`|-34.83 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native-mandrel`|-21.35 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-leyden`|2.82 (large)|0.036 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|2.64 (large)|0.034 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|7.49 (large)|0.001 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|46.72 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|42.33 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-0.65 (medium)|0.472 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|1.93 (large)|0.112 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-native`|24.83 (large)|0.001 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|23.49 (large)|0.001 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|3.50 (large)|0.022 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|35.29 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|32.62 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|56.42 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|47.01 (large)|0.000 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|-2.45 (large)|0.072 (✗ not significant)|

### Throughput density

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`dotnet10`|3|29.99|2.27|7.6%|[24.34, 35.63]|
|`quarkus3-jvm`|3|23.00|0.62|2.7%|[21.47, 24.53]|
|`quarkus3-leyden`|3|23.34|1.27|5.4%|[20.19, 26.49]|
|`quarkus3-virtual`|3|23.97|0.22|0.9%|[23.42, 24.53]|
|`quarkus3-virtual-leyden`|3|25.12|0.57|2.3%|[23.71, 26.53]|
|`quarkus3-native`|3|28.96|0.56|1.9%|[27.58, 30.35]|
|`quarkus3-native-mandrel`|3|29.53|0.86|2.9%|[27.40, 31.65]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`dotnet10` vs `quarkus3-jvm`|4.20 (large)|0.027 (✓ significant)|
|`dotnet10` vs `quarkus3-leyden`|3.61 (large)|0.020 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual`|3.72 (large)|0.043 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual-leyden`|2.94 (large)|0.058 (✗ not significant)|
|`dotnet10` vs `quarkus3-native`|0.62 (medium)|0.519 (✗ not significant)|
|`dotnet10` vs `quarkus3-native-mandrel`|0.27 (small)|0.768 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-leyden`|-0.34 (small)|0.705 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|-2.10 (large)|0.098 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|-3.58 (large)|0.012 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|-10.14 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|-8.76 (large)|0.001 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-0.70 (medium)|0.479 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|-1.81 (large)|0.121 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-native`|-5.73 (large)|0.008 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|-5.72 (large)|0.004 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|-2.66 (large)|0.058 (✗ not significant)|
|`quarkus3-virtual` vs `quarkus3-native`|-11.75 (large)|0.001 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|-8.88 (large)|0.005 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|-6.83 (large)|0.001 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|-6.07 (large)|0.003 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|-0.79 (medium)|0.398 (✗ not significant)|

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