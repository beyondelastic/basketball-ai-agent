"""
Basketball coaching workflow implementation.
"""
from agent_framework import MagenticBuilder, MagenticCallbackMode
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

from agents import create_head_coach, create_assistant_coach
from events import on_event
from config import WORKFLOW_CONFIG, DEFAULT_TASK


class BasketballCoachingWorkflow:
    """Manages the basketball coaching workflow with proper resource management."""
    
    def __init__(self):
        self.credential = None
        self.shared_client = None
        self.head_coach = None
        self.assistant_coach = None
        self.workflow = None
    
    async def __aenter__(self):
        """Initialize resources using context manager."""
        # Create shared Azure resources
        self.credential = AzureCliCredential()
        self.shared_client = AzureAIAgentClient(async_credential=self.credential)
        
        # Create agents with shared client
        self.head_coach = create_head_coach(self.shared_client)
        self.assistant_coach = create_assistant_coach(self.shared_client)
        
        # Build the workflow
        self.workflow = (
            MagenticBuilder()
            .participants(head_coach=self.head_coach, assistant_coach=self.assistant_coach)
            .on_event(on_event, mode=MagenticCallbackMode.STREAMING)
            .with_standard_manager(
                chat_client=self.shared_client,  # Use shared client for manager too
                **WORKFLOW_CONFIG
            )
            .build()
        )
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources."""
        try:
            if self.shared_client and hasattr(self.shared_client, 'close'):
                await self.shared_client.close()
            if self.credential:
                await self.credential.close()
        except Exception as cleanup_error:
            print(f"Warning: Cleanup error (non-critical): {cleanup_error}")
    
    async def run(self, task: str = None) -> str:
        """Run the basketball coaching workflow with the given task."""
        if not self.workflow:
            raise RuntimeError("Workflow not initialized. Use 'async with' statement.")
        
        task = task or DEFAULT_TASK
        
        print("Starting Basketball Coaching Workflow...")
        print("=" * 50)
        print(f"Task: {task}")
        print("=" * 50)
        
        # Run the workflow
        completion_event = None
        async for event in self.workflow.run_stream(task):
            if hasattr(event, 'type') and 'completed' in str(event.type).lower():
                completion_event = event
        
        # Display final results
        if completion_event is not None:
            data = getattr(completion_event, "data", None)
            preview = getattr(data, "text", None) or (str(data) if data is not None else "")
            print(f"\nWorkflow completed successfully!")
            print(f"Final Result:\n{preview}")
            return preview
        else:
            print("\nWorkflow completed successfully!")
            return "Workflow completed successfully!"


async def run_basketball_coaching_workflow(task: str = None) -> str:
    """Convenience function to run the basketball coaching workflow."""
    async with BasketballCoachingWorkflow() as workflow:
        return await workflow.run(task)