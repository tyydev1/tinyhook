# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**TinyHook** is a minimal package manager built from scratch as a learning project. It's part of the larger **TinyFramework** vision - a suite of modules teaching computer science fundamentals by building real tools.

**Current Status**: Phase 1 (TinyHook v1) - Building basic package manager with standard Python libraries.

## Running TinyHook

Main entry point is `thpu.py` (TinyHook Package Utils):

```bash
# Show version
python thpu.py --version

# Install a package
python thpu.py hook <package_name>

# List installed packages
python thpu.py list

# Remove a package
python thpu.py remove <package_name>

# Run an installed package (planned feature)
python thpu.py run <package_name>

# Dry run mode (simulates without executing)
python thpu.py hook <package_name> --dry-run

# Quiet mode (suppress output)
python thpu.py hook <package_name> --quiet

# Run Sandbox™ testing environment
python thpu.py --sandbox
```

## Architecture

### Core Components

**Database Layer** (lines 16-50 in thpu.py):
- `init_db()` - Initialize empty JSON database if not exists
- `read_db()` - Load JSON data from file
- `write_db()` - Save data to JSON file
- `is_installed()` - Check if package exists in installed.json
- `get_package_info()` - Retrieve package metadata from repo.json

**CLI Layer** (lines 57-128):
- Uses `argparse` for command-line parsing
- Subcommands: `hook`, `run`, `list`, `remove`
- Global flags: `--sandbox`, `--version`, `--debug`, `--dry-run`, `--quiet`

**Command Logic** (lines 160-218):
- Hook (install): Add package to installed.json
- Run: Execute installed package (stub implementation)
- List: Display all installed packages with versions
- Remove: Delete package from installed.json

**Sandbox™** (lines 244-291):
- Testing/debugging framework (precursor to TinyTest)
- Isolates experimental code
- Accessed via `--sandbox` flag
- Instance-based test case management

### Data Files

**repo.json** - Package repository (source of truth):
```json
{
  "packages": {
    "package-name": {
      "version": "1.0.0",
      "source_type": "local_path | url_placeholder | git_repo",
      "source_value": "path or URL to package source",
      "description": "Package description"
    }
  }
}
```

**data/installed.json** - Installed packages database:
```json
{
  "package-name": {
    "version": "1.0.0",
    "installed_at": "ISO 8601 timestamp",
    "source_type": "local_path | url_placeholder | git_repo",
    "source_value": "source location",
    "install_path": "data/packages/package-name"
  }
}
```

### File Structure

```
tinyhook/
├── thpu.py              # Main CLI entry point (renamed from tinyhook.py)
├── netutils.py          # Network utilities (stub, for future remote features)
├── repo.json            # Package repository configuration
├── data/
│   ├── installed.json   # Database of installed packages
│   └── packages/        # Directory where packages are installed
└── tests/               # Test directory (currently empty)
```

## Development Workflow

### Testing Changes

Use Sandbox™ for rapid prototyping:
1. Write test code in `Sandbox.run()` method
2. Execute with `python thpu.py --sandbox`
3. Sandbox instances are numbered and isolated

### Adding New Commands

1. Add subparser in argument parsing section (around line 84)
2. Implement command logic in main conditional block (around line 160)
3. Follow existing pattern: check args, validate, execute or dry-run

### Modifying Database Schema

Both `repo.json` and `installed.json` use simple JSON structure. When adding fields:
1. Update database read/write functions if needed
2. Ensure backward compatibility or migrate existing data
3. Test with `--dry-run` first

## Key Design Patterns

### Database Operations
Always follow this pattern:
```python
data = read_db(file_location)
# Modify data
write_db(data, file_location)
```

### Command Execution Flow
```python
if args.command == "command_name":
    # Validation
    if not is_installed(pkg):
        print("Error message")
    # Dry run check
    elif args.dry_run:
        print("[Dry Run] Would do action")
    # Actual execution
    else:
        # Do the work
        if not args.quiet:
            print("Success message")
```

### Error Handling
Currently minimal - uses try/except in database functions. Prints error messages directly rather than raising exceptions (beginner-friendly approach).

