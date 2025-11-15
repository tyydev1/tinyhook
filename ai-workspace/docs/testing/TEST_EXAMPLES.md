# Test Examples and Practical Usage

This guide shows how to use the TinyHook test suite in real development scenarios.

## Scenario 1: You Modified `read_db()` Function

**Situation**: You're improving the error handling in `read_db()` to return a proper dictionary instead of `{"None"}`.

### Step 1: Run Tests First (Before Changes)

```bash
cd /home/razkar/Documents/Workspace/GitHub/tyydev1/tinyhook
python -m pytest tests/test_thpu.py::TestDatabaseFunctions -v
```

**Output**: All 10 database tests pass, documenting current behavior.

### Step 2: Make Your Changes

Edit `/home/razkar/Documents/Workspace/GitHub/tyydev1/tinyhook/thpu.py` line 30-36:

```python
def read_db(file_location):
    try:
        with open(file_location, "r") as f:
            return json.load(f)
    except:
        print(f"File '{file_location}' not found.")
        return {}  # Changed from {"None"} to {}
```

### Step 3: Run Tests Again

```bash
python -m pytest tests/test_thpu.py -v
```

**Expected**: All 54 tests still pass! Plus, two previously failing tests now pass:
- `test_get_package_info_handles_missing_repo_file`
- `test_get_package_info_handles_malformed_repo_file`

### Step 4: Update Tests to Reflect Better Behavior

Update lines 414-426 in test_thpu.py to expect `None` instead of AttributeError:

```python
def test_get_package_info_handles_missing_repo_file(self):
    """Test that get_package_info handles missing repo.json gracefully."""
    nonexistent_path = os.path.join(self.test_dir, "nonexistent.json")
    result = get_package_info("numpy", nonexistent_path)
    # Now returns None safely (was AttributeError before)
    self.assertIsNone(result)
```

### Step 5: Verify All Tests Pass

```bash
python -m pytest tests/test_thpu.py -v
```

Result: All 54 tests pass, confirming your fix is solid.

---

## Scenario 2: You Added a New Command

**Situation**: You're adding a new `validate` command to check package integrity.

### Step 1: Understand the Pattern

Look at existing command tests to understand the pattern:

```bash
# Read and study the hook command tests
cat tests/test_thpu.py | grep -A 20 "class TestHookCommandLogic"
```

You'll see the pattern:
1. Setup test database
2. Call the command function
3. Assert the expected behavior

### Step 2: Write Tests for Your New Command

Add to test_thpu.py:

```python
class TestValidateCommandLogic(unittest.TestCase):
    """Tests for the 'validate' command."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.installed_json_path = os.path.join(self.test_dir, "installed.json")

        # Create test data
        test_data = {
            "numpy": {"version": "1.23.0", "install_path": "data/packages/numpy"},
            "invalid-pkg": {"version": "1.0", "install_path": "nonexistent/path"}
        }
        with open(self.installed_json_path, "w") as f:
            json.dump(test_data, f)

        self.patcher = patch("thpu.INSTALLED_JSON", self.installed_json_path)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_validate_command_checks_installed_packages(self):
        """Test that validate command checks package integrity."""
        # Your validate logic here
        pass

    def test_validate_command_reports_missing_packages(self):
        """Test that validate detects missing package files."""
        # Your validate logic here
        pass

    def test_validate_command_with_all_valid_packages(self):
        """Test that validate passes when all packages present."""
        # Your validate logic here
        pass
```

### Step 3: Run Your New Tests

```bash
python -m pytest tests/test_thpu.py::TestValidateCommandLogic -v
```

The tests will fail (red), showing you what needs to be implemented.

### Step 4: Implement the Command

Write the actual `validate` command in thpu.py.

### Step 5: Run Tests Again

```bash
python -m pytest tests/test_thpu.py::TestValidateCommandLogic -v
```

Tests turn green! You now have coverage for your new command.

---

## Scenario 3: You Found a Bug

**Situation**: The `list` command doesn't properly format package information.

### Step 1: Write a Test That Fails

Add to test_thpu.py:

```python
def test_list_command_formats_output_correctly(self):
    """
    Test that list command formats output as 'package - version X.X.X'.

    Current behavior might show wrong format.
    """
    test_data = {
        "numpy": {"version": "1.23.0"},
        "pandas": {"version": "1.5.0"}
    }
    with open(self.installed_json_path, "w") as f:
        json.dump(test_data, f)

    # Capture output (you'd need to mock print)
    # Verify format is: "package - version X.X.X"
    # This test will FAIL until you fix the bug
```

### Step 2: Run the Test

```bash
python -m pytest tests/test_thpu.py::TestListCommandLogic::test_list_command_formats_output_correctly -v
```

It fails, documenting the bug with a test.

### Step 3: Fix the Bug

Fix the list command in thpu.py to format output correctly.

### Step 4: Run the Test Again

```bash
python -m pytest tests/test_thpu.py::TestListCommandLogic::test_list_command_formats_output_correctly -v
```

Test passes! Bug is fixed and documented.

