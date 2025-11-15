# AI Workspace Index

This directory contains all AI-generated documentation, guides, and logs for the TinyHook project.

## Directory Structure

```
ai-workspace/
├── INDEX.md                           # This file - navigation guide
├── docs/                              # All documentation organized by type
│   ├── courses/                       # Complete learning courses
│   │   └── PACKAGE_MANAGER_COURSE.md # Full 4-6 week course on package manager architecture
│   ├── guides/                        # Quick reference guides and how-tos
│   │   └── QUICK_START.md             # Getting started quickly (2 minute setup)
│   └── testing/                       # Test documentation
│       ├── TEST_GUIDE.md              # Comprehensive testing guide
│       ├── TEST_EXAMPLES.md           # Specific test examples with code snippets
│       └── TESTING_SUMMARY.md         # Overview and statistics
└── .claude/                           # Claude-specific configuration
    └── agents/                        # Agent logs and utilities
        ├── README.md                  # Agent workspace documentation
        ├── log_viewer.py              # CLI utility for viewing agent logs
        └── logs/                      # Organized by date (YYYY/MM/DD)
            └── 2025/11/09/            # Date-based log directory
                └── file-organizer_reorganization-suggestion.md
```

## Quick Navigation

### For Learning
- **New to TinyHook?** Start with `docs/guides/QUICK_START.md` (2 minutes)
- **Want deep understanding?** Read `docs/courses/PACKAGE_MANAGER_COURSE.md` (4-6 weeks)

### For Testing
- **Running tests?** See `docs/guides/QUICK_START.md` for commands
- **Understanding test coverage?** Check `docs/testing/TEST_GUIDE.md`
- **Specific test examples?** Review `docs/testing/TEST_EXAMPLES.md`
- **Test statistics?** See `docs/testing/TESTING_SUMMARY.md`

## File Organization Principles

### Docs Directory
- **courses/**: Complete structured learning materials (larger files, comprehensive)
- **guides/**: Quick-start guides, how-tos, reference docs (accessible, specific)
- **testing/**: Test documentation, examples, and reports

### Agent Logs
- **Date-based organization**: `.claude/agents/logs/YYYY/MM/DD/`
- **Naming convention**: `<agent-name>_<shortened-purpose>.<extension>`
- **Examples**:
  - `file-organizer_reorganization-suggestion.md`
  - `code-review_performance-analysis.md`
  - `feature-implementer_database-layer.md`

## File Sizes (as of organization)
- PACKAGE_MANAGER_COURSE.md: 75KB (comprehensive course)
- QUICK_START.md: 8.6KB (quick reference)
- TEST_GUIDE.md: 15.3KB (detailed guide)
- TEST_EXAMPLES.md: 15.3KB (code examples)
- TESTING_SUMMARY.md: 13.4KB (overview)

## Future Organization Notes

### When Adding New Documentation
1. Determine the type: course, guide, testing reference, or other
2. Place in appropriate subdirectory under `docs/`
3. Update this INDEX.md with new entry
4. Consider cross-referencing related documents

### When Creating Agent Logs
1. Create date directory if not exists: `.claude/agents/logs/YYYY/MM/DD/`
2. Name file: `<agent-name>_<purpose>.<ext>`
3. Link to relevant docs if applicable
4. Keep logs for historical reference

### Recommended Future Directories
- `docs/architecture/` - System design and architecture diagrams
- `docs/api/` - API documentation (when needed)
- `docs/examples/` - Standalone code examples
- `.claude/agents/reports/` - Agent analysis reports and summaries
- `.claude/agents/prompts/` - Saved agent prompts for reuse

## Accessing Documentation
All documentation follows these patterns:
- Markdown format for readability and version control
- Links between related documents
- Clear headings and table of contents
- Code examples with syntax highlighting
- Summary sections for quick scanning

---

Last organized: November 9, 2025
