from semantic_kernel.agents import AgentGroupChat
from semantic_kernel.agents.strategies import TerminationStrategy, SequentialSelectionStrategy
from semantic_kernel.contents.utils.author_role import AuthorRole


class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""

    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        return "final game plan" in history[-1].content.lower()


def create_selection_strategy(head_coach_name: str, assistant_coach_name: str):
    """Factory function to create a selection strategy with the given agent names."""
    
    class SelectionStrategy(SequentialSelectionStrategy):
        """A strategy for determining which agent should take the next turn in the chat."""
        
        async def select_agent(self, agents, history):
            """Check which agent should take the next turn in the chat."""
            # The Head Coach should go after the User or the Assistant Coach
            if (history[-1].name == assistant_coach_name or history[-1].role == AuthorRole.USER):
                return next((agent for agent in agents if agent.name == head_coach_name), None)
            
            # Otherwise it is the Assistant Coach's turn
            return next((agent for agent in agents if agent.name == assistant_coach_name), None)
    
    return SelectionStrategy()


class ChatOrchestrator:
    """Orchestrates the agent group chat with custom strategies."""
    
    def __init__(self, head_coach_agent, assistant_coach_agent, head_coach_name: str, assistant_coach_name: str):
        self.head_coach_agent = head_coach_agent
        self.assistant_coach_agent = assistant_coach_agent
        self.head_coach_name = head_coach_name
        self.assistant_coach_name = assistant_coach_name
        
        # Create the group chat with custom strategies
        self.chat = AgentGroupChat(
            agents=[head_coach_agent, assistant_coach_agent],
            termination_strategy=ApprovalTerminationStrategy(
                agents=[head_coach_agent], 
                maximum_iterations=4, 
                automatic_reset=True
            ),
            selection_strategy=create_selection_strategy(
                head_coach_name=head_coach_name,
                assistant_coach_name=assistant_coach_name
            ),      
        )
    
    async def run_chat(self, task: str):
        """Run the chat with the given task."""
        try:
            # Add the task as a message to the group chat
            await self.chat.add_chat_message(message=task)
            print(f"# {AuthorRole.USER}: '{task}'")
            
            # Invoke the chat
            async for content in self.chat.invoke():
                print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
        finally:
            # Reset the chat
            print("--chat ended--")
            await self.chat.reset()
