# Claude Agents Workspace

This directory contains all agent-generated outputs, logs, and configurations for the TinyHook project.

## Directory Structure

```
.claude/
└── agents/
    ├── README.md           # This file
    ├── logs/               # Agent execution logs organized by date
    │   └── YYYY/MM/DD/     # Date-based directory structure
    ├── prompts/            # (Future) Saved agent prompts for reuse
    └── reports/            # (Future) Summary reports and analysis
```

## Agent Logs (logs/)

Logs are organized by execution date in the format `YYYY/MM/DD/` to maintain clear historical records.

### Naming Convention
Files follow the pattern: `<agent-name>_<shortened-purpose>.<extension>`

Examples:
- `file-organizer_reorganization-suggestion.md` - File organization suggestions
- `code-review_performance-analysis.md` - Code review findings
- `feature-implementer_database-layer.md` - Feature implementation details
- `documentation_api-reference.md` - API documentation

### Creating New Log Entries
1. Create date directory if needed: `logs/2025/11/09/` (use today's date)
2. Name the file descriptively with agent and purpose
3. Use appropriate file extension (.md for markdown, .txt for text, etc.)
4. Keep logs for historical reference and learning

## Best Practices

### For Claude When Creating Logs
- Use clear, descriptive filenames that indicate purpose
- Include timestamps and context at the top of files
- Link to relevant documentation in `../../../docs/`
- Keep markdown files readable with proper formatting
- Include summaries for quick scanning of important outputs

### For the User
- Review agent logs to understand decisions made
- Reference logs when troubleshooting issues
- Use logs as learning materials
- Archive or clean up old logs periodically (optional)

## File Organization Philosophy

Agent logs serve multiple purposes:
1. **Documentation**: Record what AI agents helped with
2. **Audit Trail**: Understand decisions and analysis made
3. **Learning**: Reference for similar future tasks
4. **Traceability**: Connect outputs to specific requests

---

Last updated: November 9, 2025
