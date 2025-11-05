# src/services/test_data_generator.py

# Standard library
import datetime 
import random 
import string 


def generate_message_text(prefix: str = "자동화 테스트"):
    """
    테스트용 메시지 텍스트 생성
    
    현재 시간과 랜덤 문자열을 포함한 고유한 메시지 텍스트를 생성합니다.
    형식: [prefix] YYYY-MM-DD HH:MM:SS #XXXX
    
    Args:
        prefix (str): 메시지 접두사 (기본값: "자동화 테스트")
        
    Returns:
        str: 생성된 메시지 텍스트
        예: "[자동화 테스트] 2024-11-05 14:30:00 #A1B2"
    """
    # 현재 시간을 YYYY-MM-DD HH:MM:SS 형식으로 변환
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 대문자와 숫자를 조합한 4자리 랜덤 문자열 생성
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    # 접두사, 타임스탬프, 랜덤 문자열을 조합하여 반환
    return f"[{prefix}] {ts} #{rand}"


def generate_message_payload():
    """
    카카오 메시지 전송용 페이로드 생성
    
    카카오 API의 메시지 전송 요청에 필요한 JSON 형식의 페이로드를 생성합니다.
    
    Returns:
        dict: 카카오 메시지 전송 API 페이로드
            - object_type: "text" (텍스트 메시지)
            - text: 생성된 메시지 텍스트
            - link: 웹/모바일 웹 URL 정보
    """
    # 메시지 텍스트 생성
    text = generate_message_text()
    
    # 카카오 메시지 API 페이로드 구성
    return {
        "object_type": "text",  # 텍스트 타입 메시지
        "text": text,  # 메시지 내용
        "link": {
            "web_url": "https://your.service",  # 웹 URL
            "mobile_web_url": "https://your.service"  # 모바일 웹 URL
        }
    }
