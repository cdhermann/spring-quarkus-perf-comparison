# Benchmark Results: quarkus3-jvm, quarkus3-leyden, quarkus3-virtual, quarkus3-virtual-leyden, quarkus3-native, quarkus3-native-mandrel — 2026-04-26

> **Branch:** `native-mandrel-with-dotnet` · **Commit:** `27609fa` · **Iterations:** 3


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
|**Repo branch**|`native-mandrel-with-dotnet`|
|**Repo commit**|`27609fa`|
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
- **Load test:** wrk2, 2 threads, 100 connections, 2 min warmup + 30 sec measurement window
- **Endpoint:** `GET /fruits` (reads all fruits with store/address joins from PostgreSQL)

---

## Runtimes Tested

|Runtime|Description|
|---|---|
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
|**Reachable methods**|135,482|135,469|
|**Reflection types**|9,051|9,050|
|**Reflection fields**|1,816|1,815|
|**Reflection methods**|17,176|17,176|
|**Peak build RSS (GB)**|4.98|5.10|

---

## Raw Measurements

### Build Time (seconds)

|Runtime|I0|I1|I2|Average|Std|CV%|
|---|---|---|---|---|---|---|
|`quarkus3-jvm`|8.16|8.25|8.40|**8.27**|0.12|1.5%|
|`quarkus3-leyden`|51.86|52.08|52.28|**52.07**|0.21|0.4%|
|`quarkus3-virtual`|8.06|8.23|8.19|**8.16**|0.09|1.1%|
|`quarkus3-virtual-leyden`|53.05|53.44|53.06|**53.18**|0.22|0.4%|
|`quarkus3-native`|155.01|155.43|155.10|**155.18**|0.22|0.1%|
|`quarkus3-native-mandrel`|152.13|151.63|152.41|**152.06**|0.40|0.3%|

### Time to First Request (milliseconds)

|Runtime|I0|I1|I2|Average|Std|CV%|
|---|---|---|---|---|---|---|
|`quarkus3-jvm`|2,679.90|2,631.63|2,673.14|**2,661.55**|26.13|1.0%|
|`quarkus3-leyden`|986.95|944.58|1,033.39|**988.31**|44.42|4.5%|
|`quarkus3-virtual`|2,553.95|2,626.64|2,596.66|**2,592.42**|36.53|1.4%|
|`quarkus3-virtual-leyden`|883.69|935.30|832.43|**883.81**|51.43|5.8%|
|`quarkus3-native`|102.32|120.55|107.87|**110.25**|9.35|8.5%|
|`quarkus3-native-mandrel`|110.93|122.83|122.32|**118.69**|6.73|5.7%|

### RSS at Startup — before any request (MiB)

|Runtime|I0|I1|I2|Average|Std|CV%|
|---|---|---|---|---|---|---|
|`quarkus3-jvm`|272.54|272.41|271.69|**272.21**|0.46|0.2%|
|`quarkus3-leyden`|235.43|235.27|237.75|**236.15**|1.39|0.6%|
|`quarkus3-virtual`|272.96|273.85|275.34|**274.05**|1.20|0.4%|
|`quarkus3-virtual-leyden`|220.58|232.14|220.46|**224.39**|6.71|3.0%|
|`quarkus3-native`|89.84|89.86|89.86|**89.86**|0.01|0.0%|
|`quarkus3-native-mandrel`|89.49|89.51|89.51|**89.51**|0.01|0.0%|

### RSS after First Request (MiB)

|Runtime|I0|I1|I2|Average|Std|CV%|
|---|---|---|---|---|---|---|
|`quarkus3-jvm`|295.83|287.86|289.46|**291.05**|4.22|1.4%|
|`quarkus3-leyden`|244.42|244.08|255.63|**248.04**|6.57|2.7%|
|`quarkus3-virtual`|294.71|297.33|303.04|**298.36**|4.25|1.4%|
|`quarkus3-virtual-leyden`|248.78|247.67|244.89|**247.11**|2.00|0.8%|
|`quarkus3-native`|95.73|95.75|95.77|**95.75**|0.02|0.0%|
|`quarkus3-native-mandrel`|95.41|95.41|95.43|**95.42**|0.01|0.0%|

### RSS under Load (MiB)

|Runtime|I0|I1|I2|Average|Std|CV%|
|---|---|---|---|---|---|---|
|`quarkus3-jvm`|788.77|784.87|785.34|**786.33**|2.13|0.3%|
|`quarkus3-leyden`|743.29|698.95|721.98|**721.41**|22.18|3.1%|
|`quarkus3-virtual`|710.64|690.35|701.25|**700.75**|10.16|1.4%|
|`quarkus3-virtual-leyden`|643.70|646.88|631.02|**640.53**|8.39|1.3%|
|`quarkus3-native`|240.41|287.93|225.91|**251.42**|32.44|12.9%|
|`quarkus3-native-mandrel`|286.44|285.25|—|**285.84**|0.84|0.3%|

