# Azure AI Agents + Bing Search Test

This folder contains a simple test to verify if Azure AI Agents with Bing Search are working correctly.

## Test File

### `test_end_to_end_setup.py` ⭐ **MAIN TEST**
- **Simple test for Azure AI Agents + Bing Search**
- Tests all essential aspects:
  - Environment variables
  - Azure authentication
  - AI Foundry connectivity
  - Bing Grounding Tool creation
  - Agent creation with tools
  - Basic search functionality
- Creates a test agent with Bing Grounding Tool
- Performs a real search test
- Cleans up test resources

## How to Use

### Run the Test
```bash
cd setup
python test_end_to_end_setup.py
```

## Prerequisites

Before running the test, ensure:

1. **Environment Variables**: `env.local` file is configured with:
   - `AZURE_AI_PROJECTS_CONNECTION_STRING`
   - `BING_GROUNDING_CONNECTION_ID`
   - `BING_SEARCH_API_KEY`

2. **Azure CLI**: Logged in with `az login`

3. **Python Environment**: Virtual environment activated with dependencies installed

## Expected Results

### ✅ Success Indicators
- All environment variables are set
- Azure authentication works
- AI Foundry connectivity is established
- Bing Grounding Tool can be created
- Agent with tools can be created
- Real-time search functionality works

### ❌ Common Issues
- Missing environment variables
- Authentication failures
- Connection ID not found
- Agent creation failures
- Search tool not working

## Next Steps

After the test passes:

1. ✅ Azure AI Agents + Bing Search are working
2. 🚀 Run the main experiment: `python tests/bing_grounding_experiment.py`
3. 📊 Review results in the `logs/` folder

## Notes

- The test creates a temporary agent for testing
- Test agent is automatically cleaned up
- Test includes detailed logging for debugging 