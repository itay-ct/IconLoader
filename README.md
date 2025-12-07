# Lucide Icon Loader

Create a searchable vector database of Lucide icons using semantic embeddings. Run entirely in Google Colab - no local setup required!

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/itay-ct/IconLoader/blob/main/IconLoader.ipynb)

## What It Does

- Fetches icon metadata from the Lucide GitHub repository
- Generates semantic embeddings using the `all-MiniLM-L6-v2` model
- Stores icons in Redis with vector search capabilities
- Tests the index with configurable test cases and generates pass/fail reports

## Quick Start

1. **Click the badge above** to open in Google Colab
2. **Run Step 1** - Enter your Redis URL when prompted
3. **Run Step 2** - Check what icons are already indexed
4. **Run Step 3** (optional) - Upload `icons.txt` to update icons, or skip to use existing
5. **Run Step 4** - Configure test cases with expected results
6. **Run Step 5** - Execute tests and see detailed report

## Workflow

### Step 1: Setup
- Installs dependencies
- Connects to Redis
- Creates vector index

### Step 2: Check Existing Icons
- Shows what's already indexed
- Tells you if you can skip to testing

### Step 3: Update Icons (Optional)
- Upload `icons.txt` file
- Fetches metadata from Lucide GitHub
- Generates embeddings
- Indexes in Redis
- **Skip this step if you just want to test existing icons**

### Step 4: Configure Tests
Define test cases with expected results:
```python
TEST_DATASET = [
    ("Found 5 places offering a relaxing drink", "beer"),
    ("I found 9 parks to enjoy nature", "trees"),
    # Add your test cases...
]
```

### Step 5: Run Tests
- Executes all test queries
- Shows ✓ PASS or ✗ FAIL for each
- Generates summary report with statistics

## Example Output

```
[Test 1] ✓ PASS
  Query: "Found 5 places offering a relaxing drink"
  Expected: beer
  Actual:   beer

[Test 2] ✗ FAIL
  Query: "I found 9 parks to enjoy nature"
  Expected: trees
  Actual:   tree-palm
  ⚠ Mismatch detected!

======================================
TEST SUMMARY REPORT
======================================
Total Tests:  10
Passed:       8 (80.0%)
Failed:       2 (20.0%)
```

## Prerequisites

- Google account (for Colab)
- Redis instance (local or cloud-hosted like Redis Cloud)
- `icons.txt` file with icon slugs (one per line) - only needed if updating icons

## Redis Setup

### Free Option: Redis Cloud
1. Sign up at [Redis Cloud](https://redis.com/try-free/)
2. Create a free database
3. Copy the connection URL
4. Use it in Step 1 of the notebook

### Local Option
```bash
# Install Redis (macOS)
brew install redis

# Start Redis
redis-server

# Use this URL in the notebook:
redis://localhost:6379
```

## Files

- **IconLoader.ipynb** - Main Jupyter notebook
- **icons.txt** - Sample icon list (beer, wine, trees, etc.)
- **.env.example** - Redis URL template for reference
- **LICENSE** - MIT License

## License

MIT

