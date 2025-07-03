import asyncio
import os
import euroleague_plugin

from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory

load_dotenv()

# Azure OpenAI config (set your environment variables)
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

async def main():
   # Initialize the kernel
   kernel = Kernel()
   
   # Add Azure OpenAI chat completion
   chat_completion = AzureChatCompletion(
      deployment_name=AZURE_OPENAI_DEPLOYMENT,
      api_key=AZURE_OPENAI_KEY,
      endpoint=AZURE_OPENAI_ENDPOINT,
      api_version=AZURE_OPENAI_API_VERSION,
   )
   kernel.add_service(chat_completion)

   # Add a plugin (the EuroleaguePlugin class is defined above)
   kernel.add_plugin(
      euroleague_plugin.EuroleaguePlugin(),
      plugin_name="Euroleague"
   )
   
   # Enable planning
   execution_settings = AzureChatPromptExecutionSettings()
   execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

   # Create a history of the conversation
   history = ChatHistory()
   history.add_user_message("Please give me the latest Euroleague game results for the 2024 season.")
   
   # Get the response from the AI
   result = await chat_completion.get_chat_message_content(
      chat_history=history,
      settings=execution_settings,
      kernel=kernel,
   ) 
   
   # Print the results
   print("Assistant > " + str(result))

   # Add the message from the agent to the chat history
   history.add_message(result)

if __name__ == "__main__":
    asyncio.run(main())