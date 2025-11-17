#!/usr/bin/env python3
"""
Azure AI Foundry Project Cleanup Script

This script helps clean up all agents and threads from an Azure AI Foundry project
to avoid unnecessary costs and maintain a clean environment.

Usage:
    python clean_up.py [--dry-run] [--agents-only] [--threads-only] [--confirm]

Options:
    --dry-run       Show what would be deleted without actually deleting
    --agents-only   Only delete agents (keep threads)
    --threads-only  Only delete threads (keep agents) 
    --confirm       Skip confirmation prompts
"""

import os
import sys
import asyncio
import argparse
from typing import List, Optional
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

# Load environment variables
load_dotenv()

class AzureAIFoundryCleanup:
    """Handles cleanup operations for Azure AI Foundry project resources."""
    
    def __init__(self, endpoint: str, dry_run: bool = False):
        """
        Initialize the cleanup client.
        
        Args:
            endpoint: Azure AI Foundry project endpoint
            dry_run: If True, only show what would be deleted without deleting
        """
        self.endpoint = endpoint
        self.dry_run = dry_run
        self.deleted_counts = {"agents": 0, "threads": 0, "files": 0, "vector_stores": 0}
        
        # Initialize the AI Project Client with managed identity
        self.project_client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential()
        )
        
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        try:
            self.project_client.close()
        except Exception as e:
            print(f"Warning: Error closing project client: {e}")
    
    def list_agents(self) -> List:
        """
        List all agents in the project.
        
        Returns:
            List of agent objects
        """
        try:
            print("📋 Listing all agents...")
            agents = list(self.project_client.agents.list_agents())
            print(f"   Found {len(agents)} agents")
            
            if agents:
                print("   Agents found:")
                for agent in agents:
                    print(f"   - ID: {agent.id}, Name: {agent.name}, Created: {agent.created_at}")
                    
            return agents
        except Exception as e:
            print(f"❌ Error listing agents: {e}")
            return []
    
    def list_threads(self) -> List:
        """
        List all threads in the project.
        
        Returns:
            List of thread objects
        """
        try:
            print("📋 Listing all threads...")
            threads = list(self.project_client.agents.threads.list())
            print(f"   Found {len(threads)} threads")
            
            if threads:
                print("   Threads found:")
                for thread in threads:
                    print(f"   - ID: {thread.id}, Created: {thread.created_at}")
                    
            return threads
        except Exception as e:
            print(f"❌ Error listing threads: {e}")
            return []
    
    def list_files(self) -> List:
        """
        List all files in the project.
        
        Returns:
            List of file objects
        """
        try:
            print("📋 Listing all files...")
            files = list(self.project_client.agents.files.list())
            print(f"   Found {len(files)} files")
            
            if files:
                print("   Files found:")
                for file in files:
                    try:
                        # Handle different possible file object formats
                        file_id = getattr(file, 'id', str(file))
                        file_name = getattr(file, 'filename', 'Unknown')
                        file_purpose = getattr(file, 'purpose', 'Unknown')
                        file_size = getattr(file, 'bytes', 'Unknown')
                        print(f"   - ID: {file_id}, Name: {file_name}, Purpose: {file_purpose}, Size: {file_size} bytes")
                    except Exception as fe:
                        print(f"   - File info error: {fe}, Raw: {file}")
                    
            return files
        except Exception as e:
            print(f"❌ Error listing files: {e}")
            return []
    
    def list_vector_stores(self) -> List:
        """
        List all vector stores in the project.
        
        Returns:
            List of vector store objects
        """
        try:
            print("📋 Listing all vector stores...")
            vector_stores = list(self.project_client.agents.vector_stores.list())
            print(f"   Found {len(vector_stores)} vector stores")
            
            if vector_stores:
                print("   Vector stores found:")
                for vs in vector_stores:
                    print(f"   - ID: {vs.id}, Name: {vs.name}, File count: {vs.file_counts.total}, Created: {vs.created_at}")
                    
            return vector_stores
        except Exception as e:
            print(f"❌ Error listing vector stores: {e}")
            return []
    
    def delete_agents(self, agents: Optional[List] = None, agent_ids: Optional[List[str]] = None) -> bool:
        """
        Delete agents by list of agent objects or by IDs.
        
        Args:
            agents: Optional list of agents to delete. If None, uses agent_ids.
            agent_ids: Optional list of agent IDs to delete.
            
        Returns:
            True if successful, False otherwise
        """
        # If no agents provided, try to list them (will show warning about no list method)
        if agents is None and agent_ids is None:
            agents = self.list_agents()
        
        # Convert agent_ids to a workable format if provided
        if agent_ids:
            print(f"\n🗑️  {'[DRY RUN] Would delete' if self.dry_run else 'Deleting'} agents by ID...")
            for agent_id in agent_ids:
                try:
                    if self.dry_run:
                        print(f"   [DRY RUN] Would delete agent ID: {agent_id}")
                    else:
                        print(f"   Deleting agent ID: {agent_id}")
                        self.project_client.agents.delete_agent(agent_id)
                        print(f"   ✅ Successfully deleted agent: {agent_id}")
                        
                    self.deleted_counts["agents"] += 1
                    
                except ResourceNotFoundError:
                    print(f"   ⚠️  Agent {agent_id} was already deleted or not found")
                except HttpResponseError as e:
                    print(f"   ❌ Error deleting agent {agent_id}: {e}")
                    return False
                except Exception as e:
                    print(f"   ❌ Unexpected error deleting agent {agent_id}: {e}")
                    return False
            return True
        
        # Handle deletion by agent objects (if any)
        if not agents:
            print("✅ No agents to delete")
            return True
            
        print(f"\n🗑️  {'[DRY RUN] Would delete' if self.dry_run else 'Deleting'} {len(agents)} agents...")
        
        for agent in agents:
            try:
                if self.dry_run:
                    print(f"   [DRY RUN] Would delete agent: {agent.name} (ID: {agent.id})")
                else:
                    print(f"   Deleting agent: {agent.name} (ID: {agent.id})")
                    self.project_client.agents.delete_agent(agent.id)
                    print(f"   ✅ Successfully deleted agent: {agent.name}")
                    
                self.deleted_counts["agents"] += 1
                
            except ResourceNotFoundError:
                print(f"   ⚠️  Agent {agent.id} was already deleted")
            except HttpResponseError as e:
                print(f"   ❌ Error deleting agent {agent.id}: {e}")
                return False
            except Exception as e:
                print(f"   ❌ Unexpected error deleting agent {agent.id}: {e}")
                return False
                
        return True
    
    def delete_threads(self, threads: Optional[List] = None) -> bool:
        """
        Delete all threads or a specific list of threads.
        
        Args:
            threads: Optional list of threads to delete. If None, deletes all threads.
            
        Returns:
            True if successful, False otherwise
        """
        if threads is None:
            threads = self.list_threads()
        
        if not threads:
            print("✅ No threads to delete")
            return True
            
        print(f"\n🗑️  {'[DRY RUN] Would delete' if self.dry_run else 'Deleting'} {len(threads)} threads...")
        
        for thread in threads:
            try:
                if self.dry_run:
                    print(f"   [DRY RUN] Would delete thread: {thread.id}")
                else:
                    print(f"   Deleting thread: {thread.id}")
                    self.project_client.agents.threads.delete(thread.id)
                    print(f"   ✅ Successfully deleted thread: {thread.id}")
                    
                self.deleted_counts["threads"] += 1
                
            except ResourceNotFoundError:
                print(f"   ⚠️  Thread {thread.id} was already deleted")
            except HttpResponseError as e:
                print(f"   ❌ Error deleting thread {thread.id}: {e}")
                return False
            except Exception as e:
                print(f"   ❌ Unexpected error deleting thread {thread.id}: {e}")
                return False
                
        return True
    
    def delete_files(self, files: Optional[List] = None) -> bool:
        """
        Delete all files or a specific list of files.
        
        Args:
            files: Optional list of files to delete. If None, deletes all files.
            
        Returns:
            True if successful, False otherwise
        """
        if files is None:
            files = self.list_files()
        
        if not files:
            print("✅ No files to delete")
            return True
            
        print(f"\n🗑️  {'[DRY RUN] Would delete' if self.dry_run else 'Deleting'} {len(files)} files...")
        
        for file in files:
            try:
                # Handle different file object types
                if hasattr(file, 'id'):
                    # Real file object
                    file_id = file.id
                    file_name = getattr(file, 'filename', getattr(file, 'name', 'Unknown'))
                else:
                    # String or other format
                    file_id = str(file)
                    file_name = 'Unknown'
                    
                if self.dry_run:
                    print(f"   [DRY RUN] Would delete file: {file_name} (ID: {file_id})")
                else:
                    print(f"   Deleting file: {file_name} (ID: {file_id})")
                    if hasattr(file, 'id'):
                        self.project_client.agents.files.delete(file.id)
                    else:
                        self.project_client.agents.files.delete(file_id)
                    print(f"   ✅ Successfully deleted file: {file_name}")
                    
                self.deleted_counts["files"] += 1
                
            except ResourceNotFoundError:
                file_ref = getattr(file, 'id', str(file))
                print(f"   ⚠️  File {file_ref} was already deleted")
            except HttpResponseError as e:
                file_ref = getattr(file, 'id', str(file))
                print(f"   ❌ Error deleting file {file_ref}: {e}")
                return False
            except Exception as e:
                file_ref = getattr(file, 'id', str(file))
                print(f"   ❌ Unexpected error deleting file {file_ref}: {e}")
                return False
                
        return True
    
    def delete_vector_stores(self, vector_stores: Optional[List] = None) -> bool:
        """
        Delete all vector stores or a specific list of vector stores.
        
        Args:
            vector_stores: Optional list to delete. If None, deletes all vector stores.
            
        Returns:
            True if successful, False otherwise
        """
        if vector_stores is None:
            vector_stores = self.list_vector_stores()
        
        if not vector_stores:
            print("✅ No vector stores to delete")
            return True
            
        print(f"\n🗑️  {'[DRY RUN] Would delete' if self.dry_run else 'Deleting'} {len(vector_stores)} vector stores...")
        
        for vs in vector_stores:
            try:
                if self.dry_run:
                    print(f"   [DRY RUN] Would delete vector store: {vs.name} (ID: {vs.id})")
                else:
                    print(f"   Deleting vector store: {vs.name} (ID: {vs.id})")
                    self.project_client.agents.vector_stores.delete(vs.id)
                    print(f"   ✅ Successfully deleted vector store: {vs.name}")
                    
                self.deleted_counts["vector_stores"] += 1
                
            except ResourceNotFoundError:
                print(f"   ⚠️  Vector store {vs.id} was already deleted")
            except HttpResponseError as e:
                print(f"   ❌ Error deleting vector store {vs.id}: {e}")
                return False
            except Exception as e:
                print(f"   ❌ Unexpected error deleting vector store {vs.id}: {e}")
                return False
                
        return True
    
    def cleanup_all(self, agents_only: bool = False, threads_only: bool = False, 
                   include_files: bool = True, include_vector_stores: bool = True,
                   agent_ids: Optional[List[str]] = None, list_only: bool = False) -> bool:
        """
        Perform complete cleanup of all resources.
        
        Args:
            agents_only: If True, only delete agents
            threads_only: If True, only delete threads
            include_files: If True, also delete files
            include_vector_stores: If True, also delete vector stores
            agent_ids: Optional list of specific agent IDs to delete
            list_only: If True, only list resources without deleting
            
        Returns:
            True if all operations successful, False otherwise
        """
        success = True
        
        print(f"\n🧹 Starting {'[LIST ONLY] ' if list_only else '[DRY RUN] ' if self.dry_run else ''}cleanup of Azure AI Foundry project...")
        print(f"   Project endpoint: {self.endpoint}")
        
        # If list_only, just show what exists
        if list_only:
            if not threads_only:
                self.list_agents()
                if agent_ids:
                    print(f"\n📝 Agent IDs you specified: {', '.join(agent_ids)}")
            if not agents_only:
                self.list_threads()
            if include_files and not agents_only and not threads_only:
                self.list_files()
            if include_vector_stores and not agents_only and not threads_only:
                self.list_vector_stores()
            return True
        
        # Delete agents first (they may have dependencies on other resources)
        if not threads_only:
            if not self.delete_agents(agent_ids=agent_ids):
                success = False
        
        # Delete threads
        if not agents_only:
            if not self.delete_threads():
                success = False
        
        # Delete files if requested
        if include_files and not agents_only and not threads_only:
            if not self.delete_files():
                success = False
        
        # Delete vector stores if requested
        if include_vector_stores and not agents_only and not threads_only:
            if not self.delete_vector_stores():
                success = False
        
        # Print summary
        self.print_summary()
        
        return success
    
    def print_summary(self):
        """Print cleanup summary."""
        print(f"\n📊 Cleanup Summary:")
        print(f"   Agents {'would be ' if self.dry_run else ''}deleted: {self.deleted_counts['agents']}")
        print(f"   Threads {'would be ' if self.dry_run else ''}deleted: {self.deleted_counts['threads']}")
        print(f"   Files {'would be ' if self.dry_run else ''}deleted: {self.deleted_counts['files']}")
        print(f"   Vector stores {'would be ' if self.dry_run else ''}deleted: {self.deleted_counts['vector_stores']}")
        
        if self.dry_run:
            print("\n💡 This was a dry run. Use --confirm to actually delete resources.")
        else:
            print("\n✅ Cleanup completed!")


