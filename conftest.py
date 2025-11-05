# conftest.py

# Standard library
import os  # 파일 경로 및 디렉토리 조작
import logging  # 로깅 설정
import subprocess  # 외부 스크립트 실행 (get_refresh_token.py 실행)
from datetime import datetime  # 날짜/시간 형식화

# Third-party library
import pytest  # pytest 테스트 프레임워크


# Logger setting
log = logging.getLogger(__name__)

# Path constant definition
BASE_DIR = os.path.dirname(__file__)  # 프로젝트 루트 디렉토리
TOKEN_DIR = os.path.join(BASE_DIR, "secrets", "token")  # 토큰 저장 디렉토리
ACCESS_TOKEN_PATH = os.path.join(TOKEN_DIR, "access_token.txt")  # Access Token 파일 경로
REFRESH_TOKEN_PATH = os.path.join(TOKEN_DIR, "refresh_token.txt")  # Refresh Token 파일 경로
REFRESH_SCRIPT = os.path.join(BASE_DIR, "src", "utils", "get_refresh_token.py")  # 토큰 갱신 스크립트 경로
RESULT_DIR = os.path.join(BASE_DIR, "Result")  # 테스트 리포트 저장 디렉토리


def pytest_addoption(parser):
    """pytest CLI 옵션 추가"""
    parser.addoption("--access-token", action="store", help="Kakao access token")
    parser.addoption("--refresh-token", action="store", help="Kakao refresh token")


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


def read_file(path):
    """
    Read file content
    
    Args:
        path (str): 파일 경로
        
    Returns:
        str: 파일 내용 (줄바꿈 제거) 또는 None (파일이 없는 경우)
    """
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None


def write_file(path, content):
    """
    파일에 내용 쓰기
    
    Args:
        path (str): 파일 경로
        content (str): 저장할 내용
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    log.info(f"Saved file: {path}")


def run_refresh_script():
    """
    Refresh Token을 사용하여 새 Access Token 발급
    
    Returns:
        str: 새로 발급된 Access Token 또는 None (실패 시)
    """
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