---

## Scenario 4: You're Optimizing Performance

**Situation**: Package manager is slow with 1000+ packages. You're optimizing database operations.

### Step 1: Create a Performance Test

Add to test_thpu.py:

```python
import time

def test_database_performance_with_large_dataset(self):
    """Test database operations with realistic large dataset."""
    db_path = os.path.join(self.test_dir, "large.json")

    # Create 5000 packages
    large_data = {f"package{i}": {"version": f"1.{i%10}.0"} for i in range(5000)}

    # Time the write operation
    start = time.time()
    write_db(large_data, db_path)
    write_time = time.time() - start

    # Time the read operation
    start = time.time()
    result = read_db(db_path)
    read_time = time.time() - start

    # Verify performance is acceptable
    self.assertLess(write_time, 1.0)  # Write should complete in < 1 second
    self.assertLess(read_time, 1.0)   # Read should complete in < 1 second
    self.assertEqual(len(result), 5000)
```

### Step 2: Run the Performance Test

```bash
python -m pytest tests/test_thpu.py -v -s --durations=10
```

Shows current performance baseline.

### Step 3: Make Optimizations

Refactor database operations.

### Step 4: Run Tests Again

```bash
python -m pytest tests/test_thpu.py -v --durations=10
```

Verify optimizations improved performance without breaking functionality.

---

## Scenario 5: You're Adding Unicode Support

**Situation**: You want to ensure package names can use unicode characters.

### Step 1: Look at Existing Edge Case Test

```bash
grep -A 15 "test_unicode_characters" tests/test_thpu.py
```

Reveals the pattern for unicode testing.

### Step 2: Extend the Test

```python
def test_package_names_with_unicode(self):
    """Test that package names can contain unicode characters."""
    db_path = os.path.join(self.test_dir, "unicode.json")

    test_data = {
        "numpy_日本語": {"version": "1.0"},
        "pandas_中文": {"version": "1.0"},
        "matplotlib_русский": {"version": "1.0"}
    }

    write_db(test_data, db_path)
    result = read_db(db_path)

    self.assertIn("numpy_日本語", result)
    self.assertIn("pandas_中文", result)
    self.assertIn("matplotlib_русский", result)
```

### Step 3: Run the Test

```bash
python -m pytest tests/test_thpu.py::TestEdgeCasesAndDataValidation::test_package_names_with_unicode -v
```

If it passes, unicode is already supported! If it fails, you've identified what needs fixing.

---

## Quick Reference: Common Test Commands

### Run All Tests
```bash
python -m pytest tests/test_thpu.py -v
```

### Run Specific Test Class
```bash
python -m pytest tests/test_thpu.py::TestDatabaseFunctions -v
```

### Run Specific Test
```bash
python -m pytest tests/test_thpu.py::TestDatabaseFunctions::test_read_db_loads_valid_json -v
```

### Show Test Durations (Slowest Tests)
```bash
python -m pytest tests/test_thpu.py -v --durations=5
```

### Stop on First Failure
```bash
python -m pytest tests/test_thpu.py -v -x
```

### Show Full Output (Print Statements)
```bash
python -m pytest tests/test_thpu.py -v -s
```

### Run Tests Matching a Pattern
```bash
# All tests related to 'install' or 'hook'
python -m pytest tests/test_thpu.py -v -k "hook or install"

# All error handling tests
python -m pytest tests/test_thpu.py -v -k "handles"

# All edge case tests
python -m pytest tests/test_thpu.py::TestEdgeCasesAndDataValidation -v
```

### Generate Test Report
```bash
# With coverage (requires pytest-cov)
python -m pytest tests/test_thpu.py -v --cov=thpu --cov-report=html

# With JUnit XML (for CI/CD)
python -m pytest tests/test_thpu.py -v --junit-xml=results.xml
```

---

## How Tests Guide Development

### The Red-Green-Refactor Cycle

1. **RED**: Write a test that fails (documents desired behavior)
2. **GREEN**: Write minimal code to make test pass (just works)
3. **REFACTOR**: Clean up code while keeping tests green (polish)

### Example with the hook command:

```
STEP 1 - RED (Test fails, behavior not implemented)
$ python -m pytest tests/test_thpu.py::TestHookCommandLogic::test_hook_command_adds_new_package -v
FAILED - test hasn't been implemented yet

STEP 2 - GREEN (Implement minimal functionality)
# Add hook command implementation to thpu.py
$ python -m pytest tests/test_thpu.py::TestHookCommandLogic::test_hook_command_adds_new_package -v
PASSED - basic implementation works

STEP 3 - REFACTOR (Improve quality)
# Refactor hook command for better error handling, cleaner code
$ python -m pytest tests/test_thpu.py::TestHookCommandLogic -v
PASSED - all hook tests pass, code is cleaner

STEP 4 - ADD MORE TESTS
# Write test for dry-run flag
# Write test for quiet flag
# Cycle repeats for new features
```

---

## Test-Driven Development Tips

### 1. Write the Test First

