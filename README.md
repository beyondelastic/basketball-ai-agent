# Basketball coach AI agent demo repository

Demo code for Azure AI Agent Service intro post on https://beyondelastic.github.io/posts/agent/ in folder src/app1/

Demo code for Semantic Kernel Multi-Agent AI apps post on https://beyondelastic.github.io/posts/multi-agent/ in folder src/app2

Demo code for Semantic Kernel function calling / plugins post on https://beyondelastic.github.io/posts/skfc/ in folder src/app3

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
   ```bash
   pip install -r requirements.txt
   ```
   *(If `requirements.txt` is missing, install dependencies as needed for each app, e.g. `semantic-kernel`, `openai`, etc.)*

4. **Set up environment variables:**
   - For Azure OpenAI, set the following variables in your shell or `.env` file:
     - For app1:
       - AZURE_AI_AGENT_PROJECT_CONNECTION_STRING=""
       - AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME=""
       - NBA_CSV_FILE_PATH="../data/nba3p.csv"
     - For app2:
       - AZURE_AI_AGENT_PROJECT_CONNECTION_STRING=""
       - AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME=""
     - For app3
       - AZURE_OPENAI_ENDPOINT=""
       - AZURE_OPENAI_API_KEY=""
       - AZURE_OPENAI_DEPLOYMENT=""

## Usage

- **App 1:**
  - Navigate to `src/app1/` and run the main script:
    ```bash
    cd src/app1
    python main.py
    ```

- **App 2:**
  - Navigate to `src/app2/` and run the app:
    ```bash
    cd src/app2
    python app.py
    ```

- **App 3:**
  - Navigate to `src/app3/` and run the app:
    ```bash
    cd src/app3
    python app3.py
    ```

## Data

- The `data/` folder contains basketball datasets (e.g., `nba3p.csv`) used by app1.

## Notes

- Make sure you have the necessary Azure AI Foundry Azure OpenAI access and correct API keys.
- For more details, refer to the code comments and the referenced blog posts above.
