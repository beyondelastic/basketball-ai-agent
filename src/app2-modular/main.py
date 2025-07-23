import asyncio
from dotenv import load_dotenv
from agent_handler import AgentHandler
from orchestrator import ChatOrchestrator

# Get configuration settings
load_dotenv()

# Agent names and instructions
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

# Agent task
TASK = "Could you please give me advice on how to change the game strategy for the next quarter? We are playing zone defense and the other team just scored 10 points in a row. We need to change our strategy to stop them. What should we do?"


async def main():
    """Main function that coordinates the agent creation and chat orchestration."""
    async with AgentHandler() as agent_handler:
        # Create the head coach agent
        head_coach_agent = await agent_handler.create_agent(
            name=HEAD_COACH,
            instructions=HEAD_COACH_INSTRUCTIONS
        )
        
        # Create the assistant coach agent
        assistant_coach_agent = await agent_handler.create_agent(
            name=ASSISTANT_COACH,
            instructions=ASSISTANT_COACH_INSTRUCTIONS
        )
        
        # Create the chat orchestrator and run the chat
        orchestrator = ChatOrchestrator(
            head_coach_agent=head_coach_agent,
            assistant_coach_agent=assistant_coach_agent,
            head_coach_name=HEAD_COACH,
            assistant_coach_name=ASSISTANT_COACH
        )
        
        await orchestrator.run_chat(TASK)


if __name__ == "__main__":
    asyncio.run(main())
