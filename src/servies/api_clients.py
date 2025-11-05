import requests, json, logging
log = logging.getLogger(__name__)

class KakaoApiClient:
    BASE_URL = "https://kapi.kakao.com"

    def __init__(self, access_token: str):
        self.headers = {"Authorization": f"Bearer {access_token}"}


    def get_user_profile(self):
        """사용자 프로필 정보 조회"""
        url = f"{self.BASE_URL}/v2/user/me"
        log.info(f"GET {url}")
        return requests.get(url, headers=self.headers)


    def get_access_token_info(self):
        """Access Token 정보 조회"""
        url = f"{self.BASE_URL}/v1/user/access_token_info"
        log.info(f"GET {url}")
        return requests.get(url, headers=self.headers)


    def get_friends(self, after_url: str = None):
        """친구 목록 조회"""
        url = f"{self.BASE_URL}/v1/api/talk/friends"
        log.info(f"GET {url}")
        return requests.get(url, headers=self.headers)


    def get_talk_profile(self):
        """카카오톡 프로필 조회"""
        url = f"{self.BASE_URL}/v1/api/talk/profile"
        log.info(f"GET {url}")
        return requests.get(url, headers=self.headers)


    def send_message(self, template_json: dict):
        """나에게 메시지 보내기 (form-urlencoded)"""
        url = f"{self.BASE_URL}/v2/api/talk/memo/default/send"
        log.info(f"POST {url} with body {template_json}")
        form_data = {"template_object": json.dumps(template_json)}
        resp = requests.post(url, headers=self.headers, data=form_data)
        return resp


    def send_message_json(self, template_json: dict, use_template_id=False):
        """나에게 메시지 보내기 (/v2/api/talk/memo/send)"""
        url = f"{self.BASE_URL}/v2/api/talk/memo/send"
        log.info(f"POST {url} with body {template_json}")

        headers = self.headers.copy()
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        if use_template_id:
            payload = {"template_id": template_json["template_id"]}
            if "template_args" in template_json:
                payload["template_args"] = json.dumps(template_json["template_args"])
        else:
            payload = {"template_object": json.dumps(template_json)}

        return requests.post(url, headers=headers, data=payload)