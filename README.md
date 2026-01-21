# graflow-examples
Example codes repos for Graflow workflows

## Prerequisites

- Python 3.11 or higher

## Installation

### 1. Install uv (if not already installed)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or via Homebrew (macOS):
```bash
brew install uv
```

### 2. Clone the repository

```bash
git clone https://github.com/myui/graflow-examples.git
cd graflow-examples
```

### 3. Set up the project

```bash
# Create a virtual environment and install dependencies
uv sync
```

This will automatically create a `.venv` directory and install all dependencies including `graflow[all]`.

### 4. Activate the virtual environment (optional)

```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

Alternatively, you can run commands directly using `uv run`:
```bash
uv run python your_script.py
```

## Adding graflow to a new project

If you're starting a new project and want to add graflow:

```bash
# Initialize a new project
uv init my-project
cd my-project

# Add graflow with all extras
uv add graflow --extra all
```