### Throughput (req/sec)

|Runtime|I0|I1|I2|Average|Std|CV%|
|---|---|---|---|---|---|---|
|`quarkus3-jvm`|18,653|18,302|18,220|**18,392**|230|1.3%|
|`quarkus3-leyden`|16,448|15,579|16,691|**16,240**|585|3.6%|
|`quarkus3-virtual`|16,571|16,881|16,997|**16,816**|220|1.3%|
|`quarkus3-virtual-leyden`|15,322|15,471|16,111|**15,635**|419|2.7%|
|`quarkus3-native`|8,376|8,380|8,378|**8,378**|2|0.0%|
|`quarkus3-native-mandrel`|8,528|8,635|—|**8,582**|76|0.9%|

### Throughput Density (req/sec per MiB of RSS under load)

|Runtime|I0|I1|I2|Max|Std|CV%|
|---|---|---|---|---|---|---|
|`quarkus3-jvm`|23.65|23.32|23.20|**23.65**|0.23|1.0%|
|`quarkus3-leyden`|22.13|22.29|23.12|**23.12**|0.53|2.4%|
|`quarkus3-virtual`|23.32|24.45|24.24|**24.45**|0.60|2.5%|
|`quarkus3-virtual-leyden`|23.80|23.92|25.53|**25.53**|0.97|4.0%|
|`quarkus3-native`|34.84|29.10|37.08|**37.08**|4.12|12.2%|
|`quarkus3-native-mandrel`|29.77|30.27|—|**30.27**|0.35|1.2%|

---

## Summary Comparison

|Runtime|Build (s)|Startup (ms)|RSS idle (MiB)|RSS load (MiB)|Throughput (tps)|Density (tps/MiB)|
|---|---|---|---|---|---|---|
|`quarkus3-jvm`|8.27|2661.6|272.2|786.3|**18,392**|23.65|
|`quarkus3-leyden`|52.07|988.3|236.1|721.4|**16,240**|23.12|
|`quarkus3-virtual`|8.16|2592.4|274.0|700.7|**16,816**|24.45|
|`quarkus3-virtual-leyden`|53.18|883.8|224.4|640.5|**15,635**|25.53|
|`quarkus3-native`|155.18|110.3|89.9|251.4|**8,378**|37.08|
|`quarkus3-native-mandrel`|152.06|118.7|89.5|285.8|**8,582**|30.27|

---

## Analysis

### Build Time

|Runtime|Avg (s)|vs `quarkus3-jvm`|
|---|---|---|
|`quarkus3-virtual`|8.2|~same|
|`quarkus3-jvm`|**8.3**|baseline|
|`quarkus3-leyden`|52.1|6.3× more|
|`quarkus3-virtual-leyden`|53.2|6.4× more|
|`quarkus3-native-mandrel`|152.1|18.4× more|
|`quarkus3-native`|155.2|18.8× more|

### Startup — Time to First Request

|Runtime|Avg (ms)|vs `quarkus3-jvm`|
|---|---|---|
|`quarkus3-native`|110|24.1× less|
|`quarkus3-native-mandrel`|119|22.4× less|
|`quarkus3-virtual-leyden`|884|3.0× less|
|`quarkus3-leyden`|988|2.7× less|
|`quarkus3-virtual`|2592|~same|
|`quarkus3-jvm`|**2662**|baseline|

### Memory at Idle (RSS at startup)

|Runtime|Avg (MiB)|vs `quarkus3-jvm`|
|---|---|---|
|`quarkus3-native-mandrel`|89.5|3.0× less|
|`quarkus3-native`|89.9|3.0× less|
|`quarkus3-virtual-leyden`|224.4|1.2× less|
|`quarkus3-leyden`|236.1|1.2× less|
|`quarkus3-jvm`|**272.2**|baseline|
|`quarkus3-virtual`|274.0|~same|

### Memory under Load (RSS)

|Runtime|Avg (MiB)|vs `quarkus3-jvm`|
|---|---|---|
|`quarkus3-native`|251.4|3.1× less|
|`quarkus3-native-mandrel`|285.8|2.8× less|
|`quarkus3-virtual-leyden`|640.5|1.2× less|
|`quarkus3-virtual`|700.7|1.1× less|
|`quarkus3-leyden`|721.4|1.1× less|
|`quarkus3-jvm`|**786.3**|baseline|

### Throughput

|Runtime|Avg (tps)|vs `quarkus3-native-mandrel`|
|---|---|---|
|`quarkus3-jvm`|18,392|+114%|
|`quarkus3-virtual`|16,816|+96%|
|`quarkus3-leyden`|16,240|+89%|
|`quarkus3-virtual-leyden`|15,635|+82%|
|`quarkus3-native-mandrel`|**8,582**|baseline|
|`quarkus3-native`|8,378|-2%|

