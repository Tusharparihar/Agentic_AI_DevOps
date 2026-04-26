# Agentic AI for DevOps

This repository contains my hands-on learning projects for building Agentic AI systems in real DevOps workflows.

The focus is Docker operations, troubleshooting, monitoring, and incident response automation using LLM agents, tools, and MCP.

## Repository Structure

- `Project1/`
  - Foundation project for Agentic AI + Docker assistant patterns.
  - Includes basic chat, tool-calling agent, and MCP-based setup.

- `Project2/AIOps/`
  - Advanced AIOps conversational CLI.
  - Detects Docker issues, analyzes likely root cause, and generates SOP documents.

## Project1 Overview (Agentic Docker Assistant)

`Project1` is the first learning stage where core building blocks were implemented.

### Key Components

- `my_first_generative_ai.py`
  - Basic Ollama chat loop with Docker-focused prompt behavior.

- `agent.py`
  - LangChain agent with local tool calls for Docker checks.

- `mcp_server.py`
  - FastMCP server exposing Docker operations as MCP tools.

- `agent_with_mcp.py`
  - Agent connected to MCP server for tool-enabled conversational debugging.

### What It Demonstrates

- LLM prompting strategy
- Local tool calling
- MCP server integration
- Practical Docker troubleshooting workflow

## Project2 Overview (AIOps Conversational CLI)

`Project2/AIOps` is the next stage with stronger operational focus.

### Key Components

- `main.py`
  - Conversational CLI entry point.

- `agent.py`
  - AIOps agent with tool wrappers and analysis flow.

- `monitor.py`
  - Docker signal collection layer:
    - container states
    - health checks
    - error logs
    - resource stats

- `sop_generator.py`
  - Converts latest incident analysis into `SOP.md`.

### What It Demonstrates

- Conversational incident triage
- Automated anomaly context gathering from Docker
- Root-cause oriented response generation
- SOP generation for incident handling and documentation

## Common Tech Stack

- Python
- Ollama
- LangChain
- LangGraph
- Docker CLI
- MCP (Model Context Protocol)

## Quick Start

Choose the project you want to run and open its folder first.

### Project1

```bash
cd Project1
python -m venv venv
source venv/bin/activate   # Linux/WSL
# venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
python agent.py
```

### Project2 (AIOps)

```bash
cd Project2/AIOps
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python3 main.py
```

## Notes

- Ensure Docker is running before using either project.
- Ensure Ollama is running and required model(s) are pulled.
- In WSL, use `python3` if `python` command is unavailable.

## Learning Goal

This repository tracks my progression from basic agent setup to practical AIOps workflows that can support real DevOps monitoring and incident response tasks.
