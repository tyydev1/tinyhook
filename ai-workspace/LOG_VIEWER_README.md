# TinyHook Log Viewer

Beautiful CLI REPL application for viewing and analyzing agent logs from the TinyHook AI workspace.

## Features

- **Interactive REPL Interface** - Command-line interface with beautiful formatting
- **List All Logs** - Recursively scans `.claude/agents/logs/` directory
- **View Log Contents** - Display logs with syntax highlighting and markdown rendering
- **Filter Logs** - Filter by agent name, date, or keywords
- **Search Functionality** - Full-text search across all log files with context preview
- **Beautiful Output** - Color-coded log levels and professional formatting using `rich` library
- **File Metadata** - Shows file size, modification date, and line count

## Installation

### Prerequisites

The log viewer requires the `rich` library for beautiful terminal formatting:

```bash
pip install rich
```

### Verify Installation

```bash
python -c "import rich; print('rich library available')"
```

## Usage

### Basic Usage

Run the log viewer from the `ai-workspace/` directory:

```bash
python log_viewer.py
```

Or run from anywhere by specifying the logs directory:

```bash
python /path/to/ai-workspace/log_viewer.py /path/to/logs/directory
```

### Available Commands

Once inside the REPL, you can use these commands:

| Command | Description | Example |
|---------|-------------|---------|
| `list` or `ls` | List all available log files | `list` |
| `view <number>` | View a specific log file by number | `view 1` |
| `filter <term>` | Filter logs by agent name or date | `filter file-organizer` |
| `search <query>` | Search for text across all logs | `search ERROR` |
| `refresh` | Refresh the log files cache | `refresh` |
| `clear` or `cls` | Clear the screen | `clear` |
| `help` or `?` | Show help message | `help` |
| `exit` or `quit` or `q` | Exit the log viewer | `exit` |

### Command Examples

**List all logs:**
```
log-viewer> list
```

**View the first log file:**
```
log-viewer> view 1
```

**Filter by agent name:**
```
log-viewer> filter file-organizer
```

**Filter by date:**
```
log-viewer> filter 2025-11-09
```

**Search for errors:**
```
log-viewer> search ERROR
```

**Search for phrases:**
```
log-viewer> search "package manager"
```

## Color Coding

The log viewer automatically color-codes log content:

- **ERROR** - Bold Red
- **WARN/WARNING** - Bold Yellow
- **INFO** - Cyan
- **SUCCESS** - Bold Green
- **SUGGESTION** - Bold Magenta
- **DEBUG** - Dim White
- **Timestamps** - Dim Cyan
- **Headers** (##, ===, ---) - Bold Blue/Magenta

## File Structure

The log viewer expects logs to be organized in this structure:

```
ai-workspace/
└── .claude/
    └── agents/
        └── logs/
            └── YYYY/
                └── MM/
                    └── DD/
                        └── agent-name_description.md
```

## Tips

1. **Start with `list`** - Always run `list` first to see all available logs
2. **Use file numbers** - File numbers from `list` output can be used with `view`
3. **Case-insensitive search** - All searches are case-insensitive
4. **Filter flexibility** - Filter works on both filenames and directory paths
5. **Markdown rendering** - `.md` files are rendered with proper markdown formatting
6. **Context in search** - Search results show 3 lines before and after the match

## Troubleshooting

### Missing `rich` library

If you see:
```
[ERROR] Missing 'rich' library. Install with: pip install rich
```

Install the required library:
```bash
pip install rich
```

### Logs directory not found

If you see:
```
ERROR: Logs directory not found
```

Ensure you're running the script from the correct location or specify the logs directory:
```bash
python log_viewer.py /path/to/.claude/agents/logs
```

### Permission denied

Make the script executable:
```bash
chmod +x log_viewer.py
```

## Architecture

### LogViewer Class

The main class that handles all functionality:

- `__init__()` - Initialize the viewer with logs directory
- `show_banner()` - Display welcome banner
- `scan_logs()` - Recursively find all log files
- `refresh_logs()` - Refresh the log files cache
- `display_log_list()` - Show formatted table of logs
- `display_log_content()` - Display log file with highlighting
- `search_logs()` - Full-text search with preview
- `view_file_by_number()` - View log by list number
- `show_help()` - Display help message
- `run()` - Main REPL loop

### Helper Methods

- `_format_size()` - Human-readable file sizes
- `_colorize_log_content()` - Add color coding to content

## Example Session

```
        ╔════════════════════════════════════════════════════════════╗
        ║              🔍 Agent Log Viewer v1.0.0 🔍                 ║
        ║         Beautiful CLI REPL for TinyHook Logs              ║
        ╚════════════════════════════════════════════════════════════╝

📁 Logs Directory: /home/user/tinyhook/ai-workspace/.claude/agents/logs

✓ Found 1 log files

Type 'help' for commands, 'exit' to quit

log-viewer> list

┌─────────────────────── 📋 Agent Logs (1 files) ────────────────────────┐
│ #    │ Agent            │ Date       │   Size │ File                  │
├──────┼──────────────────┼────────────┼────────┼───────────────────────┤
│ 1    │ file-organizer   │ 2025-11-09 │ 10.2KB │ 2025/11/09/file-or... │
└──────┴──────────────────┴────────────┴────────┴───────────────────────┘

log-viewer> view 1

╔═════════════════════ 📄 Log File Details ══════════════════════╗
║ File: 2025/11/09/file-organizer_reorganization-suggestion.md  ║
║ Size: 10.2KB                                                   ║
║ Modified: 2025-11-09 14:30:00                                  ║
║ Lines: 275                                                     ║
╚════════════════════════════════════════════════════════════════╝

[Log content displayed here with beautiful formatting...]

log-viewer> exit

Thanks for using TinyHook Log Viewer! 👋
```

## Contributing

This tool is part of the TinyHook AI workspace. Improvements and suggestions are welcome!

## License

Part of the TinyHook project. See main project for licensing.

---

**Created:** 2025-11-09  
**Version:** 1.0.0  
**Author:** TinyHook AI Workspace
