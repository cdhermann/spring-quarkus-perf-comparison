#!/usr/bin/env bash

callingdir="$(pwd)"
thisdir="$(realpath $(dirname "$0"))"

# Check if jbang is installed
if ! command -v jbang >/dev/null 2>&1; then
  echo "Error: jbang is not installed."
  echo "Please install jbang from https://www.jbang.dev/ before running this script."
  exit 1
fi

# Ensure the port is free before enabling halt-on-error
kill $(lsof -t -i:8080) &>/dev/null

# Ensure infrastructure/DB is down (sanity check)
${thisdir}/infra.sh -d

set -euo pipefail

# Start infrastructure (e.g., Database)
${thisdir}/infra.sh -s

# Resource Management Notes:
# -XX:ActiveProcessorCount doesn't strictly limit available cores, but guides thread pool sizing.
# On Quarkus/Spring (Virtual Threads), this affects the Loom ForkJoin pool and Netty loops.
# For .NET, we use DOTNET_ProcessorCount to achieve similar behavior.

if [ "$1" = "dotnet10" ]; then
  echo "Starting .NET 10 Application..."

  # .NET Environment variables to mimic Java -Xmx and -XX:ActiveProcessorCount:
  # DOTNET_GCHeapHardLimit: Hard memory limit in hex (0x20000000 = 512MB)
  # DOTNET_ProcessorCount: Limits the CPU cores the runtime perceives
  # DOTNET_gcServer: Enables Server GC for high-throughput
  export DOTNET_GCHeapHardLimit=0x20000000
  export DOTNET_ProcessorCount=4
  export DOTNET_gcServer=1

  # Launch the .NET binary
  Logging__LogLevel__Default=None  ${callingdir}/dotnet10/publish/dotnet10 &
else
  echo "Starting Java Application..."
  
  # Standard Java execution with memory and CPU constraints
  java -XX:ActiveProcessorCount=4 -Xms512m -Xmx512m -jar ${callingdir}/$1 &
fi

# Give the app a chance to fully start before throwing load at it
sleep 20

# Run benchmark using hyperfoil via jbang
jbang wrk@hyperfoil -t2 -c100 -d20s --timeout 1s http://localhost:8080/fruits

# Cleanup: Shut down infrastructure and kill the application process
${thisdir}/infra.sh -d
kill $(lsof -t -i:8080) &>/dev/null
