import requests
import json

REST_API_KEY = "0de06958aa0be184ed0ce28cc0bb7e47"
REDIRECT_URI = "http://3.36.219.242:8000/oauth"
CODE = open("./secrets/token/code.txt", "r").read()

data = {
    "grant_type": "authorization_code",
    "client_id": REST_API_KEY,
    "redirect_uri": REDIRECT_URI,
    "code": CODE,
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
open("./secrets/json/code_response_body.json", "w").write(json.dumps(response_body, indent=2))

