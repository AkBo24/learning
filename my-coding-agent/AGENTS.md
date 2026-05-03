# AGENTS.md

## Overview

This repository contains a Python coding-agent. `main.py` runs an interactive command line loop, currently implemented using the OpenAI Responses API. The agents receives a system prompt, maintains a conversation history, and invokes local registered tools until a final text response is produced.

## Setup

Use the existing virtual environment if present, or create one:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

The app expects environment variables to be loaded from .env via python-dotenv. Do not commit secrets.
```

## Run

Start the agent with:

```bash
python main.py
```

Exit with Ctrl-C or EOF.
