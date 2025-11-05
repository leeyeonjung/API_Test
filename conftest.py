import os
import pytest
import logging
import subprocess
from datetime import datetime
from pathlib import Path
import pytest_html

# 로그 설정
log = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(__file__)
TOKEN_DIR = os.path.join(BASE_DIR, "secrets", "token")
ACCESS_TOKEN_PATH = os.path.join(TOKEN_DIR, "access_token.txt")
REFRESH_TOKEN_PATH = os.path.join(TOKEN_DIR, "refresh_token.txt")
REFRESH_SCRIPT = os.path.join(BASE_DIR, "src", "utils", "get_refresh_token.py")
RESULT_DIR = os.path.join(BASE_DIR, "Result")

# pytest CLI 옵션 추가
def pytest_addoption(parser):
    parser.addoption("--access-token", action="store", help="Kakao access token")
    parser.addoption("--refresh-token", action="store", help="Kakao refresh token")


# pytest-html 리포트 설정
def pytest_configure(config):
    """pytest 설정 시 HTML 리포트 경로 자동 설정"""
    # Result 디렉토리 생성
    os.makedirs(RESULT_DIR, exist_ok=True)
    
    # 날짜시간 형식: YYYYMMDD_HHMMSS
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_filename = f"test_report_{timestamp}.html"
    html_path = os.path.join(RESULT_DIR, html_filename)
    
    # HTML 리포트 경로 설정
    config.option.htmlpath = html_path
    
    # CSS/JS를 HTML에 인라인으로 포함
    config.option.self_contained_html = True
    
    log.info(f"HTML report will be saved to: {html_path}")


def pytest_html_report_title(report):
    """HTML 리포트 제목 설정"""
    report.title = "API Test Report"


# 파일 유틸
def read_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    log.info(f"Saved file: {path}")

# get_refresh_token.py 실행 (자동 호출)
def run_refresh_script():
    """기존 refresh_token.py 스크립트를 호출하여 access_token 갱신"""
    result = subprocess.run(
        ["python", REFRESH_SCRIPT],
        capture_output=True,
        text=True,
        check=True
    )
    log.info("🔄 get_refresh_token.py executed successfully.")
    new_token = read_file(ACCESS_TOKEN_PATH)
    if new_token:
        log.info("New access token loaded after refresh.")
        return new_token
    else:
        log.error("Refresh script ran, but no new token found.")
    return None


# Access Token Fixture
@pytest.fixture(scope="session")
def access_token(request):
    """access_token 자동 관리 (CLI > 환경변수 > 파일 > refresh_token 순서)"""
    # 1. CLI 인자 우선
    cli_token = request.config.getoption("--access-token")
    if cli_token:
        log.info("Using access token from CLI")
        return cli_token
    
    # 2. 환경변수 확인
    env_token = os.getenv("ACCESS_TOKEN")
    if env_token:
        log.info("Using access token from environment variable")
        return env_token
    
    # 3. 파일에서 읽기
    token = read_file(ACCESS_TOKEN_PATH)
    if token:
        log.info("Using access token from file")
        return token
    
    # 4. CLI나 파일에 없으면 refresh_token 기반 자동 갱신
    refresh_token = request.config.getoption("--refresh-token") or read_file(REFRESH_TOKEN_PATH)
    if refresh_token:
        log.info("No access token found. Refreshing via script...")
        new_token = run_refresh_script()
        if new_token:
            write_file(ACCESS_TOKEN_PATH, new_token)
            return new_token
    
    # 토큰을 찾을 수 없으면 실패
    pytest.fail("No valid access token found. Provide --access-token, set ACCESS_TOKEN env var, or ensure access_token.txt exists.")