def get_user_confirmation(message: str) -> bool:
    """
    Get user confirmation before proceeding.
    
    Args:
        message: Message to display to user
        
    Returns:
        True if user confirms, False otherwise
    """
    while True:
        response = input(f"\n{message} (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no', '']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no")


def main():
    """Main function to handle command line arguments and run cleanup."""
    parser = argparse.ArgumentParser(
        description="Clean up Azure AI Foundry project resources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python clean_up.py --dry-run                    # Show what would be deleted
  python clean_up.py --confirm                    # Delete all resources
  python clean_up.py --agents-only --confirm      # Delete only agents
  python clean_up.py --threads-only --dry-run     # Show threads that would be deleted
  python clean_up.py --agent-ids agent1 agent2   # Delete specific agents by ID
        """
    )
    
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be deleted without actually deleting')
    parser.add_argument('--agents-only', action='store_true',
                       help='Only delete agents (keep threads and other resources)')
    parser.add_argument('--threads-only', action='store_true', 
                       help='Only delete threads (keep agents and other resources)')
    parser.add_argument('--confirm', action='store_true',
                       help='Skip confirmation prompts and proceed with deletion')
    parser.add_argument('--no-files', action='store_true',
                       help='Skip deletion of files')
    parser.add_argument('--no-vector-stores', action='store_true', 
                       help='Skip deletion of vector stores')
    parser.add_argument('--agent-ids', nargs='*', metavar='ID',
                       help='Specific agent IDs to delete (space-separated)')
    parser.add_argument('--list-only', action='store_true',
                       help='Only list resources without deleting anything')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.agents_only and args.threads_only:
        print("❌ Error: --agents-only and --threads-only cannot be used together")
        sys.exit(1)
    
    # Get Azure AI Foundry endpoint
    endpoint = (os.getenv("AZURE_AI_AGENT_ENDPOINT") or 
                os.getenv("AZURE_AI_PROJECT_ENDPOINT") or 
                os.getenv("PROJECT_ENDPOINT"))
    if not endpoint:
        print("❌ Error: Azure AI Foundry endpoint environment variable is required")
        print("   Please set one of these variables in your .env file or environment:")
        print("   - AZURE_AI_AGENT_ENDPOINT")
        print("   - AZURE_AI_PROJECT_ENDPOINT") 
        print("   - PROJECT_ENDPOINT")
        sys.exit(1)
    
    print("🏀 Azure AI Foundry Project Cleanup Tool")
    print("=" * 50)
    
    # Determine what will be cleaned up
    cleanup_description = []
    if args.agents_only:
        cleanup_description.append("agents")
    elif args.threads_only:
        cleanup_description.append("threads")
    else:
        cleanup_description.append("agents and threads")
        if not args.no_files:
            cleanup_description.append("files")
        if not args.no_vector_stores:
            cleanup_description.append("vector stores")
    
    operation_type = "DRY RUN - Preview" if args.dry_run else "DELETE"
    print(f"Operation: {operation_type}")
    print(f"Target: {', '.join(cleanup_description)}")
    print(f"Project: {endpoint}")
    
    # Get confirmation unless --confirm is used, it's a dry run, or list-only
    if not args.dry_run and not args.confirm and not args.list_only:
        if not get_user_confirmation("⚠️  This will permanently delete resources. Continue?"):
            print("❌ Operation cancelled by user")
            sys.exit(0)
    
    # Perform cleanup
    try:
        with AzureAIFoundryCleanup(endpoint=endpoint, dry_run=args.dry_run or args.list_only) as cleanup:
            success = cleanup.cleanup_all(
                agents_only=args.agents_only,
                threads_only=args.threads_only,
                include_files=not args.no_files,
                include_vector_stores=not args.no_vector_stores,
                agent_ids=args.agent_ids,
                list_only=args.list_only
            )
            
            if not success:
                print("\n❌ Some cleanup operations failed. Check the output above for details.")
                sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
