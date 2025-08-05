#!/usr/bin/env python3
"""
Single Bing Grounding Experiment - Focused on recording responses and understanding how it works
"""

import os
import time
import logging
import csv
import json
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import BingGroundingTool
from azure.identity import DefaultAzureCredential

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bing_grounding_experiment.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BingGroundingExperiment:
    def __init__(self, endpoint: str, connection_id: str = None):
        logger.info(f"Initializing Bing Grounding Experiment with endpoint: {endpoint}")
        self.endpoint = endpoint
        self.connection_id = connection_id
        self.agents_client = None
        self.agent = None
        self.initialize_client()
        
    def initialize_client(self):
        """Initialize the Azure AI Agents client"""
        logger.info("Initializing Azure AI Agents client...")
        try:
            # Use DefaultAzureCredential for authentication
            credential = DefaultAzureCredential()
            logger.info("DefaultAzureCredential initialized successfully")
            
            # Create the agents client with the project-specific endpoint
            # The endpoint should be the base AI Foundry endpoint
            project_endpoint = self.endpoint.rstrip('/')
            logger.info(f"Creating AgentsClient with project endpoint: {project_endpoint}")
            
            self.agents_client = AgentsClient(
                endpoint=project_endpoint,
                credential=credential
            )
            logger.info("AgentsClient created successfully")
            
            # List existing agents first
            logger.info("Listing existing agents...")
            try:
                agents = list(self.agents_client.list_agents())
                logger.info(f"Found {len(agents)} existing agents:")
                for agent in agents:
                    logger.info(f"  - ID: {agent.id}, Name: {agent.name}")
                
                # Use the first available agent
                if agents:
                    self.agent = agents[0]
                    logger.info(f"Using agent: {self.agent.id} ({self.agent.name})")
                else:
                    logger.warning("No existing agents found. Will create a new one.")
                    self.agent = None
                    
            except Exception as e:
                logger.warning(f"Could not list agents: {e}")
                self.agent = None
            
            # If no agent found, create a new one
            if not self.agent:
                logger.info("Creating new agent...")
                try:
                    # Create a new agent with basic configuration
                    self.agent = self.agents_client.create_agent(
                        name="bing-grounding-experiment-agent",
                        instructions="You are a helpful assistant with access to real-time web search via Bing Grounding Tool.",
                        model="gpt-4o",
                        temperature=0.0
                    )
                    logger.info(f"✅ New agent created: {self.agent.id} ({self.agent.name})")
                except Exception as e:
                    logger.error(f"❌ Failed to create new agent: {e}")
                    raise
            
            logger.info(f"Final agent: ID={self.agent.id}, Name={self.agent.name}")
            logger.info(f"Agent tools count: {len(self.agent.tools) if self.agent.tools else 0}")
            
            # Check if we have a connection_id and configure Bing Grounding Tool
            if self.connection_id:
                logger.info(f"🔧 Configuring Bing Grounding Tool with connection_id: {self.connection_id}")
                try:
                    # Create Bing Grounding Tool using the correct format
                    tool_definition = {
                        "type": "bing_grounding",
                        "bing_grounding": {
                            "search_configurations": [
                                {
                                    "connection_id": self.connection_id
                                }
                            ]
                        }
                    }
                    logger.info("✅ Bing Grounding Tool definition created successfully")
                    
                    # Update the agent with the Bing Grounding Tool
                    logger.info("🔄 Updating agent with Bing Grounding Tool...")
                    try:
                        updated_agent = self.agents_client.update_agent(
                            agent_id=self.agent.id,
                            tools=[tool_definition]
                        )
                        self.agent = updated_agent
                        logger.info("✅ Agent updated successfully with Bing Grounding Tool")
                        logger.info(f"Agent tools count: {len(self.agent.tools) if self.agent.tools else 0}")
                        
                        # Verify the tool was added
                        if self.agent.tools:
                            for tool in self.agent.tools:
                                logger.info(f"🔧 Tool: {type(tool).__name__}")
                                if hasattr(tool, 'connection_id'):
                                    logger.info(f"   Connection ID: {tool.connection_id}")
                        else:
                            logger.warning("⚠️  No tools found on agent after update!")
                            
                    except Exception as e:
                        logger.error(f"❌ Failed to update agent: {e}")
                        logger.info("📝 Trying alternative approach...")
                        
                        # Try creating a new agent with the tool
                        try:
                            logger.info("🔄 Creating new agent with Bing Grounding Tool...")
                            new_agent = self.agents_client.create_agent(
                                name="bing-grounding-experiment-agent",
                                instructions="You are a helpful assistant with access to real-time web search via Bing Grounding Tool.",
                                model="gpt-4o",
                                tools=[tool_definition],
                                temperature=0.0
                            )
                            self.agent = new_agent
                            logger.info("✅ New agent created successfully with Bing Grounding Tool")
                            logger.info(f"Agent tools count: {len(self.agent.tools) if self.agent.tools else 0}")
                        except Exception as e2:
                            logger.error(f"❌ Failed to create new agent: {e2}")
                            logger.info("📝 Continuing with existing agent configuration")
                    
                except Exception as e:
                    logger.error(f"❌ Failed to configure Bing Grounding Tool: {e}")
                    logger.info("📝 Continuing with existing agent configuration")
            else:
                logger.info("⚠️  NOTE: No connection_id provided")
                logger.info("   The agent will respond using its training data only")
                logger.info("   To enable web search, we need to add BingGroundingTool with connection_id")
                
        except Exception as e:
            logger.error(f"Failed to initialize client: {e}")
            raise

    def load_test_prompts(self, prompt_file: str = None) -> List[Dict[str, Any]]:
        """Load test prompts from specified file or default to CSV"""
        if prompt_file:
            logger.info(f"Loading prompts from {prompt_file}...")
        else:
            logger.info("Loading prompts from prompts/bing-prompts.csv...")
        
        prompts = []
        
        if prompt_file and prompt_file.endswith('.md'):
            # Load markdown file as a single prompt
            try:
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                prompts.append({
                    'question': content,
                    'current_response_time': '30.0s',  # Estimated baseline for long prompt
                    'expected_behavior': 'Should provide comprehensive real-time search results with citations'
                })
                
                logger.info(f"Loaded 1 long prompt from {prompt_file} ({len(content)} characters)")
                
            except Exception as e:
                logger.error(f"Failed to load prompt from {prompt_file}: {e}")
                raise
        else:
            # Load from CSV file
            try:
                import pandas as pd
                csv_file = prompt_file if prompt_file else 'prompts/bing-prompts.csv'
                df = pd.read_csv(csv_file)
                logger.info(f"Found {len(df)} prompts in CSV file")
                
                for _, row in df.iterrows():
                    # Clean up the response time (remove 's' suffix if present)
                    current_time = str(row['Current response time (seconds)'])
                    if current_time.endswith('s'):
                        current_time = current_time[:-1]
                    
                    prompts.append({
                        'question': row['Question'],
                        'current_response_time': f"{current_time}s",
                        'expected_behavior': 'Should provide real-time search results with citations'
                    })
                
                logger.info(f"Loaded {len(prompts)} prompts from CSV")
                
            except Exception as e:
                logger.error(f"Failed to load prompts from CSV: {e}")
                raise
        
        if not prompts:
            raise ValueError("No prompts loaded!")
        
        logger.info(f"Total prompts loaded: {len(prompts)}")
        return prompts

    def test_prompt_latency(self, prompt_data: Dict[str, Any], search_count: int = 1):
        """Test latency for a single prompt and record the full response"""
        question = prompt_data['question']
        current_time = prompt_data['current_response_time']
        expected_behavior = prompt_data['expected_behavior']
        
        logger.info(f"Testing prompt: {question[:100]}...")
        logger.info(f"Current response time: {current_time}")
        logger.info(f"Expected behavior: {expected_behavior}")
        logger.info(f"Running {search_count} searches")
        
        results = []
        
        for i in range(search_count):
            logger.info(f"Starting search {i+1}/{search_count}")
            
            try:
                # Use the create_thread_and_process_run method
                start_time_total = time.time()
                logger.info("Creating thread and processing run...")
                
                # Create thread and run in one call
                logger.info(f"🔍 Creating thread and run with agent: {self.agent.id}")
                logger.info(f"🔧 Agent tools: {len(self.agent.tools) if self.agent.tools else 0}")
                
                run = self.agents_client.create_thread_and_process_run(
                    agent_id=self.agent.id,
                    thread={
                        "messages": [
                            {
                                "role": "user",
                                "content": question
                            }
                        ]
                    }
                )
                
                logger.info(f"📝 Run created: {run.id}")
                logger.info(f"📊 Run status: {run.status}")
                
                total_time = time.time() - start_time_total
                logger.info(f"Search {i+1}/{search_count} completed in {total_time:.2f}s")
                
                # Get the response
                logger.info("Getting response messages...")
                try:
                    # Use the messages attribute which should have a list method
                    messages = self.agents_client.messages.list(thread_id=run.thread_id)
                    
                    # Find the assistant's response
                    assistant_message = None
                    full_response = ""
                    
                    for message in messages:
                        if message.role == "assistant":
                            assistant_message = message
                            # Extract the actual response text
                            if hasattr(message, 'content') and message.content:
                                if isinstance(message.content, list):
                                    for content_item in message.content:
                                        if hasattr(content_item, 'text') and hasattr(content_item.text, 'value'):
                                            full_response = content_item.text.value
                                            break
                                elif isinstance(message.content, str):
                                    full_response = message.content
                            break
                    
                    if assistant_message and full_response:
                        logger.info(f"✅ Response received: {len(full_response)} characters")
                        logger.info(f"📝 Full response: {full_response}")
                        
                        # Check if response mentions search limitations
                        search_limitations = []
                        if "search" in full_response.lower() and ("issue" in full_response.lower() or "unable" in full_response.lower()):
                            search_limitations.append("Mentions search issues")
                        if "training data" in full_response.lower():
                            search_limitations.append("Mentions training data cutoff")
                        if "2023" in full_response.lower() or "october" in full_response.lower():
                            search_limitations.append("Mentions 2023/October cutoff")
                            
                        logger.info(f"🔍 Search limitations detected: {search_limitations}")
                        
                    else:
                        logger.warning("No assistant response found")
                        full_response = "No response received"
                        
                except Exception as e:
                    logger.error(f"Error getting messages: {e}")
                    full_response = f"Error: {str(e)}"
                
                results.append({
                    'question': question,
                    'current_response_time': current_time,
                    'new_response_time': total_time,
                    'improvement_seconds': float(current_time.replace('s', '')) - total_time if 's' in current_time else None,
                    'improvement_percentage': ((float(current_time.replace('s', '')) - total_time) / float(current_time.replace('s', '')) * 100) if 's' in current_time else None,
                    'response_length': len(full_response),
                    'full_response': full_response,
                    'search_limitations': search_limitations if 'search_limitations' in locals() else [],
                    'expected_behavior': expected_behavior,
                    'search_number': i + 1,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Add delay between searches
                if i < search_count - 1:
                    delay = 2  # 2 second delay between searches
                    logger.info(f"Waiting {delay}s before next search...")
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error(f"Error during search {i+1}: {e}")
                results.append({
                    'question': question,
                    'current_response_time': current_time,
                    'new_response_time': None,
                    'improvement_seconds': None,
                    'improvement_percentage': None,
                    'response_length': 0,
                    'full_response': f"Error: {str(e)}",
                    'search_limitations': [],
                    'expected_behavior': expected_behavior,
                    'search_number': i + 1,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        return results

    def run_experiment(self, prompt_file: str = None, search_count: int = 1):
        """Run the complete experiment"""
        logger.info(f"Starting Bing Grounding Experiment with {search_count} searches per prompt")
        
        # Load test prompts
        prompts = self.load_test_prompts(prompt_file)
        if not prompts:
            logger.error("No prompts loaded")
            return
        
        all_results = []
        
        for i, prompt_data in enumerate(prompts):
            logger.info(f"Processing prompt {i+1}/{len(prompts)}")
            results = self.test_prompt_latency(prompt_data, search_count)
            all_results.extend(results)
            
            # Add delay between prompts
            if i < len(prompts) - 1:
                delay = 3  # 3 second delay between prompts
                logger.info(f"Waiting {delay}s before next prompt...")
                time.sleep(delay)
        
        # Convert to DataFrame
        df = pd.DataFrame(all_results)
        
        # Save latency summary to CSV (without full responses)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_df = df[['question', 'current_response_time', 'new_response_time', 'improvement_seconds', 'improvement_percentage', 'response_length', 'search_limitations', 'expected_behavior', 'search_number', 'timestamp']].copy()
        filename = f"logs/bing_grounding_results_{timestamp}.csv"
        summary_df.to_csv(filename, index=False)
        logger.info(f"Latency summary saved to {filename}")
        
        # Save full responses to a separate file for easy reading
        responses_filename = f"logs/bing_grounding_responses_{timestamp}.txt"
        with open(responses_filename, 'w', encoding='utf-8') as f:
            f.write("BING GROUNDING EXPERIMENT - FULL RESPONSES\n")
            f.write("=" * 50 + "\n\n")
            
            for i, result in enumerate(all_results):
                f.write(f"PROMPT {i+1}:\n")
                f.write(f"Question: {result['question']}\n")
                f.write(f"Response Time: {result['new_response_time']:.2f}s\n")
                f.write(f"Search Limitations: {result.get('search_limitations', [])}\n")
                f.write(f"Response Length: {result['response_length']} characters\n")
                f.write("-" * 30 + "\n")
                f.write(f"FULL RESPONSE:\n{result['full_response']}\n")
                f.write("\n" + "=" * 50 + "\n\n")
        
        logger.info(f"Full responses saved to {responses_filename}")
        
        # Print summary
        logger.info("Experiment completed!")
        logger.info(f"Total searches: {len(df)}")
        logger.info(f"Successful searches: {len(df[df['new_response_time'].notna()])}")
        logger.info(f"Failed searches: {len(df[df['new_response_time'].isna()])}")
        
        if len(df[df['new_response_time'].notna()]) > 0:
            avg_time = df[df['new_response_time'].notna()]['new_response_time'].mean()
            min_time = df[df['new_response_time'].notna()]['new_response_time'].min()
            max_time = df[df['new_response_time'].notna()]['new_response_time'].max()
            
            logger.info(f"Average response time: {avg_time:.2f}s")
            logger.info(f"Min response time: {min_time:.2f}s")
            logger.info(f"Max response time: {max_time:.2f}s")
            
            # Calculate improvements
            improvements = df[df['improvement_seconds'].notna()]
            if len(improvements) > 0:
                avg_improvement = improvements['improvement_seconds'].mean()
                avg_improvement_pct = improvements['improvement_percentage'].mean()
                logger.info(f"Average improvement: {avg_improvement:.2f}s ({avg_improvement_pct:.1f}%)")
        
        # Summary of search limitations
        all_limitations = []
        for result in all_results:
            all_limitations.extend(result.get('search_limitations', []))
        
        logger.info(f"Search limitations found: {set(all_limitations)}")
        
        return df

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Bing Grounding Experiment')
    parser.add_argument('--prompt-file', '-p', 
                       help='Path to prompt file (CSV or MD). Default: prompts/bing-prompts.csv')
    parser.add_argument('--search-count', '-s', type=int, default=1,
                       help='Number of searches per prompt (default: 1)')
    
    args = parser.parse_args()
    
    logger.info("Starting Bing Grounding Experiment")
    
    # Load environment variables
    load_dotenv('.env')
    
    endpoint = os.getenv('AZURE_AI_PROJECTS_CONNECTION_STRING')
    connection_id = os.getenv('BING_GROUNDING_CONNECTION_ID')
    
    if not endpoint:
        logger.error("AZURE_AI_PROJECTS_CONNECTION_STRING not found in environment")
        return
    
    logger.info(f"Using endpoint: {endpoint}")
    if connection_id:
        logger.info(f"Using connection_id: {connection_id}")
    else:
        logger.warning("No BING_GROUNDING_CONNECTION_ID found in environment")
    
    # Create and run experiment
    experiment = BingGroundingExperiment(endpoint, connection_id)
    experiment.run_experiment(prompt_file=args.prompt_file, search_count=args.search_count)

if __name__ == "__main__":
    main() 