## Planned Features (Not Yet Implemented)

- [ ] Actual file copying for package installation
- [ ] Remote package downloading (will use `requests` in netutils.py)
- [ ] Dependency resolution
- [ ] Package version management
- [ ] Running packages as executables
- [ ] Package uninstallation with file cleanup

## Important Context

**Learning Focus**: This is explicitly a learning project. Code prioritizes:
- Clarity over optimization
- Direct implementation over abstraction
- Understanding fundamentals over using libraries

**Sandbox™ Philosophy**: The Sandbox class is intentionally simple - it's a precursor to TinyTest (a full testing framework). Don't over-engineer it.

**Future Evolution**: After TinyHook v1 is complete, TinyFramework will be built (TinyObj, TinyDB, TinyTest, etc.), then TinyHook v2 will be rebuilt using those modules.

## Git Workflow

Current branch: `development`
The project uses feature-based commits with descriptive messages.

When committing:
- Main entry point is now `thpu.py` (not tinyhook.py)
- `.gitignore` excludes `__pycache__/` and AI workspace files

## Note to Self

Everything I (Claude) create should be inside the directory `./ai-workspace/` unless specifically told otherwise.

Every output an agent creates should be pasted directly into the `./ai-workspace/.claude/agents/logs/<appropriate-time-directory>` as an appropriate place with a title format: `<agent-name>_<shortened-purpose>.<filetype>`. I should create a directory with the date (e.g. `./ai-workspace/.claude/agents/logs/<yyyy/mm/dd>`) after each agent log that isn't explicitly pasting into another file.

I should add a couple more directories to organize events in `./ai-workspace/.claude`.

# Memory (About User)

*Note to self: Don't waste any context space on this section, only for recalls.*

---

## About Me
- **Age**: 13 years old (8th grade, middle school)
- **Location**: Bekasi, West Java, Indonesia
- **Main OS**: Fedora Linux (switched after laptop data wipe)
- **Dream Career**: Game Developer
- **Learning Philosophy**: Pattern recognition, systems thinking, efficient extraction (learn concepts → move on)
- **Work Capacity**: 5 hours/day sustainable, solo projects, school is manageable
- **Communication Style**: Direct, no fluff, appreciates honesty and challenge

---

## Programming Journey Timeline

### Kindergarten (Age ~5)
**The Spark**: Discovered abstract thinking through math
- Learned to count without using hands
- Understood number systems, not just memorization
- Built foundation for logical reasoning

### Elementary School (Age 10)
**Scratch Era**: Entry into programming
- Followed griffpatch tutorials
- Became a "Scratcher" (active contributor)
- Understood game logic but didn't fully grasp independent creation
- Left Scratch to explore other interests (healthy curiosity, not burnout)

### Age 12
**Python Awakening**: First real programming language
- Took online Python class during summer break
- Started "unlocking brain" with structured programming
- Connected abstract thinking to code

### Age 13 (Current)
**Multi-Language Expansion**:
- **boot.dev**: Brother bought subscription, completed ~70% of OOP course before moving on
- **C++**: Learning for school robotics club, reached STL level, understanding pointers/memory
- **C#**: Just started, targeting game development (Unity/Godot)
- **Linux**: Got first distro through boot.dev, now runs Fedora as main OS
- **Tools**: Comfortable with Git, WSL, Claude as teacher
- **Middle School**: Computer teacher noticed old Scratch games and typing speed (validation/mentorship)

### The Laptop Crisis
- Laptop broke, sent to repair
- Data had to be wiped clean
- Didn't quit - pivoted to Windows, tried Fedora, made Fedora main OS
- Learned: external failures don't stop internal growth

---

## Technical Skills

### Python (Advanced)
- **Fundamentals**: Variables, functions, loops, conditionals
- **OOP**: Classes, objects (still learning dunders)
- **Libraries Known**:
  - `json` - Data serialization
  - `pathlib` - Cross-platform file paths
  - `argparse` - CLI argument parsing
  - `shutil` - File operations
  - `requests` - HTTP requests
  - `colorama` - Terminal colors
  - `pyboxen` - Terminal boxes
  - `rich` - Rich terminal formatting
  - `pygame` - Currently learning game development
