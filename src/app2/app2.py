# add references
import asyncio
from dotenv import load_dotenv
from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AgentGroupChat
from semantic_kernel.agents.strategies import TerminationStrategy, SequentialSelectionStrategy
from semantic_kernel.contents.utils.author_role import AuthorRole

# get configuration settings
load_dotenv()

# agent instructions
HEAD_COACH = "HeadCoach"
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

ASSISTANT_COACH = "AssistantCoach"
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

# agent task
TASK = "Could you please give me advice on how to change the game strategy for the next quarter? We are playing zone defense and the other team just scored 10 points in a row. We need to change our strategy to stop them. What should we do?"

# this function creates Azure AI agents and adds them to a group chat with a custom termination and selection strategy.
async def main():

    ai_agent_settings = AzureAIAgentSettings.create()

    async with (
        DefaultAzureCredential(exclude_environment_credential=True, 
            exclude_managed_identity_credential=True) as creds,
        AzureAIAgent.create_client(credential=creds) as client,
    ):
        
        # create the head-coach agent on the Azure AI agent service
        headcoach_agent_definition = await client.agents.create_agent(
            model=ai_agent_settings.model_deployment_name,
            name=HEAD_COACH,
            instructions=HEAD_COACH_INSTRUCTIONS,
        )
        
        # create a Semantic Kernel agent for the Azure AI head-coach agent
        agent_headcoach = AzureAIAgent(
            client=client,
            definition=headcoach_agent_definition,
        )
        
        # create the assistant coach agent on the Azure AI agent service
        assistantcoach_agent_definition = await client.agents.create_agent(
            model=ai_agent_settings.model_deployment_name,
            name=ASSISTANT_COACH,
            instructions=ASSISTANT_COACH_INSTRUCTIONS,
        )

        # create a Semantic Kernel agent for the assistant coach Azure AI agent
        agent_assistantcoach = AzureAIAgent(
            client=client,
            definition=assistantcoach_agent_definition,
        )

        # add the agents to a group chat with a custom termination and selection strategy
        chat = AgentGroupChat(
            agents=[agent_headcoach, agent_assistantcoach],
            termination_strategy=ApprovalTerminationStrategy(
                agents=[agent_headcoach], 
                maximum_iterations=4, 
                automatic_reset=True
            ),
            selection_strategy=SelectionStrategy(agents=[agent_headcoach,agent_assistantcoach]),      
        )
        
        try:
            # add the task as a message to the group chat
            await chat.add_chat_message(message=TASK)
            print(f"# {AuthorRole.USER}: '{TASK}'")
            # invoke the chat
            async for content in chat.invoke():
                print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
        finally:
            # cleanup and delete the agents
            print("--chat ended--")
            await chat.reset()
            await client.agents.delete_agent(agent_headcoach.id)
            await client.agents.delete_agent(agent_assistantcoach.id)

# class of termination strategy
class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""

    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        return "final game plan" in history[-1].content.lower()
    
# class for selection strategy
class SelectionStrategy(SequentialSelectionStrategy):
    """A strategy for determining which agent should take the next turn in the chat."""
    
    # select the next agent that should take the next turn in the chat
    async def select_agent(self, agents, history):
        """"Check which agent should take the next turn in the chat."""

        # the Head Coach should go after the User or the Assistant Coach
        if (history[-1].name == ASSISTANT_COACH or history[-1].role == AuthorRole.USER):
            agent_name = HEAD_COACH
            return next((agent for agent in agents if agent.name == agent_name), None)
        
        # otherwise it is the Assistant Coach's turn
        return next((agent for agent in agents if agent.name == ASSISTANT_COACH), None)

if __name__ == "__main__":
    asyncio.run(main())