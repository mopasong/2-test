import streamlit as st
import json
import os
import requests
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="🧠 Mumyeong GPT (falcon-rw-1b)", layout="centered")

LOG_FILE = "falconrw_conversation_log.json"
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        session_log = json.load(f)
else:
    session_log = []

def get_color_by_emotion(text):
    if any(k in text for k in ["무서워", "싫어", "두려워"]):
        return "#6c5ce7"
    if any(k in text for k in ["그냥", "몰라", "비슷"]):
        return "#b2bec3"
    if any(k in text for k in ["화나", "짜증", "폭발"]):
        return "#d63031"
    if any(k in text for k in ["좋아", "고마워", "다행"]):
        return "#00cec9"
    return "#ffeaa7"

def get_delay():
    if "last_input_time" not in st.session_state:
        st.session_state.last_input_time = datetime.now()
        return 0
    now = datetime.now()
    delay = (now - st.session_state.last_input_time).total_seconds()
    st.session_state.last_input_time = now
    return delay

def call_huggingface_api(prompt, token, model="tiiuae/falcon-rw-1b"):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api-inference.huggingface.co/models/{model}"
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 150
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            result = response.json()
            if isinstance(result, list):
                return result[0].get("generated_text", str(result[0]))
            elif isinstance(result, dict) and "generated_text" in result:
                return result["generated_text"]
            else:
                return str(result)
        except:
            return "[Error] Invalid JSON response."
    else:
        return f"[Error {response.status_code}] {response.text}"

st.markdown("""
<style>
@keyframes fadeDots {
  0% {opacity: 1;}
  50% {opacity: 0.3;}
  100% {opacity: 0;}
}
.dot-anim {
  font-size: 32px;
  animation: fadeDots 2s infinite;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Mumyeong GPT (API: falcon-rw-1b)")

token = st.text_input("🔐 HuggingFace API Token (hf_xxxx)", type="password")
user_input = st.text_input("💬 당신의 말", key="user_input")

if token and user_input:
    delay = get_delay()
    color = get_color_by_emotion(user_input)

    if delay > 5:
        st.markdown("<div style='height:50px; background-color:#dfe6e9;'></div>", unsafe_allow_html=True)
        st.markdown("🤫 **침묵이 감지되었습니다**", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='dot-anim' style='color:{color}'>● ● ●</div>", unsafe_allow_html=True)

    with st.spinner("🤖 GPT 응답 생성 중..."):
        result = call_huggingface_api(user_input, token).strip()
        st.success(result)

        session_log.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "ai": result
        })

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(session_log, f, ensure_ascii=False, indent=2)

if session_log:
    st.markdown("### 📊 대화 시간 흐름 시각화")
    timestamps = [e["timestamp"][:19] for e in session_log]
    fig, ax = plt.subplots()
    ax.plot(timestamps, range(len(timestamps)), marker='o', color='#0984e3')
    ax.set_title("대화 시간 흐름")
    ax.set_xlabel("시간")
    ax.set_ylabel("입력 순서")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.download_button("⬇️ 대화 기록 다운로드", data=json.dumps(session_log, ensure_ascii=False, indent=2), file_name="falconrw_conversation_log.json", mime="application/json")
