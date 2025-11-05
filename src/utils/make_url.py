import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = BASE_DIR / "secrets" / "json" / "kakao_config.json"

with open(CONFIG_PATH, encoding="utf-8") as f:
    cfg = json.load(f)

AUTH_URL = (
    f"{cfg['authorize_url']}?"
    f"client_id={cfg['client_id']}&"
    f"redirect_uri={cfg['redirect_uri']}&"
    f"response_type=code&"
    f"scope={cfg['scopes']}"
)

print(AUTH_URL)

open("./secrets/url/authorize_url.txt", "w").write(AUTH_URL)