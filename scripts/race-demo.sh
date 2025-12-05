#!/usr/bin/env bash
set -euo pipefail
iterations=${1:-1000}
mutex=${MUTEX:-0}

counter=0
inc() {
  tmp=$counter
  tmp=$((tmp+1))
  counter=$tmp
}

if [[ "$mutex" == "1" ]]; then
  inc() {
    { flock 200; 
      tmp=$counter
      tmp=$((tmp+1))
      counter=$tmp
    } 200>/tmp/race-demo.lock
  }
fi

echo "[race-demo] iterations=${iterations} mutex=${mutex}"
for _ in $(seq 1 "$iterations"); do inc; done

expected=$iterations
if [[ $counter -ne $expected ]]; then
  echo "Final counter (unsynchronized): $counter"
  echo "Warning: lost updates detected"
else
  if [[ "$mutex" == "1" ]]; then
    echo "Final counter (mutex): $counter"
  else
    echo "Final counter: $counter"
  fi
fi
