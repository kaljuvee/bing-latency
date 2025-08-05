#!/bin/bash
# UAE Azure Setup Script for Bing Latency Experiments
# This script automates the creation of Azure resources in UAE region

set -e  # Exit on any error

echo "🇦🇪 UAE Azure Setup for Bing Latency Experiments"
echo "=================================================="

# Configuration
RESOURCE_GROUP_NAME="bing-latency-rg"
COGNITIVE_SERVICES_NAME="bing-latency-cognitive"
LOCATION="uaenorth"
SKU="S1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    print_error "Azure CLI is not installed. Please install it first:"
    echo "curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash"
    exit 1
fi

print_status "Azure CLI found"

# Check if user is logged in
if ! az account show &> /dev/null; then
    print_warning "You are not logged in to Azure. Please login first:"
    echo "az login"
    exit 1
fi

print_status "Logged in to Azure"

# Get current subscription
SUBSCRIPTION_NAME=$(az account show --query "name" -o tsv)
print_status "Using subscription: $SUBSCRIPTION_NAME"

# Create resource group
echo ""
echo "Creating resource group..."
if az group show --name $RESOURCE_GROUP_NAME &> /dev/null; then
    print_warning "Resource group '$RESOURCE_GROUP_NAME' already exists"
else
    az group create --name $RESOURCE_GROUP_NAME --location $LOCATION
    print_status "Resource group '$RESOURCE_GROUP_NAME' created in $LOCATION"
fi

# Create Cognitive Services resource
echo ""
echo "Creating Cognitive Services resource..."
if az cognitiveservices account show --name $COGNITIVE_SERVICES_NAME --resource-group $RESOURCE_GROUP_NAME &> /dev/null; then
    print_warning "Cognitive Services resource '$COGNITIVE_SERVICES_NAME' already exists"
else
    az cognitiveservices account create \
        --name $COGNITIVE_SERVICES_NAME \
        --resource-group $RESOURCE_GROUP_NAME \
        --kind "Bing.Search.v7" \
        --sku $SKU \
        --location $LOCATION \
        --yes
    
    print_status "Cognitive Services resource '$COGNITIVE_SERVICES_NAME' created"
fi

# Get credentials
echo ""
echo "Retrieving credentials..."

# Get subscription key
SUBSCRIPTION_KEY=$(az cognitiveservices account keys list \
    --name $COGNITIVE_SERVICES_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --query "key1" \
    --output tsv)

# Get endpoint
ENDPOINT=$(az cognitiveservices account show \
    --name $COGNITIVE_SERVICES_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --query "properties.endpoint" \
    --output tsv)

print_status "Credentials retrieved successfully"

# Create .env file
echo ""
echo "Creating .env file..."
if [ -f .env ]; then
    print_warning ".env file already exists. Backing up to .env.backup"
    cp .env .env.backup
fi

cat > .env << EOF
# Azure Cognitive Services Configuration for UAE
# Generated on $(date)

# Your Azure Cognitive Services subscription key
AZURE_COGNITIVE_SERVICES_KEY=$SUBSCRIPTION_KEY

# Your Azure Cognitive Services endpoint URL
AZURE_COGNITIVE_SERVICES_ENDPOINT=$ENDPOINT

# Azure region
AZURE_REGION=$LOCATION
EOF

print_status ".env file created with your credentials"

# Display summary
echo ""
echo "🎉 UAE Azure Setup Complete!"
echo "============================"
echo "Resource Group: $RESOURCE_GROUP_NAME"
echo "Cognitive Services: $COGNITIVE_SERVICES_NAME"
echo "Location: $LOCATION"
echo "SKU: $SKU"
echo "Endpoint: $ENDPOINT"
echo "Key: ${SUBSCRIPTION_KEY:0:8}...${SUBSCRIPTION_KEY: -4}"

echo ""
print_status "Next steps:"
echo "1. Install Python dependencies: pip install -r requirements.txt"
echo "2. Edit tests/custom_prompts.py with your 3 prompts"
echo "3. Test your setup: python tests/test_setup.py"
echo "4. Run your experiment: python tests/run_custom_experiment.py"

echo ""
print_warning "Important: Keep your .env file secure and never commit it to version control!"

echo ""
echo "To clean up resources when done:"
echo "az group delete --name $RESOURCE_GROUP_NAME --yes" 