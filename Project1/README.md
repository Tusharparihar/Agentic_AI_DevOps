# Agentic AI for DevOps (Docker Assistant)

This project is my hands-on practice for building an AI DevOps assistant using Ollama, LangChain, and MCP.

The assistant focuses on Docker troubleshooting in short, practical answers:
- what went wrong
- likely root cause
- quick fix

## What This Project Contains

- `my_first_generative_ai.py`
  - Basic Ollama chat loop.
  - Uses a system prompt to keep answers short and Docker-focused.

- `agent.py`
  - LangChain agent with local Python tools.
  - Tools can run Docker commands:
    - show running containers (`docker ps`)
    - show logs for a container (`docker logs --tail 10 <container_name>`)

- `mcp_server.py`
  - FastMCP server that exposes Docker tools.
  - This lets an external agent call Docker tools through MCP.

- `agent_with_mcp.py`
  - LangChain agent connected to `mcp_server.py` using MCP adapters.
  - Runs as continuous chat so user can ask multiple questions.

- `requirements.txt`
  - Python dependencies used in this project.

## Tech Stack

- Python
- Ollama
- LangChain
- LangGraph
- FastMCP
- LangChain MCP Adapters
- Docker CLI

## How To Run

## 1) Setup

```bash
python -m venv venv
source venv/bin/activate   # Linux/WSL
# venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
```

Make sure:
- Ollama is installed and running
- Model is available (example: `gemma4:31b-cloud`)
- Docker is installed and running

## 2) Run Basic Chat

```bash
python my_first_generative_ai.py
```

## 3) Run Tool-Based Agent

```bash
python agent.py
```

## 4) Run MCP-Based Agent

```bash
python agent_with_mcp.py
```

## Example Questions

- `show me running containers`
- `check logs of container nginx`
- `why my container is restarting again and again?`

## Why I Built This

I am learning Agentic AI for real DevOps workflows.
This project shows my progress in:
- LLM prompting
- tool calling
- MCP integration
- practical Docker debugging assistant design

## Note

This is a learning project and currently focused on Docker-only troubleshooting.