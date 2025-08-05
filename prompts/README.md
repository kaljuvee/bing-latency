# Bing Grounding Search Prompts

This directory contains markdown files with optimized prompts for testing Bing Grounding Search capabilities. Each file contains a set of prompts focused on specific domains or use cases.

## Available Prompt Sets

### 1. `bing_grounding_main.md`
**Primary prompts for general Bing Grounding Search testing**
- Current events and news
- Market and financial data
- Company initiatives and sustainability
- Technology trends
- Scientific developments

### 2. `business_financial.md`
**Business and financial market focused prompts**
- Quarterly earnings and financial results
- Cryptocurrency and digital assets
- Mergers and acquisitions
- Economic indicators
- ESG and sustainable finance

### 3. `technology_innovation.md`
**Technology and innovation focused prompts**
- Artificial intelligence and machine learning
- Cloud computing and edge computing
- Quantum computing research
- Cybersecurity and data protection
- 5G and telecommunications

### 4. `healthcare_science.md`
**Healthcare and scientific research focused prompts**
- COVID-19 research and treatments
- Personalized medicine and genomics
- Renewable energy storage
- Climate change research
- Space exploration and satellite technology

### 5. `regional_uae.md`
**Regional UAE and Middle East focused prompts**
- UAE renewable energy projects
- Middle East technology investments
- Dubai smart city initiatives
- Middle East fintech and digital banking
- Abu Dhabi economic diversification

## Usage

### Loading Prompts in Python

```python
from prompts.prompt_loader import PromptLoader

# Load a specific prompt set
loader = PromptLoader()
main_prompts = loader.load_prompts_from_markdown('bing_grounding_main.md')

# Or use convenience functions
from prompts.prompt_loader import get_bing_grounding_prompts_v2
prompts = get_bing_grounding_prompts_v2()
```

### Available Convenience Functions

- `get_bing_grounding_prompts_v2()` - Main prompts
- `get_business_financial_prompts()` - Business/financial prompts
- `get_technology_innovation_prompts()` - Technology prompts
- `get_healthcare_science_prompts()` - Healthcare/science prompts
- `get_regional_uae_prompts()` - Regional UAE prompts

### Testing the Prompt Loader

```bash
python prompts/prompt_loader.py
```

This will show all available prompt sets and their contents.

## Prompt Format

Each prompt in the markdown files follows this format:

```markdown
- What is the current state of [topic]?
```

Prompts are designed to:
- Require real-time information
- Test different types of queries
- Cover diverse topics and domains
- Generate meaningful search results

## Adding New Prompts

To add new prompts:

1. Create a new markdown file or edit an existing one
2. Use the format: `- [Your question here?]`
3. Ensure the question requires current information
4. Test with the prompt loader utility

## Best Practices

- Keep prompts focused and specific
- Ensure they require current information
- Test prompts before using in experiments
- Use diverse topics to test different search capabilities
- Include regional variations when relevant 