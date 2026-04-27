# Benchmark Results: dotnet10, quarkus3-jvm, quarkus3-leyden, quarkus3-virtual, quarkus3-virtual-leyden, quarkus3-native, quarkus3-native-mandrel — 2026-04-27

> **Branch:** `native-mandrel-with-dotnet` · **Commit:** `4cff206` · **Iterations:** 7


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
|**Repo commit**|`4cff206`|
|**Iterations**|7|

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
|**Total image size (MB)**|121.82|123.00|
|**Reachable types**|27,587|27,587|
|**Reachable fields**|37,248|37,247|
|**Reachable methods**|135,482|135,478|
|**Reflection types**|9,051|9,050|
|**Reflection fields**|1,816|1,815|
|**Reflection methods**|17,176|17,176|
|**Peak build RSS (GB)**|4.97|5.10|

---

## Raw Measurements

### Build Time (seconds)

|Runtime|I0|I1|I2|I3|I4|I5|I6|Average|Std|CV%|
|---|---|---|---|---|---|---|---|---|---|---|
|`dotnet10`|7.01|1.70|1.72|1.77|1.74|1.76|1.69|**2.48**|2.00|80.3%|
|`quarkus3-jvm`|8.09|8.18|8.10|7.99|8.03|8.18|8.16|**8.10**|0.07|0.9%|
|`quarkus3-leyden`|67.35|52.27|52.19|51.71|52.37|51.88|52.41|**54.31**|5.76|10.6%|
|`quarkus3-virtual`|8.22|7.82|8.05|8.11|8.16|8.13|8.11|**8.09**|0.13|1.6%|
|`quarkus3-virtual-leyden`|52.13|52.64|52.28|52.40|52.88|52.49|52.10|**52.42**|0.28|0.5%|
|`quarkus3-native`|155.07|155.81|155.67|154.00|153.60|151.33|157.62|**154.73**|2.00|1.3%|
|`quarkus3-native-mandrel`|150.19|150.40|150.22|151.60|151.63|153.18|151.74|**151.28**|1.09|0.7%|

### Time to First Request (milliseconds)

|Runtime|I0|I1|I2|I3|I4|I5|I6|Average|Std|CV%|
|---|---|---|---|---|---|---|---|---|---|---|
|`dotnet10`|1,762.95|1,670.98|1,697.73|1,693.47|1,714.32|1,651.55|1,772.09|**1,709.01**|44.79|2.6%|
|`quarkus3-jvm`|2,548.84|2,549.20|2,561.12|2,637.34|2,514.52|2,688.02|2,658.12|**2,593.88**|66.17|2.6%|
|`quarkus3-leyden`|948.16|999.09|1,045.12|990.74|960.48|1,032.03|991.29|**995.28**|34.92|3.5%|
|`quarkus3-virtual`|2,599.16|2,532.83|2,661.82|2,594.82|2,540.85|2,548.33|2,613.00|**2,584.40**|46.54|1.8%|
|`quarkus3-virtual-leyden`|829.21|833.12|918.38|895.39|908.32|882.68|858.91|**875.14**|35.53|4.1%|
|`quarkus3-native`|99.46|121.95|122.10|119.11|106.57|107.70|88.88|**109.40**|12.54|11.5%|
|`quarkus3-native-mandrel`|110.14|119.41|113.08|112.88|123.31|81.99|124.79|**112.23**|14.45|12.9%|

### RSS at Startup — before any request (MiB)

|Runtime|I0|I1|I2|I3|I4|I5|I6|Average|Std|CV%|
|---|---|---|---|---|---|---|---|---|---|---|
|`dotnet10`|69.00|68.80|69.23|69.18|68.88|69.00|69.07|**69.02**|0.15|0.2%|
|`quarkus3-jvm`|269.60|272.16|272.54|272.66|273.42|277.59|273.15|**273.02**|2.37|0.9%|
|`quarkus3-leyden`|221.46|237.36|240.04|242.88|241.05|241.67|237.59|**237.44**|7.33|3.1%|
|`quarkus3-virtual`|273.24|273.35|273.63|270.74|276.62|276.87|271.79|**273.75**|2.28|0.8%|
|`quarkus3-virtual-leyden`|233.91|234.99|232.75|236.70|238.75|219.83|215.35|**230.33**|9.00|3.9%|
|`quarkus3-native`|88.96|88.94|88.93|88.92|88.96|88.94|88.97|**88.94**|0.02|0.0%|
|`quarkus3-native-mandrel`|89.57|89.57|89.57|89.57|89.55|89.57|89.57|**89.57**|0.01|0.0%|

