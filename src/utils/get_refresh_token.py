# src/utils/get_refresh_token.py

# Standard library
import json  # JSON 처리
from pathlib import Path  # 경로 조작

# Third-party library
import requests  # HTTP 요청

# Project root directory path setting
BASE_DIR = Path(__file__).resolve().parents[2]  # src/utils/get_refresh_token.py -> api_Test/
CONFIG_PATH = BASE_DIR / "secrets" / "json" / "kakao_config.json"  # 설정 파일 경로

# 설정 파일 읽기
with open(CONFIG_PATH, encoding="utf-8") as f:
    config = json.load(f)

# 설정 파일에서 API 키 및 리다이렉트 URI 읽기
REST_API_KEY = config["client_id"]  # REST API 키 (client_id)
REDIRECT_URI = config["redirect_uri"]  # 리다이렉트 URI

# Refresh Token 파일에서 읽기
REFRESH_TOKEN = open("./secrets/token/refresh_token.txt", "r").read()

# 토큰 갱신 요청 데이터 구성
data = { 
    "grant_type": "refresh_token",  # OAuth grant type
    "client_id": REST_API_KEY,  # 클라이언트 ID
    "refresh_token": REFRESH_TOKEN  # Refresh Token
}

# 카카오 OAuth API 호출 (토큰 갱신)
res = requests.post("https://kauth.kakao.com/oauth/token", data=data)
response_body = res.json()

# access_token을 access_token.txt에 저장
if "access_token" in response_body:
    open("./secrets/token/access_token.txt", "w").write(response_body["access_token"])

# refresh_token이 있으면 refresh_token.txt에 저장 (새로운 Refresh Token이 발급될 수 있음)
if "refresh_token" in response_body:
    open("./secrets/token/refresh_token.txt", "w").write(response_body["refresh_token"])

# 전체 응답을 JSON 파일로 저장 (디버깅 및 로그 목적)
open("./secrets/json/refresh_response_body.json", "w").write(json.dumps(response_body, indent=2))