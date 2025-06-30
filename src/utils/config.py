import yaml
from pathlib import Path

def load_config(config_file='config/settings.yaml'):
    """Load configuration from YAML file"""
    config_path = Path(__file__).parent.parent / config_file
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}