### RSS after First Request (MiB)

|Runtime|I0|I1|I2|I3|I4|I5|I6|Average|Std|CV%|
|---|---|---|---|---|---|---|---|---|---|---|
|`dotnet10`|128.46|128.45|128.84|129.11|128.73|128.79|128.73|**128.73**|0.23|0.2%|
|`quarkus3-jvm`|287.08|289.25|288.15|292.04|288.87|293.04|289.80|**289.75**|2.11|0.7%|
|`quarkus3-leyden`|239.43|245.58|249.39|254.54|256.99|257.90|246.07|**249.98**|6.82|2.7%|
|`quarkus3-virtual`|289.85|292.62|302.23|294.65|303.11|306.64|288.83|**296.85**|7.07|2.4%|
|`quarkus3-virtual-leyden`|247.67|244.96|258.58|249.95|249.93|250.06|244.08|**249.32**|4.77|1.9%|
|`quarkus3-native`|95.17|95.14|95.14|95.11|95.17|95.12|95.17|**95.14**|0.02|0.0%|
|`quarkus3-native-mandrel`|95.72|95.69|95.73|95.69|95.70|95.71|95.73|**95.71**|0.02|0.0%|

### RSS under Load (MiB)

|Runtime|I0|I1|I2|I3|I4|I5|I6|Average|Std|CV%|
|---|---|---|---|---|---|---|---|---|---|---|
|`dotnet10`|221.32|202.28|228.27|222.69|224.69|219.08|229.33|**221.09**|9.06|4.1%|
|`quarkus3-jvm`|762.76|788.89|787.30|773.68|787.33|766.50|759.28|**775.10**|12.70|1.6%|
|`quarkus3-leyden`|709.24|728.87|735.78|719.39|725.36|725.64|706.62|**721.56**|10.54|1.5%|
|`quarkus3-virtual`|689.02|705.57|711.63|700.27|698.71|688.57|677.76|**695.93**|11.53|1.7%|
|`quarkus3-virtual-leyden`|661.89|631.57|657.46|679.58|654.25|666.80|627.69|**654.18**|18.65|2.9%|
|`quarkus3-native`|291.91|284.73|285.84|295.22|289.09|295.96|285.62|**289.77**|4.68|1.6%|
|`quarkus3-native-mandrel`|285.64|286.01|288.90|293.14|290.14|285.71|279.97|**287.07**|4.18|1.5%|

### Throughput (req/sec)

|Runtime|I0|I1|I2|I3|I4|I5|I6|Average|Std|CV%|
|---|---|---|---|---|---|---|---|---|---|---|
|`dotnet10`|6,495|6,466|6,483|6,414|6,493|6,622|6,510|**6,498**|63|1.0%|
|`quarkus3-jvm`|17,799|18,256|18,691|17,918|18,146|17,822|17,564|**18,028**|371|2.1%|
|`quarkus3-leyden`|16,735|16,857|16,887|16,403|16,637|16,791|15,745|**16,579**|402|2.4%|
|`quarkus3-virtual`|16,776|17,043|17,168|16,715|16,675|16,878|16,136|**16,770**|331|2.0%|
|`quarkus3-virtual-leyden`|15,781|15,760|15,170|15,466|15,713|15,840|15,242|**15,567**|274|1.8%|
|`quarkus3-native`|8,452|8,330|8,468|8,534|8,401|8,538|8,383|**8,444**|78|0.9%|
|`quarkus3-native-mandrel`|8,493|8,392|8,346|8,602|8,275|8,073|8,553|**8,391**|182|2.2%|

