# src/utils/config.py

import yaml
import os

def load_yaml(filename: str) -> dict:
    """
    Load a YAML file from the project’s config/ folder.
    Returns the parsed dict.
    """
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config"))
    path = os.path.join(base, filename)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_site_config(site_name: str) -> dict:
    """
    Fetch the config for a given site (e.g. "amazon", "ebay", "aliexpress").
    Looks inside scrappers.yaml.
    """
    cfg = load_yaml("scrappers.yaml")
    return cfg.get(site_name, {})
