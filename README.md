# 🧪 Kakao API Test

카카오 Open REST API 기반으로
인증(OAuth 2.0), 테스트 데이터 생성, 메시지 전송 과정을 자동화한 테스트 프로젝트입니다.
- **Open REST API:** Kakao Developers의 사용자 정보, 친구 목록, 메시지 전송 API를 활용  
- **OAuth 2.0 인증:** Authorization Code Grant로 Access/Refresh Token 자동 관리  
- **Test Data 생성:** 실행 시마다 자동으로 메시지 본문 생성 (`generate_message_payload()`)

---

## 🌐 Open REST API

Kakao Developers의 다음 Open REST API를 활용하였습니다:

- 사용자 정보 조회 (`/v2/user/me`)
- Access Token 정보 조회 (`/v1/user/access_token_info`)
- 친구 목록 조회 (`/v1/api/talk/friends`)
- 카카오톡 프로필 조회 (`/v1/api/talk/profile`)
- 나에게 메시지 보내기 (`/v2/api/talk/memo/default/send`, `/v2/api/talk/memo/send`)

---

## 🔐 OAuth 2.0 인증

Authorization Code Grant 방식을 사용하여 **인가 코드(code)**를 발급받고,  
Access Token / Refresh Token을 생성해 **파일로 저장**합니다.  

pytest 실행 시에는 아래 우선순위에 따라 자동으로 토큰을 읽어 API 호출에 사용됩니다.

1. CLI 인자 (`--access-token`)
2. 환경변수 (`ACCESS_TOKEN`)
3. 파일 (`secrets/token/access_token.txt`)
4. Refresh Token 자동 갱신 (`get_refresh_token.py` 실행)

이 과정을 통해 테스트 실행 시 별도의 수동 로그인 없이 **자동 인증 흐름**이 완성됩니다.

---

## 🧩 Test Data 생성

테스트 실행 시마다 메시지 내용을 **타임스탬프 + 랜덤 문자열**로 자동 생성하는  
`generate_message_payload()`를 구현했습니다.

- 매 테스트마다 다른 데이터가 생성됨
- 동일 API에 대해 **다양한 입력값을 반복 테스트** 가능  
- 자동으로 생성된 메시지는 카카오톡 “나와의 채팅방”으로 전송되어 **실제 전송 결과를 검증**

또한, 별도 유틸 스크립트에서 테스트용 토큰(`access_token`, `refresh_token`)을  
자동으로 생성 및 갱신하여 **수동 설정 없이도 재현 가능한 테스트 환경**을 구축했습니다.

---

## 📁 프로젝트 구조

```
api_Test/
├── conftest.py                               # pytest 설정 및 fixture 정의
├── src/
│   ├── services/
│   │   ├── api_clients.py                    # Kakao API 클라이언트 (API 호출 함수)
│   │   └── test_data_generator.py            # 테스트 데이터 자동 생성 유틸리티
│   └── utils/
│       ├── code_to_token.py                  # Code → Token 변환 스크립트
│       ├── get_refresh_token.py              # Refresh Token으로 새 Token 발급
│       └── make_url.py                       # 인증 URL 생성 스크립트
├── testcase/
│   └── test_api.py                           # 테스트 케이스 (pytest)
└── secrets/                                  # 토큰 및 url 저장 폴더 (Git 제외)
    ├── url/
    │   └── authorize_url.txt                 # 생성된 인증 URL
    ├── token/
    │   ├── access_token.txt                  # Access Token
    │   ├── refresh_token.txt                 # Refresh Token
    │   └── code.txt                          # Authorization Code
    └── json/
        ├── kakao_config.json                 # API 설정 파일 (client_id, redirect_uri 등)
        ├── code_response_body.json           # Code → Token 응답
        └── refresh_response_body.json        # Refresh Token 응답
```

---

## 🚀 시작하기

### 0️⃣ 설정 파일 작성 (`kakao_config.json`)

`secrets/json/kakao_config.json` 파일에 카카오 API 설정 정보를 작성합니다:

