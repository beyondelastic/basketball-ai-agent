# Basketball Coaching AI - App5

## Overview

App5 demonstrates a multi-agent basketball coaching system using the Azure AI Agent Framework with Magnetics orchestration. The system features two specialized AI agents that collaborate to provide comprehensive basketball strategy advice:

- **Head Coach Agent**: Specializes in offensive strategies and overall game planning
- **Assistant Coach Agent**: Focuses on defensive strategies and adjustments

## Architecture

### Agent Collaboration Model
The agents use a workflow-based collaboration where:
1. Both agents receive the same task/situation
2. They collaborate through the Magnetics orchestrator
3. The Head Coach leads the decision-making but consults the Assistant Coach for defensive matters
4. The system produces a coordinated final game plan

### Key Features
- **Streaming responses**: Real-time feedback as agents think and collaborate
- **Event-driven architecture**: Comprehensive event handling for orchestration, agent messages, and final results
- **Role-based specialization**: Clear separation of responsibilities between coaches
- **Error handling**: Robust error management for production use

## Code Structure

### Main Components

1. **Agent Definitions**
   - `HEAD_COACH_NAME` & `ASSISTANT_COACH_NAME`: Agent identifiers
   - `HEAD_COACH_INSTRUCTIONS` & `ASSISTANT_COACH_INSTRUCTIONS`: Detailed role specifications

2. **Agent Factory**
   - `create_agents()`: Creates and configures the coaching agents

3. **Event Handling**
   - `on_event()`: Processes different types of workflow events
   - Handles orchestrator messages, agent responses, and final results

4. **Workflow Management**
   - `run_basketball_coaching_workflow()`: Main orchestration function
   - `MagenticBuilder`: Configures the multi-agent workflow
   - `workflow.run_stream()`: Executes the collaborative process

### Configuration Options
- `max_round_count=10`: Maximum collaboration rounds
- `max_stall_count=3`: Maximum rounds without progress before intervention
- `max_reset_count=2`: Maximum plan resets allowed

## Usage

### Prerequisites
1. Install dependencies: `pip install -r requirements.txt`
2. Configure Azure credentials (ensure `az login` is completed)
3. Set up environment variables in `.env` file if needed

### Running the Application
```bash
cd src/app5
python3 app5.py
```

### Expected Flow
1. System initializes both coaching agents
2. The task is presented to the workflow
3. Agents collaborate in real-time with streaming output:
   - Orchestrator messages show planning
   - Agent messages show individual responses
   - Delta events show streaming text
4. Final coordinated strategy is presented

## Sample Task
The default task simulates a common basketball scenario:
> "We are playing zone defense and the other team just scored 10 points in a row. We need to change our strategy to stop them. What should we do?"

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

## Error Handling
- Import fallbacks for optional framework components
- Comprehensive exception handling in main workflow
- Graceful degradation if certain events aren't available

## Testing
Run the structure test to validate the code organization:
```bash
python3 test_structure.py
```

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure `agent-framework` is properly installed
2. **Authentication**: Verify Azure CLI login status
3. **Event Handling**: Some events might not be available in all framework versions

### Dependencies
- `python-dotenv`: Environment variable management
- `azure-identity`: Azure authentication
- `agent-framework`: Core AI agent functionality

## Future Enhancements
- Add more specialized coaching roles (e.g., Analytics Coach)
- Implement game situation templates
- Add persistent conversation history
- Integrate with real basketball data sources