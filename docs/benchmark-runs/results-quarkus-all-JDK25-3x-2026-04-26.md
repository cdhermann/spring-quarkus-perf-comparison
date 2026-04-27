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

|Runtime|I0|I1|I2|Average|
|---|---|---|---|---|
|`quarkus3-jvm`|8.16|8.25|8.40|**8.27**|
|`quarkus3-leyden`|51.86|52.08|52.28|**52.07**|
|`quarkus3-virtual`|8.06|8.23|8.19|**8.16**|
|`quarkus3-virtual-leyden`|53.05|53.44|53.06|**53.18**|
|`quarkus3-native`|155.01|155.43|155.10|**155.18**|
|`quarkus3-native-mandrel`|152.13|151.63|152.41|**152.06**|

### Time to First Request (milliseconds)

|Runtime|I0|I1|I2|Average|
|---|---|---|---|---|
|`quarkus3-jvm`|2,679.90|2,631.63|2,673.14|**2,661.55**|
|`quarkus3-leyden`|986.95|944.58|1,033.39|**988.31**|
|`quarkus3-virtual`|2,553.95|2,626.64|2,596.66|**2,592.42**|
|`quarkus3-virtual-leyden`|883.69|935.30|832.43|**883.81**|
|`quarkus3-native`|102.32|120.55|107.87|**110.25**|
|`quarkus3-native-mandrel`|110.93|122.83|122.32|**118.69**|

### RSS at Startup — before any request (MiB)

|Runtime|I0|I1|I2|Average|
|---|---|---|---|---|
|`quarkus3-jvm`|272.54|272.41|271.69|**272.21**|
|`quarkus3-leyden`|235.43|235.27|237.75|**236.15**|
|`quarkus3-virtual`|272.96|273.85|275.34|**274.05**|
|`quarkus3-virtual-leyden`|220.58|232.14|220.46|**224.39**|
|`quarkus3-native`|89.84|89.86|89.86|**89.86**|
|`quarkus3-native-mandrel`|89.49|89.51|89.51|**89.51**|

### RSS after First Request (MiB)

|Runtime|I0|I1|I2|Average|
|---|---|---|---|---|
|`quarkus3-jvm`|295.83|287.86|289.46|**291.05**|
|`quarkus3-leyden`|244.42|244.08|255.63|**248.04**|
|`quarkus3-virtual`|294.71|297.33|303.04|**298.36**|
|`quarkus3-virtual-leyden`|248.78|247.67|244.89|**247.11**|
|`quarkus3-native`|95.73|95.75|95.77|**95.75**|
|`quarkus3-native-mandrel`|95.41|95.41|95.43|**95.42**|

### RSS under Load (MiB)

|Runtime|I0|I1|I2|Average|
|---|---|---|---|---|
|`quarkus3-jvm`|788.77|784.87|785.34|**786.33**|
|`quarkus3-leyden`|743.29|698.95|721.98|**721.41**|
|`quarkus3-virtual`|710.64|690.35|701.25|**700.75**|
|`quarkus3-virtual-leyden`|643.70|646.88|631.02|**640.53**|
|`quarkus3-native`|240.41|287.93|225.91|**251.42**|
|`quarkus3-native-mandrel`|286.44|285.25|—|**285.84**|

### Throughput (req/sec)

|Runtime|I0|I1|I2|Average|
|---|---|---|---|---|
|`quarkus3-jvm`|18,653|18,302|18,220|**18,392**|
|`quarkus3-leyden`|16,448|15,579|16,691|**16,240**|
|`quarkus3-virtual`|16,571|16,881|16,997|**16,816**|
|`quarkus3-virtual-leyden`|15,322|15,471|16,111|**15,635**|
|`quarkus3-native`|8,376|8,380|8,378|**8,378**|
|`quarkus3-native-mandrel`|8,528|8,635|—|**8,582**|

### Throughput Density (req/sec per MiB of RSS under load)

|Runtime|I0|I1|I2|Max|
|---|---|---|---|---|
|`quarkus3-jvm`|23.65|23.32|23.20|**23.65**|
|`quarkus3-leyden`|22.13|22.29|23.12|**23.12**|
|`quarkus3-virtual`|23.32|24.45|24.24|**24.45**|
|`quarkus3-virtual-leyden`|23.80|23.92|25.53|**25.53**|
|`quarkus3-native`|34.84|29.10|37.08|**37.08**|
|`quarkus3-native-mandrel`|29.77|30.27|—|**30.27**|

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

*Generated by `scripts/perf-lab/generate-report.py` from the [spring-quarkus-perf-comparison](https://github.com/quarkusio/spring-quarkus-perf-comparison) perf-lab tooling.*