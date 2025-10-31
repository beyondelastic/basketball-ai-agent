"""
Configuration settings for the basketball coaching application.
"""
import os
from dotenv import load_dotenv

# Load environment configuration
load_dotenv()

# Agent role names (constants)
HEAD_COACH_NAME = "HeadCoach"
ASSISTANT_COACH_NAME = "AssistantCoach"

# Workflow configuration
WORKFLOW_CONFIG = {
    "max_round_count": 10,  # Maximum collaboration rounds
    "max_stall_count": 3,   # Maximum rounds without progress
    "max_reset_count": 2,   # Maximum plan resets allowed
}

# Default task for testing
DEFAULT_TASK = """Could you please give me advice on how to change the game strategy for the next quarter? 
We are playing zone defense and the other team just scored 10 points in a row. 
We need to change our strategy to stop them. What should we do?"""

# Azure configuration (if needed for custom endpoints)
AZURE_CONFIG = {
    # Add any specific Azure configuration here if needed
    # "endpoint": os.getenv("AZURE_AI_ENDPOINT"),
    # "api_version": os.getenv("AZURE_API_VERSION", "2024-02-15-preview"),
}