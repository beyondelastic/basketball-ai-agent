# Azure AI Foundry Cleanup Script

This script helps clean up all agents, threads, files, and vector stores from your Azure AI Foundry project to avoid unnecessary costs and maintain a clean environment.

## Features

- **Safe operation**: Dry-run mode to preview what will be deleted
- **Selective cleanup**: Choose to delete only agents, only threads, or everything  
- **Comprehensive**: Handles agents, threads, files, and vector stores
- **Error handling**: Robust error handling with detailed feedback
- **Managed Identity**: Uses Azure Managed Identity for secure authentication

## Prerequisites

1. **Azure AI Foundry Project**: You need an active Azure AI Foundry project
2. **Environment Variables**: Set up your environment variables (see Configuration section)
3. **Permissions**: Ensure your identity has appropriate permissions to delete resources
4. **Python Dependencies**: Install required packages (see Installation section)

## Installation

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Configuration

Set up your environment variables in a `.env` file or your environment:

```bash
# Required: Azure AI Foundry project endpoint
AZURE_AI_AGENT_ENDPOINT=https://your-project.cognitiveservices.azure.com/
# Alternative name (either works)
PROJECT_ENDPOINT=https://your-project.cognitiveservices.azure.com/
```

## Usage

### Basic Usage

```bash
# Preview what will be deleted (safe - doesn't delete anything)
python clean_up.py --dry-run

# Delete all resources (agents, threads, files, vector stores)
python clean_up.py --confirm

# Interactive mode (asks for confirmation)
python clean_up.py
```

### Selective Cleanup

```bash
# Delete only agents (keep threads)
python clean_up.py --agents-only --confirm

# Delete only threads (keep agents)  
python clean_up.py --threads-only --confirm

# Delete agents and threads, but keep files and vector stores
python clean_up.py --no-files --no-vector-stores --confirm
```

### Advanced Examples

```bash
# Preview deletion of only agents
python clean_up.py --agents-only --dry-run

# Interactive deletion of only threads
python clean_up.py --threads-only

# Delete everything except files
python clean_up.py --no-files --confirm
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Show what would be deleted without actually deleting anything |
| `--agents-only` | Only delete agents (keep threads and other resources) |
| `--threads-only` | Only delete threads (keep agents and other resources) |  
| `--confirm` | Skip confirmation prompts and proceed with deletion |
| `--no-files` | Skip deletion of files |
| `--no-vector-stores` | Skip deletion of vector stores |

## What Gets Deleted

By default, the script will clean up:

1. **Agents**: All AI agents created in your project
2. **Threads**: All conversation threads
3. **Files**: All uploaded files used by agents
4. **Vector Stores**: All vector stores used for file search

## Security Features

- **Managed Identity Authentication**: Uses `DefaultAzureCredential` for secure authentication
- **Dry Run Mode**: Always test with `--dry-run` first
- **Confirmation Prompts**: Interactive confirmation unless `--confirm` is used
- **Error Handling**: Graceful handling of missing resources and permission errors

## Output Example

```
🏀 Azure AI Foundry Project Cleanup Tool
==================================================
Operation: DELETE
Target: agents and threads, files, vector stores
Project: https://your-project.cognitiveservices.azure.com/

⚠️  This will permanently delete resources. Continue? (y/N): y

🧹 Starting cleanup of Azure AI Foundry project...
   Project endpoint: https://your-project.cognitiveservices.azure.com/

📋 Listing all agents...
   Found 3 agents
   Agents found:
   - ID: asst_abc123, Name: HeadCoach, Created: 2024-11-13T10:30:00Z
   - ID: asst_def456, Name: AssistantCoach, Created: 2024-11-13T10:31:00Z
   - ID: asst_ghi789, Name: WebSearchAgent, Created: 2024-11-13T10:32:00Z

🗑️  Deleting 3 agents...
   Deleting agent: HeadCoach (ID: asst_abc123)
   ✅ Successfully deleted agent: HeadCoach
   Deleting agent: AssistantCoach (ID: asst_def456)  
   ✅ Successfully deleted agent: AssistantCoach
   Deleting agent: WebSearchAgent (ID: asst_ghi789)
   ✅ Successfully deleted agent: WebSearchAgent

📋 Listing all threads...
   Found 2 threads
   Threads found:
   - ID: thread_123abc, Created: 2024-11-13T10:35:00Z
   - ID: thread_456def, Created: 2024-11-13T10:40:00Z

🗑️  Deleting 2 threads...
   Deleting thread: thread_123abc
   ✅ Successfully deleted thread: thread_123abc
   Deleting thread: thread_456def
   ✅ Successfully deleted thread: thread_456def

📊 Cleanup Summary:
   Agents deleted: 3
   Threads deleted: 2  
   Files deleted: 0
   Vector stores deleted: 0

✅ Cleanup completed!
```

## Error Handling

The script handles common scenarios gracefully:

- **Already deleted resources**: Shows a warning but continues
- **Permission errors**: Clear error messages about access rights
- **Network issues**: Retry logic for transient failures  
- **Invalid endpoints**: Validation of configuration

## Best Practices

1. **Always use dry-run first**: `python clean_up.py --dry-run`
2. **Test with a development project**: Don't run on production without testing
3. **Backup important data**: The deletions are permanent
4. **Check permissions**: Ensure your identity has delete permissions
5. **Monitor costs**: Regular cleanup helps control Azure costs

## Troubleshooting

### Authentication Issues
```bash
# Check if you're logged into Azure CLI
az login
az account show
```

### Permission Issues
Ensure your identity has these roles on the Azure AI Foundry project:
- **Cognitive Services Contributor** (for agent operations)
- **Cognitive Services User** (for basic access)

### Environment Variable Issues
```bash
# Check if environment variables are set
echo $AZURE_AI_AGENT_ENDPOINT
# or
python -c "import os; print(os.getenv('AZURE_AI_AGENT_ENDPOINT'))"
```

## Safety Notes

⚠️ **Important**: This script permanently deletes resources. Always:
- Use `--dry-run` to preview changes first
- Test on a development environment before production
- Ensure you have backups of any important conversation history
- Verify the correct project endpoint is configured

The deletions are **permanent** and cannot be undone!