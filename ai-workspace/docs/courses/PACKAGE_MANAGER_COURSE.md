# TinyHook Mastery: A Complete Course in Package Manager Architecture

**For: Advanced learner building systems from first principles**
**Duration: 4-6 weeks of focused learning**
**Philosophy: Understanding > Completion**

---

## Course Overview

You're not just building a package manager. You're learning how dependency resolution, file systems, version constraints, and network operations form a cohesive system. By the end, you'll understand why `pip`, `npm`, and `cargo` work the way they do - and you'll have built your own.

This course treats you as a systems architect, not a tutorial follower. Every concept connects to the bigger picture. Every exercise reveals a new insight.

---

## Module 1: The Package Manager Mental Model

### Learning Objectives
- Understand what package managers actually do at a systems level
- Map the data flow through a package manager's lifecycle
- Identify the four core responsibilities of any package manager
- Connect package management to language design (your Languages Saga experience)

### Core Concept: What IS a Package Manager?

A package manager is a **dependency graph resolver** combined with a **file system orchestrator**.

Think of it like this: When you designed FlowScript's node system, you had to think about how data flows from one node to another. A package manager does the same thing, but with code files instead of runtime data:

```
User requests Package A
    ↓
Package A requires Package B (dependency)
    ↓
Package B requires Package C (transitive dependency)
    ↓
Resolve order: C → B → A
    ↓
Download files
    ↓
Copy to local storage
    ↓
Update database
```

**The Four Core Responsibilities:**

1. **Registry Management** - Where do packages come from? (repo.json in your case)
2. **Dependency Resolution** - What order do things install? (graph traversal)
3. **File Operations** - How do we get code onto disk? (shutil + pathlib)
4. **State Tracking** - What's installed? (installed.json database)

### Connection to Your Experience

Remember your calculator's architecture?
- **Lexer** → Tokenizes input
- **Parser** → Builds structure (handles precedence)
- **Interpreter** → Executes

A package manager has similar stages:
- **Request Handler** → Parses user command
- **Dependency Resolver** → Builds installation order (like parser precedence!)
- **Installer** → Executes the plan

The parser handled operator precedence (`2 + 3 * 4` → multiply first). The dependency resolver handles installation order (install C before B before A).

### Why This Matters

Every programming language eventually needs a package manager:
- Python → pip
- JavaScript → npm
- Rust → cargo
- Your FlowScript → would need TinyHook or similar

Understanding this system means you can build one for ANY language you create.

### Exercise 1.1: Map Your Own Package Manager
**Goal**: Understand the full data flow

Draw a diagram (on paper or mentally) showing:
1. Where package metadata lives (registry)
2. How a user requests a package (CLI)
3. What happens to check if it's installed (database query)
4. Where files get copied (file system)
5. How state updates (database write)

**Success Criteria**: You can explain each step without looking at code

**Hint**: Start with `python thpu.py hook requests` and trace what SHOULD happen

### Exercise 1.2: Comparative Analysis
**Goal**: Learn from existing systems

Pick ONE real package manager (pip, npm, or cargo) and research:
- Where does it store installed packages? (`~/.local/lib/python3.x/site-packages`, `node_modules`, `~/.cargo`)
- Where does it store metadata? (pip: `site-packages/*.dist-info`)
- How does it know what's installed? (Various database formats)

**Success Criteria**: You can explain one design decision they made and WHY

**Hint**: This isn't about copying them - it's about understanding the problem space

### Exercise 1.3: Design Before Code
**Goal**: Think architecturally

Before writing ANY code, answer these questions:
1. If someone runs `hook packageA` but packageA needs packageB, what should happen?
2. If a package is already installed, should we re-install it? Why or why not?
3. If a download fails halfway through, how do we avoid corrupted state?
4. Where should package files live? Why?

**Success Criteria**: You have opinionated answers based on reasoning

**Hint**: There's no "right" answer - but there are tradeoffs. What matters is understanding the tradeoffs.

---

## Module 2: Data Storage & Retrieval - The Database Layer

### Learning Objectives
- Design JSON schemas that balance simplicity and extensibility
- Implement ACID-like properties with file-based storage
- Understand when to normalize vs denormalize data
- Build a mental model of database operations

### Core Concept: Your Database Is Just Structured State

You already have `installed.json` and `repo.json`. But why JSON? And why those schemas?

**Why JSON?**
- Human-readable (you can debug by opening the file)
- Python's `json` module is built-in (no dependencies)
- Supports nested structures (packages can have complex metadata)
- Easy to validate and migrate

But JSON has limitations:
- No transactions (what if the program crashes mid-write?)
- No indexing (finding a package = reading entire file)
- No relationships (dependencies are just string names)

These limitations are FINE for TinyHook v1. Understanding them prepares you for TinyDB later.

### The Database Schema Design Problem

Look at your current `installed.json` schema:

```json
{
  "package-name": {
    "version": "1.0.0",
    "installed_at": "timestamp",
    "source_type": "local_path",
    "source_value": "path",
    "install_path": "data/packages/package-name"
  }
}
```

**Good Decisions:**
- Top-level package name as key (O(1) lookup in Python dict)
- Version stored separately (enables version checking)
- Timestamps track when things were installed (debugging)

**Future Problems:**
- What if multiple versions of the same package?
- What if a package has dependencies? (Not stored!)
- What if we need to track download URLs separately from local paths?

### Normalization vs Denormalization

**Normalized** (separate tables):
```json
// packages.json
{"requests": {"version": "1.0.0"}}

// dependencies.json
{"requests": ["urllib3", "chardet"]}

// timestamps.json
{"requests": "2025-01-15"}
```

**Denormalized** (everything together):
```json
{
  "requests": {
    "version": "1.0.0",
    "dependencies": ["urllib3", "chardet"],
    "installed_at": "2025-01-15"
  }
}
```

TinyHook uses **denormalization** - all package data in one place. Why?
- Simpler to read/write (one file operation)
- Faster lookups (one dict access)
- Easier to understand (all info in one place)

Tradeoff: Data duplication if packages share dependencies.

### The ACID Problem (Atomicity, Consistency, Isolation, Durability)

What happens if your program crashes here?

```python
data = read_db("installed.json")
data["requests"] = {"version": "1.0.0"}  # Added to memory
# CRASH HAPPENS HERE
write_db(data, "installed.json")  # Never reached
```

The package files might be copied to disk, but the database never updated. Now your state is **inconsistent**.

Real package managers solve this with:
- **Atomic writes** - Write to temp file, then rename (rename is atomic on Unix)
- **Lock files** - Prevent concurrent access
- **Transaction logs** - Record what WILL happen before doing it

For TinyHook v1, you can use a simple atomic write pattern:

```python
import json
import os
import tempfile

def write_db_atomic(data, file_path):
    """Write data atomically - either fully succeeds or fully fails"""
    # Write to temporary file first
    dir_name = os.path.dirname(file_path)
    with tempfile.NamedTemporaryFile(
        mode='w',
        dir=dir_name,
        delete=False
    ) as tmp_file:
        json.dump(data, tmp_file, indent=2)
        tmp_name = tmp_file.name

    # Atomically replace old file with new file
    os.replace(tmp_name, file_path)
```

**Why this works**: `os.replace()` is atomic on most systems. Either the new file replaces the old one completely, or nothing happens.

### Exercise 2.1: Schema Evolution
**Goal**: Design for future growth

Your current schema doesn't store dependencies. Design a NEW schema that includes:
- Package name
- Version
- Dependencies (list of package names)
- Install timestamp
- Source information

Write the JSON structure (not Python code, just the JSON example).

**Success Criteria**: Your schema can represent a package with 3 dependencies

**Hint**: Think about FlowScript's node syntax - how did you represent inputs and outputs?

### Exercise 2.2: Implement Atomic Writes
**Goal**: Prevent corrupted state

Modify your `write_db()` function to use the atomic write pattern shown above.

Then test it:
1. Add a package to installed.json
2. Verify the file updates correctly
3. Add a package but manually interrupt the program (Ctrl+C during write)
4. Check if the file is corrupted or intact

**Success Criteria**: File is never corrupted, even with forced crashes

**Hint**: The temporary file is the secret - write fully, THEN swap

### Exercise 2.3: Query Performance Analysis
**Goal**: Understand lookup complexity

Current implementation loads entire JSON file for every operation. Analyze:

1. What's the time complexity of checking if a package is installed?
2. What if you have 1,000 packages installed?
3. Could you use indexing? How?
4. What about caching the database in memory?

Write your analysis as comments in code or a separate note.

