#!/usr/bin/env bash
set -euo pipefail
threads=${1:-1}
duration=${2:-5}

echo "[spin-core] threads=${threads} duration=${duration}s" >&2
for _ in $(seq 1 "$threads"); do
  (
    end=$((SECONDS+duration))
    while (( SECONDS < end )); do :; done
  ) &
done
wait
