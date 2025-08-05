# Bing Latency Experiments

A comprehensive tool for testing and analyzing Bing search API latency with Azure Cognitive Services. This project allows you to run controlled experiments with custom prompts and generates detailed performance reports with visualizations.

## Features

- **Dual Approach Support**: 
  - Standard Azure Cognitive Services Bing Search API
  - Azure AI Projects with Bing Grounding Tool
- **Latency Testing**: Measure response times for Bing search queries
- **Custom Prompts**: Test with your own 3 prompts
- **Comprehensive Logging**: Detailed logs and performance metrics
- **Data Visualization**: Generate charts and reports automatically
- **Azure Integration**: Seamless integration with Azure services
- **Statistical Analysis**: Calculate averages, min/max, standard deviation
- **UAE Region Support**: Optimized for UAE Azure regions

## Project Structure

```
bing-latency/
├── tests/
│   ├── experiment_1_basic_latency.py           # Experiment 1: Basic latency testing
│   ├── experiment_2_system_prompt_optimization.py # Experiment 2: System prompt optimization
│   ├── experiment_3_concurrent_optimization.py  # Experiment 3: Concurrent optimization
│   ├── run_all_experiments.py                  # Master script to run all experiments
│   ├── bing_latency_experiment.py              # Legacy: Standard Bing Search API experiment
│   ├── bing_grounding_experiment.py            # Legacy: Azure AI Projects + Bing Grounding Tool
│   ├── custom_prompts.py                       # Prompts for standard Bing Search API
│   ├── bing_grounding_prompts.py               # Prompts for Bing Grounding Tool
│   ├── run_custom_experiment.py                # Run standard experiment with custom prompts
│   ├── test_setup.py                           # Test standard setup
│   └── test_bing_grounding_setup.py            # Test Bing Grounding Tool setup
├── logs/                                       # Experiment results and logs
├── requirements.txt                            # Python dependencies
├── env.example                                 # Environment variables template
├── setup_azure_resources.md                    # Azure setup guide
└── README.md                                   # This file
```

## Quick Start

### 1. Prerequisites

- Azure subscription
- Azure CLI installed
- Python 3.8+
- Git

### 2. Setup Azure Resources (UAE Region)

**Option A: Automated Setup (Recommended)**
```bash
# Run the UAE-specific setup script
./setup_uae_azure.sh
```

**Option B: Manual Setup**
Follow the detailed guide in [setup_azure_resources.md](setup_azure_resources.md) to:
- Install Azure CLI
- Create Azure Cognitive Services resource in UAE region
- Get your credentials

### 3. Configure Environment

```bash
# Copy environment template
cp env.example .env

# Edit .env with your Azure credentials
nano .env
```

### 4. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Choose Your Approach

**Option A: Run All Three Optimization Experiments (Recommended)**
```bash
# Run all three experiments in sequence
python tests/run_all_experiments.py
```

**Option B: Run Individual Experiments**
```bash
# Experiment 1: Basic latency testing
python tests/experiment_1_basic_latency.py

# Experiment 2: System prompt optimization
python tests/experiment_2_system_prompt_optimization.py

# Experiment 3: Concurrent optimization
python tests/experiment_3_concurrent_optimization.py
```

**Option C: Legacy Approaches**
```bash
# Standard Bing Search API
python tests/run_custom_experiment.py

# Azure AI Projects + Bing Grounding Tool
python tests/bing_grounding_experiment.py
```

## Output Files

After running the experiments, check the `logs/` folder for:

**Three Optimization Experiments:**
- **`experiment_1_basic_latency_*.log`**: Basic latency testing logs
- **`experiment_2_system_prompt_optimization_*.log`**: System prompt optimization logs
- **`experiment_3_concurrent_optimization_*.log`**: Concurrent optimization logs
- **`all_experiments_master.log`**: Master experiment runner logs
- **`comprehensive_results_YYYYMMDD_HHMMSS.json`**: All experiments combined results
- **`comprehensive_visualization_YYYYMMDD_HHMMSS.png`**: Comprehensive comparison charts

**Individual Experiment Results:**
- **`experiment_1_basic_latency_results_*.json`**: Basic latency raw results
- **`experiment_2_system_prompt_optimization_results_*.json`**: System prompt optimization results
- **`experiment_3_concurrent_optimization_results_*.json`**: Concurrent optimization results
- **`experiment_*_report_*.csv`**: Processed results for each experiment
- **`experiment_*_visualization_*.png`**: Performance charts for each experiment

**Legacy Approaches:**
- **`experiment.log`**: Standard Bing Search API logs
- **`bing_grounding_experiment.log`**: Bing Grounding Tool logs

## Sample Output

The experiment generates comprehensive reports including:

```
==================================================
EXPERIMENT SUMMARY
==================================================
Total prompts tested: 3
Total searches performed: 15
Total successful searches: 15
Total errors: 0
Overall success rate: 100.00%

Latency Statistics:
Overall average latency: 245.67ms
Fastest average: 198.45ms
Slowest average: 312.89ms
Latency standard deviation: 45.23ms

Per-Prompt Results:
Prompt 1: 198.45ms avg, 0 errors
Prompt 2: 225.78ms avg, 0 errors
Prompt 3: 312.89ms avg, 0 errors
```

## Configuration Options

### Environment Variables

- `AZURE_COGNITIVE_SERVICES_KEY`: Your Azure subscription key
- `AZURE_COGNITIVE_SERVICES_ENDPOINT`: Your Azure endpoint URL
- `AZURE_REGION`: Azure region (optional)

### Experiment Parameters

You can modify the experiment parameters in `tests/bing_latency_experiment.py`:

- `search_count`: Number of searches per prompt (default: 5)
- Delay between requests (default: 1 second)
- Delay between different prompts (default: 2 seconds)

## Cost Considerations

- **S1 Tier**: ~$3 per 1000 transactions (UAE pricing may vary)
- **F0 Tier**: Free, but limited to 3 calls per minute
- Monitor usage in Azure Portal under Cost Management

## Troubleshooting

### Common Issues

1. **Authentication Error**: Run `az login` again
2. **Resource Not Found**: Check resource names in Azure
3. **Rate Limiting**: Increase delays between requests
4. **Permission Denied**: Ensure proper Azure role assignments

### Getting Help

- Check the detailed setup guide: [setup_azure_resources.md](setup_azure_resources.md)
- Review logs in the `logs/` folder
- Monitor Azure resource usage via Azure Portal

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Azure documentation
3. Open an issue on GitHub

---

**Note**: This tool is designed for research and testing purposes. Please ensure compliance with Azure's terms of service and rate limits when running experiments.