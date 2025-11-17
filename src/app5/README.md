# Basketball Coaching AI - App5

## Overview

Clean, modular implementation of a multi-agent basketball coaching system using Azure AI Agent Framework with proper resource management.

## Project Structure

```
src/app5/
├── app5.py          # Main application entry point
├── config.py        # Configuration settings and constants
├── agents.py        # Agent definitions and creation functions
├── events.py        # Event handling for workflow callbacks
├── workflow.py      # Workflow orchestration and resource management
└── requirements.txt # Python dependencies
```

## Key Features

- **Clean Architecture**: Modular design with separation of concerns
- **Proper Resource Management**: Uses context managers for automatic cleanup
- **Shared Client Pattern**: Single Azure client instance for all agents and manager
- **Exception Safety**: Robust error handling with guaranteed resource cleanup
- **Simple Usage**: Easy-to-understand code structure

## Usage

### Basic Usage
```bash
python app5.py
```

### Custom Task
```bash
python app5.py "We need help with our defense against pick and roll plays"
```

## Architecture Benefits

### 1. **Context Manager Pattern**
- Automatic resource cleanup (no more "unclosed client session" warnings)
- Exception-safe resource management
- Clear lifecycle management

### 2. **Shared Client Architecture**
- Single `AzureAIAgentClient` instance for all agents and workflow manager
- Reduced resource overhead
- Better connection pooling

### 3. **Modular Design**
- **config.py**: All configuration in one place
- **agents.py**: Agent definitions and creation logic
- **events.py**: Event handling separated from business logic
- **workflow.py**: Complete workflow orchestration with resource management
- **app5.py**: Clean entry point

### 4. **Resource Management**
```python
# Automatic cleanup with context manager
async with BasketballCoachingWorkflow() as workflow:
    result = await workflow.run(task)
# Resources automatically cleaned up here
```

## Technical Improvements

1. **Fixed Resource Leaks**: Context manager ensures proper cleanup
2. **Simplified Client Management**: Single shared client instance
3. **Better Error Handling**: Comprehensive exception management
4. **Cleaner Code**: Separated concerns into logical modules
5. **Type Safety**: Clear function signatures and return types

## Agent Behavior

### Head Coach Agent
- Leads overall strategy decisions
- Handles offensive adjustments independently
- Consults Assistant Coach for defensive matters
- Creates the final game plan
- Responses prefixed with "head_coach > "

### Assistant Coach Agent  
- Provides defensive strategy expertise
- Cannot make offensive recommendations
- Gives clear, concise defensive advice
- Supports Head Coach's final decisions
- Responses prefixed with "assistant_coach > "

## Observability & Tracing

This application includes integrated Azure Application Insights observability for monitoring multi-agent conversations and performance.

### Setup
1. Copy `.env.example` to `.env`
2. Set your Azure AI Foundry project configuration:
   ```
   AZURE_AI_PROJECT_ENDPOINT=https://your-project.eastus2.api.azureml.ms
   AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1
   ```
3. Ensure Application Insights is connected to your Azure AI Foundry project

### Features
- **End-to-End Tracing**: Full workflow visibility from request to completion
- **Agent Performance Monitoring**: Individual agent response times and interactions
- **Custom Spans**: Basketball-specific metrics and attributes
- **Trace Correlation**: Each run includes a Trace ID for easy debugging
- **Application Insights Integration**: Automatic telemetry data collection

### Trace Information
Each workflow run displays a Trace ID that can be used to correlate logs in Application Insights:
```
🔍 Trace ID: 1234567890abcdef1234567890abcdef
```

## Dependencies

- `agent-framework`: Core AI agent functionality
- `azure-identity`: Azure authentication
- `python-dotenv`: Environment variable management
- `azure-ai-projects`: Azure AI Foundry project integration
- `azure-ai-agents`: Azure AI agents client library

## Future Enhancements

- Easy to extend with new agent types
- Simple to add new event handlers
- Configuration can be externalized to files
- Easy to add DevUI integration as separate module