#!/usr/bin/env python3
"""
Basketball Coaching AI - Clean and Modular Implementation

This application demonstrates multi-agent collaboration using Azure AI Agent Framework.
Two specialized AI coaches (Head Coach and Assistant Coach) work together to provide
comprehensive basketball strategy advice.
"""
import asyncio
import sys

from workflow import run_basketball_coaching_workflow
from config import DEFAULT_TASK


async def main():
    """Main entry point for the basketball coaching application."""
    try:
        # Check for custom task from command line
        task = None
        if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
            task = ' '.join(sys.argv[1:])
        
        # Run the workflow with clean resource management
        result = await run_basketball_coaching_workflow(task)
        
    except KeyboardInterrupt:
        print("\n\nWorkflow interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())