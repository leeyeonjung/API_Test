# src/utils/code_to_token.py

# Standard library
import json  # JSON 처리
from pathlib import Path  # 경로 조작

# Third-party library
import requests  # HTTP 요청

# Project root directory path setting
BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = BASE_DIR / "secrets" / "json" / "kakao_config.json"  # 설정 파일 경로

# 설정 파일 읽기
with open(CONFIG_PATH, encoding="utf-8") as f:
    config = json.load(f)

# 설정 파일에서 API 키 및 리다이렉트 URI 읽기
REST_API_KEY = config["client_id"]  # REST API 키 (client_id)
REDIRECT_URI = config["redirect_uri"]  # 리다이렉트 URI

# Authorization Code 파일에서 읽기
CODE = open("./secrets/token/code.txt", "r").read()

# 토큰 발급 요청 데이터 구성
data = {
    "grant_type": "authorization_code",  # OAuth grant type
    "client_id": REST_API_KEY,  # 클라이언트 ID
    "redirect_uri": REDIRECT_URI,  # 리다이렉트 URI (인증 URL 생성 시 사용한 것과 동일해야 함)
    "code": CODE,  # Authorization Code
}

# 카카오 OAuth API 호출 (Code → Token 변환)
res = requests.post("https://kauth.kakao.com/oauth/token", data=data)

# 응답 JSON 파싱
response_body = res.json()

# access_token을 access_token.txt에 저장
if "access_token" in response_body:
    open("./secrets/token/access_token.txt", "w").write(response_body["access_token"])

# refresh_token이 있으면 refresh_token.txt에 저장
if "refresh_token" in response_body:
    open("./secrets/token/refresh_token.txt", "w").write(response_body["refresh_token"])

# 전체 응답을 JSON 파일로 저장 (디버깅 및 로그 목적)
open("./secrets/json/code_response_body.json", "w").write(json.dumps(response_body, indent=2))

