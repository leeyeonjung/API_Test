import requests, json, logging
log = logging.getLogger(__name__)

class KakaoApiClient:
    BASE_URL = "https://kapi.kakao.com"

    def __init__(self, access_token: str):
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def get_user_profile(self):
        url = f"{self.BASE_URL}/v2/user/me"
        log.info(f"GET {url}")
        return requests.get(url, headers=self.headers)

    def get_friends(self, after_url: str = None):
        url = f"{self.BASE_URL}/v1/api/talk/friends"
        log.info(f"GET {url}")
        return requests.get(url, headers=self.headers)

    def send_message(self, template_json: dict):
        url = f"{self.BASE_URL}/v2/api/talk/memo/default/send"
        log.info(f"POST {url} with body {template_json}")

        form_data = {"template_object": json.dumps(template_json)}

        resp = requests.post(url, headers=self.headers, data=form_data)

        return resp