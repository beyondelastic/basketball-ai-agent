"""
Basketball coaching workflow implementation.
"""
from agent_framework import MagenticBuilder, MagenticCallbackMode
from agent_framework.azure import AzureAIAgentClient
from agent_framework.observability import get_tracer
from azure.identity.aio import AzureCliCredential
from azure.ai.projects.aio import AIProjectClient
from azure.core.exceptions import ResourceNotFoundError
from opentelemetry.trace import SpanKind
from opentelemetry.trace.span import format_trace_id

from agents import create_head_coach, create_assistant_coach
from events import on_event
from config import WORKFLOW_CONFIG, DEFAULT_TASK, AZURE_AI_PROJECT_ENDPOINT, AZURE_AI_MODEL_DEPLOYMENT_NAME


async def setup_azure_ai_observability(
    project_client: AIProjectClient, enable_sensitive_data: bool = True
) -> None:
    """Setup tracing in your Azure AI Project using Application Insights."""
    
    # Suppress Azure Monitor configuration warnings
    import logging
    logging.getLogger("azure.monitor.opentelemetry.exporter._configuration").setLevel(logging.ERROR)
    
    try:
        conn_string = await project_client.telemetry.get_application_insights_connection_string()
        print(f"✓ Connected to Application Insights for observability")
    except ResourceNotFoundError:
        print("⚠️  No Application Insights connection string found for the Azure AI Project.")
        return
    
    from agent_framework.observability import setup_observability
    setup_observability(
        applicationinsights_connection_string=conn_string,
        enable_sensitive_data=enable_sensitive_data
    )


