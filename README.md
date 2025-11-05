# Kakao API Test

카카오 API 테스트 프로젝트입니다.

## 📁 프로젝트 구조

```
api_Test/
├── conftest.py                               # pytest 설정 및 fixture 정의
├── src/
│   ├── servies/
│   │   └── api_clients.py                    # Kakao API 클라이언트
│   └── utils/
│       ├── code_to_token.py                  # Code → Token 변환 스크립트
│       ├── get_refresh_token.py              # Refresh Token으로 새 Token 발급
│       └── make_url.py                       # 인증 URL 생성 스크립트
├── testcase/
│   └── test_api.py                           # 테스트 케이스
└── secrets/                                  # 토큰 및 url 저장 폴더 (Git 제외)
    ├── url/
    │   └── authorize_url.txt                 # 생성된 인증 URL
    ├── token/                                # 토큰 저장 디렉토리
    │   ├── access_token.txt                  # Access Token
    │   ├── refresh_token.txt                 # Refresh Token
    │   └── code.txt                          # Authorization Code
    └── json/                                 # API 응답 JSON 저장 디렉토리
        ├── kakao_config.json                 # 카카오 API 설정 파일 (client_id, redirect_uri 등)
        ├── code_response_body.json           # Code → Token 응답
        └── refresh_response_body.json        # Refresh Token 응답
```

## 🚀 시작하기

### 0. 설정 파일 작성

**카카오 API 설정 파일 작성**
- `secrets/json/kakao_config.json` 파일에 필요한 정보를 입력합니다:
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
- `client_id`는 REST API 키와 동일한 값입니다.
- `code_to_token.py`와 `get_refresh_token.py` 스크립트가 이 파일의 `client_id`와 `redirect_uri`를 사용합니다.

### 1. 최초 Code 발급

1. **인증 URL 생성**
   ```bash
   python src/utils/make_url.py
   ```
   - 생성된 URL이 콘솔에 출력되고 `secrets/url/authorize_url.txt`에 저장됩니다.

2. **Code 발급**
   - 생성된 URL에 접속하여 카카오 로그인을 진행합니다.
   - 리다이렉트 URL에서 `code` 파라미터 값을 확인합니다.

### 2. Code → Token 변환

1. **Code 저장**
   - 1단계에서 받은 `code`를 `secrets/token/code.txt` 파일에 저장합니다.

2. **Token 최초 발급**
   ```bash
   python src/utils/code_to_token.py
   ```
   - `secrets/token/` 디렉토리에 다음 파일들이 생성됩니다:
     - `access_token.txt` - Access Token
     - `refresh_token.txt` - Refresh Token (응답에 refresh token이 있는 경우)
   - API 응답은 `secrets/json/code_response_body.json`에 저장됩니다.

### 3. Refresh Token으로 새 Token 발급

Access Token이 만료된 경우, Refresh Token을 사용하여 새 Token을 발급할 수 있습니다:

```bash
python src/utils/get_refresh_token.py
```

- `secrets/token/refresh_token.txt` 파일에서 Refresh Token을 읽어옵니다.
- 새 Access Token과 Refresh Token이 `secrets/token/` 디렉토리에 저장됩니다.
- API 응답은 `secrets/json/refresh_response_body.json`에 저장됩니다.

### 4. 테스트 실행

**토큰 우선순위:**
1. CLI 인자 (`--access-token`)
2. 환경변수 (`ACCESS_TOKEN`)
3. 파일 (`secrets/token/access_token.txt`)
4. Refresh Token 자동 갱신 (Refresh Token이 있는 경우)

#### 기본 실행 (파일에서 토큰 읽기)

```bash
pytest
```

- `secrets/token/access_token.txt` 파일에서 Access Token을 자동으로 읽어옵니다.

#### CLI로 토큰 직접 전달

```bash
# Access Token 직접 전달
pytest --access-token=YOUR_ACCESS_TOKEN

# Refresh Token 직접 전달 (자동으로 새 Access Token 발급)
pytest --refresh-token=YOUR_REFRESH_TOKEN
```

#### 환경변수로 토큰 전달

```bash
# Windows
set ACCESS_TOKEN=YOUR_ACCESS_TOKEN
pytest

# Linux/Mac
export ACCESS_TOKEN=YOUR_ACCESS_TOKEN
pytest
```


## 📝 테스트 케이스

- `test_get_user_profile_success`: 사용자 프로필 정보 조회
- `test_get_access_token_info`: Access Token 정보 조회
- `test_get_friends_list`: 친구 목록 조회
- `test_get_talk_profile`: 카카오톡 프로필 조회
- `test_send_message`: 나에게 메시지 보내기 (form-urlencoded)
- `test_send_message_json`: 나에게 메시지 보내기 (JSON 템플릿 ID 사용)

## ⚠️ 주의사항

- `secrets/` 디렉토리의 파일들은 `.gitignore`에 포함되어 Git에 업로드되지 않습니다.

## 📦 의존성

```bash
pip install -r requirements.txt
```