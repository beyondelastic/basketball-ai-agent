import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import CodeInterpreterTool, FilePurpose
from pathlib import Path

# load environment variables from local .env file
load_dotenv()
MODEL_DEPLOYMENT = os.getenv("AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME")
PROJECT_ENDPOINT = os.getenv("AZURE_AI_AGENT_ENDPOINT")
FILE_PATH = Path(__file__).parent.parent / os.getenv("NBA_CSV_FILE_PATH")  # Adjusted to resolve relative path

# create ai project client
project_client = AIProjectClient(
  endpoint=PROJECT_ENDPOINT,
  credential=DefaultAzureCredential()
)
with project_client:

    # upload a file and add it to the client 
    file = project_client.agents.files.upload_and_poll(
        file_path=FILE_PATH, purpose=FilePurpose.AGENTS
    )
    print(f"Uploaded file, file ID: {file.id}")

    # create a code interpreter tool instance referencing the uploaded file
    code_interpreter = CodeInterpreterTool(file_ids=[file.id])

    # create an agent
    agent = project_client.agents.create_agent(
        model=MODEL_DEPLOYMENT,
        name="assistant-coach-agent",
        instructions="You are a Basketball assistant coach that knows everything about the game of Basketball. You give advice about Basketball rules, training, statistics and strategies.",
        tools=code_interpreter.definitions,
        tool_resources=code_interpreter.resources,
    )
    print(f"Using agent: {agent.name}")

    # create a thread with message
    thread = project_client.agents.threads.create()
    print(f"Thread created: {thread.id}")

    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content="Could you please create a bar chart for 3Pointers made vs attempts during the NBA seasons 1996 until 2020 and save it as a .png file?",
    )

    # ask the agent to perform work on the thread
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

    # fetch and print the conversation history including the last message
    print("\nConversation Log:\n")
    messages = project_client.agents.messages.list(thread_id=thread.id)
    message_list = list(messages)
    for message_data in reversed(message_list):
        last_message_content = message_data.content[-1]
        print(f"{message_data.role}: {last_message_content.text.value}\n")

    # fetch any generated files
    for message_data in message_list:
        if hasattr(message_data, 'file_path_annotations') and message_data.file_path_annotations:
            for file_path_annotation in message_data.file_path_annotations:
                file_id = file_path_annotation.file_path.file_id
                file_name = Path(file_path_annotation.text).name
                
                # Download the file content
                file_content_generator = project_client.agents.files.get_content(file_id=file_id)
                
                # Save the file locally
                with open(file_name, 'wb') as f:
                    for chunk in file_content_generator:
                        f.write(chunk)
                print(f"File saved as {file_name}")
        
    # clean up
    project_client.agents.delete_agent(agent.id)
    project_client.agents.threads.delete(thread.id)