```json
{
    "client_id": "YOUR_CLIENT_ID_HERE",
    "redirect_uri": "http://localhost:8000/oauth",
    "scopes": "talk_message,friends,profile_nickname,profile_image",
    "authorize_url": "https://kauth.kakao.com/oauth/authorize",
    "token_url": "https://kauth.kakao.com/oauth/token"
}
```

- 이 파일은 `.gitignore`에 포함되어 Git에 업로드되지 않습니다.
- `client_id`는 Kakao Developers의 REST API 키입니다.
- `code_to_token.py`, `get_refresh_token.py` 스크립트에서 자동으로 이 파일의 설정을 사용합니다.

---

### 1️⃣ Code 발급
```bash
python src/utils/make_url.py
```
- 콘솔에 출력된 URL을 열어 카카오 로그인 → `code`를 확인  
- URL은 `secrets/url/authorize_url.txt`에 자동 저장

---

### 2️⃣ Code → Token 변환
```bash
python src/utils/code_to_token.py
```
- `secrets/token/` 경로에 아래 파일이 자동 생성:
  - `access_token.txt`
  - `refresh_token.txt`
- API 응답은 `secrets/json/code_response_body.json`에 저장

---

### 3️⃣ Refresh Token으로 새 Token 발급
```bash
python src/utils/get_refresh_token.py
```
- `refresh_token.txt`를 이용해 새 Access Token 갱신  
- 결과는 `secrets/json/refresh_response_body.json`에 저장

---

### 4️⃣ 테스트 실행

**Access Token 읽기 우선순위**
1. CLI 인자 (`--access-token`)
2. 환경변수 (`ACCESS_TOKEN`)
3. 파일 (`secrets/token/access_token.txt`)
4. Refresh Token 자동 갱신

#### 기본 실행
```bash
pytest
```

#### CLI로 토큰 직접 전달
```bash
pytest --access-token=YOUR_ACCESS_TOKEN
```

#### 환경변수로 실행
```bash
export ACCESS_TOKEN=YOUR_ACCESS_TOKEN
pytest
```

---

## 🧪 테스트 케이스

- `test_get_user_profile_success`: 사용자 프로필 정보 조회  
- `test_get_access_token_info`: Access Token 정보 조회  
- `test_get_friends_list`: 친구 목록 조회  
- `test_get_talk_profile`: 카카오톡 프로필 조회  
- `test_send_message`: 기본 메시지 전송 (form-urlencoded)  
- `test_send_message_default_text`: 자동 생성된 메시지 전송 (Test Data 생성)  
- `test_send_message_with_template`: 등록된 템플릿(`template_id`) 메시지 전송  

---

## 📋 결과

### 🧾 결과 Report

테스트 실행 결과는 HTML Report로 확인할 수 있습니다.  
🔗 [Result 폴더 (HTML Report)](https://github.com/leeyeonjung/API_Test/tree/main/Result)



### 📸 카카오톡 메시지 전송 API 결과 화면 캡처

**🔹 test_send_message**
<p align="left">
  <img width="304" height="274" alt="test_send_message 결과" src="https://github.com/user-attachments/assets/176345b8-0011-4109-b172-9bc2c8c29cbc" />
</p>

**🔹 test_send_message_default_text**
<p align="left">
  <img width="303" height="283" alt="test_send_message_default_text 결과" src="https://github.com/user-attachments/assets/b3e7ea87-b1c2-4a86-a2a2-3b43aa66d99c" />
</p>

**🔹 test_send_message_with_template**
<p align="left">
  <img width="299" height="393" alt="test_send_message_with_template 결과" src="https://github.com/user-attachments/assets/17c4bb53-75e0-4469-a444-172b6f707856" />
</p>
---

## ⚠️ .gitignore

- `secrets/` 디렉토리는 `.gitignore`에 포함되어 있어 Git에 업로드되지 않습니다.
- 실제 카카오톡 메시지 전송을 위해선 **“카카오톡 메시지 전송” 권한 동의 및 앱 연결**이 필요합니다.

---

## 📦 requirements

```bash
pip install -r requirements.txt
```

---
