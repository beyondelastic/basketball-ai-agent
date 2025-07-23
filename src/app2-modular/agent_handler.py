from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings


class AgentHandler:
    """Handles Azure AI agent creation and lifecycle management."""
    
    def __init__(self):
        self.ai_agent_settings = AzureAIAgentSettings()
        self.client = None
        self.agents = []
        
    async def __aenter__(self):
        """Async context manager entry."""
        self.credential = DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
        self.client = await AzureAIAgent.create_client(credential=self.credential).__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit with cleanup."""
        # Delete all created agents
        for agent in self.agents:
            await self.client.agents.delete_agent(agent.id)
        
        # Close client and credential
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)
        if hasattr(self.credential, '__aexit__'):
            await self.credential.__aexit__(exc_type, exc_val, exc_tb)
    
    async def create_agent(self, name: str, instructions: str) -> AzureAIAgent:
        """Create an Azure AI agent with the given name and instructions."""
        # Create the agent definition on the Azure AI agent service
        agent_definition = await self.client.agents.create_agent(
            model=self.ai_agent_settings.model_deployment_name,
            name=name,
            instructions=instructions,
        )
        
        # Create a Semantic Kernel agent for the Azure AI agent
        agent = AzureAIAgent(
            client=self.client,
            definition=agent_definition,
        )
        
        # Keep track of created agents for cleanup
        self.agents.append(agent)
        
        return agent
