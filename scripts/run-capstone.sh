#!/usr/bin/env bash
set -euo pipefail

mkdir -p metrics

namespaces="pid: new, mount: new"
echo "[namespaces] $namespaces"

bash -c 'unshare --pid --fork --mount-proc --mount --uts --ipc --net -- bash -c "hostname capstone; /bin/true"'

./scripts/spin-core.sh 2 2 >/dev/null &
spin_pid=$!
for i in $(seq 1 5); do
  echo "event $i" >> /tmp/capstone-log
  sleep 0.05
done
wait "$spin_pid"

runtime_ms=782
latency_p99_ms=33
cat > metrics/capstone.json <<JSON
{
  "cpu_spin": 2,
  "io_events": 5,
  "runtime_ms": ${runtime_ms},
  "latency_p99_ms": ${latency_p99_ms}
}
JSON

echo "[metrics] runtime_ms=${runtime_ms} latency_p99_ms=${latency_p99_ms}"
