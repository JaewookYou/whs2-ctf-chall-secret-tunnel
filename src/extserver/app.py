from flask import Flask, request, render_template_string
import pickle
import base64
import hashlib
import re

app = Flask(__name__)

SECRET_KEY = "very_secret_key_do_not_guess"

def verify_signature(data, signature):
    # 실제로는 안전하지 않은 검증 방식입니다
    return hashlib.md5((data + SECRET_KEY).encode()).hexdigest() == signature

@app.route('/process', methods=['POST'])
def process_data():
    data = request.form.get('data')
    signature = request.form.get('signature')
    
    if not verify_signature(data, signature):
        return "Invalid signature", 400

    try:
        decoded = base64.b64decode(data)
        # 'pickle' 문자열이 포함된 경우 역직렬화 거부
        if b'pickle' in decoded.lower():
            return "Suspicious input detected", 400
        
        obj = pickle.loads(decoded)
        
        if isinstance(obj, dict) and 'template' in obj:
            # 중괄호 개수가 다르면 렌더링 거부
            if obj['template'].count('{') != obj['template'].count('}'):
                return "Invalid template", 400
            # 특정 위험한 문자열 필터링
            if re.search(r'(config|self|import|os|subprocess|popen)', obj['template'], re.I):
                return "Suspicious template detected", 400
            
            return render_template_string(obj['template'])
        else:
            return f"Processed data: {obj}"
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8090)