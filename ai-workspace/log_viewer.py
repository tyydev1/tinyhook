#!/usr/bin/env python3
"""
TinyHook Log Viewer - Beautiful CLI REPL for viewing agent logs
Author: TinyHook AI Workspace
Created: 2025-11-09
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import re

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.text import Text
    from rich.markdown import Markdown
    from rich import box
except ImportError:
    print("[ERROR] Missing 'rich' library. Install with: pip install rich")
    sys.exit(1)


class LogViewer:
    """Interactive REPL for viewing agent logs from .claude/agents/logs/"""

    def __init__(self, logs_dir: str = None):
        """
        Initialize the log viewer.

        Args:
            logs_dir: Path to logs directory. Defaults to .claude/agents/logs/
        """
        self.console = Console()

        # Determine logs directory
        if logs_dir:
            self.logs_dir = Path(logs_dir)
        else:
            # Assume we're in ai-workspace/ or can access it
            script_dir = Path(__file__).parent
            self.logs_dir = script_dir / ".claude" / "agents" / "logs"

        # Create logs directory if it doesn't exist
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Cache for log files
        self.log_files: List[Path] = []
        self.current_filter: Optional[str] = None

        # Color scheme for log levels
        self.log_colors = {
            "ERROR": "bold red",
            "WARN": "bold yellow",
            "WARNING": "bold yellow",
            "INFO": "cyan",
            "SUCCESS": "bold green",
            "SUGGESTION": "bold magenta",
            "DEBUG": "dim white",
        }

    def show_banner(self):
        """Display welcome banner with ASCII art"""
        banner_text = """
        ╔════════════════════════════════════════════════════════════╗
        ║                                                            ║
        ║       ████████╗██╗███╗   ██╗██╗   ██╗██╗  ██╗ ██████╗    ║
        ║       ╚══██╔══╝██║████╗  ██║╚██╗ ██╔╝██║  ██║██╔═══██╗   ║
        ║          ██║   ██║██╔██╗ ██║ ╚████╔╝ ███████║██║   ██║   ║
        ║          ██║   ██║██║╚██╗██║  ╚██╔╝  ██╔══██║██║   ██║   ║
        ║          ██║   ██║██║ ╚████║   ██║   ██║  ██║╚██████╔╝   ║
        ║          ╚═╝   ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝    ║
        ║                                                            ║
        ║              🔍 Agent Log Viewer v1.0.0 🔍                 ║
        ║                                                            ║
        ║         Beautiful CLI REPL for TinyHook Logs              ║
        ║                                                            ║
        ╚════════════════════════════════════════════════════════════╝
        """

        self.console.print(banner_text, style="bold cyan")
        self.console.print(
            f"\n[dim]📁 Logs Directory: {self.logs_dir.absolute()}[/dim]\n"
        )

    def scan_logs(self) -> List[Path]:
        """
        Recursively scan for all log files in the logs directory.

        Returns:
            List of Path objects for log files
        """
        log_files = []

        if not self.logs_dir.exists():
            self.console.print(
                f"[bold red]ERROR:[/bold red] Logs directory not found: {self.logs_dir}",
                style="red"
            )
            return log_files

        # Recursively find all .md and .txt files
        for ext in ["*.md", "*.txt", "*.log"]:
            log_files.extend(self.logs_dir.rglob(ext))

        # Sort by modification time (newest first)
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        return log_files

    def refresh_logs(self):
        """Refresh the log files cache"""
        self.log_files = self.scan_logs()
        self.console.print(
            f"[bold green]✓[/bold green] Found {len(self.log_files)} log files\n"
        )

    def display_log_list(self, filter_term: Optional[str] = None):
        """
        Display a formatted table of all log files.

        Args:
            filter_term: Optional filter string for filename/agent
        """
        files = self.log_files

        # Apply filter if provided
        if filter_term:
            filter_term_lower = filter_term.lower()
            files = [
                f for f in files
                if filter_term_lower in f.name.lower() or
                   filter_term_lower in str(f.relative_to(self.logs_dir)).lower()
            ]
            self.console.print(
                f"[bold]Filtered results for:[/bold] [cyan]{filter_term}[/cyan]\n"
            )

        if not files:
            self.console.print("[yellow]No log files found.[/yellow]")
            return

        # Create table
        table = Table(
            title=f"📋 Agent Logs ({len(files)} files)",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )

        table.add_column("#", style="dim", width=4)
        table.add_column("Agent", style="cyan", width=20)
        table.add_column("Date", style="green", width=12)
        table.add_column("Size", justify="right", width=8)
        table.add_column("File", style="blue")

        for idx, log_file in enumerate(files, 1):
            # Extract agent name from filename
            filename = log_file.name
            agent_name = filename.split("_")[0] if "_" in filename else "unknown"

            # Get file stats
            stats = log_file.stat()
            size = self._format_size(stats.st_size)
            modified = datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d")

            # Get relative path
            rel_path = str(log_file.relative_to(self.logs_dir))

            table.add_row(
                str(idx),
                agent_name,
                modified,
                size,
                rel_path
            )

        self.console.print(table)
        self.console.print()

    def display_log_content(self, file_path: Path):
        """
        Display the contents of a log file with syntax highlighting.

        Args:
            file_path: Path to the log file
        """
        if not file_path.exists():
            self.console.print(
                f"[bold red]ERROR:[/bold red] File not found: {file_path}",
                style="red"
            )
            return

        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.console.print(
                f"[bold red]ERROR:[/bold red] Failed to read file: {e}",
                style="red"
            )
            return

        # Get file metadata
        stats = file_path.stat()
        size = self._format_size(stats.st_size)
        modified = datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

        # Create header panel
        rel_path = str(file_path.relative_to(self.logs_dir))
        header = f"""
