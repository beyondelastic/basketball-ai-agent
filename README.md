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
   - Each app has its own `requirements.txt` file. Install dependencies for the app you want to run:
     - For **App 1**:
       ```bash
       pip install -r src/app1/requirements.txt
       ```
     - For **App 2**:
       ```bash
       pip install -r src/app2/requirements.txt
       ```
     - For **App 3**:
       ```bash
       pip install -r src/app3/requirements.txt
       ```
     - For **App 4**:
       ```bash
       pip install -r src/app4/requirements.txt
       ```
   - *(If a `requirements.txt` is missing, install dependencies as needed for that app, e.g. `semantic-kernel`, `openai`, etc.)*

4. **Set up environment variables:**
   - For Azure OpenAI, set the following variables in your shell or `.env` file as needed for each app:
     - **App 1:**
       - `AZURE_AI_AGENT_PROJECT_CONNECTION_STRING=""`
       - `AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME=""`
       - `NBA_CSV_FILE_PATH="../data/nba3p.csv"`
     - **App 2:**
       - `AZURE_AI_AGENT_PROJECT_CONNECTION_STRING=""`
       - `AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME=""`
     - **App 3:**
       - `AZURE_OPENAI_ENDPOINT=""`
       - `AZURE_OPENAI_API_KEY=""`
       - `AZURE_OPENAI_DEPLOYMENT=""`

## Usage

- **App 1:**
  - Navigate to `src/app1/` and run the main script:
    ```bash
    cd src/app1
    python app1.py
    ```

- **App 2:**
  - Navigate to `src/app2/` and run the app:
    ```bash
    cd src/app2
    python app2.py
    ```

- **App 3:**
  - Navigate to `src/app3/` and run the app:
    ```bash
    cd src/app3
    python app3.py
    ```

- **App 4:**
  - Navigate to `src/app4/` and run the app:
    ```bash
    cd src/app4
    python app4.py
    ```

## Data

- The `data/` folder contains basketball datasets (e.g., `nba3p.csv`) used by app1.

## Notes

- Make sure you have the necessary Azure AI Foundry Azure OpenAI access and correct API keys.
- For more details, refer to the code comments and the referenced blog posts above.
