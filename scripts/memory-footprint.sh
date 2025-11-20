#!/usr/bin/env bash
set -euo pipefail
stress_mb=${1:-16}
if [[ "${1:-}" == "--stress" ]]; then
  stress_mb=${2:-64}
fi

echo "[memory-footprint] allocating ${stress_mb}MB"
python - <<'PY'
import os, sys, time
mb = int(sys.argv[1])
block = b"0" * (1024 * 1024)
buffer = []
for _ in range(mb):
    buffer.append(block)
    if _ % 8 == 0:
        time.sleep(0.01)
print(f"pid={os.getpid()} allocated_mb={mb}")
time.sleep(2)
PY
"$stress_mb"