[bold cyan]File:[/bold cyan] {rel_path}
[bold green]Size:[/bold green] {size}
[bold magenta]Modified:[/bold magenta] {modified}
[bold yellow]Lines:[/bold yellow] {len(content.splitlines())}
        """

        self.console.print(
            Panel(
                header.strip(),
                title="📄 Log File Details",
                border_style="cyan",
                box=box.DOUBLE
            )
        )
        self.console.print()

        # Color-code log levels in content
        colored_content = self._colorize_log_content(content)

        # Display content with markdown rendering
        if file_path.suffix == ".md":
            # Render as markdown
            self.console.print(Panel(
                Markdown(content),
                title="📝 Log Content (Markdown)",
                border_style="blue",
                box=box.ROUNDED
            ))
        else:
            # Display as plain text with color coding
            self.console.print(Panel(
                colored_content,
                title="📝 Log Content",
                border_style="blue",
                box=box.ROUNDED
            ))

        self.console.print()

    def search_logs(self, query: str):
        """
        Search for a query string across all log files.

        Args:
            query: Search query string
        """
        results = []
        query_lower = query.lower()

        for log_file in self.log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Search for query (case-insensitive)
                    if query_lower in content.lower():
                        # Count matches
                        matches = len(re.findall(
                            re.escape(query),
                            content,
                            re.IGNORECASE
                        ))
                        results.append((log_file, matches, content))
            except Exception:
                continue

        if not results:
            self.console.print(
                f"[yellow]No results found for:[/yellow] [bold]{query}[/bold]"
            )
            return

        # Display results summary
        table = Table(
            title=f"🔍 Search Results for '{query}' ({len(results)} files)",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )

        table.add_column("#", style="dim", width=4)
        table.add_column("File", style="cyan")
        table.add_column("Matches", justify="right", style="green", width=8)

        for idx, (log_file, match_count, _) in enumerate(results, 1):
            rel_path = str(log_file.relative_to(self.logs_dir))
            table.add_row(str(idx), rel_path, str(match_count))

        self.console.print(table)
        self.console.print()

        # Display preview of first result
        if results:
            self.console.print("[bold]Preview of first match:[/bold]\n")
            first_file, _, content = results[0]

            # Find context around first match
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if query_lower in line.lower():
                    # Show 3 lines before and after
                    start = max(0, i - 3)
                    end = min(len(lines), i + 4)
                    preview_lines = lines[start:end]

                    # Highlight the matching line
                    preview = []
                    for j, pline in enumerate(preview_lines):
                        line_num = start + j + 1
                        if start + j == i:
                            # Highlight query in the line
                            highlighted = re.sub(
                                f"({re.escape(query)})",
                                r"[bold yellow on red]\1[/bold yellow on red]",
                                pline,
                                flags=re.IGNORECASE
                            )
                            preview.append(f"[bold green]{line_num:4d}[/bold green] → {highlighted}")
                        else:
                            preview.append(f"[dim]{line_num:4d}[/dim]   {pline}")

                    self.console.print('\n'.join(preview))
                    break

            self.console.print()

    def view_file_by_number(self, file_num: int):
        """
        View a log file by its list number.

        Args:
            file_num: File number from the list (1-indexed)
        """
        if file_num < 1 or file_num > len(self.log_files):
            self.console.print(
                f"[bold red]ERROR:[/bold red] Invalid file number. Use 1-{len(self.log_files)}",
                style="red"
            )
            return

        log_file = self.log_files[file_num - 1]
        self.display_log_content(log_file)

    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}TB"

    def _colorize_log_content(self, content: str) -> Text:
        """
        Add color coding to log content based on log levels.

        Args:
            content: Raw log content

        Returns:
            Rich Text object with colored content
        """
        text = Text()

        for line in content.split('\n'):
            # Check for log level markers
            colored = False
            for level, color in self.log_colors.items():
                if f"[{level}]" in line.upper():
                    text.append(line + '\n', style=color)
                    colored = True
                    break

            if not colored:
                # Check for timestamps
                if line.strip().startswith('[2') and ']' in line[:30]:
                    text.append(line + '\n', style="dim cyan")
                # Check for section headers (===, ---, ###)
                elif line.strip().startswith('===') or line.strip().startswith('---'):
                    text.append(line + '\n', style="bold magenta")
                elif line.strip().startswith('##'):
                    text.append(line + '\n', style="bold blue")
                else:
                    text.append(line + '\n')

        return text

    def show_help(self):
        """Display help message with available commands"""
        help_text = """
