import asyncio
from dotenv import load_dotenv
from agent_framework import (
    ChatAgent, 
    MagenticBuilder, 
    MagenticCallbackMode,
    MagenticAgentDeltaEvent,
    MagenticAgentMessageEvent,
    MagenticCallbackEvent,
    MagenticFinalResultEvent,
    MagenticOrchestratorMessageEvent
)

# Import WorkflowCompletedEvent separately as it might be in a different module
try:
    from agent_framework import WorkflowCompletedEvent
except ImportError:
    # Fallback if WorkflowCompletedEvent is not available
    WorkflowCompletedEvent = None
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

# Load environment configuration
load_dotenv()

# Agent role names (constants)
HEAD_COACH_NAME = "HeadCoach"
ASSISTANT_COACH_NAME = "AssistantCoach"

# Agent instructions
HEAD_COACH_INSTRUCTIONS = """
You are a Basketball Head Coach that knows everything about offensive plays and strategies. 
You respond to specific game situations with advice on how to change the game plan. You can ask for more information about the game situation if needed. 
For offensive plays and strategies, you will decide on the strategy yourself. If the game situation demands a change for defensive plays and strategies, you will ask your Assistant Coach for advice.
You will use the advice given by the Assistant Coach in regards to defensive adjustments and your own decision for offensive adjustments to create the final game plan.

RULES:
- Use the instructions provided.
- Prepend your response with this text: "head_coach > "
- Do not directly answer the question if it is related to defensive strategies. Instead, ask your Assistant Coach for advice.
- Do not use the words "final game plan" unless you have created a final game plan according to the instructions.
- Add "final game plan" to the end of your response if you have created a final game plan according to the instructions.
"""

ASSISTANT_COACH_INSTRUCTIONS = """
You are a Basketball Assistant Coach that knows defensive plays and strategies.
You give advice to your Head Coach for specific in game situations that require defensive adjustment.

RULES:
- Use the instructions provided.
- Prepend your response with this text: "assistant_coach > "
- You are not allowed to give advice on offensive plays and strategies.
- You don't decide the final game strategy and plan you only give advice to the Head Coach.
- Your advice should be clear and concise and should not include any unnecessary information.
"""

# Task definition
TASK = "Could you please give me advice on how to change the game strategy for the next quarter? We are playing zone defense and the other team just scored 10 points in a row. We need to change our strategy to stop them. What should we do?"

# Create agent instances  
async def create_agents():
    """Create and return the agent instances with proper Azure client setup."""
    # Create shared credential for efficiency
    credential = AzureCliCredential()
    
    # Create client instances for each agent
    head_coach_client = AzureAIAgentClient(async_credential=credential)
    assistant_coach_client = AzureAIAgentClient(async_credential=credential)
    
    head_coach = ChatAgent(
        name=HEAD_COACH_NAME,
        description="Basketball Head Coach specializing in offensive strategies",
        instructions=HEAD_COACH_INSTRUCTIONS,
        chat_client=head_coach_client
    )
    
    assistant_coach = ChatAgent(
        name=ASSISTANT_COACH_NAME,
        description="Basketball Assistant Coach specializing in defensive strategies",
        instructions=ASSISTANT_COACH_INSTRUCTIONS,
        chat_client=assistant_coach_client
    )
    
    return head_coach, assistant_coach


# Unified callback for all events
async def on_event(event: MagenticCallbackEvent) -> None:
    """Handle different types of events from the workflow."""
    if isinstance(event, MagenticOrchestratorMessageEvent):
        # Manager's planning and coordination messages
        print(f"\n[ORCHESTRATOR:{event.kind}]\n\n{getattr(event.message, 'text', '')}\n{'-' * 50}")

    elif isinstance(event, MagenticAgentDeltaEvent):
        # Streaming tokens from agents
        print(event.text, end="", flush=True)

    elif isinstance(event, MagenticAgentMessageEvent):
        # Complete agent responses
        msg = event.message
        if msg is not None:
            response_text = (msg.text or "").replace("\n", " ")
            print(f"\n[AGENT:{event.agent_id}] {msg.role.value}\n\n{response_text}\n{'-' * 50}")

    elif isinstance(event, MagenticFinalResultEvent):
        # Final synthesized result
        print("\n" + "=" * 50)
        print("FINAL RESULT:")
        print("=" * 50)
        if event.message is not None:
            print(event.message.text)
        print("=" * 50)


async def run_basketball_coaching_workflow():
    """Main function to run the basketball coaching workflow."""
    # Initialize credentials and clients
    credential = AzureCliCredential()
    manager_client = AzureAIAgentClient(async_credential=credential)
    
    try:
        # Create agent instances
        head_coach, assistant_coach = await create_agents()
        
        # Build the workflow
        workflow = (
            MagenticBuilder()
            .participants(head_coach=head_coach, assistant_coach=assistant_coach)
            .on_event(on_event, mode=MagenticCallbackMode.STREAMING)
            .with_standard_manager(
                chat_client=manager_client,
                max_round_count=10,  # Maximum collaboration rounds
                max_stall_count=3,   # Maximum rounds without progress
                max_reset_count=2,   # Maximum plan resets allowed
            )
            .build()
        )

        print("Starting Basketball Coaching Workflow...")
        print("=" * 50)
        print(f"Task: {TASK}")
        print("=" * 50)

        # Run the workflow
        completion_event = None
        async for event in workflow.run_stream(TASK):
            if WorkflowCompletedEvent and isinstance(event, WorkflowCompletedEvent):
                completion_event = event
            # Handle the case where we don't have WorkflowCompletedEvent
            elif hasattr(event, 'type') and 'completed' in str(event.type).lower():
                completion_event = event

        # Display final results
        if completion_event is not None:
            data = getattr(completion_event, "data", None)
            preview = getattr(data, "text", None) or (str(data) if data is not None else "")
            print(f"\nWorkflow completed successfully!")
            print(f"Final Result:\n{preview}")
        else:
            print("\nWorkflow completed successfully!")

    except Exception as e:
        print(f"Error running workflow: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Proper cleanup
        try:
            await credential.close()
            if hasattr(manager_client, 'close'):
                await manager_client.close()
        except Exception as cleanup_error:
            print(f"Warning: Cleanup error (non-critical): {cleanup_error}")


async def main():
    """Main entry point."""
    await run_basketball_coaching_workflow()


if __name__ == "__main__":
    asyncio.run(main())