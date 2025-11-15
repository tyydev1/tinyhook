# Quick Start - TinyHook Log Viewer

Get started with the log viewer in 60 seconds!

## 1. Check Prerequisites

```bash
# Check if rich library is installed
python -c "import rich; print('✓ ready to go!')"
```

If you see an error, install rich:
```bash
pip install rich
```

## 2. Run the Log Viewer

```bash
cd /home/razkar/Documents/Workspace/GitHub/tyydev1/tinyhook/ai-workspace
python log_viewer.py
```

## 3. Try These Commands

Once inside the REPL:

```
log-viewer> list          # See all logs
log-viewer> view 1        # View first log
log-viewer> help          # See all commands
log-viewer> exit          # Quit
```

## Common Workflows

### View All Logs
```
log-viewer> list
log-viewer> view 1
```

### Find Errors
```
log-viewer> search ERROR
```

### Filter by Agent
```
log-viewer> filter file-organizer
log-viewer> view 1
```

### Filter by Date
```
log-viewer> filter 2025-11-09
log-viewer> view 1
```

## Tips

- Run `list` first to see what's available
- File numbers come from the `list` command
- Use `clear` to clean up the screen
- Press Ctrl+C to cancel, then type `exit` to quit

## Full Documentation

See `LOG_VIEWER_README.md` for complete documentation.

---

**Happy log viewing!** 📊✨
