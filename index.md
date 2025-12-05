# CMPN202 Operating Systems Project Journal

Welcome to the CMPN202 Operating Systems GitHub Pages site. Use this landing page to navigate weekly logs, check rubric alignment, and review deployment notes.

## Navigation
- [Week 1: Process Basics](week1/log.md)
- [Week 2: Scheduling Strategies](week2/log.md)
- [Week 3: Synchronization](week3/log.md)
- [Week 4: Memory Management](week4/log.md)
- [Week 5: File Systems](week5/log.md)
- [Week 6: Virtualization](week6/log.md)
- [Week 7: Systems Integration](week7/log.md)
- [Supporting Scripts](scripts/)
- [Images and Diagrams](images/)

## Rubric Mapping
| Rubric Area | Evidence | Location |
| --- | --- | --- |
| Annotated experimentation logs | Weekly log sections include command outputs and annotations | `week*/log.md` |
| Diagrams and visual aids | Inline mermaid diagrams and linked SVG assets | `week*/log.md`, `images/` |
| Automation/scripts | Repeatable scripts for tracing, stats collection, and cleanup | `scripts/` |
| Reflection and next steps | End-of-week reflection in each log | `week*/log.md` |
| Deployment readiness | GitHub Pages config and navigation | `_config.yml`, `index.md` |

## Deployment Notes
1. Enable GitHub Pages using the `main` branch and root directory. The Jekyll configuration below disables layouts, making Markdown render cleanly.
2. Verify that `_config.yml` is at the repository root and includes `theme: minima` for simple styling.
3. After pushing, wait a few minutes for Pages to build. Check the **Pages** tab in repository settings for status.
4. Use relative links (as above) so navigation works in both the GitHub UI and the published site.
5. To add screenshots or diagrams, drop assets into `images/` and reference them from the appropriate weekly log.
