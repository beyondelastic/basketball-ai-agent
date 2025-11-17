# Basketball Coach AI Agent Demo Repository

This repository contains multiple basketball coaching AI agent implementations demonstrating different Azure AI technologies and frameworks.

## Applications Overview

### App1 - Azure AI Foundry Agent Service
**Technology**: Azure AI Foundry  
**Framework**: Azure AI Agent Service  
**Description**: Demo code for Azure AI Agent Service intro post. Basic agent implementation using Azure AI Foundry's native agent capabilities.  
**Blog Post**: https://beyondelastic.github.io/posts/agent/

### App2 - Semantic Kernel Multi-Agent System
**Technology**: Azure AI Foundry  
**Framework**: Semantic Kernel  
**Description**: Multi-agent basketball coaching system using Semantic Kernel's agent orchestration capabilities.  
**Blog Post**: https://beyondelastic.github.io/posts/multi-agent/

### App2-Modular - Modular Semantic Kernel Implementation
**Technology**: Azure AI Foundry  
**Framework**: Semantic Kernel  
**Description**: Refactored version of App2 with improved modularity and separation of concerns using Semantic Kernel agents.

### App3 - Semantic Kernel Function Calling
**Technology**: Azure OpenAI  
**Framework**: Semantic Kernel  
**Description**: Demonstrates Semantic Kernel function calling and plugins for basketball coaching scenarios.  
**Blog Post**: https://beyondelastic.github.io/posts/skfc/

### App4 - Advanced Azure AI Foundry Features
**Technology**: Azure AI Foundry  
**Framework**: Azure AI Agent Service  
**Description**: Advanced implementation showcasing Azure AI Foundry features like Bing Grounding Tool, Connected Agent Tool, and File Search capabilities.

### App5 - Microsoft Agent Framework Implementation
**Technology**: Azure AI Foundry  
**Framework**: Microsoft Agent Framework  
**Description**: Clean, modular multi-agent basketball coaching system using the new Microsoft Agent Framework with proper resource management and workflow orchestration.

### Clean-up - Azure AI Foundry Resource Management
**Technology**: Azure AI Foundry  
**Framework**: Azure AI Projects SDK  
**Description**: Utility script for cleaning up Azure AI Foundry resources (agents, threads, files, vector stores) to manage costs and maintain clean environments.

---

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/basketball-ai-agent.git
   cd basketball-ai-agent
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```


3. **Install dependencies:**
   - Each app has its own `requirements.txt` file. Install dependencies for the app you want to run:
     - For **App 1**:
       ```bash
       pip install -r src/app1/requirements.txt
       ```
     - For **App 2**:
       ```bash
       pip install -r src/app2/requirements.txt
       ```
     - For **App 2-Modular**:
       ```bash
       pip install -r src/app2-modular/requirements.txt
       ```
     - For **App 3**:
       ```bash
       pip install -r src/app3/requirements.txt
       ```
     - For **App 4**:
       ```bash
       pip install -r src/app4/requirements.txt
       ```
     - For **App 5**:
       ```bash
       pip install -r src/app5/requirements.txt
       ```
     - For **Clean-up**:
       ```bash
       pip install -r src/clean-up/requirements.txt
       ```
   - *(If a `requirements.txt` is missing, install dependencies as needed for that app, e.g. `semantic-kernel`, `openai`, etc.)*

4. **Set up environment variables:**
   - Set the following variables in your shell or `.env` file as needed for each app:
     - **App 1** (Azure AI Foundry):
       - `AZURE_AI_AGENT_PROJECT_CONNECTION_STRING=""`
       - `AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME=""`
       - `NBA_CSV_FILE_PATH="../data/nba3p.csv"`
     - **App 2** (Azure AI Foundry + Semantic Kernel):
       - `AZURE_AI_AGENT_PROJECT_CONNECTION_STRING=""`
       - `AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME=""`
     - **App 2-Modular** (Azure AI Foundry + Semantic Kernel):
       - `AZURE_AI_AGENT_PROJECT_CONNECTION_STRING=""`
       - `AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME=""`
     - **App 3** (Azure OpenAI + Semantic Kernel):
       - `AZURE_OPENAI_ENDPOINT=""`
       - `AZURE_OPENAI_API_KEY=""`
       - `AZURE_OPENAI_DEPLOYMENT=""`
     - **App 4** (Azure AI Foundry):
       - `AZURE_AI_AGENT_PROJECT_CONNECTION_STRING=""`
       - `AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME=""`
     - **App 5** (Azure AI Foundry + Agent Framework):
       - `AZURE_AI_AGENT_PROJECT_CONNECTION_STRING=""`
       - `AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME=""`
     - **Clean-up** (Azure AI Foundry):
       - `AZURE_AI_AGENT_PROJECT_CONNECTION_STRING=""`

## Usage

- **App 1** (Azure AI Foundry Agent Service):
  - Navigate to `src/app1/` and run the main script:
    ```bash
    cd src/app1
    python app1.py
    ```

- **App 2** (Semantic Kernel Multi-Agent):
  - Navigate to `src/app2/` and run the app:
    ```bash
    cd src/app2
    python app2.py
    ```

- **App 2-Modular** (Modular Semantic Kernel):
  - Navigate to `src/app2-modular/` and run the main app:
    ```bash
    cd src/app2-modular
    python main.py
    ```

- **App 3** (Semantic Kernel Function Calling):
  - Navigate to `src/app3/` and run the app:
    ```bash
    cd src/app3
    python app3.py
    ```

- **App 4** (Advanced Azure AI Foundry):
  - Navigate to `src/app4/` and run the app:
    ```bash
    cd src/app4
    python app4.py
    ```

- **App 5** (Microsoft Agent Framework):
  - Navigate to `src/app5/` and run the app:
    ```bash
    cd src/app5
    python app5.py
    ```
  - Or with custom task:
    ```bash
    cd src/app5
    python app5.py "We need help with our defense against pick and roll plays"
    ```

- **Clean-up** (Resource Management):
  - Navigate to `src/clean-up/` and run the cleanup script:
    ```bash
    cd src/clean-up
    python clean_up.py
    ```
  - Use dry-run mode to preview deletions:
    ```bash
    python clean_up.py --dry-run
    ```

## Data

- The `data/` folder contains basketball datasets (e.g., `nba3p.csv`) used by app1.

## Technology Stack Summary

| App | Technology | Framework | Use Case |
|-----|------------|-----------|----------|
| App1 | Azure AI Foundry | Azure AI Agent Service | Basic agent implementation |
| App2 | Azure AI Foundry | Semantic Kernel | Multi-agent orchestration |
| App2-Modular | Azure AI Foundry | Semantic Kernel | Modular multi-agent system |
| App3 | Azure OpenAI | Semantic Kernel | Function calling & plugins |
| App4 | Azure AI Foundry | Azure AI Agent Service | Advanced features (Bing, File Search) |
| App5 | Azure AI Foundry | Microsoft Agent Framework | Clean workflow orchestration |
| Clean-up | Azure AI Foundry | Azure AI Projects SDK | Resource management utility |

## Notes

- Make sure you have the necessary Azure AI Foundry or Azure OpenAI access and correct API keys/connection strings.
- For Azure AI Foundry apps, you'll need a project connection string.
- For Azure OpenAI apps (App3), you'll need direct Azure OpenAI service credentials.
- Each app demonstrates different approaches to building basketball coaching AI agents.
- For more details, refer to the code comments and the referenced blog posts above.
