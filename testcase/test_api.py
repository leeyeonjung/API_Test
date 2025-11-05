import logging
import pytest_check as check

from src.servies.api_clients import KakaoApiClient

log = logging.getLogger(__name__)


def test_get_user_profile_success(access_token):
    """사용자 프로필 정보 조회 테스트"""
    api_client = KakaoApiClient(access_token)
    resp = api_client.get_user_profile()
    data = resp.json()

    # Assertions: resp.status_code = 200
    check.equal(resp.status_code, 200, "status code is not 200")

    # Assertions: data contains "id" and "connected_at"
    check.is_true("id" in data, "id is not in data")
    check.is_true("connected_at" in data, "connected_at is not in data")


def test_get_access_token_info(access_token):
    """Access Token 정보 조회 테스트"""
    api_client = KakaoApiClient(access_token)
    resp = api_client.get_access_token_info()
    data = resp.json()

    log.info(resp.status_code)
    log.info(data)

    # Assertions: resp.status_code = 200
    check.equal(resp.status_code, 200, "status code is not 200")
    # Assertions: data contains "id"
    check.is_true("id" in data, "id is not in data")


def test_get_friends_list(access_token):
    """친구 목록 조회 테스트"""
    api_client = KakaoApiClient(access_token)
    resp = api_client.get_friends()
    log.info(resp.status_code)
    log.info(resp.json())
    data = resp.json()
    
    # 비즈 계정 아니므로 403으로 assertion 할당
    # Assertions: resp.status_code = 403
    check.equal(resp.status_code, 403, "status code is not 403")

    # Assertions: data contains "msg" and "There are no team members except the caller for App"
    check.is_true("There are no team members except the caller for App" in data["msg"], f"msg is not {data['msg']}")


def test_get_talk_profile(access_token):
    """카카오톡 프로필 조회 테스트"""
    api_client = KakaoApiClient(access_token)
    resp = api_client.get_talk_profile()
    data = resp.json()

    log.info(resp.status_code)
    log.info(data)

    # Assertions: resp.status_code = 200
    check.equal(resp.status_code, 200, "status code is not 200")


def test_send_message(access_token):
    """나에게 메시지 보내기 테스트 (form-urlencoded)"""
    # 템플릿 예시 JSON
    body = {
        "object_type": "text",
        "text": "Test message from automation",
        "link": {
            "web_url": "https://your.service",
            "mobile_web_url": "https://your.service"
        }
    }

    api_client = KakaoApiClient(access_token)
    resp = api_client.send_message(body)
    log.info(f"send_message response: {resp.json()}")
    data = resp.json()

    log.info(resp.status_code)
    log.info(data)

    # Assertions: resp.status_code = 200
    check.equal(resp.status_code, 200, "status code is not 200")

    
    # Assertions: data contains "result_code" and "result_code" = 0
    check.is_true("result_code" in data, "result_code is not in data")
    check.equal(data["result_code"], 0, "result_code is not 0")


def test_send_message_json(access_token):
    """나에게 메시지 보내기 테스트 (JSON 템플릿 ID 사용)"""

    body = {
        "template_id": 125606,
        "template_args": {"msg": "자동화 테스트 메시지입니다."}
    }

    api_client = KakaoApiClient(access_token)
    resp = api_client.send_message_json(body, use_template_id=True)
    log.info(f"send_message_json response: {resp.json()}")

    data = resp.json()
    log.info(resp.status_code)
    log.info(data)

    # Assertions: resp.status_code = 200
    check.equal(resp.status_code, 200, "status code is not 200")
    # Assertions: data contains "result_code"
    check.is_true("result_code" in data, "result_code is not in data")
    # Assertions: data["result_code"] = 0
    check.equal(data["result_code"], 0, "result_code is not 0")