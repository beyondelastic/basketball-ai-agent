"""
Event handling for the basketball coaching workflow.
"""
from agent_framework import (
    MagenticCallbackEvent,
    MagenticOrchestratorMessageEvent,
    MagenticAgentDeltaEvent,
    MagenticAgentMessageEvent,
    MagenticFinalResultEvent,
)


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