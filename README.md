# Local AI Labs (Autonomous Coding Agents with MLX)

A collection of experiments, benchmarks, and architectures for building autonomous AI coding agents running locally on Apple Silicon using [MLX](https://github.com/ml-explore/mlx) and open-weights LLMs (such as Qwen 2.5 Coder 7B).

## Projects & Demos

### 1. MLX Autonomous TDD Coding Agent (`agent/` + `project/`)
An autonomous Test-Driven Development (TDD) loop running locally on an M-series Mac:
- **Planner (`agent/planner.py`)**: Prompts the local LLM with available tools, failing test traces, and rules.
- **Executor (`agent/executor.py`)**: Dispatches parsed tool invocations.
- **Tools (`agent/tools.py`)**: File system inspection (`read_file`, `write_file`, `replace_in_file`) and test runner execution (`run_tests` running Vitest).
- **Target Project (`project/`)**: A TypeScript test suite with mathematical logic and concurrency queue tasks.

---

## Quickstart: Running the Agent Demo

### Interactive Tutorial Branches:
- **`demo-start`**: The initial buggy baseline (`math.ts` logic bug, `queue.ts` concurrency timeout, and `tools.py` `.strip()` bug).
- **`demo-end`**: The fully resolved, passing reference solution.

### Step-by-Step Reproduction:

```bash
# 1. Clone the repository and checkout the starting buggy branch
git clone -b demo-start https://github.com/Amoyaw-Curtis/local-ai-labs.git
cd local-ai-labs

# 2. Set up Python virtual environment with MLX
python -m venv venv
source venv/bin/activate
pip install mlx-lm

# 3. Install TypeScript project dependencies
cd project && npm install && cd ..

# 4. Launch the autonomous agent loop
python -m agent.agent
```

---

## Branch Comparison

Compare the starting buggy state directly against the resolved solution:
- [View Compare: `demo-start` vs `demo-end`](https://github.com/Amoyaw-Curtis/local-ai-labs/compare/demo-start...demo-end)
