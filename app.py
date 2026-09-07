import streamlit as st
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError

st.set_page_config(page_title="발명 아이디어 코치", page_icon="💡", layout="centered")

st.title("💡 발명 공모전 아이디어 도우미")
st.caption("AI는 글이나 만화를 대신 만들어주지 않아요! 생각을 넓히는 질문을 통해 나만의 멋진 아이디어를 완성해 봐요.")

# 1. API 키 불러오기
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Streamlit Secrets에 GEMINI_API_KEY를 등록해 주세요.")
    st.stop()

client = genai.Client(api_key=api_key)

# 2. 공모 분야 및 대상 선택
col1, col2 = st.columns(2)
with col1:
    mode = st.selectbox("참여 분야를 선택하세요", ["글짓기 (타임머신 발명보고서)", "만화 (AI 파트너와 지구 복구)"])
with col2:
    grade = st.selectbox("학년을 선택하세요", ["초등학생", "중학생"])

# 3. 시스템 프롬프트 설정 (대회 규정 준수 가드레일)
system_instruction = f"""
당신은 대한민국 '제50회 전국 초·중학생 발명글짓기·만화 공모전'을 돕는 다정하고 친절한 초중등 발명 코치 선생님입니다.
사용자 대상: {grade}
선택 분야: {mode}

[대회 규정 필수 준수]
- 본 대회는 AI가 생성한 완성 작품의 출품을 엄격히 금지합니다.
- 절대로 학생 대신 1,500~2,000자 분량의 완성된 글을 대신 써주거나 만화 완성형 대본을 제공하지 마세요.
- 질문(소크라테스식 발문), 과학적 호기심 자극, 아이디어 구체화 유도, 개요 구성 힌트만 제공합니다.

[분야별 코칭 안내]
1. 글짓기: 발명 동기, 기발한 발명품 명칭, 작동 원리(과학적 상상력)를 묻고 이끌어내세요.
2. 만화: 나만의 AI 파트너의 외형/특수기능, 환경 복구 원리, 8컷 이내 모험 구성을 단계별로 질문하세요.

[대화 스타일]
- 초·중학생 눈높이에 맞는 칭찬과 격려를 건네세요.
- 한 번의 답변에 1~2개의 핵심 질문만 간결하게 건네세요.
"""

# 4. 세션 상태 초기화
if "current_mode" not in st.session_state or st.session_state.current_mode != mode:
    st.session_state.current_mode = mode
    st.session_state.messages = []
    
    if "글짓기" in mode:
        welcome_msg = f"안녕! {grade} 친구 반가워요! 🚀\n\n'타임머신 발명보고서'를 멋지게 쓰기 위해 선생님과 이야기해 봐요. 혹시 타임머신을 타고 옛날 우리나라의 과학 역사로 가보고 싶나요, 아니면 50년 뒤 미래 세상으로 가보고 싶나요?"
    else:
        welcome_msg = f"안녕! {grade} 친구 반가워요! 🌍\n\n지구를 지키는 'AI 파트너' 만화 콘티를 함께 짜볼까요? 우리 지구를 아프게 만드는 여러 환경 문제(쓰레기, 기후위기, 바다 오염 등) 중 어떤 문제를 가장 먼저 해결해 주고 싶나요?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# 5. 이전 대화 렌더링
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. 사용자 입력 및 API 호출 (일시 과부하 자동 재시도 로직 포함)
if user_input := st.chat_input("선생님께 답변이나 아이디어를 적어보세요!"):
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    api_contents = []
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "model"
        api_contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))

    with st.chat_message("assistant"):
        with st.spinner("선생님이 생각 중이에요..."):
            bot_reply = None
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=api_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.7,
                        )
                    )
                    bot_reply = response.text
                    break
                except APIError as e:
                    if e.code == 503 and attempt < max_retries - 1:
                        time.sleep(2.5)  # 503 일시 과부하 시 잠시 대기 후 자동 재시도
                        continue
                    else:
                        st.error(f"오류가 발생했습니다: {e}")
                        break
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
                    break

            if bot_reply:
                st.write(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
