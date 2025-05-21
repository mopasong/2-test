# 🌐 HuggingFace API 기반 GPT 대화 예시 (Colab 실행용)
# 모델: bigscience/bloomz-560m (Inference API 사용)

!pip install -q requests

import requests

# ✅ HuggingFace API 토큰 입력 (맨 처음 한 번만)
HUGGINGFACE_TOKEN = "hf_your_token_here"  # ← 여기에 본인의 토큰 입력하세요
MODEL = "bigscience/bloomz-560m"

def call_huggingface_api(prompt, token=HUGGINGFACE_TOKEN, model=MODEL):
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 150
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list):
            return result[0].get("generated_text", str(result[0]))
        return str(result)
    else:
        return f"[❌ Error {response.status_code}] {response.text}"

# 🧪 테스트
prompt = "왜 사람은 반복해서 같은 감정을 느낄까요?"
print("🤖 GPT 응답:", call_huggingface_api(prompt))
