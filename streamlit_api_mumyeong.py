import streamlit as st
import requests
import json
from datetime import datetime
import random

st.set_page_config(page_title="Mumyeong GPT - 감정형 UI", layout="centered")
st.title("🧠 무명 GPT (Falcon-7B 기반)")
st.markdown("#### 감정 기반 점멸 UI + 프롬프트 응답 + 자동 JSON 저장")

def draw_emotion_dot():
    color = random.choice(["#ff4d4d", "#ffc107", "#17c0eb", "#1dd1a1", "#c56cf0"])
    st.markdown(
        f"<div style='text-align:center;margin-top:15px;'>"
        f"<div style='width:20px;height:20px;border-radius:50%;background-color:{color};"
        f"animation: blink 1.2s infinite alternate; display:inline-block;'></div></div>",
        unsafe_allow_html=True
    )
    st.markdown("""
        <style>
        @keyframes blink {
            0% {opacity: 0.1;}
            100% {opacity: 1;}
        }
        </style>
    """, unsafe_allow_html=True)

def call_falcon(prompt):
    try:
        response = requests.post(
            "http://localhost:8000/generate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"prompt": prompt}),
            timeout=60
        )
        return response.json().get("response", "응답을 생성하지 못했습니다.")
    except Exception as e:
        return f"[오류 발생] {str(e)}"

with st.form("prompt_form"):
    user_prompt = st.text_area("✍️ 프롬프트 입력", height=120, placeholder="예: 감정은 왜 반복될까?")
    submitted = st.form_submit_button("🧠 무명에게 물어보기")

if submitted and user_prompt.strip():
    with st.spinner("무명이 응답 중..."):
        draw_emotion_dot()
        answer = call_falcon(user_prompt)

        st.markdown("#### 🤖 무명의 응답")
        st.success(answer)

        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"mumyeong_log_{now}.json", "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": now,
                "prompt": user_prompt,
                "response": answer
            }, f, ensure_ascii=False, indent=2)
        st.info("✅ 대화가 JSON 파일로 저장되었습니다.")
