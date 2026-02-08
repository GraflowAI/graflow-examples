# graflow-examples

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GraflowAI/graflow-examples/blob/main/examples/notebooks/simple_etl.ipynb)

Example workflows for [Graflow](https://github.com/GraflowAI/graflow).

## Quick Start

```bash
git clone https://github.com/GraflowAI/graflow-examples.git
cd graflow-examples
uv sync
```

Run an example:

```bash
PYTHONPATH=. uv run python examples/simple_etl/workflow.py
```

## Generate Workflows with Claude Code

This repo includes a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that generates Graflow workflows through a structured plan-implement-review process.

```bash
# Launch Claude Code in this repo (the skill is auto-loaded from .claude/skills/)
claude

# Then use the /graflow-workflow command
> /graflow-workflow Create an ETL pipeline that loads CSV data, filters rows, and outputs a summary
```

The `/graflow-workflow` skill guides you through:
1. **Plan** — Requirements gathering and design document
2. **Implement** — Code generation following Graflow patterns
3. **Review** — Validation and README creation

<p align="left">
  <a href="https://youtu.be/Wda9v0ndUYQ">
    <img width="467" height="282" alt="image" src="https://github.com/user-attachments/assets/af48a126-0378-4521-af11-b0394e1b5fda" />
  </a>
</p>