### Throughput Density (req/sec per MiB of RSS under load)

|Runtime|I0|I1|I2|I3|I4|I5|I6|Max|Std|CV%|
|---|---|---|---|---|---|---|---|---|---|---|
|`dotnet10`|29.35|31.97|28.40|28.80|28.90|30.23|28.39|**31.97**|1.28|4.4%|
|`quarkus3-jvm`|23.33|23.14|23.74|23.16|23.05|23.25|23.13|**23.74**|0.23|1.0%|
|`quarkus3-leyden`|23.60|23.13|22.95|22.80|22.94|23.14|22.28|**23.60**|0.40|1.7%|
|`quarkus3-virtual`|24.35|24.15|24.13|23.87|23.87|24.51|23.81|**24.51**|0.27|1.1%|
|`quarkus3-virtual-leyden`|23.84|24.95|23.07|22.76|24.02|23.76|24.28|**24.95**|0.73|3.1%|
|`quarkus3-native`|28.95|29.26|29.62|28.91|29.06|28.85|29.35|**29.62**|0.28|1.0%|
|`quarkus3-native-mandrel`|29.73|29.34|28.89|29.34|28.52|28.25|30.55|**30.55**|0.77|2.6%|

---

## Summary Comparison

|Runtime|Build (s)|Startup (ms)|RSS idle (MiB)|RSS load (MiB)|Throughput (tps)|Density (tps/MiB)|
|---|---|---|---|---|---|---|
|`dotnet10`|2.48|1709.0|69.0|221.1|**6,498**|31.97|
|`quarkus3-jvm`|8.10|2593.9|273.0|775.1|**18,028**|23.74|
|`quarkus3-leyden`|54.31|995.3|237.4|721.6|**16,579**|23.60|
|`quarkus3-virtual`|8.09|2584.4|273.7|695.9|**16,770**|24.51|
|`quarkus3-virtual-leyden`|52.42|875.1|230.3|654.2|**15,567**|24.95|
|`quarkus3-native`|154.73|109.4|88.9|289.8|**8,444**|29.62|
|`quarkus3-native-mandrel`|151.28|112.2|89.6|287.1|**8,391**|30.55|

---

## Analysis

### Build Time

|Runtime|Avg (s)|vs `quarkus3-jvm`|
|---|---|---|
|`dotnet10`|2.5|3.3× less|
|`quarkus3-virtual`|8.1|~same|
|`quarkus3-jvm`|**8.1**|baseline|
|`quarkus3-virtual-leyden`|52.4|6.5× more|
|`quarkus3-leyden`|54.3|6.7× more|
|`quarkus3-native-mandrel`|151.3|18.7× more|
|`quarkus3-native`|154.7|19.1× more|

### Startup — Time to First Request

|Runtime|Avg (ms)|vs `quarkus3-jvm`|
|---|---|---|
|`quarkus3-native`|109|23.7× less|
|`quarkus3-native-mandrel`|112|23.1× less|
|`quarkus3-virtual-leyden`|875|3.0× less|
|`quarkus3-leyden`|995|2.6× less|
|`dotnet10`|1709|1.5× less|
|`quarkus3-virtual`|2584|~same|
|`quarkus3-jvm`|**2594**|baseline|

### Memory at Idle (RSS at startup)

|Runtime|Avg (MiB)|vs `quarkus3-jvm`|
|---|---|---|
|`dotnet10`|69.0|4.0× less|
|`quarkus3-native`|88.9|3.1× less|
|`quarkus3-native-mandrel`|89.6|3.0× less|
|`quarkus3-virtual-leyden`|230.3|1.2× less|
|`quarkus3-leyden`|237.4|1.1× less|
|`quarkus3-jvm`|**273.0**|baseline|
|`quarkus3-virtual`|273.7|~same|

### Memory under Load (RSS)

|Runtime|Avg (MiB)|vs `quarkus3-jvm`|
|---|---|---|
|`dotnet10`|221.1|3.5× less|
|`quarkus3-native-mandrel`|287.1|2.7× less|
|`quarkus3-native`|289.8|2.7× less|
|`quarkus3-virtual-leyden`|654.2|1.2× less|
|`quarkus3-virtual`|695.9|1.1× less|
|`quarkus3-leyden`|721.6|1.1× less|
|`quarkus3-jvm`|**775.1**|baseline|

