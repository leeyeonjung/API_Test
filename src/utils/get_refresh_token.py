import requests
import json
from pathlib import Path

# 설정 파일 경로
BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = BASE_DIR / "secrets" / "json" / "kakao_config.json"

# 설정 파일 읽기
with open(CONFIG_PATH, encoding="utf-8") as f:
    config = json.load(f)

REST_API_KEY = config["client_id"]
REDIRECT_URI = config["redirect_uri"]
REFRESH_TOKEN = open("./secrets/token/refresh_token.txt", "r").read()

data = { 
    "grant_type": "refresh_token", 
    "client_id": REST_API_KEY, 
    "refresh_token": REFRESH_TOKEN
    }

res = requests.post("https://kauth.kakao.com/oauth/token", data=data)
response_body = res.json()

# access_token을 access_token.txt에 저장
if "access_token" in response_body:
    open("./secrets/token/access_token.txt", "w").write(response_body["access_token"])

# refresh_token이 있으면 refresh_token.txt에 저장
if "refresh_token" in response_body:
    open("./secrets/token/refresh_token.txt", "w").write(response_body["refresh_token"])

# 전체 응답을 response_body.json에 저장
open("./secrets/json/refresh_response_body.json", "w").write(json.dumps(response_body, indent=2))