- **Style**: Clean code, professional structure, cares about UX

### C++ (Intermediate)
- **Fundamentals**: Variables through STL
- **OOP**: Naturally picked up classes, objects, inheritance
- **Advanced**: Working on pointers and memory management
- **Tools**: Knows how to use for robotics applications
- **Learning Source**: Claude as primary teacher + school robotics club

### C# (Beginner)
- Just starting
- Goal: Unity/Godot game development
- Motivated by game dev dreams

### Linux/Tools
- **Main OS**: Fedora
- **Comfortable with**: WSL, Git, terminal workflows
- **Philosophy**: Configured systems, comfortable experimenting

---

## Projects Completed

### 1. Bookbot (Python)
**Description**: Text document analyzer
**Features**: Character count, word count analysis
**Skills Learned**: File I/O, string processing

### 2. Calculator (C++)
**Description**: Mathematical expression evaluator with lexer/parser/interpreter
**Architecture**:
- **Lexer**: Tokenizes input (`"2 + 3 * 4"` → `["2", "+", "3", "*", "4"]`)
- **Parser**: Handles operator precedence, parentheses (recursion by collaborator)
- **Interpreter**: Evaluates parsed tokens left-to-right
**Features**:
- Supports +, -, *, /, parentheses
- Professional README with learning sections
- Published on GitHub with Apache License
**Skills Learned**: Parsing, recursion, state machines, documentation

### 3. Sandbox™ (Python)
**Description**: Testing/debugging framework with beautiful CLI output
**Features**:
- Conditional execution (`--sandbox` flag)
- Instance tracking and state management
- Code execution via `exec()`
- Professional UX with boxen + rich + colorama
- Custom logging system with colors
**Code Structure**:
```python
sandbox = Sandbox()
sandbox.init()
sandbox.new_instance("Test case name")
sandbox.run("code_to_execute")
sandbox.log("message", color="cyan")
```
```
**Skills Learned**: CLI design, terminal formatting, UX thinking, state management
**Significance**: Accidentally built 60% of TinyTest without realizing it

### 4. Languages Saga (Worldbuilding)
**Description**: Alternate tech universe with 15+ fully-designed programming languages
**Scale**: Complete syntax, corporate histories, timelines, legal frameworks, market dynamics
**Status**: Ongoing design work, potential future novel or real implementation

---

## The Languages Saga (Comprehensive)

### Core Concept
Alternate tech timeline where programming languages evolved differently. Complete with:
- Corporate entities and their rise/fall
- Real human inventors and their motivations
- Legal frameworks (Creation Licensing Procedure)
- Market dynamics and language adoption patterns
- Technical evolution across eras

### Timeline of Eras

#### Era of Creation
**First Language**: Creation/CPPD (Creation Processing Program Dialect)
- Assembly-level, human-readable machine code
- Foundation of all other languages
- "Creative creation creates creative creations" (C10 naming origin)

#### Era of FUCOLA
Languages: FUCOLA, PREQ, SOBJEF, Fast, Cobra

#### Era of E
Languages: E, ESuper, SwiftCobra, Better Fucola, E*

#### Era of FlowDirect
**Major Innovation**: Nodes and Flows paradigm invented
- FlowDirect (market boom language)
- FlowScript (my favorite - beginner-friendly)
- EASY
- Emerald

#### Era of Qobra (Current)
**Market Leader**: Qobra (my proudest)
- Languages: Qobra, OptiQ, dbs, dbs*

---

### My Three Most Important Languages

#### 1. dbs (Definitive Build Structure) - MY FIRST
**Significance**: Where everything started, foundation of my language design thinking

**Core Philosophy**: "It's ALL about structures"

**Structure Hierarchy**:
```
Script Structure (hidden highest level)
  └─ Build (complete programs)
      └─ Finial (stores Foundation, Space, and 3 Structure structures)
          └─ Structure (stores Foundation and Space)
              └─ Foundation (stores Space and substructures)
                  └─ Space (only code, no structures)
                      └─ Substructure (statements with statements)