### Throughput

|Runtime|Avg (tps)|vs `dotnet10`|
|---|---|---|
|`quarkus3-jvm`|18,028|+177%|
|`quarkus3-virtual`|16,770|+158%|
|`quarkus3-leyden`|16,579|+155%|
|`quarkus3-virtual-leyden`|15,567|+140%|
|`quarkus3-native`|8,444|+30%|
|`quarkus3-native-mandrel`|8,391|+29%|
|`dotnet10`|**6,498**|baseline|

### Throughput Density (tps per MiB of RAM under load)

|Runtime|Avg (tps/MiB)|vs `quarkus3-jvm`|
|---|---|---|
|`dotnet10`|31.97|+35%|
|`quarkus3-native-mandrel`|30.55|+29%|
|`quarkus3-native`|29.62|+25%|
|`quarkus3-virtual-leyden`|24.95|+5%|
|`quarkus3-virtual`|24.51|+3%|
|`quarkus3-jvm`|**23.74**|baseline|
|`quarkus3-leyden`|23.60|-1%|

---

## Key Trade-offs

|Goal|Best choice|
|---|---|
|Lowest startup latency|`quarkus3-native` (109.4)|
|Highest raw throughput|`quarkus3-jvm` (18027.9)|
|Lowest memory footprint (idle)|`dotnet10` (69.0)|
|Lowest memory footprint (load)|`dotnet10` (221.1)|
|Best throughput per MiB of RAM|`dotnet10` (32.0)|
|Fastest build|`dotnet10` (2.5)|

---

## Statistical Significance

### Build Time (s)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`dotnet10`|7|2.48|2.00|80.3%|[0.64, 4.33]|
|`quarkus3-jvm`|7|8.10|0.07|0.9%|[8.04, 8.17]|
|`quarkus3-leyden`|7|54.31|5.76|10.6%|[48.99, 59.63]|
|`quarkus3-virtual`|7|8.09|0.13|1.6%|[7.97, 8.20]|
|`quarkus3-virtual-leyden`|7|52.42|0.28|0.5%|[52.16, 52.68]|
|`quarkus3-native`|7|154.73|2.00|1.3%|[152.88, 156.57]|
|`quarkus3-native-mandrel`|7|151.28|1.09|0.7%|[150.27, 152.29]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`dotnet10` vs `quarkus3-jvm`|-3.98 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-leyden`|-12.03 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual`|-3.96 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual-leyden`|-35.04 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native`|-76.29 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native-mandrel`|-92.53 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-leyden`|-11.35 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|0.18 (negligible)|0.747 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|-216.07 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|-103.85 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|-185.28 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|11.36 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|0.46 (small)|0.418 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-native`|-23.31 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|-23.41 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|-203.42 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|-103.72 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|-184.46 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|-71.81 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|-124.20 (large)|0.000 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|2.14 (large)|0.003 (✓ significant)|

### Startup — TTFR (ms)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`dotnet10`|7|1709.01|44.79|2.6%|[1667.59, 1750.43]|
|`quarkus3-jvm`|7|2593.88|66.17|2.6%|[2532.68, 2655.08]|
|`quarkus3-leyden`|7|995.28|34.92|3.5%|[962.98, 1027.58]|
|`quarkus3-virtual`|7|2584.40|46.54|1.8%|[2541.36, 2627.44]|
|`quarkus3-virtual-leyden`|7|875.14|35.53|4.1%|[842.28, 908.01]|
|`quarkus3-native`|7|109.40|12.54|11.5%|[97.80, 121.00]|
|`quarkus3-native-mandrel`|7|112.23|14.45|12.9%|[98.87, 125.59]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`dotnet10` vs `quarkus3-jvm`|-15.66 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-leyden`|17.77 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual`|-19.17 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual-leyden`|20.63 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native`|48.64 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native-mandrel`|47.99 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-leyden`|30.21 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|0.17 (negligible)|0.762 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|32.36 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|52.17 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|51.82 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-38.62 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|3.41 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native`|33.76 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|33.04 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|41.28 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|72.62 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|71.75 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|28.74 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|28.13 (large)|0.000 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|-0.21 (small)|0.702 (✗ not significant)|

