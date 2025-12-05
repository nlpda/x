# Week 1 — Process Basics

## Goals
- Map the lifecycle of a Linux process from `fork()` to `execve()`.
- Capture process metadata for rubric evidence on annotated logs.

## Annotated Lab Log
- ✅ Ran a baseline process tree capture to understand parent/child relationships:
  ```bash
  pstree -p | head -n 5
  ```
  ```text
  systemd(1)─┬─cron(672)
             ├─sshd(731)───bash(9124)───pstree(9201)
             └─systemd-journal(457)
  ```
  *Annotation:* Confirmed that shell sessions branch from SSH, which will help justify later scheduling experiments.
- ✅ Observed default process priorities:
  ```bash
  ps -eo pid,ppid,pri,ni,cmd | head -n 5
  ```
  The output highlighted that interactive shells inherit neutral nice values (0), matching the lecture expectations.

## Commands & Scripts
- Collected quick stats with `scripts/process-snapshot.sh`, which stores JSON-like fields for reproducibility.
- Verified script exit codes with `bash -n scripts/process-snapshot.sh` before execution.

## Diagram
```mermaid
graph TD;
  Parent[Parent process] -->|fork()| Child[Child process];
  Child -->|execve()| NewImage[Replaced image];
  Child -->|exit()| Reaper[Reaped by init];
```

## Screenshot References
- `images/week1-process-tree.svg` — simple process tree sketch for lecture recap.

## Reflection
Documented the first-week baseline. Next week will adjust nice values and observe scheduler choices.
