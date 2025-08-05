# Azure Resources Setup Guide for Bing Latency Experiments

This guide will help you set up the necessary Azure resources to run Bing latency experiments with Azure Cognitive Services.

## Prerequisites

1. **Azure Account**: You need an active Azure subscription
2. **Azure CLI**: Install Azure CLI on your system
3. **Python**: Python 3.8 or higher
4. **Git**: For cloning and managing the project

## Step 1: Install Azure CLI

### On Ubuntu/Debian:
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### On macOS:
```bash
brew install azure-cli
```

### On Windows:
Download and install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows

## Step 2: Login to Azure

```bash
az login
```

This will open a browser window for authentication. After successful login, you'll see your subscription information.

## Step 3: Set Your Subscription (if you have multiple)

List your subscriptions:
```bash
az account list --output table
```

Set your active subscription:
```bash
az account set --subscription "Your-Subscription-Name"
```

## Step 4: Create a Resource Group

```bash
# Create a resource group in UAE region
az group create --name "bing-latency-rg" --location "uaenorth"

# Alternative regions you might prefer:
# --location "uaesouth" (UAE Central)
# --location "westeurope" (West Europe)
# --location "southeastasia" (Southeast Asia)
```

## Step 5: Create Azure Cognitive Services Resource

```bash
# Create a Cognitive Services resource
az cognitiveservices account create \
    --name "bing-latency-cognitive" \
    --resource-group "bing-latency-rg" \
    --kind "Bing.Search.v7" \
    --sku "S1" \
    --location "uaenorth" \
    --yes
```

**Note**: The `Bing.Search.v7` kind provides access to Bing Search APIs including web search, news search, and more.

## Step 6: Get Your Credentials

### Get the subscription key:
```bash
az cognitiveservices account keys list \
    --name "bing-latency-cognitive" \
    --resource-group "bing-latency-rg" \
    --query "key1" \
    --output tsv
```

### Get the endpoint:
```bash
az cognitiveservices account show \
    --name "bing-latency-cognitive" \
    --resource-group "bing-latency-rg" \
    --query "properties.endpoint" \
    --output tsv
```

## Step 7: Configure Environment Variables

Create a `.env` file in your project root:

```bash
cp env.example .env
```

Edit the `.env` file with your actual credentials:

```bash
# Replace with your actual values from Step 6
AZURE_COGNITIVE_SERVICES_KEY=your_actual_subscription_key_here
AZURE_COGNITIVE_SERVICES_ENDPOINT=https://bing-latency-cognitive.cognitiveservices.azure.com/
AZURE_REGION=uaenorth
```

## Step 8: Install Python Dependencies

```bash
# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 9: Test Your Setup

Run a quick test to verify everything is working:

```bash
python tests/bing_latency_experiment.py
```

## Step 10: Customize Your Prompts

Edit `tests/custom_prompts.py` to define your 3 prompts:

```python
CUSTOM_PROMPTS = [
    "Your first prompt here",
    "Your second prompt here", 
    "Your third prompt here"
]
```

## Step 11: Run the Experiment

```bash
# Run the experiment with default prompts
python tests/bing_latency_experiment.py

# Or run with custom prompts (modify the script to import from custom_prompts.py)
```

## Monitoring and Cleanup

### Monitor Resource Usage:
```bash
# Check resource usage
az cognitiveservices account show \
    --name "bing-latency-cognitive" \
    --resource-group "bing-latency-rg"
```

### View Logs:
```bash
# View experiment logs
tail -f logs/experiment.log
```

### Cleanup (when done):
```bash
# Delete the resource group (this will delete all resources)
az group delete --name "bing-latency-rg" --yes
```

## Troubleshooting

### Common Issues:

1. **Authentication Error**: Run `az login` again
2. **Resource Not Found**: Check resource group and resource names
3. **Rate Limiting**: The script includes delays, but you might need to increase them
4. **Permission Denied**: Ensure your account has Contributor or Owner role on the subscription

### Check Resource Status:
```bash
# List all cognitive services in your subscription
az cognitiveservices account list --output table

# Check specific resource
az cognitiveservices account show \
    --name "bing-latency-cognitive" \
    --resource-group "bing-latency-rg"
```

### Cost Management:
- S1 tier costs approximately $3 per 1000 transactions
- Monitor usage in Azure Portal under Cost Management
- Consider using F0 (free) tier for testing (limited to 3 calls per minute)

## Security Best Practices

1. **Never commit credentials**: The `.env` file is in `.gitignore`
2. **Use Managed Identity**: For production, consider using Azure Managed Identity
3. **Network Security**: Consider adding network restrictions if needed
4. **Regular Rotation**: Rotate keys periodically

## Next Steps

After running the experiment, check the `logs/` folder for:
- `experiment.log`: Detailed execution log
- `bing_latency_results_*.json`: Raw results data
- `bing_latency_report_*.csv`: Processed results
- `bing_latency_visualization_*.png`: Performance charts

The experiment will provide comprehensive latency analysis including:
- Average, minimum, and maximum latency per prompt
- Success rates and error counts
- Statistical analysis and visualizations
- Trend analysis over time 