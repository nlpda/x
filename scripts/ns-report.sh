#!/usr/bin/env bash
set -euo pipefail
ns=${1:-pid}

case "$ns" in
  pid)
    unshare --pid --fork --mount-proc bash -c 'echo "Namespace: pid"; ps -o pid,cmd'
    ;;
  mount)
    unshare --mount bash -c 'echo "Namespace: mount"; mount | grep proc | head -n 1; mount --make-rprivate /tmp; echo "/tmp bind: private"'
    ;;
  *)
    echo "usage: $0 [pid|mount]" >&2
    exit 1
    ;;
esac