class BasketballCoachingWorkflow:
    """Manages the basketball coaching workflow with proper resource management."""
    
    def __init__(self):
        self.credential = None
        self.project_client = None
        self.manager_client = None
        self.head_coach = None
        self.assistant_coach = None
        self.workflow = None
        self.shared_thread = None  # Shared thread for conversation continuity
    
    async def __aenter__(self):
        """Initialize resources using context manager."""
        # Validate required configuration
        if not AZURE_AI_MODEL_DEPLOYMENT_NAME:
            raise ValueError("AZURE_AI_MODEL_DEPLOYMENT_NAME environment variable is required")
        
        print(f"🤖 Using model deployment: {AZURE_AI_MODEL_DEPLOYMENT_NAME}")
        
        # Create shared Azure credential
        self.credential = AzureCliCredential()
        
        # Setup observability if Azure AI Project endpoint is available
        if AZURE_AI_PROJECT_ENDPOINT:
            self.project_client = AIProjectClient(
                endpoint=AZURE_AI_PROJECT_ENDPOINT,
                credential=self.credential
            )
            await setup_azure_ai_observability(self.project_client)
        else:
            print("⚠️  AZURE_AI_PROJECT_ENDPOINT not set. Observability disabled.")
        
        # Create separate client for the workflow manager
        self.manager_client = AzureAIAgentClient(
            async_credential=self.credential,
            agent_name="WorkflowManager",
            model_deployment_name=AZURE_AI_MODEL_DEPLOYMENT_NAME,
            should_cleanup_agent=False
        )
        
        # Create agents with individual clients for proper registration
        self.head_coach = await create_head_coach(self.credential)
        self.assistant_coach = await create_assistant_coach(self.credential)
        
        # Create a shared thread for conversation continuity
        # Use the head coach's client to create the initial thread
        self.shared_thread = self.head_coach.get_new_thread()
        
        # Build the workflow
        self.workflow = (
            MagenticBuilder()
            .participants(head_coach=self.head_coach, assistant_coach=self.assistant_coach)
            .on_event(on_event, mode=MagenticCallbackMode.STREAMING)
            .with_standard_manager(
                chat_client=self.manager_client,
                **WORKFLOW_CONFIG
            )
            .build()
        )
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources."""
        cleanup_errors = []
        
        # Clean up agent clients
        try:
            if self.head_coach and hasattr(self.head_coach, 'chat_client') and hasattr(self.head_coach.chat_client, 'close'):
                await self.head_coach.chat_client.close()
        except Exception as cleanup_error:
            cleanup_errors.append(f"HeadCoach client cleanup: {cleanup_error}")
        
        try:
            if self.assistant_coach and hasattr(self.assistant_coach, 'chat_client') and hasattr(self.assistant_coach.chat_client, 'close'):
                await self.assistant_coach.chat_client.close()
        except Exception as cleanup_error:
            cleanup_errors.append(f"AssistantCoach client cleanup: {cleanup_error}")
        
        # Clean up manager client
        try:
            if self.manager_client and hasattr(self.manager_client, 'close'):
                await self.manager_client.close()
        except Exception as cleanup_error:
            cleanup_errors.append(f"Manager client cleanup: {cleanup_error}")
        
        # Clean up project client
        try:
            if self.project_client and hasattr(self.project_client, 'close'):
                await self.project_client.close()
        except Exception as cleanup_error:
            cleanup_errors.append(f"Project client cleanup: {cleanup_error}")
        
        # Clean up credential
        try:
            if self.credential and hasattr(self.credential, 'close'):
                await self.credential.close()
        except Exception as cleanup_error:
            cleanup_errors.append(f"Credential cleanup: {cleanup_error}")
        
        if cleanup_errors:
            print(f"Warning: Cleanup errors (non-critical): {'; '.join(cleanup_errors)}")
    
    async def run(self, task: str = None) -> str:
        """Run the basketball coaching workflow with the given task."""
        if not self.workflow:
            raise RuntimeError("Workflow not initialized. Use 'async with' statement.")
        
        task = task or DEFAULT_TASK
        
        # Create a top-level span for the entire basketball coaching workflow
        with get_tracer().start_as_current_span(
            "Basketball Coaching Workflow", 
            kind=SpanKind.CLIENT
        ) as current_span:
            
            # Add trace ID to output for correlation
            trace_id = format_trace_id(current_span.get_span_context().trace_id)
            print(f"🔍 Trace ID: {trace_id}")
            
            print("Starting Basketball Coaching Workflow...")
            print("=" * 50)
            print(f"Task: {task}")
            print("=" * 50)
            
            # Get thread ID for tracking conversation continuity
            thread_id = getattr(self.shared_thread, 'service_thread_id', None)
            thread_id_display = thread_id or 'local-thread'
            print(f"Using conversation thread: {thread_id_display}")
            print("=" * 50)
            
            # Add span attributes for better filtering and analysis
            current_span.set_attribute("basketball.task_length", len(task))
            current_span.set_attribute("basketball.thread_id", thread_id_display)
            
            # Run the workflow with shared thread context
            completion_event = None
            async for event in self.workflow.run_stream(task):
                if hasattr(event, 'type') and 'completed' in str(event.type).lower():
                    completion_event = event
            
            # Display final results
            if completion_event is not None:
                data = getattr(completion_event, "data", None)
                preview = getattr(data, "text", None) or (str(data) if data is not None else "")
                
                # Add result metrics to span
                current_span.set_attribute("basketball.result_length", len(preview))
                current_span.set_attribute("basketball.status", "completed_with_result")
                
                print(f"\nWorkflow completed successfully!")
                print(f"Final Result:\n{preview}")
                print(f"Conversation thread: {thread_id_display}")
                print(f"🔍 Trace ID: {trace_id}")
                return preview
            else:
                current_span.set_attribute("basketball.status", "completed_no_result")
                print("\nWorkflow completed successfully!")
                print(f"Conversation thread: {thread_id_display}")
                print(f"🔍 Trace ID: {trace_id}")
                return "Workflow completed successfully!"


async def run_basketball_coaching_workflow(task: str = None) -> str:
    """Convenience function to run the basketball coaching workflow."""
    async with BasketballCoachingWorkflow() as workflow:
        return await workflow.run(task)