### RSS at startup (MiB)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`dotnet10`|7|69.02|0.15|0.2%|[68.88, 69.17]|
|`quarkus3-jvm`|7|273.02|2.37|0.9%|[270.82, 275.21]|
|`quarkus3-leyden`|7|237.44|7.33|3.1%|[230.66, 244.22]|
|`quarkus3-virtual`|7|273.75|2.28|0.8%|[271.64, 275.86]|
|`quarkus3-virtual-leyden`|7|230.33|9.00|3.9%|[222.00, 238.65]|
|`quarkus3-native`|7|88.94|0.02|0.0%|[88.93, 88.96]|
|`quarkus3-native-mandrel`|7|89.57|0.01|0.0%|[89.56, 89.58]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`dotnet10` vs `quarkus3-jvm`|-121.23 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-leyden`|-32.48 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual`|-126.53 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual-leyden`|-25.33 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native`|-182.95 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native-mandrel`|-189.69 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-leyden`|6.53 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|-0.31 (small)|0.567 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|6.48 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|109.62 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|109.25 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-6.69 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|0.87 (large)|0.132 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-native`|28.64 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|28.52 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|6.61 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|114.47 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|114.08 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|22.21 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|22.11 (large)|0.000 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|-44.46 (large)|0.000 (✓ significant)|

### RSS after 1st req (MiB)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`dotnet10`|7|128.73|0.23|0.2%|[128.52, 128.94]|
|`quarkus3-jvm`|7|289.75|2.11|0.7%|[287.79, 291.70]|
|`quarkus3-leyden`|7|249.98|6.82|2.7%|[243.68, 256.29]|
|`quarkus3-virtual`|7|296.85|7.07|2.4%|[290.31, 303.39]|
|`quarkus3-virtual-leyden`|7|249.32|4.77|1.9%|[244.91, 253.73]|
|`quarkus3-native`|7|95.14|0.02|0.0%|[95.12, 95.17]|
|`quarkus3-native-mandrel`|7|95.71|0.02|0.0%|[95.69, 95.73]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`dotnet10` vs `quarkus3-jvm`|-107.16 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-leyden`|-25.13 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual`|-33.60 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual-leyden`|-35.74 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native`|207.02 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native-mandrel`|204.17 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-leyden`|7.88 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|-1.36 (large)|0.038 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|10.97 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|130.26 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|129.88 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-6.75 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|0.11 (negligible)|0.836 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-native`|32.11 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|32.00 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|7.88 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|40.34 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|40.22 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|45.75 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|45.58 (large)|0.000 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|-26.82 (large)|0.000 (✓ significant)|

