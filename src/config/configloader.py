import yaml
import os
from datetime import date, timedelta


def load_config() -> dict:
    # Combine settings.yaml + secrets.yaml into one config dict
    base_dir = os.path.dirname(os.path.abspath(__file__))

    settings_path = os.path.join(base_dir, "settings.yaml")
    secrets_path  = os.path.join(base_dir, "secrets.yaml")

    with open(settings_path, "r") as f:
        config = yaml.safe_load(f)

    with open(secrets_path, "r") as f:
        secrets = yaml.safe_load(f)

    config["api_keys"]    = secrets.get("api_keys", {})
    config["target_date"] = (date.today() - timedelta(days=1)).isoformat()

    return config
