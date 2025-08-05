#!/usr/bin/env python3
"""
Prompt Loader Utility
Loads prompts from markdown files in the prompts directory.
"""

import os
import re
from typing import List, Dict, Any
from pathlib import Path

class PromptLoader:
    """Utility class to load prompts from markdown files."""
    
    def __init__(self, prompts_dir: str = "prompts"):
        """
        Initialize the prompt loader.
        
        Args:
            prompts_dir: Directory containing markdown prompt files
        """
        self.prompts_dir = Path(prompts_dir)
        
    def load_prompts_from_markdown(self, filename: str) -> List[str]:
        """
        Load prompts from a markdown file.
        
        Args:
            filename: Name of the markdown file (e.g., 'bing_grounding_main.md')
            
        Returns:
            List of prompts extracted from the markdown file
        """
        file_path = self.prompts_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
        
        prompts = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract prompts using regex pattern
        # Look for lines that start with "- " (both with and without question marks)
        prompt_pattern = r'^\s*-\s*(.+?)(?:\?|\.)?\s*$'
        matches = re.findall(prompt_pattern, content, re.MULTILINE)
        
        for match in matches:
            prompt = match.strip()
            if prompt:
                # Add question mark if not present
                if not prompt.endswith('?'):
                    prompt += '?'
                prompts.append(prompt)
        
        return prompts
    
    def load_prompts_from_csv(self, filename: str) -> List[Dict[str, Any]]:
        """
        Load prompts from a CSV file.
        
        Args:
            filename: Name of the CSV file (e.g., 'bing-prompts.csv')
            
        Returns:
            List of dictionaries containing prompt data
        """
        import pandas as pd
        
        file_path = self.prompts_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
        
        df = pd.read_csv(file_path)
        prompts = []
        
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
        
        return prompts
    
    def load_all_prompts(self) -> List[Dict[str, Any]]:
        """
        Load all prompts from both CSV and markdown files.
        
        Returns:
            List of dictionaries containing all prompt data
        """
        all_prompts = []
        
        # Load prompts from CSV file
        try:
            csv_prompts = self.load_prompts_from_csv('bing-prompts.csv')
            all_prompts.extend(csv_prompts)
            print(f"Loaded {len(csv_prompts)} prompts from CSV")
        except Exception as e:
            print(f"Warning: Could not load prompts from CSV: {e}")
        
        # Load prompts from markdown file
        try:
            md_prompts = self.load_prompts_from_markdown('long_prompt.md')
            # Convert markdown prompts to the same format as CSV prompts
            for prompt in md_prompts:
                all_prompts.append({
                    'question': prompt,
                    'current_response_time': '15.0s',  # Estimated baseline
                    'expected_behavior': 'Should provide real-time search results with citations'
                })
            print(f"Loaded {len(md_prompts)} prompts from markdown")
        except Exception as e:
            print(f"Warning: Could not load prompts from markdown: {e}")
        
        return all_prompts
    
    def get_available_prompt_files(self) -> List[str]:
        """
        Get list of available markdown prompt files.
        
        Returns:
            List of markdown filenames
        """
        if not self.prompts_dir.exists():
            return []
        
        markdown_files = []
        for file_path in self.prompts_dir.glob("*.md"):
            if file_path.name != "README.md":  # Exclude README
                markdown_files.append(file_path.name)
        
        return sorted(markdown_files)
    
    def load_all_prompt_sets(self) -> Dict[str, List[str]]:
        """
        Load all available prompt sets from markdown files.
        
        Returns:
            Dictionary mapping filename to list of prompts
        """
        prompt_sets = {}
        
        for filename in self.get_available_prompt_files():
            try:
                prompts = self.load_prompts_from_markdown(filename)
                # Remove .md extension for key name
                key = filename.replace('.md', '')
                prompt_sets[key] = prompts
            except Exception as e:
                print(f"Warning: Could not load prompts from {filename}: {e}")
        
        return prompt_sets
    
    def get_prompt_set_info(self) -> Dict[str, Any]:
        """
        Get information about all available prompt sets.
        
        Returns:
            Dictionary with prompt set information
        """
        prompt_sets = self.load_all_prompt_sets()
        
        info = {
            'total_sets': len(prompt_sets),
            'total_prompts': sum(len(prompts) for prompts in prompt_sets.values()),
            'sets': {}
        }
        
        for set_name, prompts in prompt_sets.items():
            info['sets'][set_name] = {
                'count': len(prompts),
                'prompts': prompts
            }
        
        return info

def get_bing_grounding_prompts_v2() -> List[str]:
    """
    Convenience function to get the main Bing Grounding prompts.
    
    Returns:
        List of main Bing Grounding prompts
    """
    loader = PromptLoader()
    return loader.load_prompts_from_markdown('bing_grounding_main.md')

def get_business_financial_prompts() -> List[str]:
    """
    Convenience function to get business and financial prompts.
    
    Returns:
        List of business and financial prompts
    """
    loader = PromptLoader()
    return loader.load_prompts_from_markdown('business_financial.md')

def get_technology_innovation_prompts() -> List[str]:
    """
    Convenience function to get technology and innovation prompts.
    
    Returns:
        List of technology and innovation prompts
    """
    loader = PromptLoader()
    return loader.load_prompts_from_markdown('technology_innovation.md')

def get_healthcare_science_prompts() -> List[str]:
    """
    Convenience function to get healthcare and science prompts.
    
    Returns:
        List of healthcare and science prompts
    """
    loader = PromptLoader()
    return loader.load_prompts_from_markdown('healthcare_science.md')

def get_regional_uae_prompts() -> List[str]:
    """
    Convenience function to get regional UAE prompts.
    
    Returns:
        List of regional UAE prompts
    """
    loader = PromptLoader()
    return loader.load_prompts_from_markdown('regional_uae.md')

if __name__ == "__main__":
    # Test the prompt loader
    loader = PromptLoader()
    
    print("Available prompt files:")
    print("=" * 40)
    for filename in loader.get_available_prompt_files():
        print(f"- {filename}")
    
    print("\nPrompt set information:")
    print("=" * 40)
    info = loader.get_prompt_set_info()
    print(f"Total sets: {info['total_sets']}")
    print(f"Total prompts: {info['total_prompts']}")
    
    print("\nDetailed breakdown:")
    print("-" * 40)
    for set_name, set_info in info['sets'].items():
        print(f"{set_name}: {set_info['count']} prompts")
        for i, prompt in enumerate(set_info['prompts'], 1):
            print(f"  {i}. {prompt}")
        print() 