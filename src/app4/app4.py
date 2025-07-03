import os
import time

# Set the environment variable BEFORE importing Azure libraries
os.environ["AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED"] = "true"

from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import BingGroundingTool, ConnectedAgentTool, MessageRole, FilePurpose, FileSearchTool
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

load_dotenv()
PROJECT_ENDPOINT = os.getenv("AZURE_AI_AGENT_ENDPOINT")
MODEL_DEPLOYMENT = os.getenv("AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME")
BING_CONNECTION_NAME = os.getenv("BING_CONNECTION_NAME")

# Create ai project client
project_client = AIProjectClient(
  endpoint=PROJECT_ENDPOINT,
  credential=DefaultAzureCredential()
)
connection_string = project_client.telemetry.get_connection_string()

if not connection_string:
    print("Application Insights is not enabled. Enable by going to Tracing in your Azure AI Foundry project.")
    exit()

# Configure Azure Monitor FIRST
configure_azure_monitor(connection_string=connection_string)

# Get tracer AFTER configuring Azure Monitor
tracer = trace.get_tracer(__name__)

# Now start the main span
with project_client:
    with tracer.start_as_current_span("agent-tracing"):
        # Ensure the BING_CONNECTION_NAME environment variable is set
        conn_id = BING_CONNECTION_NAME  
        print(f"Using Bing connection ID: {conn_id}")  

        # Initialize the Bing Grounding tool
        bing = BingGroundingTool(connection_id=conn_id)

        # Create the web search agent
        websearch_agent = project_client.agents.create_agent(
            model=MODEL_DEPLOYMENT,
            name="websearchagent",
            instructions="You are a web-search agent that can find and provide up-to-date from the internet.",
            tools=bing.definitions,
        )
        
        # Define the path to the file to be uploaded
        file_path = "./data/31-Basketball-Drills-and-Games-for-Kids.pdf"  # Adjust the path as needed

        # Upload the file
        file = project_client.agents.files.upload_and_poll(file_path=file_path, purpose=FilePurpose.AGENTS)
        print(f"Uploaded file, file ID: {file.id}")

        # Create a vector store with the uploaded file
        vector_store = project_client.agents.vector_stores.create_and_poll(file_ids=[file.id], name="my_vectorstore")
        print(f"Created vector store, vector store ID: {vector_store.id}")
        
        # Create a file search tool
        file_search = FileSearchTool(vector_store_ids=[vector_store.id])
        
        # Create a mini basketball assistant agent that uses file search
        mini_basketball_agent = project_client.agents.create_agent(
        model=MODEL_DEPLOYMENT,
        name="minibasketballagent",
        instructions="You are a basketball assistant coach who creates trainings plans for children basketball (aka minibasketball). The training plans should include between 3-4 exercises with a short description, the equipment that is required, how long the exercise should last and what skill it is targeting. The plan should not be longer than a DIN A4 page. Solely use exercises from the document you have access to.",
        tools=file_search.definitions,  # Tools available to the agent
        tool_resources=file_search.resources,  # Resources for the tools
        )
        
            
        connected_websearch_agent = ConnectedAgentTool(
            id=websearch_agent.id, name="websearchagent", description="Every time the request demands up-to-date or recent data from the internet, use this agent to search the web."
        )
        connected_minibasketball_agent = ConnectedAgentTool(
            id=mini_basketball_agent.id, name="minibasketballagent", description="For creating training plans for children basketball aka minibasketball."
        )

        agent = project_client.agents.create_agent(
            model=MODEL_DEPLOYMENT,
            name="my-basketball-agent",
            instructions="You are a basketball assistant that can answer all sorts of basketball related questions.",
            tools=connected_websearch_agent.definitions + connected_minibasketball_agent.definitions,
        )

        print(f"Created agent, ID: {agent.id}")

        # Create a thread using the correct method
        thread = project_client.agents.threads.create()
        print(f"Created thread, ID: {thread.id}")

        print("\n🏀 Basketball Assistant Chat - Type 'quit', 'exit', or 'bye' to end the conversation\n")
        
        # Conversation loop
        while True:
            # Get user input for the message content
            user_message = input("\nYou: ").strip()
            
            # Check if user wants to quit
            if user_message.lower() in ['quit', 'exit', 'bye', 'q']:
                print("Thanks for chatting! Goodbye! 🏀")
                break
                
            if not user_message:
                print("Please enter a message or 'quit' to exit.")
                continue

            # Create message to thread using the correct method
            message = project_client.agents.messages.create(
                thread_id=thread.id,
                role=MessageRole.USER,
                content=user_message,
            )
            print(f"Created message, ID: {message.id}")

            # Create and process Agent run in thread with tools
            run = project_client.agents.runs.create(thread_id=thread.id, agent_id=agent.id)
                
            # Wait for the run to complete and fetch the agent's response
            max_wait = 60  # seconds - increased for more complex queries
            poll_interval = 2  # seconds
            waited = 0
            print("🤔 Agent is thinking...")
            
            while run.status not in ("completed", "failed") and waited < max_wait:
                time.sleep(poll_interval)
                waited += poll_interval
                run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)

            if run.status == "failed":
                print(f"❌ Run failed: {run.last_error}")
            else:
                # Print the Agent's response message with optional citation
                messages = project_client.agents.messages.list(thread_id=thread.id)
                
                # Convert to list and sort by created_at to get chronological order
                message_list = list(messages)
                message_list.sort(key=lambda x: x.created_at, reverse=True)  # Newest first
                
                # Find the most recent agent message
                latest_agent_message = None
                for msg in message_list:
                    if msg.role == MessageRole.AGENT:
                        latest_agent_message = msg
                        break
                
                if latest_agent_message:
                    print("\n🤖 Assistant:")
                    for text_message in latest_agent_message.text_messages:
                        print(f"{text_message.text.value}")
                    
                    # Print citations if any
                    citations = getattr(latest_agent_message, 'url_citation_annotations', [])
                    if citations:
                        print("\n📚 Sources:")
                        for annotation in citations:
                            print(f"• {annotation.url_citation.title}: {annotation.url_citation.url}")
                else:
                    print("❌ No agent response message found.")

            print(f"\n✅ Run finished with status: {run.status}")

        print("\n🧹 Cleaning up resources...")

        # Delete the Agent when done
        project_client.agents.delete_agent(agent.id)
        print("Deleted agent")

        # Delete the connected Agent when done
        project_client.agents.delete_agent(websearch_agent.id)
        project_client.agents.delete_agent(mini_basketball_agent.id)
        print("Deleted connected agent")

        # Delete the thread when done
        project_client.agents.threads.delete(thread.id)
        print("Deleted thread")