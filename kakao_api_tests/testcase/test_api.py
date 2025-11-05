import logging
import pytest_check as check

from kakao_api_tests.api_list.api_clients import KakaoApiClient

log = logging.getLogger(__name__)


def test_get_user_profile_success(access_token):
    api_client = KakaoApiClient(access_token)
    resp = api_client.get_user_profile()
    data = resp.json()

    # Assertions: resp.status_code = 200
    check.equal(resp.status_code, 200, "status code is not 200")

    # Assertions: data contains "id" and "connected_at"
    check.is_true("id" in data, "id is not in data")
    check.is_true("connected_at" in data, "connected_at is not in data")


def test_get_friends_list(access_token):
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


def test_send_message(access_token):
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