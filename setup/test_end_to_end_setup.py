#!/usr/bin/env python3
"""
Azure AI Agents + Bing Search Test
Simple test to verify if Azure AI Agents with Bing Search are working correctly.
"""

import os
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import BingGroundingTool
from azure.identity import DefaultAzureCredential

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AzureAIBingTest:
    def __init__(self):
        self.agents_client = None
        self.test_agent = None
        self.results = {}
        
    def test_environment_variables(self):
        """Test 1: Environment Variables"""
        logger.info("🧪 Test 1: Environment Variables")
        
        # Load from parent directory
        load_dotenv('../env.local')
        
        required_vars = {
            'AZURE_AI_PROJECTS_CONNECTION_STRING': 'Azure AI Foundry endpoint',
            'BING_GROUNDING_CONNECTION_ID': 'Bing Grounding connection ID',
            'BING_SEARCH_API_KEY': 'Bing Search API key'
        }
        
        all_good = True
        for var, description in required_vars.items():
            value = os.getenv(var)
            if value:
                logger.info(f"✅ {description}: {value[:50]}{'...' if len(value) > 50 else ''}")
            else:
                logger.error(f"❌ {description}: Not set")
                all_good = False
        
        self.results['environment_variables'] = all_good
        return all_good
    
    def test_azure_authentication(self):
        """Test 2: Azure Authentication"""
        logger.info("🧪 Test 2: Azure Authentication")
        
        try:
            credential = DefaultAzureCredential()
            logger.info("✅ DefaultAzureCredential created")
            
            # Test getting a token
            token = credential.get_token("https://ai.azure.com/.default")
            logger.info(f"✅ Access token obtained: {token.token[:20]}...")
            
            self.results['azure_authentication'] = True
            return True
            
        except Exception as e:
            logger.error(f"❌ Azure authentication failed: {e}")
            self.results['azure_authentication'] = False
            return False
    
    def test_ai_foundry_connectivity(self):
        """Test 3: AI Foundry Connectivity"""
        logger.info("🧪 Test 3: AI Foundry Connectivity")
        
        try:
            endpoint = os.getenv('AZURE_AI_PROJECTS_CONNECTION_STRING')
            project_endpoint = f"{endpoint}/api/projects/adnoc"
            
            logger.info(f"🔗 Project endpoint: {project_endpoint}")
            
            self.agents_client = AgentsClient(
                endpoint=project_endpoint,
                credential=DefaultAzureCredential()
            )
            
            logger.info("✅ Agents client created successfully")
            
            # Test listing agents
            agents = list(self.agents_client.list_agents(limit=5))
            logger.info(f"✅ Found {len(agents)} existing agents")
            
            self.results['ai_foundry_connectivity'] = True
            return True
            
        except Exception as e:
            logger.error(f"❌ AI Foundry connectivity failed: {e}")
            self.results['ai_foundry_connectivity'] = False
            return False
    
    def test_bing_grounding_tool_creation(self):
        """Test 4: Bing Grounding Tool Creation"""
        logger.info("🧪 Test 4: Bing Grounding Tool Creation")
        
        try:
            connection_id = os.getenv('BING_GROUNDING_CONNECTION_ID')
            
            if not connection_id:
                logger.error("❌ BING_GROUNDING_CONNECTION_ID not set")
                self.results['bing_grounding_tool_creation'] = False
                return False
            
            # Create Bing Grounding Tool
            bing_tool = BingGroundingTool(connection_id=connection_id)
            logger.info("✅ Bing Grounding Tool created successfully")
            
            self.results['bing_grounding_tool_creation'] = True
            return True
            
        except Exception as e:
            logger.error(f"❌ Bing Grounding Tool creation failed: {e}")
            self.results['bing_grounding_tool_creation'] = False
            return False
    
    def test_agent_creation_with_tools(self):
        """Test 5: Agent Creation with Bing Grounding Tool"""
        logger.info("🧪 Test 5: Agent Creation with Bing Grounding Tool")
        
        try:
            connection_id = os.getenv('BING_GROUNDING_CONNECTION_ID')
            bing_tool = BingGroundingTool(connection_id=connection_id)
            
            # Create agent with Bing Grounding Tool
            agent_name = f"test-agent-bing-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            # Create agent with Bing Grounding Tool using tool definition
            tool_definition = {
                "type": "bing_grounding",
                "bing_grounding": {
                    "search_configurations": [
                        {
                            "connection_id": connection_id
                        }
                    ]
                }
            }
            
            self.test_agent = self.agents_client.create_agent(
                model="gpt-4o",
                name=agent_name,
                instructions="You are a helpful assistant with access to real-time web search via Bing Grounding Tool.",
                tools=[tool_definition],
                temperature=0.0,
                top_p=1.0
            )
            
            logger.info(f"✅ Agent created successfully: {self.test_agent.id}")
            logger.info(f"🔧 Agent tools count: {len(self.test_agent.tools) if self.test_agent.tools else 0}")
            
            self.results['agent_creation_with_tools'] = True
            return True
            
        except Exception as e:
            logger.error(f"❌ Agent creation with tools failed: {e}")
            self.results['agent_creation_with_tools'] = False
            return False
    
    def test_basic_search_functionality(self):
        """Test 6: Basic Search Functionality"""
        logger.info("🧪 Test 6: Basic Search Functionality")
        
        if not self.test_agent:
            logger.error("❌ No test agent available")
            self.results['basic_search_functionality'] = False
            return False
        
        try:
            # Test with a simple search query
            test_question = "What is the current weather in Dubai?"
            
            logger.info(f"🔍 Testing search with: {test_question}")
            
            start_time = time.time()
            
            # Create thread and run
            run = self.agents_client.create_thread_and_process_run(
                agent_id=self.test_agent.id,
                thread={
                    "messages": [
                        {
                            "role": "user",
                            "content": test_question
                        }
                    ]
                }
            )
            
            logger.info(f"📝 Run created: {run.id}")
            
            # Wait for completion
            while run.status in ['queued', 'in_progress']:
                time.sleep(1)
                run = self.agents_client.get_run(thread_id=run.thread_id, run_id=run.id)
            
            total_time = time.time() - start_time
            logger.info(f"⏱️  Total time: {total_time:.2f}s")
            
            # Get response
            messages = self.agents_client.messages.list(thread_id=run.thread_id)
            
            assistant_message = None
            for message in messages:
                if message.role == "assistant":
                    assistant_message = message
                    break
            
            if assistant_message:
                # Extract response text
                full_response = ""
                if hasattr(assistant_message, 'content') and assistant_message.content:
                    if isinstance(assistant_message.content, list):
                        for content_item in assistant_message.content:
                            if hasattr(content_item, 'text') and hasattr(content_item.text, 'value'):
                                full_response = content_item.text.value
                                break
                    elif isinstance(assistant_message.content, str):
                        full_response = assistant_message.content
                
                logger.info(f"✅ Response received: {len(full_response)} characters")
                logger.info(f"📝 Response: {full_response}")
                
                # Check if it's using real-time search
                if "search" in full_response.lower() and ("issue" in full_response.lower() or "unable" in full_response.lower()):
                    logger.warning("⚠️  Response indicates search issues - may not be using real-time search")
                    self.results['basic_search_functionality'] = False
                    return False
                else:
                    logger.info("✅ Response appears to be from real-time search")
                    self.results['basic_search_functionality'] = True
                    return True
            else:
                logger.error("❌ No assistant response received")
                self.results['basic_search_functionality'] = False
                return False
                
        except Exception as e:
            logger.error(f"❌ Basic search functionality failed: {e}")
            self.results['basic_search_functionality'] = False
            return False
    
    def cleanup(self):
        """Clean up test resources"""
        logger.info("🧹 Cleaning up test resources...")
        
        try:
            if self.test_agent:
                self.agents_client.delete_agent(self.test_agent.id)
                logger.info("✅ Test agent deleted")
        except Exception as e:
            logger.warning(f"⚠️  Cleanup warning: {e}")
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        logger.info("🚀 Testing Azure AI Agents + Bing Search")
        logger.info("=" * 60)
        
        tests = [
            ("Environment Variables", self.test_environment_variables),
            ("Azure Authentication", self.test_azure_authentication),
            ("AI Foundry Connectivity", self.test_ai_foundry_connectivity),
            ("Bing Grounding Tool Creation", self.test_bing_grounding_tool_creation),
            ("Agent Creation with Tools", self.test_agent_creation_with_tools),
            ("Basic Search Functionality", self.test_basic_search_functionality)
        ]
        
        all_passed = True
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                if not result:
                    all_passed = False
            except Exception as e:
                logger.error(f"❌ {test_name} failed with exception: {e}")
                self.results[test_name.lower().replace(' ', '_')] = False
                all_passed = False
        
        # Cleanup
        self.cleanup()
        
        # Print summary
        logger.info("\n" + "=" * 60)
        logger.info("📊 TEST RESULTS SUMMARY")
        logger.info("=" * 60)
        
        for test_name, test_func in tests:
            test_key = test_name.lower().replace(' ', '_')
            status = "✅ PASS" if self.results.get(test_key, False) else "❌ FAIL"
            logger.info(f"{test_name}: {status}")
        
        logger.info("\n" + "=" * 60)
        if all_passed:
            logger.info("🎉 Azure AI Agents + Bing Search are working!")
        else:
            logger.info("⚠️  Some issues found. Please check the configuration.")
        
        return all_passed

def main():
    """Main function"""
    test = AzureAIBingTest()
    success = test.run_all_tests()
    
    if success:
        print("\n🎉 Azure AI Agents + Bing Search are working!")
        print("You can now run the main experiment.")
    else:
        print("\n❌ Azure AI Agents + Bing Search test failed!")
        print("Please fix the issues before running the main experiment.")

if __name__ == "__main__":
    main() 