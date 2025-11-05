# src/utils/make_url.py

# Standard library
import json  # JSON 파일 읽기
from pathlib import Path  # Path 조작

# Project root directory path setting
BASE_DIR = Path(__file__).resolve().parents[2]  # src/utils/make_url.py -> api_Test/
CONFIG_PATH = BASE_DIR / "secrets" / "json" / "kakao_config.json"  # Configuration file path

# Configuration file reading
with open(CONFIG_PATH, encoding="utf-8") as f:
    cfg = json.load(f)

# 인증 URL 생성 (카카오 OAuth 인증 URL)
AUTH_URL = (
    f"{cfg['authorize_url']}?"
    f"client_id={cfg['client_id']}&"
    f"redirect_uri={cfg['redirect_uri']}&"
    f"response_type=code&"
    f"scope={cfg['scopes']}"
)

# 콘솔에 URL 출력
print(AUTH_URL)

# URL을 파일로 저장
open("./secrets/url/authorize_url.txt", "w").write(AUTH_URL)