Before implementing a feature:
```bash
# 1. Write test that describes desired behavior
# 2. Run test (it fails - RED)
# 3. Implement feature (test passes - GREEN)
# 4. Improve code quality (stay GREEN)
```

### 2. Use Test Names as Documentation

Good test names describe behavior better than comments:

```python
# Good: Test name is self-documenting
def test_hook_command_rejects_duplicate_installation(self):
    """Prevents installing same package twice."""

# Bad: Name doesn't explain what's being tested
def test_hook_2(self):
    """Test hook."""
```

### 3. One Assertion Per Test (Usually)

Tests are easiest to understand with one clear assertion:

```python
# Good: One clear thing being tested
def test_init_db_creates_file(self):
    init_db(path)
    self.assertTrue(os.path.exists(path))

# Less clear: Multiple assertions make failures ambiguous
def test_init_db(self):
    init_db(path)
    self.assertTrue(os.path.exists(path))
    with open(path) as f:
        data = json.load(f)
    self.assertEqual(data, {})
    self.assertIsNotNone(data)
```

### 4. Test the Behavior, Not the Implementation

```python
# Good: Tests what the function does (behavior)
def test_is_installed_detects_installed_package(self):
    # Setup
    installed_data = {"numpy": {...}}
    # Act & Assert
    self.assertTrue(is_installed("numpy"))

# Less good: Tests how it's implemented (fragile)
def test_is_installed_reads_json_file(self):
    # Would break if implementation changed to use database
    with patch('json.load') as mock_load:
        is_installed("numpy")
        mock_load.assert_called_once()
```

### 5. Use Fixtures for Common Setup

The test classes already do this with setUp/tearDown:

```python
def setUp(self):
    """This runs before each test - common setup"""
    self.test_dir = tempfile.mkdtemp()
    self.test_db = os.path.join(self.test_dir, "test.json")

def tearDown(self):
    """This runs after each test - cleanup"""
    shutil.rmtree(self.test_dir, ignore_errors=True)
```

---

## Understanding Test Failure Messages

### Example 1: Assertion Failure

```
FAILED tests/test_thpu.py::TestDatabaseFunctions::test_read_db_loads_valid_json

AssertionError: {'package1': {'version': '1.0'}} != {'package2': {'version': '2.0'}}
```

**What it means**: Expected one data but got different data. Check if write_db is working.

### Example 2: File Not Found

```
FAILED tests/test_thpu.py::TestIsInstalledFunction::test_is_installed_returns_true

FileNotFoundError: [Errno 2] No such file or directory: '/tmp/.../installed.json'
```

**What it means**: The test database wasn't created. Check setUp method.

### Example 3: Unexpected Exception

```
FAILED tests/test_thpu.py::TestHookCommandLogic::test_hook_command_adds_new_package

AttributeError: 'set' object has no attribute 'get'
```

**What it means**: Function raised unexpected error. This is the bug we documented - read_db returns wrong type.

### Example 4: Timeout

```
FAILED tests/test_thpu.py::TestDatabaseIntegration - Timeout
```

**What it means**: Test took too long (infinite loop?). Check for proper cleanup and error handling.

---

## Running Tests with Your Favorite Editor

### VS Code

1. Install Python extension
2. Create `.vscode/settings.json`:
```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"]
}
```
3. Click test icon on left sidebar
4. Run tests directly from editor

### PyCharm / IntelliJ

1. Right-click on test file
2. Select "Run pytest in tests"
3. View results in test panel

### Command Line (vim/nano users)

```bash
# Run in tmux window
tmux new-window -n tests "cd /path && python -m pytest tests/test_thpu.py -v"

# Run with watch mode (requires pytest-watch)
ptw tests/test_thpu.py -v
```

---

## Making Tests Part of Your Workflow

### Before Every Commit

```bash
# 1. Run all tests
python -m pytest tests/test_thpu.py -v

# 2. Verify they all pass
# 3. Check for new issues
python -m pytest tests/test_thpu.py --tb=short

# 4. Commit only if all tests pass
git add .
git commit -m "Feature: ..."
```

### Creating a Git Hook

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
cd /home/razkar/Documents/Workspace/GitHub/tyydev1/tinyhook
python -m pytest tests/test_thpu.py -v --tb=short
if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

Now tests run automatically before commits.

---

## Next Learning Steps

1. **Read the test docstrings** - Each test has a detailed explanation
2. **Run a single test** - `pytest tests/test_thpu.py::TestDatabaseFunctions::test_read_db_loads_valid_json -v`
3. **Modify a test** - Change an assertion to understand what tests validate
4. **Write a new test** - Add a test for the next feature you want to implement
5. **Study setUp/tearDown** - Understand how tests are isolated
6. **Explore mocking** - Look at @patch usage in edge case tests

---

## Resources

- **Official pytest docs**: https://docs.pytest.org/
- **Python unittest docs**: https://docs.python.org/3/library/unittest.html
- **Test-Driven Development (TDD)**: Understanding the philosophy behind these tests

---

**Created**: 2025-11-09
**Version**: 1.0
**Status**: Learning Reference