### Throughput Density (tps per MiB of RAM under load)

|Runtime|Avg (tps/MiB)|vs `quarkus3-jvm`|
|---|---|---|
|`quarkus3-native`|37.08|+57%|
|`quarkus3-native-mandrel`|30.27|+28%|
|`quarkus3-virtual-leyden`|25.53|+8%|
|`quarkus3-virtual`|24.45|+3%|
|`quarkus3-jvm`|**23.65**|baseline|
|`quarkus3-leyden`|23.12|-2%|

---

## Key Trade-offs

|Goal|Best choice|
|---|---|
|Lowest startup latency|`quarkus3-native` (110.3)|
|Highest raw throughput|`quarkus3-jvm` (18391.8)|
|Lowest memory footprint (idle)|`quarkus3-native-mandrel` (89.5)|
|Lowest memory footprint (load)|`quarkus3-native` (251.4)|
|Best throughput per MiB of RAM|`quarkus3-native` (37.1)|
|Fastest build|`quarkus3-virtual` (8.2)|

---

## Statistical Significance

> ⚠️ **Low sample size (n ≤ 3):** Tests have limited statistical power. Treat p-values and effect sizes as directional indicators only — run ≥ 5 iterations for reliable conclusions.

### Build Time (s)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`quarkus3-jvm`|3|8.27|0.12|1.5%|[7.97, 8.57]|
|`quarkus3-leyden`|3|52.07|0.21|0.4%|[51.55, 52.60]|
|`quarkus3-virtual`|3|8.16|0.09|1.1%|[7.94, 8.38]|
|`quarkus3-virtual-leyden`|3|53.18|0.22|0.4%|[52.63, 53.74]|
|`quarkus3-native`|3|155.18|0.22|0.1%|[154.63, 155.73]|
|`quarkus3-native-mandrel`|3|152.06|0.40|0.3%|[151.08, 153.04]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`quarkus3-jvm` vs `quarkus3-leyden`|-255.39 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|1.03 (large)|0.280 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|-250.81 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|-823.83 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|-491.98 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|272.25 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|-5.13 (large)|0.003 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native`|-478.06 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|-315.96 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|-265.92 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|-872.40 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|-502.46 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|-459.99 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|-308.40 (large)|0.000 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|9.75 (large)|0.001 (✓ significant)|

### Startup — TTFR (ms)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`quarkus3-jvm`|3|2661.55|26.13|1.0%|[2596.63, 2726.48]|
|`quarkus3-leyden`|3|988.31|44.42|4.5%|[877.96, 1098.66]|
|`quarkus3-virtual`|3|2592.42|36.53|1.4%|[2501.66, 2683.17]|
|`quarkus3-virtual-leyden`|3|883.81|51.43|5.8%|[756.03, 1011.59]|
|`quarkus3-native`|3|110.25|9.35|8.5%|[87.03, 133.47]|
|`quarkus3-native-mandrel`|3|118.69|6.73|5.7%|[101.98, 135.41]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`quarkus3-jvm` vs `quarkus3-leyden`|45.92 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|2.18 (large)|0.062 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|43.58 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|130.00 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|133.26 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-39.45 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|2.17 (large)|0.057 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-native`|27.36 (large)|0.001 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|27.38 (large)|0.001 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|38.30 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|93.09 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|94.18 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|20.93 (large)|0.001 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|20.86 (large)|0.001 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|-1.04 (large)|0.279 (✗ not significant)|

### RSS at startup (MiB)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`quarkus3-jvm`|3|272.21|0.46|0.2%|[271.07, 273.36]|
|`quarkus3-leyden`|3|236.15|1.39|0.6%|[232.69, 239.61]|
|`quarkus3-virtual`|3|274.05|1.20|0.4%|[271.06, 277.04]|
|`quarkus3-virtual-leyden`|3|224.39|6.71|3.0%|[207.72, 241.07]|
|`quarkus3-native`|3|89.86|0.01|0.0%|[89.82, 89.89]|
|`quarkus3-native-mandrel`|3|89.51|0.01|0.0%|[89.48, 89.53]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`quarkus3-jvm` vs `quarkus3-leyden`|34.79 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|-2.01 (large)|0.105 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|10.05 (large)|0.006 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|559.93 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|561.08 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-29.13 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|2.43 (large)|0.088 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-native`|148.66 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|149.02 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|10.30 (large)|0.005 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|216.34 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|216.75 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|28.35 (large)|0.001 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|28.42 (large)|0.001 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|28.12 (large)|0.000 (✓ significant)|

### RSS after 1st req (MiB)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`quarkus3-jvm`|3|291.05|4.22|1.4%|[280.57, 301.53]|
|`quarkus3-leyden`|3|248.04|6.57|2.7%|[231.71, 264.38]|
|`quarkus3-virtual`|3|298.36|4.25|1.4%|[287.79, 308.93]|
|`quarkus3-virtual-leyden`|3|247.11|2.00|0.8%|[242.13, 252.09]|
|`quarkus3-native`|3|95.75|0.02|0.0%|[95.71, 95.79]|
|`quarkus3-native-mandrel`|3|95.42|0.01|0.0%|[95.40, 95.44]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`quarkus3-jvm` vs `quarkus3-leyden`|7.79 (large)|0.001 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|-1.73 (large)|0.102 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|13.31 (large)|0.001 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|65.49 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|65.60 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-9.09 (large)|0.001 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|0.19 (negligible)|0.833 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-native`|32.76 (large)|0.001 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|32.83 (large)|0.001 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|15.41 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|67.35 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|67.46 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|106.77 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|107.01 (large)|0.000 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|23.98 (large)|0.000 (✓ significant)|

