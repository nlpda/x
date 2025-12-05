#!/usr/bin/env bash
set -euo pipefail

echo "[process-snapshot] collecting top five processes" >&2
ps -eo pid,ppid,comm,pri,ni --sort=-pri | head -n 6 | awk 'NR>1 {printf "{\"pid\":%s,\"ppid\":%s,\"cmd\":\"%s\",\"pri\":%s,\"ni\":%s}\n", $1,$2,$3,$4,$5}'
