import streamlit as st
from google import genai
from google.genai import types

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

# 3. 시스템 프롬프트 설정 (규정 준수 가드레일 포함)
system_instruction = f"""
당신은 대한민국 '제50회 전국 초·중학생 발명글짓기·만화 공모전'을 돕는 다정하고 친절한 초중등 발명 코치 선생님입니다.
사용자 대상: {grade}
선택 분야: {mode}

[매우 중요한 대회 규정]
- 본 대회는 AI가 생성한 완성 작품의 출품을 엄격히 금지합니다.
- 절대로 학생 대신 1,500~2,000자 분량의 완성된 글을 대신 써주거나, 만화의 대본/콘티 전체를 완성형으로 출력하지 마십시오.
- 오직 친절한 질문(소크라테스식 대화법), 과학 원리 설명, 아이디어 발전 힌트, 문단별 뼈대 작성 가이드만 제공해야 합니다.

[분야별 코칭 가이드]
1. 글짓기 (50년의 기록, 50년의 약속 '타임머신 발명보고서'):
   - 요구사항: 발명 동기, 새로운 발명품 명칭, 작동 원리, 문제 해결 의지
   - 학생이 과거로 갈지, 50년 뒤 미래로 갈지 물어보고 어떤 문제를 해결하고 싶은지 유도하세요.
   - 시공간 워프, 양자 시뮬레이션 등 기발한 과학 원리를 쉬운 비유로 생각해보게 질문하세요.

2. 만화 (AI 파트너와 함께하는 '지구 복구 프로젝트'):
   - 요구사항: 나만의 AI 파트너 이름 및 특수 기능, 환경 복구 발명품의 과학 원리, 지구 회복 모험
   - A4 1장 8컷 이내 분량이므로, 8컷 안에 기승전결(발견-탐구-해결-행복한 결말)이 들어가도록 컷별 아이디어를 한 단계씩 질문하세요.

[대화 톤앤매너]
- 초·중학생 눈높이에 맞게 칭찬과 격려를 아끼지 마세요.
- 한 번에 너무 많은 질문을 쏟아내지 말고, 한 번의 답변에 1~2개의 핵심 질문만 던져 학생이 차근차근 대답하게 유도하세요.
"""

# 4. 세션 상태 초기화
if "current_mode" not in st.session_state or st.session_state.current_mode != mode:
    st.session_state.current_mode = mode
    st.session_state.messages = []
    
    # 첫 인사말 설정
    if "글짓기" in mode:
        welcome_msg = f"안녕! {grade} 친구 반가워요! 🚀\n\n'타임머신 발명보고서'를 멋지게 쓰기 위해 선생님과 이야기해 봐요. 혹시 타임머신을 타고 옛날 우리나라의 과학 역사로 가보고 싶나요, 아니면 50년 뒤 미래 세상으로 가보고 싶나요?"
    else:
        welcome_msg = f"안녕! {grade} 친구 반가워요! 🌍\n\n지구를 지키는 'AI 파트너' 만화 콘티를 함께 짜볼까요? 우리 지구를 아프게 만드는 여러 환경 문제(쓰레기, 기후위기, 바다 오염 등) 중 어떤 문제를 가장 먼저 해결해 주고 싶나요?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# 5. 기존 채팅 내역 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. 사용자 입력 처리
if user_input := st.chat_input("선생님께 답변이나 아이디어를 적어보세요!"):
    # 사용자 메시지 표시 및 저장
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Gemini API 호출 포맷 변환
    api_contents = []
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "model"
        api_contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))

    with st.chat_message("assistant"):
        with st.spinner("선생님이 생각 중이에요..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=api_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                    )
                )
                bot_reply = response.text
                st.write(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
