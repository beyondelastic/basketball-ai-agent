"""
Configuration settings for the basketball coaching application.
"""
import os
from dotenv import load_dotenv

# Load environment configuration
load_dotenv()

# Agent role names (constants) - These will be registered in Azure AI Foundry
HEAD_COACH_NAME = "BasketballHeadCoach"
ASSISTANT_COACH_NAME = "BasketballAssistantCoach"

# Workflow configuration
WORKFLOW_CONFIG = {
    "max_round_count": 10,  # Maximum collaboration rounds
    "max_stall_count": 3,   # Maximum rounds without progress
    "max_reset_count": 2,   # Maximum plan resets allowed
}

# Default task for testing
DEFAULT_TASK = """We're in the 4th quarter and trailing by 8 points. The opposing team just went on a 12-0 run with zone defense. 
I need you to check our current roster status and make strategic recommendations including:
1. Any necessary substitutions based on player fatigue, foul trouble, or performance
2. Offensive adjustments to break their zone defense
3. Defensive changes to stop their momentum

Head coach, please review our roster and suggest the best lineup and strategy for a comeback."""

# Azure configuration (if needed for custom endpoints)
AZURE_CONFIG = {
    # Add any specific Azure configuration here if needed
    # "endpoint": os.getenv("AZURE_AI_ENDPOINT"),
    # "api_version": os.getenv("AZURE_API_VERSION", "2024-02-15-preview"),
}

# Azure AI Project configuration for observability
AZURE_AI_PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")

# Model deployment configuration
AZURE_AI_MODEL_DEPLOYMENT_NAME = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")