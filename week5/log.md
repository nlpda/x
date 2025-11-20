# Week 5 — File Systems

## Goals
- Trace inode lookups and cache effects using `strace` and `statx`.
- Document command outputs for rubric coverage.

## Annotated Lab Log
- ✅ Measured metadata path length via `strace`:
  ```bash
  strace -c -e statx,openat ./scripts/fs-probe.sh
  ```
  ```text
  % time     seconds  usecs/call     calls    errors syscall
  ------ ----------- ----------- --------- --------- ----------------
   42.00    0.000120           6        20           statx
  ```
  *Annotation:* Repeated `statx` calls dominate microbenchmark time when cache is cold.
- ✅ Compared cached access:
  ```bash
  ./scripts/fs-probe.sh --warm
  strace -c -e statx,openat ./scripts/fs-probe.sh --warm
  ```
  *Annotation:* Cached run reduces syscall count because content is already in page cache.

## Diagram
```mermaid
graph TD;
  App[User process] -->|open()| VFS[VFS layer];
  VFS -->|lookup| DCache[dentry cache];
  DCache -->|hit| Inode[Inode struct];
  DCache -->|miss| Disk[Disk I/O];
```

## Screenshot References
- `images/week5-vfs.svg` — Visual showing VFS, dentry cache, and inode path.

## Reflection
File system probes reveal how cold caches punish metadata-heavy workloads. Plan to profile ext4 journaling next.