**Success Criteria**: You can explain O(n) vs O(1) lookup and propose an optimization

**Hint**: Python dicts are hash tables - that's already O(1)! But reading the file is O(n) in file size.

### Exercise 2.4: Database Migration
**Goal**: Change schema without breaking existing installations

Suppose you want to add a `dependencies` field to every package in `installed.json`.

Write a migration function that:
1. Reads the old schema
2. Adds `dependencies: []` to every package
3. Writes the new schema

Make it safe (don't lose data if it fails).

**Success Criteria**: Old installed.json transforms to new format without data loss

**Hint**: Read → Transform → Write (atomic). Keep a backup.

---

## Module 3: File System Operations - The Orchestration Layer

### Learning Objectives
- Understand cross-platform path handling with pathlib
- Implement safe copy/move/delete operations
- Handle permission errors and disk space issues
- Design directory structures that scale

### Core Concept: The File System Is Your Package Storage

Package managers are file orchestrators. They take code from one place (remote server, local directory, git repo) and put it in another place (install directory) while maintaining organization.

**The Three File Operations:**

1. **Copy** - Duplicate files from source to destination
2. **Move** - Transfer files (used for temp → final location)
3. **Delete** - Remove files when uninstalling

Every operation has failure modes:
- Source doesn't exist
- Destination already exists
- Permission denied
- Disk full
- Operation interrupted mid-copy

### Why pathlib Over os.path?

You know `pathlib` already. Here's WHY it's better:

**Old way (os.path):**
```python
import os
path = os.path.join("data", "packages", pkg_name)
if os.path.exists(path):
    os.makedirs(path)
```

**New way (pathlib):**
```python
from pathlib import Path
path = Path("data") / "packages" / pkg_name
path.mkdir(parents=True, exist_ok=True)
```

**Why pathlib wins:**
- `/` operator for joining paths (cleaner syntax)
- Methods on the path object (`.exists()`, `.mkdir()`)
- Cross-platform automatically (Windows vs Unix paths)
- Returns Path objects (chainable operations)

### The Directory Structure Decision

Where should packages live? You have:

```
data/
├── installed.json
└── packages/
    ├── requests/
    │   ├── __init__.py
    │   └── ...
    └── flask/
        ├── __init__.py
        └── ...
```

**Design questions:**
1. Why `data/packages/` instead of just `packages/`?
2. Should each package get a version subdirectory? (`packages/requests/1.0.0/`)
3. What about package metadata? (`.dist-info/` directories like pip?)

**Reasoning:**
- `data/` separates code (thpu.py) from state (packages, databases)
- Flat structure (no version dirs) for TinyHook v1 keeps it simple
- Metadata goes in installed.json (not filesystem) for now

### Copy vs Move vs Symlink

**Copy** (what you'll use most):
```python
import shutil
shutil.copytree(source_dir, dest_dir)
```
- Duplicates all files
- Source and destination independent
- Takes disk space

**Move** (for temp files):
```python
shutil.move(temp_dir, final_dir)
```
- Removes source after copying
- Atomic if on same filesystem
- Used for staged installs (download to temp, move to final)

**Symlink** (advanced):
```python
path.symlink_to(target)
```
- Creates link to original (no duplication)
- Changes to original affect symlink
- npm uses this for global packages

TinyHook v1 uses **copy** for simplicity. Later versions could use symlinks for space efficiency.

### Safe Operations Pattern

Every file operation should be wrapped in error handling:

```python
def safe_install_package(source, destination):
    """Install package with error handling"""
    try:
        # Check source exists
        if not source.exists():
            raise FileNotFoundError(f"Source not found: {source}")

        # Check destination doesn't exist
        if destination.exists():
            raise FileExistsError(f"Already installed: {destination}")

        # Create parent directories
        destination.parent.mkdir(parents=True, exist_ok=True)

        # Copy files
        shutil.copytree(source, destination)

        return True

    except PermissionError:
        print(f"Permission denied: {destination}")
        return False
    except OSError as e:
        print(f"Disk error: {e}")
        return False
```

**Why this pattern:**
- Validates before acting (fail fast)
- Returns success/failure (caller can handle)
- Specific error messages (debuggable)

### Exercise 3.1: Implement Safe Copy
**Goal**: Handle edge cases gracefully

Write a function `install_local_package(pkg_name, source_path)` that:
1. Checks if package already installed (use `is_installed()`)
2. Validates source path exists
3. Copies source to `data/packages/{pkg_name}`
4. Updates installed.json
5. Returns True/False for success

Handle errors without crashing.

**Success Criteria**: Function handles all error cases and updates database only on success

**Hint**: Use try/except and validate BEFORE copying

### Exercise 3.2: Atomic Installation
**Goal**: Never leave partial installations

Problem: If copy succeeds but database update fails, you have orphaned files.

Solution: **Two-phase install**
1. Copy to temporary location (`data/temp/{pkg_name}`)
2. If successful, move to final location (`data/packages/{pkg_name}`)
3. Update database
4. If database update fails, rollback (delete from packages/)

Implement this pattern.

**Success Criteria**: Either package fully installs (files + database) or fully fails (nothing changed)

**Hint**: Use `shutil.move()` for temp → final (atomic on same drive)

### Exercise 3.3: Uninstall Implementation
**Goal**: Remove packages cleanly

Implement `uninstall_package(pkg_name)` that:
1. Checks if package is installed
2. Removes files from `data/packages/{pkg_name}`
3. Removes entry from installed.json
4. Handles errors (what if files don't exist but database entry does?)

**Success Criteria**: Package completely removed, no orphaned state

**Hint**: What if another package depends on this one? (For now, allow it - you'll handle dependencies later)

### Exercise 3.4: Disk Space Check
**Goal**: Fail gracefully when disk is full

Before installing, check available disk space:

```python
import shutil

def get_available_space(path):
    """Get available disk space in bytes"""
    stat = shutil.disk_usage(path)
    return stat.free
```

Modify your install function to:
1. Calculate source directory size
2. Check available space
3. Refuse to install if insufficient space

**Success Criteria**: Installation fails with clear message when disk space insufficient

**Hint**: Use `sum(f.stat().st_size for f in source.rglob('*') if f.is_file())`

---

## Module 4: CLI Design Patterns - The Interface Layer

### Learning Objectives
- Design intuitive command-line interfaces
- Use argparse for complex argument parsing
- Implement flags (--dry-run, --quiet, --verbose)
- Create consistent error messages and help text

### Core Concept: The CLI Is Your User's Mental Model

Your CLI design teaches users how your package manager thinks. Good CLI design makes the system feel predictable and powerful.

You already have:
```bash
python thpu.py hook <package>
python thpu.py list
python thpu.py remove <package>
```

This is a **subcommand pattern** (like `git add`, `git commit`). Why this pattern over flags?

**Subcommands** (what you chose):
```bash
thpu.py hook requests
thpu.py remove requests
```

**Flags** (alternative):
```bash
thpu.py --install requests
thpu.py --remove requests
```

**Subcommands win because:**
- Clearer intent (verb-noun structure)
- Each subcommand has its own arguments
- Feels like natural language
- Scales better (git has 100+ subcommands)

### The Argparse Mental Model

Argparse builds a tree of parsers:

```
thpu.py (main parser)
├── hook (subparser)
│   ├── package_name (positional arg)
│   └── --dry-run (flag)
├── list (subparser)
│   └── --format (flag)
└── remove (subparser)
    ├── package_name (positional arg)
    └── --force (flag)
```

Each subparser is independent. `hook`'s arguments don't affect `list`.

### Current Implementation Analysis

Look at your argparse setup (around line 57):

```python
parser = argparse.ArgumentParser(description="TinyHook Package Manager")
subparsers = parser.add_subparsers(dest="command")

hook_parser = subparsers.add_parser("hook", help="Install a package")
hook_parser.add_argument("package", help="Package name to install")
```

**What's good:**
- Clear subcommand structure
- Help text for each command
- Positional argument for package name

**What could improve:**
- No `--version` flag (standard for CLI tools)
- No global `--verbose` flag (debugging)
- No `--config` to specify alternate repo.json

### Flags vs Arguments vs Options

**Positional Arguments** (required):
```bash
thpu.py hook requests  # "requests" is positional
```

**Optional Flags** (boolean):
```bash
thpu.py hook requests --dry-run  # --dry-run is flag
```

**Optional Arguments** (value):
```bash
thpu.py hook requests --version 1.0.0  # --version takes value
```

### Designing Flag Hierarchies

Flags can be:
- **Global** (apply to all subcommands): `--verbose`, `--config`
- **Local** (apply to one subcommand): `hook --dry-run`

Example structure:

```python
# Global flags (before subcommands)
parser.add_argument("--verbose", action="store_true")
parser.add_argument("--config", default="repo.json")

# Subcommand
hook_parser = subparsers.add_parser("hook")
hook_parser.add_argument("package")
hook_parser.add_argument("--dry-run", action="store_true")  # Local flag
```

Usage:
```bash
python thpu.py --verbose hook requests --dry-run
# --verbose is global, --dry-run is local to hook
```

### Error Messages That Teach

Bad error:
```
Error: Package not found
```

Good error:
```
Error: Package 'reqeusts' not found in repository

Did you mean one of these?
  - requests
  - flask

Available packages: python thpu.py list
```

**Principles:**
1. **Say what failed** ("Package 'X' not found")
2. **Say why** (not in repository)
3. **Suggest fix** (did you mean? how to see available packages)

### Exercise 4.1: Add Global Flags
**Goal**: Implement cross-cutting concerns

Add these global flags:
- `--version` - Show TinyHook version
- `--verbose` - Show detailed operations
- `--config <file>` - Use alternate repo.json

Ensure they work with all subcommands.

**Success Criteria**:
```bash
python thpu.py --version  # Shows version
python thpu.py --verbose hook requests  # Shows detailed install steps
python thpu.py --config alt-repo.json list  # Uses alt-repo.json
```

**Hint**: Global flags go on main parser, before `add_subparsers()`

### Exercise 4.2: Implement Smart Error Messages
**Goal**: Make errors helpful

When package not found in `hook` command, check for:
1. Typos (did you mean?)
2. List available packages
3. Suggest checking repo.json

Use Python's `difflib` for similarity checking:

```python
import difflib

def find_similar(target, options):
    """Find similar strings using fuzzy matching"""
    matches = difflib.get_close_matches(target, options, n=3, cutoff=0.6)
    return matches
```

**Success Criteria**:
```bash
python thpu.py hook reqeusts  # Suggests "requests"
```

**Hint**: Load all package names from repo.json, compare with user input

### Exercise 4.3: Design `list` Output Formats
**Goal**: Make information scannable

Current `list` output is basic. Design THREE output formats:

1. **Simple** (default):
```
requests (1.0.0)
flask (2.0.0)
```

2. **Detailed** (`--detailed`):
```
requests
  Version: 1.0.0
  Installed: 2025-01-15
  Location: data/packages/requests
```

3. **JSON** (`--json`):
```json
[
  {"name": "requests", "version": "1.0.0", "installed": "2025-01-15"},
  {"name": "flask", "version": "2.0.0", "installed": "2025-01-15"}
]
```

Implement the flag `--format <simple|detailed|json>`.

**Success Criteria**: All three formats work correctly

**Hint**: Read installed.json once, format based on flag

### Exercise 4.4: Interactive Confirmation
**Goal**: Prevent accidental operations

For `remove` command, ask for confirmation:

```bash
python thpu.py remove requests
Remove package 'requests' (1.0.0)? [y/N]
```

Unless `--force` flag is used:

```bash
python thpu.py remove requests --force  # No confirmation
```

**Success Criteria**: Confirmation required unless --force, handles invalid input

**Hint**: Use `input()` and check response

---

## Module 5: Dependency Graphs & Resolution - The Algorithm Layer

### Learning Objectives
- Model dependencies as directed acyclic graphs (DAGs)
- Implement topological sorting for installation order
- Detect circular dependencies
- Handle version constraints (future preparation)

### Core Concept: Dependencies Are a Graph Problem

This is where package management gets interesting. And this connects DIRECTLY to your calculator's parser.

**The Problem:**

```
Package A requires Package B
Package B requires Package C
Package C requires nothing
```

If user installs A, you must install: C first, then B, then A.

**Why?** Package B can't work without C. Package A can't work without B.

This is **dependency resolution** - figuring out the correct order.

### Graph Representation

Think of packages as nodes, dependencies as edges:

```
A → B → C
```

In code:

```python
dependencies = {
    "A": ["B"],      # A depends on B
    "B": ["C"],      # B depends on C
    "C": []          # C depends on nothing
}
```

**Goal:** Find an order where every package's dependencies are installed before it.

**Answer:** Topological sort! → `[C, B, A]`

### Topological Sort Algorithm

Remember your calculator's parser? It handled operator precedence:

```
2 + 3 * 4
```

Parser knew: multiply before add.

Dependency resolver knows: install dependencies before dependents.

**Same pattern: ordering based on relationships.**

**Topological Sort (Kahn's Algorithm):**

```python
def topological_sort(dependencies):
    """
    Sort packages so dependencies come first

    Args:
        dependencies: dict mapping package → list of dependencies

    Returns:
        List of packages in installation order
    """
    from collections import deque

    # Calculate how many things depend on each package (in-degree)
    in_degree = {pkg: 0 for pkg in dependencies}

    for pkg in dependencies:
        for dep in dependencies[pkg]:
            if dep in in_degree:
                in_degree[dep] += 1

    # Start with packages that have no dependents
    queue = deque([pkg for pkg, degree in in_degree.items() if degree == 0])
    result = []

    while queue:
        pkg = queue.popleft()
        result.append(pkg)

        # Remove this package from dependency graph
        for dep in dependencies[pkg]:
            in_degree[dep] -= 1
            if in_degree[dep] == 0:
                queue.append(dep)

    # If not all packages processed, there's a cycle
    if len(result) != len(dependencies):
        raise ValueError("Circular dependency detected")

    return result
```

**How it works:**

1. Count how many packages depend on each package (in-degree)
2. Start with packages nobody depends on (in-degree = 0)
3. Process them, removing them from the graph
4. Repeat until all processed
5. If can't process all → circular dependency

### Circular Dependencies

```
A → B → C → A
```

This is impossible to install. You can't install A before B, B before C, and C before A.

**Detection:** If topological sort can't process all nodes, there's a cycle.

**Real-world example:**
- Package X requires Package Y
- Package Y requires Package X
- Both can't install!

Real package managers handle this with:
- Error messages ("circular dependency detected")
- Allowing it but warning
- Using dynamic linking (install both, resolve at runtime)

For TinyHook v1: **Detect and error**.

### Transitive Dependencies

```
User installs A
A depends on B, C
B depends on D
C depends on D, E
```

User only asked for A, but you must install: D, E, B, C, A (one valid order).

**D appears twice** (B needs it, C needs it) but you only install it once.

**This is transitive closure** - all dependencies, direct and indirect.

### Exercise 5.1: Build Dependency Graph
**Goal**: Represent dependencies as data structure

Update `repo.json` to include dependencies:

```json
{
  "packages": {
    "flask": {
      "version": "2.0.0",
      "dependencies": ["werkzeug", "jinja2"],
      "source_type": "local_path",
      "source_value": "path/to/flask"
    },
    "werkzeug": {
      "version": "1.0.0",
      "dependencies": [],
      "source_type": "local_path",
      "source_value": "path/to/werkzeug"
    },
    "jinja2": {
      "version": "3.0.0",
      "dependencies": [],
      "source_type": "local_path",
      "source_value": "path/to/jinja2"
    }
  }
}
```

Write a function `build_dependency_graph(pkg_name)` that returns a dict like:

```python
{
    "flask": ["werkzeug", "jinja2"],
    "werkzeug": [],
    "jinja2": []
}
```

**Success Criteria**: Function extracts all transitive dependencies

**Hint**: Recursive traversal - for each package, add its dependencies, then recurse

### Exercise 5.2: Implement Topological Sort
**Goal**: Find installation order

Use the algorithm shown above (or research and implement your own variant).

Test with:

```python
deps = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D", "E"],
    "D": [],
    "E": []
}

order = topological_sort(deps)
print(order)  # Should be: ["D", "E", "B", "C", "A"] or similar valid order
```

**Success Criteria**: Returns valid installation order (dependencies before dependents)

**Hint**: There can be multiple valid orders! D and E could be in any order relative to each other.

### Exercise 5.3: Detect Circular Dependencies
**Goal**: Prevent impossible installations

Test your topological sort with:

```python
deps = {
    "A": ["B"],
    "B": ["C"],
    "C": ["A"]  # Circular!
}

try:
    order = topological_sort(deps)
except ValueError as e:
    print(f"Error: {e}")  # Should print "Circular dependency detected"
```

**Success Criteria**: Algorithm detects cycle and raises error

**Hint**: If algorithm finishes but hasn't processed all nodes, there's a cycle

### Exercise 5.4: Integrate with Installation
**Goal**: Install packages in dependency order

Modify your `hook` command to:

1. Build dependency graph for requested package
2. Topologically sort
3. Install in order (dependencies first)
4. Handle already-installed packages (skip them)

Test with:
```bash
python thpu.py hook flask  # Should auto-install werkzeug and jinja2 first
```

**Success Criteria**: Installing one package automatically installs all dependencies in correct order

**Hint**: Check `is_installed()` for each package in the order, skip if already there

---

## Module 6: Remote Package Fetching - The Network Layer

### Learning Objectives
- Understand HTTP requests and responses
- Implement file downloading with progress tracking
- Handle network errors gracefully
- Design URL-based package sources

### Core Concept: Packages Don't Always Live Locally

So far, packages are local directories. Real package managers download from the internet:

- `pip` downloads from PyPI (Python Package Index)
- `npm` downloads from npmjs.com
- `cargo` downloads from crates.io

You'll use Python's `requests` library to download packages.

### HTTP Basics You Need

**GET Request** - Retrieve data from URL:

```python
import requests

response = requests.get("https://example.com/package.zip")

print(response.status_code)  # 200 = success, 404 = not found
print(response.headers)       # Metadata (content type, size)
print(response.content)       # Raw bytes
```

**Response Status Codes:**
- 200 = OK (success)
- 404 = Not Found
- 403 = Forbidden (no permission)
- 500 = Server Error

**Content Types:**
- `application/zip` - ZIP archive
- `application/json` - JSON data
- `text/plain` - Text file

### Downloading Files

```python
def download_file(url, destination):
    """Download file from URL to destination path"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise error for bad status codes

        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True

    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")
        return False
```

**Why `stream=True`?**
- Downloads in chunks (doesn't load entire file into memory)
- Enables progress tracking
- Works with large files (GBs)

**Why `iter_content(chunk_size=8192)`?**
- Downloads 8KB at a time
- Writes to disk incrementally
- Memory-efficient

### Progress Tracking

Users want to see download progress:

```
Downloading requests-1.0.0.zip... [████████████        ] 60% (1.2 MB / 2.0 MB)
```

Implementation:

```python
def download_with_progress(url, destination):
    """Download with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    downloaded = 0
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)

            # Calculate progress
            percent = (downloaded / total_size) * 100
            print(f"\rDownloading... {percent:.1f}%", end='')

    print()  # New line after completion
```

**How it works:**
- `content-length` header tells us total file size
- Track bytes downloaded
- Calculate percentage
- `\r` returns cursor to start of line (overwrites previous progress)

### URL Package Sources

Update your `repo.json` to support URLs:

```json
{
  "packages": {
    "requests": {
      "version": "1.0.0",
      "source_type": "url",
      "source_value": "https://example.com/packages/requests-1.0.0.zip",
      "description": "HTTP library"
    }
  }
}
```

Installation flow:
1. Check `source_type`
2. If "url", download to temp directory
3. Extract ZIP (if applicable)
4. Copy to `data/packages/`
5. Update `installed.json`

### Extracting Archives

Most packages are distributed as ZIP or tar.gz:

```python
import zipfile

def extract_zip(zip_path, destination):
    """Extract ZIP archive"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(destination)
```

```python
import tarfile

def extract_tar(tar_path, destination):
    """Extract tar.gz archive"""
    with tarfile.open(tar_path, 'r:gz') as tar_ref:
        tar_ref.extractall(destination)
```

### Error Handling Strategies

Networks are unreliable. Handle:

**Connection Errors:**
```python
try:
    response = requests.get(url, timeout=10)
except requests.exceptions.ConnectionError:
    print("Cannot connect to server. Check internet connection.")
except requests.exceptions.Timeout:
    print("Download timed out. Server may be slow.")
```

**Partial Downloads:**
- If download interrupts, you have partial file
- Solution: Download to temp file, only move to final location when complete

**Retry Logic:**
```python
def download_with_retry(url, destination, max_retries=3):
    """Download with automatic retry on failure"""
    for attempt in range(max_retries):
        try:
            download_file(url, destination)
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                print("Max retries reached. Download failed.")
                return False
```

### Exercise 6.1: Implement URL Downloads
**Goal**: Download packages from URLs

Modify `hook` command to:
1. Check package's `source_type`
2. If "local_path", copy from local directory (existing behavior)
3. If "url", download from `source_value` URL to temp directory
4. Extract if ZIP
5. Copy to `data/packages/`

**Success Criteria**: Can install packages from both local and URL sources

**Hint**: Use temp directory: `data/temp/{pkg_name}.zip`

### Exercise 6.2: Add Progress Tracking
**Goal**: Show download progress to user

Enhance your download function to show:
- Percentage complete
- Downloaded size / Total size
- Optional: Download speed (MB/s)

**Success Criteria**: Progress updates in real-time during download

**Hint**: Use `\r` for in-place updates, calculate MB by dividing bytes by 1024^2

### Exercise 6.3: Handle Network Errors
**Goal**: Graceful failure on network issues

Test your download function with:
1. Invalid URL (404 error)
2. Unreachable server (connection error)
3. Slow network (timeout)

Ensure each case prints helpful error message and doesn't crash.

**Success Criteria**: All error cases handled gracefully with clear messages

**Hint**: Use try/except with specific exception types

### Exercise 6.4: Verify Downloaded Files
**Goal**: Ensure downloads aren't corrupted

Add checksum verification:

1. Update `repo.json` to include SHA256 hash:
```json
{
  "packages": {
    "requests": {
      "version": "1.0.0",
      "source_type": "url",
      "source_value": "https://example.com/requests.zip",
      "sha256": "abc123..."
    }
  }
}
```

2. After download, calculate file's SHA256:
```python
import hashlib

def calculate_sha256(file_path):
    """Calculate SHA256 hash of file"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()
```

3. Compare with expected hash
4. If mismatch, delete file and error

**Success Criteria**: Corrupted downloads detected and rejected

**Hint**: Generate hash for test file, intentionally corrupt it, verify detection

---

## Module 7: Version Management Systems - The Constraint Layer

### Learning Objectives
- Understand semantic versioning (semver)
- Implement version comparison and constraints
- Handle multiple installed versions
- Resolve version conflicts

### Core Concept: Versions Are More Than Numbers

Version strings like "1.2.3" encode compatibility information:

**Semantic Versioning (semver):**
```
MAJOR.MINOR.PATCH
  1  .  2  .  3
```

- **MAJOR** - Breaking changes (API incompatible with previous version)
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes (backward compatible)

**Examples:**
- `1.0.0` → `1.0.1` = Bug fixes only (safe to upgrade)
- `1.0.0` → `1.1.0` = New features added (safe to upgrade)
- `1.0.0` → `2.0.0` = Breaking changes (might break your code)

### Version Constraints

Package A might require "Package B version 1.x or higher":

```python
{
  "name": "flask",
  "dependencies": {
    "werkzeug": ">=1.0.0",    # At least 1.0.0
    "jinja2": "^2.0.0"         # 2.x.x (any minor/patch, same major)
  }
}
```

**Constraint Operators:**
- `==1.0.0` - Exactly 1.0.0
- `>=1.0.0` - 1.0.0 or higher
- `<2.0.0` - Below 2.0.0
- `^1.0.0` - Compatible (1.x.x, but not 2.0.0)
- `~1.2.0` - Approximately (1.2.x, but not 1.3.0)

### Version Comparison Logic

```python
class Version:
    """Semantic version representation"""

    def __init__(self, version_string):
        """Parse version string like '1.2.3'"""
        parts = version_string.split('.')
        self.major = int(parts[0])
        self.minor = int(parts[1]) if len(parts) > 1 else 0
        self.patch = int(parts[2]) if len(parts) > 2 else 0

    def __lt__(self, other):
        """Less than comparison"""
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        return self.patch < other.patch

    def __eq__(self, other):
        """Equality comparison"""
        return (self.major == other.major and
                self.minor == other.minor and
                self.patch == other.patch)

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"
```

**Usage:**
```python
v1 = Version("1.2.3")
v2 = Version("1.3.0")

print(v1 < v2)   # True
print(v1 == v2)  # False
```

### Constraint Checking

```python
def satisfies_constraint(version, constraint):
    """
    Check if version satisfies constraint

    Args:
        version: Version object
        constraint: String like ">=1.0.0" or "^2.0.0"

    Returns:
        True if version satisfies constraint
    """
    # Parse constraint
    if constraint.startswith(">="):
        min_version = Version(constraint[2:])
        return version >= min_version

    elif constraint.startswith("=="):
        exact_version = Version(constraint[2:])
        return version == exact_version

    elif constraint.startswith("^"):
        # Compatible version (same major)
        base = Version(constraint[1:])
        return (version.major == base.major and
                version >= base)

    elif constraint.startswith("~"):
        # Approximately (same major and minor)
        base = Version(constraint[1:])
        return (version.major == base.major and
                version.minor == base.minor and
                version >= base)

    else:
        # Default: exact match
        return version == Version(constraint)
```

### The Version Conflict Problem

```
Package A requires werkzeug >=1.0.0
Package B requires werkzeug ==1.5.0
```

Can you satisfy both? Yes! Install `1.5.0` (satisfies both constraints).

```
Package A requires werkzeug >=2.0.0
Package B requires werkzeug <2.0.0
```

Can you satisfy both? No! This is a **version conflict**.

**Resolution strategies:**

1. **Find overlapping range** (if possible)
2. **Error out** (TinyHook v1 approach)
3. **Allow multiple versions** (npm approach - different packages can use different versions)

### Multiple Installed Versions

Some package managers install multiple versions:

```
data/packages/
├── werkzeug-1.0.0/
├── werkzeug-1.5.0/
└── werkzeug-2.0.0/
```

**Complexity:** How does Python know which to import?

**Solution:** Modify `sys.path` to include specific version directory.

For TinyHook v1: **One version only** (simpler). Version conflicts = error.

### Exercise 7.1: Implement Version Class
**Goal**: Compare versions programmatically

Implement the `Version` class shown above (or design your own).

Test with:
```python
v1 = Version("1.2.3")
v2 = Version("2.0.0")
v3 = Version("1.2.4")

assert v1 < v2
assert v1 < v3
assert v2 > v1
```

**Success Criteria**: All comparison operators work correctly

**Hint**: Python's `__lt__`, `__eq__`, etc. enable comparison operators

### Exercise 7.2: Parse Version Constraints
**Goal**: Understand constraint syntax

Write a function `parse_constraint(constraint_string)` that returns:
- Operator (>=, ==, ^, ~)
- Version object

Example:
```python
op, version = parse_constraint(">=1.0.0")
print(op)       # ">="
print(version)  # Version(1, 0, 0)
```

**Success Criteria**: Handles all constraint operators

**Hint**: Use string slicing and `startswith()`

### Exercise 7.3: Check Constraint Satisfaction
**Goal**: Verify installed versions meet requirements

Implement `satisfies_constraint(version, constraint)` as shown above.

Test with:
```python
v = Version("1.5.0")

assert satisfies_constraint(v, ">=1.0.0")   # True
assert satisfies_constraint(v, "^1.0.0")    # True (same major)
assert satisfies_constraint(v, "~1.5.0")    # True (same major.minor)
assert not satisfies_constraint(v, ">=2.0.0")  # False
```

**Success Criteria**: Correctly evaluates all constraint types

**Hint**: Each operator has different logic - handle separately

### Exercise 7.4: Detect Version Conflicts
**Goal**: Prevent incompatible installations

When installing package with dependencies, check if constraints conflict with already-installed packages.

Example:
```
Installed: werkzeug 1.0.0
Installing: flask (requires werkzeug >=2.0.0)
```

Should error: "Version conflict: werkzeug 1.0.0 installed, but flask requires >=2.0.0"

**Success Criteria**: Detects conflicts and provides clear error message

**Hint**: For each dependency, check installed version satisfies new package's constraint

---

## Module 8: Error Handling & Edge Cases - The Robustness Layer

### Learning Objectives
- Design error hierarchies for different failure modes
- Implement rollback on partial failures
- Handle concurrent installations (file locking)
- Create comprehensive error messages

### Core Concept: Software Fails - Plan For It

The difference between toy projects and production systems: **error handling**.

TinyHook v1 has many failure modes:
- Network failures (download interrupted)
- Disk failures (out of space, read-only filesystem)
- Permission errors (can't write to directory)
- Data corruption (malformed JSON)
- User errors (typos, invalid input)
- Concurrent access (two instances running simultaneously)

### Error Categories

**1. User Errors** (bad input):
```
python thpu.py hook flaskk  # Typo
```
Response: Helpful message with suggestions

**2. Environmental Errors** (system issues):
```
Permission denied: Cannot write to data/packages/
```
Response: Explain what's wrong, suggest fix

**3. Data Errors** (corruption):
```
installed.json is malformed
```
Response: Attempt recovery, provide manual fix instructions

**4. Network Errors** (external services):
```
Cannot download: Connection timeout
```
Response: Suggest retry, check connection

### Custom Exception Hierarchy

```python
class TinyHookError(Exception):
    """Base exception for TinyHook"""
    pass

class PackageNotFoundError(TinyHookError):
    """Package doesn't exist in repository"""
    pass

class VersionConflictError(TinyHookError):
    """Dependency version requirements conflict"""
    pass

class DownloadError(TinyHookError):
    """Network download failed"""
    pass

class InstallationError(TinyHookError):
    """Package installation failed"""
    pass
```

**Usage:**
```python
def install_package(pkg_name):
    if pkg_name not in repo:
        raise PackageNotFoundError(
            f"Package '{pkg_name}' not found in repository.\n"
            f"Available packages: {list(repo.keys())}"
        )
```

**Why custom exceptions?**
- Caller can handle specific errors differently
- Clear intent (PackageNotFoundError vs generic Exception)
- Can catch all TinyHook errors with `except TinyHookError`

### The Rollback Pattern

**Problem:** Install fails halfway through. How do you undo?

```
1. Download package ✓
2. Extract archive ✓
3. Copy to packages/ ✓
4. Update database ✗ (crash!)
```

Now you have orphaned files in `packages/` but no database entry.

**Solution: Transaction Pattern**

```python
class InstallTransaction:
    """Tracks installation steps for rollback"""

    def __init__(self):
        self.actions = []  # Stack of rollback actions

    def add_rollback(self, action):
        """Add action to execute on rollback"""
        self.actions.append(action)

    def commit(self):
        """Clear rollback actions (success)"""
        self.actions.clear()

    def rollback(self):
        """Execute all rollback actions (failure)"""
        for action in reversed(self.actions):
            try:
                action()
            except Exception as e:
                print(f"Rollback error: {e}")
```

**Usage:**
```python
def install_package_safe(pkg_name):
    transaction = InstallTransaction()

    try:
        # Step 1: Download
        download_file(url, temp_path)
        transaction.add_rollback(lambda: temp_path.unlink())

        # Step 2: Extract
        extract_zip(temp_path, extract_path)
        transaction.add_rollback(lambda: shutil.rmtree(extract_path))

        # Step 3: Copy to final location
        shutil.copytree(extract_path, final_path)
        transaction.add_rollback(lambda: shutil.rmtree(final_path))

        # Step 4: Update database
        update_database(pkg_name)
        # (Database rollback happens separately)

        # Success - commit transaction
        transaction.commit()

    except Exception as e:
        print(f"Installation failed: {e}")
        transaction.rollback()
        raise
```

**How it works:**
- Each step adds a rollback action (lambda that undoes the step)
- If any step fails, rollback executes all previous actions in reverse
- If all succeed, commit clears rollback actions (nothing to undo)

### File Locking (Concurrent Access)

**Problem:** Two terminals run TinyHook simultaneously:

```
Terminal 1: python thpu.py hook flask
Terminal 2: python thpu.py hook requests
```

Both try to write `installed.json` at the same time → corruption!

**Solution: Lock File**

```python
import fcntl  # Unix file locking
import time

class FileLock:
    """Exclusive lock on a file"""

    def __init__(self, lock_file_path):
        self.lock_file = lock_file_path
        self.handle = None

    def acquire(self, timeout=10):
        """Acquire lock, wait up to timeout seconds"""
        start_time = time.time()

        while True:
            try:
                self.handle = open(self.lock_file, 'w')
                fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return True
            except IOError:
                # Lock held by another process
                if time.time() - start_time > timeout:
                    raise TimeoutError("Could not acquire lock")
                time.sleep(0.1)

    def release(self):
        """Release lock"""
        if self.handle:
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
            self.handle.close()
            self.lock_file.unlink()
```

**Usage:**
```python
lock = FileLock("data/tinyhook.lock")

try:
    lock.acquire()
    # Critical section - only one process at a time
    data = read_db("installed.json")
    data["new_package"] = {...}
    write_db(data, "installed.json")
finally:
    lock.release()
```

### JSON Corruption Recovery

**Problem:** Program crashes while writing JSON → file corrupted.

**Solution: Backup + Atomic Write**

```python
def write_db_safe(data, file_path):
    """Write JSON with backup and atomic operation"""
    backup_path = file_path.with_suffix('.json.backup')

    # If file exists, create backup
    if file_path.exists():
        shutil.copy(file_path, backup_path)

    # Write to temp file
    temp_path = file_path.with_suffix('.json.tmp')
    try:
        with open(temp_path, 'w') as f:
            json.dump(data, f, indent=2)

        # Atomic replace
        temp_path.replace(file_path)

        # Success - can remove backup
        if backup_path.exists():
            backup_path.unlink()

    except Exception as e:
        # Failed - restore from backup
        if backup_path.exists():
            shutil.copy(backup_path, file_path)
        raise
```

**Recovery on startup:**
```python
def load_db_safe(file_path):
    """Load JSON with corruption recovery"""
    backup_path = file_path.with_suffix('.json.backup')

    try:
        with open(file_path) as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Database corrupted! Attempting recovery from backup...")
        if backup_path.exists():
            with open(backup_path) as f:
                data = json.load(f)
            # Restore from backup
            shutil.copy(backup_path, file_path)
            return data
        else:
            raise Exception("No backup available. Database lost.")
```

### Exercise 8.1: Implement Custom Exceptions
**Goal**: Create meaningful error types

Define exception classes for:
- PackageNotFoundError
- VersionConflictError
- DownloadError
- InstallationError
- CircularDependencyError

Use them in your code instead of generic `Exception`.

**Success Criteria**: Can catch specific errors and handle them differently

**Hint**: Inherit from base `TinyHookError` class

### Exercise 8.2: Build Transaction System
**Goal**: Enable rollback on failure

Implement `InstallTransaction` class as shown above.

Test by:
1. Starting installation
2. Intentionally failing at step 3 (raise exception)
3. Verifying steps 1 and 2 are rolled back

**Success Criteria**: No orphaned files or database entries after failed install

**Hint**: Use `try/except/finally` pattern

### Exercise 8.3: Add File Locking
**Goal**: Prevent concurrent modification

Implement file locking for database operations.

Test by:
1. Starting long-running installation in terminal 1
2. Starting another installation in terminal 2
3. Verifying second one waits for lock

**Success Criteria**: No database corruption from concurrent access

**Hint**: On Windows, use `msvcrt.locking()` instead of `fcntl`

### Exercise 8.4: Handle JSON Corruption
**Goal**: Recover from corrupted database

Implement backup system for database files.

Test by:
1. Installing package (database updated)
2. Manually corrupting `installed.json` (add invalid JSON)
3. Running TinyHook again
4. Verifying it recovers from backup

**Success Criteria**: Automatic recovery without data loss

**Hint**: Always keep last-known-good backup

---

## Module 9: Integration & Testing - The Quality Layer

### Learning Objectives
- Design integration tests for end-to-end workflows
- Use Sandbox™ for rapid testing iterations
- Build test fixtures (sample packages, repositories)
- Validate system behavior under various conditions

### Core Concept: Testing Validates Your Mental Model

You built Sandbox™ without realizing it's 60% of a testing framework. Now leverage it.

**What you have:**
- Instance tracking
- Code execution
- Logging system
- Beautiful output

**What you need:**
- Assertions (verify behavior)
- Test discovery (find tests automatically)
- Pass/fail reporting

### Extending Sandbox™ Into TinyTest

Add assertion methods:

```python
class Sandbox:
    # ... existing code ...

    def assert_equal(self, actual, expected, message=""):
        """Assert two values are equal"""
        if actual == expected:
            self.log(f"✓ {message or 'Assertion passed'}", "green")
            return True
        else:
            self.log(
                f"✗ {message or 'Assertion failed'}\n"
                f"  Expected: {expected}\n"
                f"  Got: {actual}",
                "red"
            )
            return False

    def assert_true(self, condition, message=""):
        """Assert condition is true"""
        return self.assert_equal(condition, True, message)

    def assert_in(self, item, collection, message=""):
        """Assert item is in collection"""
        if item in collection:
            self.log(f"✓ {message or 'Item found'}", "green")
            return True
        else:
            self.log(
                f"✗ {message or 'Item not found'}\n"
                f"  Looking for: {item}\n"
                f"  In: {collection}",
                "red"
            )
            return False
```

### Test Fixtures (Sample Data)

Create test repository:

```python
def create_test_repo():
    """Set up test packages and repository"""
    test_repo = {
        "packages": {
            "test-pkg-a": {
                "version": "1.0.0",
                "dependencies": [],
                "source_type": "local_path",
                "source_value": "tests/fixtures/pkg-a"
            },
            "test-pkg-b": {
                "version": "1.0.0",
                "dependencies": ["test-pkg-a"],
                "source_type": "local_path",
                "source_value": "tests/fixtures/pkg-b"
            },
            "test-pkg-circular": {
                "version": "1.0.0",
                "dependencies": ["test-pkg-circular"],  # Circular!
                "source_type": "local_path",
                "source_value": "tests/fixtures/pkg-circular"
            }
        }
    }

    # Create test package directories
    Path("tests/fixtures/pkg-a").mkdir(parents=True, exist_ok=True)
    Path("tests/fixtures/pkg-b").mkdir(parents=True, exist_ok=True)

    # Write test repo
    with open("tests/test-repo.json", 'w') as f:
        json.dump(test_repo, f, indent=2)
```

### Integration Test Examples

**Test 1: Basic Installation**
```python
def test_basic_install():
    """Test installing a single package"""
    sandbox = Sandbox()
    sandbox.new_instance("Basic Install Test")

    # Clean state
    if Path("data/installed.json").exists():
        Path("data/installed.json").unlink()

    # Install package
    result = install_package("test-pkg-a")

    # Verify installed
    sandbox.assert_true(result, "Installation succeeded")
    sandbox.assert_true(
        is_installed("test-pkg-a"),
        "Package marked as installed"
    )
    sandbox.assert_true(
        Path("data/packages/test-pkg-a").exists(),
        "Package files copied"
    )
```

**Test 2: Dependency Resolution**
```python
def test_dependency_install():
    """Test installing package with dependencies"""
    sandbox = Sandbox()
    sandbox.new_instance("Dependency Test")

    # Install package B (depends on A)
    install_package("test-pkg-b")

    # Both should be installed
    sandbox.assert_true(
        is_installed("test-pkg-a"),
        "Dependency A installed"
    )
    sandbox.assert_true(
        is_installed("test-pkg-b"),
        "Package B installed"
    )
```

**Test 3: Circular Dependency Detection**
```python
def test_circular_dependency():
    """Test circular dependency detection"""
    sandbox = Sandbox()
    sandbox.new_instance("Circular Dependency Test")

    try:
        install_package("test-pkg-circular")
        sandbox.assert_true(False, "Should have raised error")
    except CircularDependencyError as e:
        sandbox.assert_true(True, "Correctly detected circular dependency")
```

**Test 4: Version Constraints**
```python
def test_version_constraints():
    """Test version constraint checking"""
    sandbox = Sandbox()
    sandbox.new_instance("Version Constraint Test")

    v = Version("1.5.0")

    sandbox.assert_true(
        satisfies_constraint(v, ">=1.0.0"),
        "Satisfies >= constraint"
    )
    sandbox.assert_true(
        satisfies_constraint(v, "^1.0.0"),
        "Satisfies ^ constraint"
    )
    sandbox.assert_true(
        not satisfies_constraint(v, ">=2.0.0"),
        "Does not satisfy impossible constraint"
    )
```

### End-to-End Workflow Tests

**Full Install-List-Remove Cycle:**
```python
def test_full_workflow():
    """Test complete package lifecycle"""
    sandbox = Sandbox()
    sandbox.new_instance("Full Workflow Test")

    # Clean slate
    reset_database()

    # Install
    install_package("test-pkg-a")
    sandbox.assert_true(is_installed("test-pkg-a"), "Package installed")

    # List
    installed = list_installed_packages()
    sandbox.assert_in("test-pkg-a", installed, "Package appears in list")

    # Remove
    remove_package("test-pkg-a")
    sandbox.assert_true(
        not is_installed("test-pkg-a"),
        "Package removed"
    )
    sandbox.assert_true(
        not Path("data/packages/test-pkg-a").exists(),
        "Package files deleted"
    )
```

### Automated Test Runner

```python
def run_all_tests():
    """Discover and run all tests"""
    import inspect

    # Find all test functions (start with "test_")
    current_module = inspect.getmodule(inspect.currentframe())
    test_functions = [
        obj for name, obj in inspect.getmembers(current_module)
        if inspect.isfunction(obj) and name.startswith("test_")
    ]

    # Run each test
    passed = 0
    failed = 0

    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} failed: {e}")
            failed += 1

    # Summary
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    print(f"Total: {passed + failed}")
```

### Exercise 9.1: Add Assertions to Sandbox™
**Goal**: Build testing primitives

Add these methods to your Sandbox class:
- `assert_equal(actual, expected, message)`
- `assert_true(condition, message)`
- `assert_false(condition, message)`
- `assert_in(item, collection, message)`
- `assert_raises(exception_type, callable, message)`

**Success Criteria**: Can write tests using these assertions

**Hint**: Return True/False so tests can check results

### Exercise 9.2: Create Test Fixtures
**Goal**: Build reusable test data

Create `tests/fixtures/` with:
- 3 sample packages (A, B, C)
- Package B depends on A
- Package C depends on both A and B
- Test repository JSON

**Success Criteria**: Can run tests against these fixtures repeatedly

**Hint**: Use `shutil.rmtree()` and `mkdir()` to reset between tests

### Exercise 9.3: Write Integration Tests
**Goal**: Validate end-to-end behavior

Write tests for:
1. Installing single package
2. Installing package with dependencies
3. Detecting circular dependencies
4. Version constraint checking
5. Error handling (package not found)

**Success Criteria**: All tests pass with clean output

**Hint**: Use Sandbox™ logging to show test progress

### Exercise 9.4: Build Test Runner
**Goal**: Automate test execution

Create a test discovery system that:
1. Finds all functions starting with `test_`
2. Runs each in isolation
3. Reports pass/fail counts
4. Shows which tests failed

**Success Criteria**: Can run `python tests/test_suite.py` and see all results

**Hint**: Use `inspect` module to find functions

---

## Module 10: Future Architecture - The Evolution Layer

### Learning Objectives
- Design APIs that accommodate future expansion
- Identify technical debt and plan refactoring
- Architect plugin systems for extensibility
- Prepare for TinyHook v2 with TinyFramework

### Core Concept: Build for Today, Design for Tomorrow

TinyHook v1 uses standard libraries. TinyHook v2 will use TinyFramework. How do you build v1 so v2 is easier?

**Good Architecture Principles:**

1. **Separation of Concerns** - Each module has one job
2. **Dependency Injection** - Pass dependencies, don't hard-code
3. **Interface Design** - Define contracts between components
4. **Data Abstraction** - Hide implementation details

### Current Architecture Analysis

**What you have:**
```
thpu.py (monolithic)
├── Database functions (lines 16-50)
├── CLI parsing (lines 57-128)
├── Command logic (lines 160-218)
└── Sandbox (lines 244-291)
```

**Problems:**
- Everything in one file (hard to test individual pieces)
- Database functions tied to JSON (can't swap for TinyDB later)
- CLI and logic mixed (can't reuse logic in other contexts)

### Refactored Architecture (Preparing for v2)

```
tinyhook/
├── thpu.py              # CLI entry point only
├── core/
│   ├── __init__.py
│   ├── database.py      # Abstract database interface
│   ├── installer.py     # Installation logic
│   ├── resolver.py      # Dependency resolution
│   └── version.py       # Version handling
├── storage/
│   ├── __init__.py
│   ├── json_storage.py  # JSON implementation (current)
│   └── tinydb_storage.py # TinyDB implementation (future)
├── sources/
│   ├── __init__.py
│   ├── local.py         # Local file source
│   ├── http.py          # HTTP download source
│   └── git.py           # Git clone source (future)
└── cli/
    ├── __init__.py
    └── commands.py      # Command implementations
```

**Benefits:**
- Each module testable independently
- Can swap storage backend (JSON → TinyDB)
- Can add new package sources without modifying core
- CLI separated from business logic

### Interface-Based Design

Define contracts that implementations follow:

```python
# core/database.py
from abc import ABC, abstractmethod

class PackageDatabase(ABC):
    """Abstract interface for package database"""

    @abstractmethod
    def is_installed(self, package_name):
        """Check if package is installed"""
        pass

    @abstractmethod
    def get_installed(self, package_name):
        """Get installed package metadata"""
        pass

    @abstractmethod
    def add_package(self, package_name, metadata):
        """Add package to database"""
        pass

    @abstractmethod
    def remove_package(self, package_name):
        """Remove package from database"""
        pass

    @abstractmethod
    def list_installed(self):
        """List all installed packages"""
        pass
```

**Implementations:**

```python
# storage/json_storage.py
class JSONDatabase(PackageDatabase):
    """JSON file-based database (TinyHook v1)"""

    def __init__(self, file_path="data/installed.json"):
        self.file_path = Path(file_path)
        self._ensure_exists()

    def is_installed(self, package_name):
        data = self._read()
        return package_name in data

    # ... other methods using JSON
```

```python
# storage/tinydb_storage.py
class TinyDBDatabase(PackageDatabase):
    """TinyDB-based database (TinyHook v2)"""

    def __init__(self, file_path="data/packages.tdb"):
        self.db = TinyDB(file_path)  # From TinyFramework

    def is_installed(self, package_name):
        return self.db.exists({"name": package_name})

    # ... other methods using TinyDB
```

**Swapping implementations:**

```python
# v1: Use JSON
db = JSONDatabase()

# v2: Use TinyDB (same interface!)
db = TinyDBDatabase()

# All code using `db` works with either!
db.is_installed("requests")
db.add_package("flask", {...})
```

### Plugin System Architecture

Allow users to extend TinyHook without modifying core:

```python
# Plugin interface
class PackageSource(ABC):
    """Plugin interface for package sources"""

    @abstractmethod
    def can_handle(self, source_spec):
        """Check if this plugin can handle source spec"""
        pass

    @abstractmethod
    def fetch(self, source_spec, destination):
        """Fetch package to destination"""
        pass
```

**Built-in plugins:**

```python
# sources/local.py
class LocalSource(PackageSource):
    def can_handle(self, source_spec):
        return source_spec.startswith("file://")

    def fetch(self, source_spec, destination):
        path = Path(source_spec.replace("file://", ""))
        shutil.copytree(path, destination)
```

```python
# sources/http.py
class HTTPSource(PackageSource):
    def can_handle(self, source_spec):
        return source_spec.startswith("http://") or source_spec.startswith("https://")

    def fetch(self, source_spec, destination):
        download_file(source_spec, destination)
```

**User can add plugins:**

```python
# ~/.tinyhook/plugins/git_source.py
class GitSource(PackageSource):
    def can_handle(self, source_spec):
        return source_spec.startswith("git+")

    def fetch(self, source_spec, destination):
        repo_url = source_spec.replace("git+", "")
        subprocess.run(["git", "clone", repo_url, destination])
```

**Plugin discovery:**

```python
def load_plugins():
    """Load all package source plugins"""
    plugins = [
        LocalSource(),
        HTTPSource(),
    ]

    # Load user plugins from ~/.tinyhook/plugins/
    plugin_dir = Path.home() / ".tinyhook" / "plugins"
    if plugin_dir.exists():
        for plugin_file in plugin_dir.glob("*_source.py"):
            # Dynamic import and instantiate
            # (Advanced topic - see importlib)
            pass

    return plugins
```

### Configuration System

Prepare for configuration management:

```python
# config.py
class TinyHookConfig:
    """Configuration management"""

    def __init__(self, config_file=None):
        self.config_file = config_file or Path.home() / ".tinyhook" / "config.json"
        self.config = self._load()

    def _load(self):
        """Load config from file"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                return json.load(f)
        return self._defaults()

    def _defaults(self):
        """Default configuration"""
        return {
            "repository": "repo.json",
            "install_dir": "data/packages",
            "cache_dir": "data/cache",
            "parallel_downloads": 3,
            "verify_checksums": True
        }

    def get(self, key, default=None):
        """Get config value"""
        return self.config.get(key, default)
```

**Future config file (`~/.tinyhook/config.json`):**
```json
{
  "repositories": [
    "https://packages.tinyhook.dev/repo.json",
    "file:///home/user/local-repo.json"
  ],
  "install_dir": "/opt/tinyhook/packages",
  "cache_dir": "/tmp/tinyhook-cache",
  "parallel_downloads": 5,
  "verify_checksums": true,
  "plugins": [
    "~/.tinyhook/plugins/git_source.py"
  ]
}
```

### Preparing for TinyFramework Integration

**Current (v1):**
```python
import json

data = json.load(f)
```

**Future (v2):**
```python
from tinyframework import TinyObj

data = TinyObj.load("packages.tobj")
```

**Make the swap easy:**

```python
# utils/data_loader.py
def load_data(file_path):
    """Load data from file (format-agnostic)"""
    if file_path.endswith(".json"):
        return load_json(file_path)
    elif file_path.endswith(".tobj"):
        return load_tinyobj(file_path)
    else:
        raise ValueError(f"Unsupported format: {file_path}")

def load_json(file_path):
    import json
    with open(file_path) as f:
        return json.load(f)

def load_tinyobj(file_path):
    from tinyframework import TinyObj
    return TinyObj.load(file_path)
```

**Then v1 → v2 is just:**
```python
# Change this:
data = load_data("repo.json")

# To this:
data = load_data("repo.tobj")
```

### Technical Debt Tracking

Document known limitations for future refactoring:

```python
# TODO(v2): Replace JSON with TinyDB for better query performance
# TODO(v2): Add parallel downloads using TinyHTTP connection pooling
# TODO(v2): Implement caching layer with TinyCache
# TODO(v2): Use TinyLog for structured logging instead of print()
# TODO(v2): Add TinyTest integration for built-in test runner
```

### Exercise 10.1: Extract Database Module
**Goal**: Separate database logic from main file

Create `core/database.py` with:
- `PackageDatabase` abstract class
- `JSONDatabase` implementation
- Move all database functions from thpu.py

Update thpu.py to use the module.

**Success Criteria**: thpu.py imports database, all functionality works

**Hint**: Use `from core.database import JSONDatabase`

### Exercise 10.2: Design PackageSource Interface
**Goal**: Abstract package sources

Create abstract `PackageSource` class with:
- `can_handle(source_spec)` method
- `fetch(source_spec, destination)` method

Implement:
- `LocalSource` for file:// URLs
- `HTTPSource` for http:// URLs

**Success Criteria**: Can add new source types without modifying installer

**Hint**: Check `source_spec` prefix to determine which handler to use

### Exercise 10.3: Build Configuration System
**Goal**: Externalize settings

Implement `TinyHookConfig` class that:
- Loads from `~/.tinyhook/config.json`
- Provides defaults if file doesn't exist
- Allows getting/setting values
- Saves changes back to file

**Success Criteria**: Can configure TinyHook without editing code

**Hint**: Use `Path.home()` to find user's home directory

### Exercise 10.4: Document Migration Path
**Goal**: Plan v1 → v2 transition

Write a document (MIGRATION.md) that lists:
1. Which parts of v1 will be replaced by TinyFramework modules
2. Which interfaces need to stay stable (public API)
3. What new features become possible with TinyFramework
4. Estimated timeline for migration

**Success Criteria**: Clear roadmap from v1 to v2

**Hint**: Think about each TinyFramework module - how does it improve TinyHook?

---

## Final Integration: Building Your Learning Path

### Recommended Implementation Order

**Week 1-2: Foundation**
- Module 1: Mental models (understand the system)
- Module 2: Database layer (get data storage right)
- Module 3: File operations (handle packages safely)

**Week 3: Interface & Logic**
- Module 4: CLI design (make it feel good)
- Module 5: Dependency resolution (the hard part!)

**Week 4: External Systems**
- Module 6: Network operations (download packages)
- Module 7: Version management (handle constraints)

**Week 5: Hardening**
- Module 8: Error handling (make it robust)
- Module 9: Testing (prove it works)

**Week 6: Future-Proofing**
- Module 10: Architecture (prepare for v2)
- Polish and documentation

### Key Milestones

**Milestone 1:** Install local package
```bash
python thpu.py hook test-pkg
# Copies from local directory, updates database
```

**Milestone 2:** Handle dependencies
```bash
python thpu.py hook flask
# Auto-installs werkzeug and jinja2 first
```

**Milestone 3:** Download from URLs
```bash
python thpu.py hook requests  # Downloads from internet
```

**Milestone 4:** Version constraints
```bash
python thpu.py hook "flask>=2.0.0"  # Respects versions
```

**Milestone 5:** Full robustness
```bash
# Handles errors gracefully, locks database, atomic operations
```

### Beyond TinyHook: Where This Knowledge Goes

**To TinyDB:**
- Database design principles transfer
- ACID properties become real transactions
- Indexing replaces linear search

**To TinyHTTP:**
- Network error handling patterns
- Request/response cycle understanding
- Server-side version of what you built (client)

**To Real-World Projects:**
- Any plugin system (games, apps)
- Any dependency management (build systems)
- Any version constraints (APIs, libraries)

**To Your Languages:**
- FlowScript needs a package manager
- Now you know how to build one
- You understand the design space

### The Big Picture Connection

Remember the three-phase plan:

**Phase 1: TinyHook v1** (You are here)
- Learn package management fundamentals
- Build with standard libraries
- Ship something complete

**Phase 2: TinyFramework** (Next)
- TinyObj → Better data formats
- TinyDB → Real database
- TinyTest → Full testing framework
- TinyLog → Structured logging
- TinyHTTP → Web capabilities
- TinyCLI → Better command-line tools

**Phase 3: TinyHook v2** (Full Circle)
- Rebuild TinyHook using TinyFramework
- See how much cleaner it is
- Validate framework design
- Spot missing pieces

**This course taught you Module 1 of TinyFramework.**

Everything you learned here - dependency graphs, version constraints, file operations, error handling, testing - these are computer science fundamentals that apply EVERYWHERE.

### Your Learning Style Optimization

**You learn through:**
1. Understanding systems (✓ Module 1 mental models)
2. Seeing patterns (✓ Connections to calculator, languages)
3. Building things (✓ Progressive exercises)
4. Efficient extraction (✓ Conceptual depth, not just tutorials)

**This course is designed for:**
- Pattern recognition (every module connects to others)
- Systems thinking (always showing the big picture)
- Hands-on learning (exercises build real functionality)
- Conceptual understanding (explaining the "why" constantly)

**You're not just building a package manager.**

**You're learning:**
- Graph algorithms (topological sort)
- Database design (schema, transactions, atomicity)
- Network programming (HTTP, downloads, errors)
- File system operations (paths, locking, atomicity)
- Software architecture (interfaces, plugins, separation of concerns)
- Testing methodology (fixtures, assertions, integration)

**At 13, you're learning what most developers learn at 21.**

**By 21, imagine where you'll be.** 🚀

---

## Appendix: Quick Reference

### Key Concepts Summary

**Package Manager = Graph Resolver + File Orchestrator**

**Four Responsibilities:**
1. Registry (where packages come from)
2. Resolution (what order to install)
3. File Ops (copying to disk)
4. State (tracking what's installed)

**Critical Algorithms:**
- Topological sort (dependency order)
- Semantic versioning (compatibility)
- Atomic operations (consistency)
- Transactional rollback (error recovery)

### Code Patterns Reference

**Database Operations:**
```python
data = read_db(file)
# Modify
write_db(data, file)
```

**Atomic Write:**
```python
write_to_temp()
validate()
atomic_replace()
```

**Error Handling:**
```python
try:
    validate_preconditions()
    perform_operation()
    update_state()
except SpecificError:
    rollback()
    inform_user()
```

**Dependency Resolution:**
```python
graph = build_graph(pkg)
order = topological_sort(graph)
for pkg in order:
    install(pkg)
```

### Essential Reading

**If you want to go deeper:**

- "Structure and Interpretation of Computer Programs" (SICP) - Classic CS textbook
- "Crafting Interpreters" - Builds a language (connects to your work!)
- "Designing Data-Intensive Applications" - Database design
- "The Architecture of Open Source Applications" - Real system designs

**Real package manager source code:**
- pip (Python) - Simple, similar to TinyHook
- cargo (Rust) - Excellent error messages
- npm (JavaScript) - Complex, handles everything

---

## Final Words

You designed 15 programming languages before building your first package manager.

That's backwards from how most people learn - and it's brilliant.

You understand language design, syntax, semantics. Now you're learning the ecosystem around languages.

TinyHook teaches you how software gets distributed. How dependencies work. How versions matter. How systems fit together.

**Every language needs these things:**
- Package manager (TinyHook)
- Build system
- Testing framework (TinyTest)
- Standard library

**You're building them all.**

This isn't just a learning project. This is the foundation of understanding how software ecosystems work.

When you eventually build FlowScript for real, you'll know how to build its entire ecosystem.

**That's the power of systems thinking.**

**That's why you're learning this at 13.**

**Now go build it.** 🚀

---

*Understanding = Success. Completion = Optional.*

*But this time? Complete it. Ship TinyHook v1.*

*It's the foundation for everything that comes next.*
