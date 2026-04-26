# AIOps Conversational CLI (Docker Monitoring + SOP Generator)

This project is a learning-focused AIOps assistant that helps you monitor Docker containers, detect issues, explain likely root cause, and generate a Standard Operating Procedure (SOP) document from the latest analysis.

It is built with Python, LangChain, Ollama, and Docker CLI tools.

## What This Project Does

- Detects container-level operational issues:
  - exited/crashed containers
  - unhealthy containers (if health checks exist)
  - recent error logs
  - resource usage snapshots (CPU/Memory)
- Gives conversational incident analysis and suggested fixes
- Generates a structured `SOP.md` from the last detected incident analysis

## Project Files

- `main.py`
  - Entry point for the conversational CLI.
  - Handles chat loop (`AIOps >`) and SOP generation trigger.

- `agent.py`
  - Core AIOps agent (`AIOpsAgent`).
  - Defines tool wrappers for Docker monitoring functions.
  - Uses `ChatOllama` model (`gemma4:31b-cloud`) for analysis.
  - Stores `last_analysis` for SOP generation.

- `monitor.py`
  - Docker command execution layer.
  - Fetches:
    - containers list (`docker ps -a`)
    - health status (`docker inspect`)
    - error logs (`docker logs --tail 50` with keyword filtering)
    - stats (`docker stats --no-stream`)

- `sop_generator.py`
  - Converts the latest analysis text into a structured incident SOP document.
  - Writes output to `SOP.md`.

- `SOP.md`
  - Example/generated output document.

- `requirements.txt`
  - Python dependencies.

## How It Works (Flow)

1. You ask a question in CLI (example: "scan containers for issues").
2. Agent calls monitoring tools from `monitor.py`.
3. Tool output (container states/logs/health/stats) is passed to the LLM.
4. LLM returns analysis with root-cause guidance and fix steps.
5. If response includes analysis/root-cause style content, it is saved as `last_analysis`.
6. When you ask for SOP, `sop_generator.py` creates `SOP.md` from `last_analysis`.

## Prerequisites

Install and verify:

- Python 3.10+
- Docker Desktop (or Docker Engine in Linux/WSL)
- Ollama running locally
- Ollama model pulled:

```bash
ollama pull gemma4:31b-cloud
```

Also ensure Docker daemon is running before starting this tool.

## Setup

### 1) Create and activate virtual environment

Linux/WSL:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Important: Always prefer `python -m pip ...` (or `python3 -m pip ...`) to ensure pip installs into the active environment.

## Run the Project

From the `AIOps` folder:

Linux/WSL:

```bash
python3 main.py
```

Windows PowerShell:

```powershell
python main.py
```

You will see a prompt like:

```text
AIOps >
```

Then ask conversational questions.

## Example Prompts

- `Scan my containers for any issues`
- `Why is my db container crashing?`
- `Check health of all services`
- `Analyze recent container errors`
- `Generate an SOP for the last issue`

## SOP Generation

SOP generation works only after at least one analysis is available.

Recommended sequence:

1. Ask for scan/analysis first.
2. Ask for SOP:

```text
generate sop
```

Output file created/updated:

- `SOP.md`

## Important CLI Note

Current `main.py` is conversational and does not define command-line flags like `--scan` or `--sop`.

So this command is not supported by current code:

```bash
python main.py --scan --sop
```

Use interactive prompts after running `main.py`.

## Troubleshooting

### 1) `python: command not found` (WSL)

Use `python3` instead:

```bash
python3 main.py
```

### 2) `externally-managed-environment` during pip install

You are hitting system Python restrictions (PEP 668). Use a venv and install via the venv Python:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

If needed, verify which Python is active:

```bash
which python
which pip
```

Both should point inside `.../AIOps/venv/...` while venv is active.

### 3) Docker command errors

If tools fail to get container data:

- Confirm Docker is running
- Check permission to run Docker commands
- Test manually:

```bash
docker ps -a
docker logs --tail 50 <container_id>
```

### 4) Ollama/model issues

If model invocation fails:

- Ensure Ollama service is running
- Ensure model exists:

```bash
ollama list
```

- Pull the model again if missing

## Tech Stack

- Python
- LangChain
- LangChain Community
- LangGraph
- Ollama
- Docker CLI

## Learning Scope and Current Limits

This is a learning project focused on Docker-centric AIOps workflows.

Current limits:

- No built-in CLI flags (`--scan`, `--sop`) yet
- Health checks depend on container images defining `HEALTHCHECK`
- Detection quality depends on available logs and runtime metadata

## Suggested Next Improvements

- Add argparse flags (`--scan`, `--sop`, `--container <id>`)
- Add structured JSON incident report output
- Add severity scoring (Critical/High/Medium/Low)
- Add optional auto-remediation command suggestions
- Add tests for monitor functions and SOP generation

---

Built as hands-on practice for Agentic AI in DevOps operations and incident response.