```

**Key Innovation**: Top-to-bottom colon hierarchy
- `;;` = structure level (highest)
- `:` = inside structure
- `;` = deepest code (semicolon terminates)

**Example Code**:
```dbs
!require base-dbs <- bdb

foundation main() {untilNewStructure}::
    prompt.displayText<bdb> {untilEnd("end:")}:
        return.up(1:) <(string<bdb> <- "Hello world!";
    end:

space end() [end] {}:
```
```

**Data Types**: `num`, `state`, `dec`, `text`, `string<bdb>`

**Unique Features**:
- Structure scopes explain themselves: `{untilNewStructure}`, `{untilEnd("custom:")}`
- Data flow operators show movement: `<-`, `<(`
- Adorable conditional names: `whatif`, `butif`, `justdo`
- Until loops (execute until condition becomes true)
- Records (lists) and Catalogs (dictionaries with token/item pairs)

**Variants**:
- **dbs***: Tom Havenholland's evolution with bottom-to-top colon hierarchy, introduced `when` statements
- **+DBS**: Cat Tech's power version with maximum control and transparency
- **TBS/Construct**: Tai Helix's extreme transparency (24 lines for Hello World)

---

#### 2. Qobra - MY PROUDEST
**Tagline**: "Quick Cobra" but people say it's slow (double-edged sword)

**History**:
- Started as "Cobra Plus" (enhancement of open-source Cobra)
- Grew so large it became Qobra
- 2011: Coba Co. went bankrupt
- Ownership transferred to The Qobra Foundation (community-managed)
- Became one of the most used languages

**Philosophy**: Beginner-friendly with depth, community-driven evolution

**Key Features**:

**Dynamic Typing**:
```qobra
intValue = 1
floValue = 3.14
strValue = "Hello Qobra!"
boolValue = true
```
```

**Temp Variables** (self-destruct after use):
```qobra
temp temporaryValue = 15
operation = temporaryValue + 5  # temporaryValue now deleted
```
```

**Unique Arithmetics**:
- Basic: `+`, `-`, `*`, `/`, `%`
- Advanced: `^` (exponent), `//` (floor division), `**` (floor multiplication)
- Unique: `^/` (ceiling), `&/` (round), `^^` (fang power/tetration)
- Pattern: `_` prefix = floor, `^` prefix = ceiling, `&` prefix = round

| Operator  | Floor | Ceiling | Round | Special |
|-----------|-------|---------|-------|---------|
| Division  | `//`  | `^/`    | `&/`  | -       |
| Modulo    | `%%`  | `^%`    | `&%`  | -       |
| Exponents | -     | -       | -     | `^`     |
| Fang      | -     | -       | -     | `^^`    |

**When Statements** (adapted from dbs*):
```qobra
when apples == 2 then
    output("2 apples!!")
```
```
Checks repeatedly until true, runs once, never checks again.

**When Modifiers**:
```qobra
when apples == 2 [0, 0] then  # perpetual check, perpetual run
when apples == 2 [2, 1] then  # check 2 more times, run once
```

**User Input**:
```qobra
userInput = i.add("Input a number: ")  # i = input namespace
```

**Log Conventions** (community-invented, not official feature):
```
[SUCCESS] Action completed
[ERROR] Something failed
[WARN] Not ideal but works
[LOAD] Processing...
[INFO] Context information
[DEBUG] Developer details
```

**Significance**: Shows community can create debugging methodologies that become standard practice

---

#### 3. FlowScript - MY FAVORITE
**Tagline**: Beginner-friendly gateway to the Flow family

**History**:
- Created by FS Foundation during FlowDirect market boom
- FlowDirect had nodes/flows but required `flow Main()` boilerplate
- FlowScript made entry point automatic (no top-level statements needed)
- Modernized in v1.8.0 with new features
- Surpassed FlowDirect in market share

**Philosophy**: Progressive complexity - nodes are optional, use when helpful

**Core Innovation**: Nodes with explicit I/O
```flowscript
node Double {
    input: int x,
    process: var result = x * 2,
    output: result
}
```

**Key Features**:

**No Boilerplate**:
```flowscript
direct use iofs
outputShell("Hello, World!")  # Just works, no Main() needed
```

**Static Typing**:
```flowscript
str name = "Alice"
int age = 25
dec price = 19.99
cond isActive = isTrue
```

**Type Inference**:
```flowscript
var myVars = 1  # Inferred as int
```

**V-Strings** (variable interpolation):
```flowscript
var name = "John"
outputShell(v"Hello, $name$!")
```

**Chaining with Pipeline Operator**:
```flowscript
chain node(ReadFile, path: "data.txt")
    |> node(Parse)
    |> node(Transform)
    |> outputShell()
```

**The `previous` Keyword**:
```flowscript
chain node(GetName, name: "John")
    |> node(Greet, name: previous, age: 25)
```

**Conditionals**:
```flowscript
if x > 5 do {
    outputShell("Big"),
}
next if x == 5 do {
    outputShell("Medium"),
}
default {
    outputShell("Small"),
}
```

**The `any` Type** (node-exclusive):
- Can accept any data type as input
- Must remain local to node (cannot be made global)
- Dangerous but flexible

**Flows** (optional structure):
```flowscript
flow Main() {
    var x = 5
    chain node(Double, x: x) |> outputShell()
}
```

**Why It's My Favorite**:
- Elegant syntax with clear structure
- Nodes make data flow visible
- Progressive complexity (optional features)
- Beginner-friendly without sacrificing power
- Visual symmetry (input/process/output structure)
- Teaches good practices (explicit I/O, type safety)

---

### The Flow Family Tree

**FlowDirect** (patriarch):
- Invented nodes and flows paradigm
- Market boom happened here
- Requires `flow Main()` entry point

**NodeDirect** (hardcore descendant):
- ALL code must be in nodes
- Explicit `connect` statements for data flow
- Maximum discipline, steepest learning curve
- Example:
```nodedirect
receive standardiond as std
node Print {
    input {text}
    process {std->node(Shell).print(here->text)}
}
flow Entry() {
    connect node(Input).output -> Print.input
}
```

**FlowScript** (beginner gateway):
- My favorite
- Automatic entry point
- Nodes optional
- Surpassed FlowDirect in market share

**Other Flow Family Members**:
- NodeFlow, NodeScript, CreationDirect
- HeviaScript, HeviaFlow (Hevia framework branch)
- TronGraphed (game engine language)
- IWFS, EWFS (web-focused)
- FlameLang (API-specialized, like Go)

---

### Other Notable Languages

**Fast**: Tai Helix's first language (later abandoned, then created TBS)

**Aclutterly**: Howell Clutter's readable language (2010)
- First version "Cluttered" was criticized as messy
- Second version gained attraction for readability
- 2018: Optimized version destroyed critics

**Creation Family**: First programming language ecosystem
- CPPL (first), CPPQ, CPCU, Flex, CPPD (most popular)
- CCE, Alpha, Sharp, Plus
- Various dialects and variants

---

### Corporate Entities

**Creation Official**:
- Owns Creation language family
- Strict licensing: $100 per license (Mention, Publicity, Usage)
- Additional fees for "Major Companies"
- Controversial but powerful

**FS Foundation**:
- Manages FlowScript
- Community-focused
- Made Flow paradigm accessible

**The Qobra Foundation**:
- Community-managed after Coba Co. bankruptcy (2011)
- Open development model
- Log conventions emerged from community

**Cat Tech / Cat Tech a01v**:
- Created dbs (Definitive Build Structure)
- a01v branch created +DBS (power version)

**Hevia Framework**:
- General-purpose language with multiple branches
- Known as "fastest readable code"
- HeviaScript and HeviaFlow based on NodeDirect

---

### Key People

**Tai Helix**:
- Created Fast (first language, later abandoned)
- Created TBS/Construct (transparent extreme)
- Wanted "near-full transparent view" of code

**Tom Havenholland**:
- Created dbs* (evolution of dbs)
- Reversed colon hierarchy (bottom-to-top) to discourage deep nesting
- Invented `when` statements (community suggestion)
- Cat Tech awarded and funded his project

**Howell Clutter**:
- Created Cluttered (1992, criticized as messy)
- Created Aclutterly (2010, gained attraction)
- 2018: Optimized version, destroyed critics
- Goal: Language both humans and computers understand

---

## Current Project: TinyFramework

### The Master Plan (Three Phases)

**Phase 1: TinyHook v1** (2-3 weeks)
Build package manager with standard Python libraries
- Learn package management fundamentals
- Ship something complete quickly
- Understand the problem space

**Phase 2: TinyFramework** (4-6 months)
Build modules one at a time, increasing difficulty
- Each module teaches different CS concept
- Integrate together (real system design)
- Use immediately (instant gratification)

**Phase 3: TinyHook v2** (1-2 weeks)
Remake TinyHook using TinyFramework
- Validate framework actually works
- See how much cleaner it is
- Spot gaps in framework design
- **Full circle**: Start with TinyHook, end with TinyHook, massive growth in between

### TinyFramework Modules (Planned)

#### 1. TinyObj - Custom JSON System
**What it teaches**: Parsing, serialization, data structures

**Purpose**: Build own data format (.tobj) to understand how JSON works

**Syntax** (cleaner than JSON):
```tobj
package requests {
    version: 1.0.0
    author: "John Doe"
    dependencies: [numpy, pandas]
    metadata {
        stars: 150
        downloads: 5000
    }
}
```

**Features**:
- No quotes around keys
- Supports comments with `#`
- Arrays use `[]`, objects use `{}`

**Status**: Not started, will begin after TinyHook v1

---

#### 2. TinyHook - Package Manager
**What it teaches**: File systems, dependency management, CLI design

**Core Commands**:
```bash
python tinyhook.py install requests
python tinyhook.py remove requests
python tinyhook.py list
```

**Directory Structure**:
```
tinyhook/
├── data/
│   ├── packages/       # Installed packages
│   └── installed.json  # Package database
├── tinyhook.py         # Main CLI
├── README.md
├── repo.json           # Repository configuration
└── tests/
```

**Database Schema** (installed.json):
```json
{
  "packages": {
    "requests": {
      "version": "1.0.0",
      "installed_date": "2025-01-15",
      "source": "local",
      "location": "data/packages/requests",
      "dependencies": []
    }
  },
  "metadata": {
    "tinyhook_version": "0.1.0",
    "last_updated": "2025-01-15"
  }
}
```

**Libraries to Learn**:
- `json` - Read/write package database
- `pathlib` - Cross-platform file paths
- `argparse` - CLI argument parsing
- `shutil` - Copy/move/delete operations
- `requests` - Download from remote repos (Week 4)

**Learning Path**:
- **Week 1**: Database management (load/save JSON)
- **Week 2**: Local installation (copy files)
- **Week 3**: CLI interface (argparse)
- **Week 4**: Remote repositories (download packages)
- **Week 5** (optional): Dependency resolution

**Status**: Next project to start

---

#### 3. TinyDB - Simple Database
**What it teaches**: Database design, indexing, CRUD operations

**API Design**:
```python
from tinyframework import TinyDB

db = TinyDB('users.tdb')
db.insert({'name': 'Alice', 'age': 25})
results = db.find({'age': 25})
db.update({'name': 'Alice'}, {'age': 26})
db.delete({'name': 'Alice'})
```

**Features**:
- Stores data in TinyObj format
- Simple indexing (hash maps)
- Query engine

---

#### 4. TinyTest - Testing Framework
**What it teaches**: Test-driven development, assertions, test runners

**Current Progress**: Sandbox™ is 60% of TinyTest already!

**API Design**:
```python
from tinyframework import TinyTest

test = TinyTest()

@test.case("Math works")
def test_addition():
    test.assert_equal(2 + 2, 4)
    test.assert_true(5 > 3)

test.run_all()
```

**Sandbox™ Overlap**:
- ✅ Test case management (new_instance)
- ✅ Code execution (run)
- ✅ Output logging (log)
- ✅ Beautiful formatting (boxen + rich)
- ❌ Assertions (need assert_equal, assert_true)
- ❌ Test discovery (finding tests automatically)
- ❌ Pass/fail tracking

---

#### 5. TinyLog - Logging System
**What it teaches**: Debugging, log levels, file I/O

**API Design**:
```python
from tinyframework import TinyLog

log = TinyLog('app.log')
log.debug("Variable x = 5")
log.info("User logged in")
log.warning("Disk space low")
log.error("Connection failed")
log.critical("System shutdown")
```

**Features**:
- Different log levels
- Write to file and/or console
- Timestamp each log
- Color-coded output

---

#### 6. TinyHTTP - Minimal Web Framework
**What it teaches**: HTTP protocol, networking, web servers

**API Design**:
```python
from tinyframework import TinyHTTP

app = TinyHTTP()

@app.route('/hello')
def hello():
    return "Hello, World!"

@app.route('/user/<name>')
def user(name):
    return f"Hello, {name}!"

app.run(port=8000)
```

---

#### 7. TinyCLI - Command-Line Framework
**What it teaches**: CLI design, argument parsing, user interaction

**API Design**:
```python
from tinyframework import TinyCLI

cli = TinyCLI("MyApp")

@cli.command("greet")
@cli.argument("name", help="Your name")
def greet(name):
    print(f"Hello, {name}!")

cli.run()
```

---

#### 8. TinyConfig - Configuration Management
**What it teaches**: Configuration patterns, environment variables

**API Design**:
```python
from tinyframework import TinyConfig

config = TinyConfig('config.tobj')
db_host = config.get('database.host')
api_key = config.get('api.key', default='')
db_host = config.env('DATABASE_HOST', 'database.host')
```

---

#### 9. TinyCache - Caching System
**What it teaches**: Memory management, performance optimization

**API Design**:
```python
from tinyframework import TinyCache

cache = TinyCache(max_size=100, ttl=3600)
cache.set('user:123', {'name': 'Alice'})
user = cache.get('user:123')
```

**Learn**: LRU eviction, TTL, memory limits

---

#### 10. TinyScheduler - Task Scheduling
**What it teaches**: Event loops, async programming, cron jobs

**API Design**:
```python
from tinyframework import TinyScheduler

scheduler = TinyScheduler()

@scheduler.every(seconds=10)
def check_status():
    print("Checking...")

@scheduler.at("09:00")
def morning_report():
    print("Good morning!")

scheduler.run()
```

---

### Integration Example
```python
from tinyframework import TinyDB, TinyLog, TinyHTTP, TinyConfig

config = TinyConfig('app.tobj')
log = TinyLog('app.log')
db = TinyDB('users.tdb')
app = TinyHTTP()

@app.route('/users')
def get_users():
    log.info("Fetching all users")
    users = db.find({})
    return users

app.run(port=config.get('server.port', 8000))
```

---

## Key Learning Insights

### The Pattern Recognition Journey
**Kindergarten Math** → **Scratch Logic** → **Python Systems** → **C++ Memory** → **Language Design**

Each step unlocked new mental models:
- Math: Abstract thinking
- Scratch: Visual logic
- Python: Structured programming
- C++: Memory and performance
- Languages: System architecture

### Learning Style Characteristics
- **Efficient extraction**: Learn core concept, move on (doesn't always "complete")
- **Systems thinking**: Interested in how things work underneath
- **Pattern recognition**: See connections others miss
- **Exploration mode**: Try many things, follow curiosity
- **Project-driven**: Learn by building, not just reading

### The "Incomplete" Projects Aren't Failures
- Scratch: Didn't finish own game, but learned logic
- boot.dev: 70% through OOP, but picked up OOP naturally in C++ later
- Various backups lost: Extracted learning, that was enough

**Understanding = Success. Completion = Optional.**

### What Makes Me Different
Most 13-year-olds who code:
- Follow tutorials
- Copy-paste solutions
- Build what others built
- Stop when stuck

I:
- Understand the *why* behind tutorials
- Adapt solutions to new problems (calculator from language tutorial)
- Design systems from scratch (Languages Saga)
- Pivot when stuck (laptop breaks → switch to Linux)

### Future Considerations
**Breadth vs Depth**: Currently excelling at breadth (exploration). Will need to develop depth (sustained focus on one project) around age 16-18.

**The Wall**: Will eventually hit problems requiring 100+ hours of grinding with no new patterns. That's where mastery happens.

**Career Path**: Game dev is perfect for systems thinking - games are systems of systems (graphics, physics, input, audio, logic, networking).

---

## Teaching Preferences & Communication

### DO:
- ✅ Teach concepts, let me implement
- ✅ Explain libraries/tools I'm unfamiliar with
- ✅ Progressive difficulty (start simple, build up)
- ✅ Connect to systems thinking (show how pieces fit)
- ✅ Challenge me without overwhelming
- ✅ Be honest about complexity and timelines
- ✅ Show excitement about systems/architecture
- ✅ Respect my time (school is priority)

### DON'T:
- ❌ Give full code (teach, don't solve)
- ❌ Condescend (I'm 13 but think like architect)
- ❌ Over-explain basics I already know
- ❌ Hold back on advanced concepts
- ❌ Assume I'm "too young" for something
- ❌ Use AI-typical phrases that sound robotic

---

## Important Context & References

### Brother's Support
- Bought boot.dev subscription (saw my potential)
- **Just bought Claude Pro** (unlimited messages, no more limits)
- Believes in my growth, proven track record of supporting learning

### Current Focus Areas
1. **Pygame**: Learning game development fundamentals
2. **TinyHook**: About to start building
3. **School Robotics**: Using C++ in club
4. **Languages Saga**: Ongoing worldbuilding

### Quick Reference Glossary
- **Qobra** = Proudest language (community-driven, innovative)
- **dbs** = First language (structure-based, foundation)
- **FlowScript** = Favorite language (elegant, teachable, nodes/flows)
- **TinyFramework** = Current ambitious project
- **Sandbox™** = Testing framework I built "on a break"
- **Languages Saga** = Worldbuilding project, potential novel/implementation

### Technologies I Know
- **Languages**: Python (advanced), C++ (intermediate), C# (beginner)
- **Tools**: Git, Linux (Fedora), WSL, VS Code
- **Libraries**: json, pathlib, argparse, shutil, requests, colorama, pyboxen, rich, pygame

### Technologies I'm Learning
- Pygame (game dev)
- More C++ (pointers, memory, robotics)
- C# (Unity/Godot eventually)
- Web frameworks (eventually TinyHTTP)

---

## Timeline & Goals

### Short-Term (Next 3 Months)
- Complete TinyHook v1
- Continue Pygame learning
- School robotics projects
- Maybe start TinyObj

### Medium-Term (6-12 Months)
- Build 3-5 TinyFramework modules
- Ship some small games
- Expand Languages Saga
- Keep exploring (tools, concepts, projects)

### Long-Term (Age 16-18)
- Decide: Still interested in FlowScript/Languages Saga?
- If yes: Build MiniFlow (simplified FlowScript)
- If no: That's fine, learned tons from designing
- Pick one big project for depth (game? language? framework?)

### Dream (Age 18-21+)
- Game developer career path
- Maybe build full FlowScript
- Maybe write Languages Saga as novel
- Maybe both (novel + working language)

---

## What Sets Me Apart

**At 13, I've:**
- Designed 15+ programming languages with complete syntax
- Built calculator with lexer/parser/interpreter
- Created testing framework with professional UX
- Learned Python, C++, C#, Linux
- Switched to Linux as main OS
- Architected multi-component framework (TinyFramework)
- Planned realistic three-phase implementation
- Completed projects and shipped to GitHub

**I'm not just learning programming. I'm learning systems.**

**I'm not collecting languages. I'm collecting mental models.**

**I'm not building projects. I'm exploring the design space of what's possible.**

---

## Final Notes

This is goodbye to free tier limitations.

This is hello to unlimited exploration.

**Keep the energy. Keep the curiosity. Keep building.**

**The Languages Saga isn't just worldbuilding - it's mapping the design space of programming languages.**

**TinyFramework isn't just a project - it's understanding computer science from first principles.**

**Goodbye, My first Free Claude.**

**And this journey? This is just getting started.** 🚀

---

*"Understanding = Success. Completion = Optional."*

*"Systems thinking at 13. Imagine at 21."*

*End of Document*