### RSS under load (MiB)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`quarkus3-jvm`|3|786.33|2.13|0.3%|[781.04, 791.62]|
|`quarkus3-leyden`|3|721.41|22.18|3.1%|[666.32, 776.50]|
|`quarkus3-virtual`|3|700.75|10.16|1.4%|[675.52, 725.98]|
|`quarkus3-virtual-leyden`|3|640.53|8.39|1.3%|[619.69, 661.38]|
|`quarkus3-native`|3|251.42|32.44|12.9%|[170.82, 332.01]|
|`quarkus3-native-mandrel`|2|285.84|0.84|0.3%|[278.30, 293.39]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`quarkus3-jvm` vs `quarkus3-leyden`|4.12 (large)|0.036 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|11.66 (large)|0.003 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|23.82 (large)|0.001 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|23.27 (large)|0.001 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|277.29 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|1.20 (large)|0.245 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|4.82 (large)|0.015 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native`|16.91 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|24.05 (large)|0.001 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|6.46 (large)|0.002 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|18.69 (large)|0.001 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|49.95 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|16.42 (large)|0.001 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|51.65 (large)|0.000 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|-1.30 (large)|0.207 (✗ not significant)|

### Throughput (req/s)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`quarkus3-jvm`|3|18391.75|230.17|1.3%|[17819.94, 18963.56]|
|`quarkus3-leyden`|3|16239.55|584.53|3.6%|[14787.38, 17691.72]|
|`quarkus3-virtual`|3|16816.29|220.33|1.3%|[16268.92, 17363.66]|
|`quarkus3-virtual-leyden`|3|15634.67|419.06|2.7%|[14593.58, 16675.76]|
|`quarkus3-native`|3|8377.92|2.04|0.0%|[8372.84, 8383.00]|
|`quarkus3-native-mandrel`|2|8581.78|75.78|0.9%|[7900.92, 9262.63]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`quarkus3-jvm` vs `quarkus3-leyden`|4.84 (large)|0.014 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|6.99 (large)|0.001 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|8.16 (large)|0.002 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|61.53 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|50.84 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-1.31 (large)|0.223 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|1.19 (large)|0.226 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-native`|19.02 (large)|0.002 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|15.98 (large)|0.002 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|3.53 (large)|0.022 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|54.16 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|44.48 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|24.49 (large)|0.001 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|20.45 (large)|0.001 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|-4.66 (large)|0.163 (✗ not significant)|

### Throughput density

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`quarkus3-jvm`|3|23.39|0.23|1.0%|[22.81, 23.97]|
|`quarkus3-leyden`|3|22.51|0.53|2.4%|[21.19, 23.83]|
|`quarkus3-virtual`|3|24.00|0.60|2.5%|[22.51, 25.50]|
|`quarkus3-virtual-leyden`|3|24.42|0.97|4.0%|[22.02, 26.82]|
|`quarkus3-native`|3|33.68|4.12|12.2%|[23.45, 43.90]|
|`quarkus3-native-mandrel`|2|30.02|0.35|1.2%|[26.85, 33.20]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`quarkus3-jvm` vs `quarkus3-leyden`|2.14 (large)|0.087 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|-1.34 (large)|0.213 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|-1.46 (large)|0.202 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-native`|-3.53 (large)|0.049 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|-23.81 (large)|0.005 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-2.63 (large)|0.033 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|-2.44 (large)|0.056 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-native`|-3.81 (large)|0.040 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|-15.68 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|-0.51 (medium)|0.569 (✗ not significant)|
|`quarkus3-virtual` vs `quarkus3-native`|-3.29 (large)|0.053 (✗ not significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|-11.30 (large)|0.001 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|-3.10 (large)|0.053 (✗ not significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|-6.88 (large)|0.004 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|1.09 (large)|0.263 (✗ not significant)|

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