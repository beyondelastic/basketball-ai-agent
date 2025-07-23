# Basketball AI Agent - Modular Version

This is a modular version of the basketball coaching AI agent application.

## Structure

- **agent_handler.py**: Contains the `AgentHandler` class that manages Azure AI agent creation and lifecycle
- **orchestrator.py**: Contains the chat orchestration logic with custom termination and selection strategies
- **main.py**: The main runner that coordinates everything and serves as the entry point

## Usage

```bash
cd src/app2-modular
pip install -r requirements.txt
python main.py
```

## Components

### AgentHandler
- Manages Azure AI agent creation and cleanup
- Implements async context manager for proper resource management
- Handles credential management

### ChatOrchestrator
- Manages the group chat between agents
- Implements custom termination and selection strategies
- Handles chat flow and output

### Main Runner
- Coordinates the entire application
- Sets up agent configurations and instructions
- Runs the main chat workflow