### RSS under load (MiB)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`dotnet10`|7|221.09|9.06|4.1%|[212.71, 229.48]|
|`quarkus3-jvm`|7|775.10|12.70|1.6%|[763.36, 786.85]|
|`quarkus3-leyden`|7|721.56|10.54|1.5%|[711.81, 731.31]|
|`quarkus3-virtual`|7|695.93|11.53|1.7%|[685.26, 706.60]|
|`quarkus3-virtual-leyden`|7|654.18|18.65|2.9%|[636.92, 671.43]|
|`quarkus3-native`|7|289.77|4.68|1.6%|[285.44, 294.09]|
|`quarkus3-native-mandrel`|7|287.07|4.18|1.5%|[283.21, 290.94]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`dotnet10` vs `quarkus3-jvm`|-50.22 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-leyden`|-50.92 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual`|-45.78 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual-leyden`|-29.53 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native`|-9.52 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native-mandrel`|-9.35 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-leyden`|4.59 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|6.53 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|7.58 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|50.73 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|51.63 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|2.32 (large)|0.001 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|4.45 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native`|52.96 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|54.19 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|2.69 (large)|0.001 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|46.15 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|47.13 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|26.80 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|27.16 (large)|0.000 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|0.61 (medium)|0.279 (✗ not significant)|

### Throughput (req/s)

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`dotnet10`|7|6497.68|63.27|1.0%|[6439.16, 6556.19]|
|`quarkus3-jvm`|7|18027.87|371.30|2.1%|[17684.47, 18371.28]|
|`quarkus3-leyden`|7|16579.41|402.48|2.4%|[16207.16, 16951.65]|
|`quarkus3-virtual`|7|16770.14|331.25|2.0%|[16463.78, 17076.51]|
|`quarkus3-virtual-leyden`|7|15567.30|274.47|1.8%|[15313.44, 15821.15]|
|`quarkus3-native`|7|8443.66|77.51|0.9%|[8371.97, 8515.35]|
|`quarkus3-native-mandrel`|7|8390.61|181.60|2.2%|[8222.65, 8558.57]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`dotnet10` vs `quarkus3-jvm`|-43.29 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-leyden`|-35.00 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual`|-43.08 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual-leyden`|-45.54 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native`|-27.51 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native-mandrel`|-13.92 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-leyden`|3.74 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|3.57 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|7.54 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native`|35.73 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|32.97 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-0.52 (medium)|0.353 (✗ not significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|2.94 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native`|28.07 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|26.23 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|3.95 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native`|34.61 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|31.37 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|35.32 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|30.84 (large)|0.000 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|0.38 (small)|0.497 (✗ not significant)|

### Throughput density

|Runtime|n|Mean|Std|CV%|95% CI|
|---|---|---|---|---|---|
|`dotnet10`|7|29.43|1.28|4.4%|[28.25, 30.62]|
|`quarkus3-jvm`|7|23.26|0.23|1.0%|[23.04, 23.47]|
|`quarkus3-leyden`|7|22.98|0.40|1.7%|[22.61, 23.34]|
|`quarkus3-virtual`|7|24.10|0.27|1.1%|[23.85, 24.34]|
|`quarkus3-virtual-leyden`|7|23.81|0.73|3.1%|[23.13, 24.49]|
|`quarkus3-native`|7|29.14|0.28|1.0%|[28.88, 29.40]|
|`quarkus3-native-mandrel`|7|29.23|0.77|2.6%|[28.52, 29.95]|

|Comparison|Cohen's d|Welch p-value|
|---|---|---|
|`dotnet10` vs `quarkus3-jvm`|6.69 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-leyden`|6.79 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual`|5.75 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-virtual-leyden`|5.38 (large)|0.000 (✓ significant)|
|`dotnet10` vs `quarkus3-native`|0.31 (small)|0.579 (✗ not significant)|
|`dotnet10` vs `quarkus3-native-mandrel`|0.19 (negligible)|0.732 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-leyden`|0.87 (large)|0.137 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-virtual`|-3.36 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-virtual-leyden`|-1.02 (large)|0.097 (✗ not significant)|
|`quarkus3-jvm` vs `quarkus3-native`|-22.87 (large)|0.000 (✓ significant)|
|`quarkus3-jvm` vs `quarkus3-native-mandrel`|-10.47 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual`|-3.31 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-virtual-leyden`|-1.42 (large)|0.026 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native`|-17.92 (large)|0.000 (✓ significant)|
|`quarkus3-leyden` vs `quarkus3-native-mandrel`|-10.17 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-virtual-leyden`|0.52 (medium)|0.363 (✗ not significant)|
|`quarkus3-virtual` vs `quarkus3-native`|-18.42 (large)|0.000 (✓ significant)|
|`quarkus3-virtual` vs `quarkus3-native-mandrel`|-8.88 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native`|-9.60 (large)|0.000 (✓ significant)|
|`quarkus3-virtual-leyden` vs `quarkus3-native-mandrel`|-7.19 (large)|0.000 (✓ significant)|
|`quarkus3-native` vs `quarkus3-native-mandrel`|-0.16 (negligible)|0.779 (✗ not significant)|

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