[bold cyan]Available Commands:[/bold cyan]

  [bold green]list[/bold green]              - List all available log files
  [bold green]view <file>[/bold green]       - View log file by number or path
  [bold green]filter <term>[/bold green]     - Filter log list by agent name or date
  [bold green]search <query>[/bold green]    - Search for text across all logs
  [bold green]refresh[/bold green]           - Refresh log files cache
  [bold green]clear[/bold green]             - Clear the screen
  [bold green]help[/bold green]              - Show this help message
  [bold green]exit[/bold green] | [bold green]quit[/bold green]     - Exit the log viewer

[bold cyan]Examples:[/bold cyan]

  list                          - Show all logs
  view 1                        - View first log file from list
  filter file-organizer         - Show only file-organizer logs
  filter 2025-11-09             - Show logs from specific date
  search "ERROR"                - Find all logs containing ERROR
  search "package manager"      - Search for phrase

[bold cyan]Tips:[/bold cyan]

  • Use [bold]list[/bold] first to see all available logs
  • File numbers are from the [bold]list[/bold] command output
  • Search is case-insensitive
  • Filter works on filenames and dates
        """

        self.console.print(Panel(
            help_text.strip(),
            title="📖 Help & Commands",
            border_style="yellow",
            box=box.DOUBLE
        ))
        self.console.print()

    def run(self):
        """Run the interactive REPL"""
        self.show_banner()
        self.refresh_logs()

        self.console.print(
            "[dim]Type 'help' for commands, 'exit' to quit[/dim]\n"
        )

        while True:
            try:
                # Display prompt
                user_input = self.console.input("[bold cyan]log-viewer>[/bold cyan] ")

                # Parse command
                parts = user_input.strip().split(maxsplit=1)
                if not parts:
                    continue

                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                # Handle commands
                if command in ["exit", "quit", "q"]:
                    self.console.print(
                        "\n[bold green]Thanks for using TinyHook Log Viewer! 👋[/bold green]\n"
                    )
                    break

                elif command == "help" or command == "?":
                    self.show_help()

                elif command == "list" or command == "ls":
                    self.display_log_list()

                elif command == "refresh":
                    self.refresh_logs()

                elif command == "view":
                    if not args:
                        self.console.print(
                            "[bold red]ERROR:[/bold red] Usage: view <file_number>",
                            style="red"
                        )
                        continue

                    try:
                        file_num = int(args)
                        self.view_file_by_number(file_num)
                    except ValueError:
                        self.console.print(
                            "[bold red]ERROR:[/bold red] File number must be an integer",
                            style="red"
                        )

                elif command == "filter":
                    if not args:
                        self.console.print(
                            "[bold red]ERROR:[/bold red] Usage: filter <term>",
                            style="red"
                        )
                        continue

                    self.display_log_list(filter_term=args)

                elif command == "search":
                    if not args:
                        self.console.print(
                            "[bold red]ERROR:[/bold red] Usage: search <query>",
                            style="red"
                        )
                        continue

                    self.search_logs(args)

                elif command == "clear" or command == "cls":
                    os.system('clear' if os.name != 'nt' else 'cls')
                    self.show_banner()

                else:
                    self.console.print(
                        f"[bold red]ERROR:[/bold red] Unknown command: {command}",
                        style="red"
                    )
                    self.console.print(
                        "[dim]Type 'help' to see available commands[/dim]\n"
                    )

            except KeyboardInterrupt:
                self.console.print(
                    "\n\n[bold yellow]Interrupted. Type 'exit' to quit.[/bold yellow]\n"
                )
                continue

            except Exception as e:
                self.console.print(
                    f"\n[bold red]ERROR:[/bold red] {str(e)}",
                    style="red"
                )
                self.console.print()


def main():
    """Entry point for the log viewer"""
    # Parse command-line arguments
    logs_dir = None
    if len(sys.argv) > 1:
        logs_dir = sys.argv[1]

    viewer = LogViewer(logs_dir=logs_dir)
    viewer.run()


if __name__ == "__main__":
    main()
