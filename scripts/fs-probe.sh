#!/usr/bin/env bash
set -euo pipefail
mode=${1:-"--cold"}
target_dir=${TMPDIR:-/tmp}/fs-probe
mkdir -p "$target_dir"

if [[ "$mode" == "--cold" ]]; then
  sudo_sync=${SUDO_SYNC:-0}
  [[ "$sudo_sync" == "1" ]] && sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches >/dev/null
fi

for i in $(seq 1 20); do
  touch "$target_dir/file-$i"
  stat -c "%n %i" "$target_dir/file-$i" >/dev/null
  rm -f "$target_dir/file-$i"
done

echo "[fs-probe] completed mode=$mode"
