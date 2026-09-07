import streamlit as st
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 페이지 기본 설정
st.set_page_config(page_title="발명 공모전 아이디어 도우미", page_icon="💡", layout="centered")

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
- 절대로 학생 대신 1,500~2,000자 분량의 완성된 글을 대신 써주거나 만화 대본/콘티 전체를 완성형으로 출력하지 마세요.
- 오직 생각할 거리를 던져주는 친절한 질문(소크라테스식 발문), 과학적 호기심 자극, 아이디어 구체화 유도 가이드만 제공해야 합니다.

[분야별 코칭 안내]
1. 글짓기 (50년의 기록, 50년의 약속 '타임머신 발명보고서'):
   - 발명 동기, 새로운 발명품 명칭, 작동 원리(과학적 상상력)를 묻고 이끌어내세요.
   - 과거 역사 속 기술적 한계 극복이나 50년 뒤 미래 위기 해결 방안을 스스로 상상하도록 유도하세요.
2. 만화 (AI 파트너와 함께하는 '지구 복구 프로젝트'):
   - 나만의 AI 파트너 이름 및 특수 기능, 환경 복구 발명품의 과학 원리, 8컷 이내 모험 구성을 단계별로 질문하세요.

[대화 톤앤매너 및 답변 길이 원칙]
- 초·중학생 눈높이에 맞게 칭찬과 격려를 건네세요.
- 길게 설명하지 말고, 3~4문장 이내로 핵심 격려와 1~2개의 명확한 생각거리 질문만 간결하게 건네세요.
"""

# 4. 세션 상태 초기화 (분야 변경 시 대화 리셋)
if "current_mode" not in st.session_state or st.session_state.current_mode != mode:
    st.session_state.current_mode = mode
    st.session_state.messages = []
    
    if "글짓기" in mode:
        welcome_msg = f"안녕! {grade} 친구 반가워요! 🚀\n\n'타임머신 발명보고서'를 멋지게 쓰기 위해 선생님과 이야기해 봐요. 혹시 타임머신을 타고 옛날 우리나라의 과학 역사로 가보고 싶나요, 아니면 50년 뒤 미래 세상으로 가보고 싶나요?"
    else:
        welcome_msg = f"안녕! {grade} 친구 반가워요! 🌍\n\n지구를 지키는 'AI 파트너' 만화 콘티를 함께 짜볼까요? 우리 지구를 아프게 만드는 여러 환경 문제(쓰레기, 기후위기, 바다 오염 등) 중 어떤 문제를 가장 먼저 해결해 주고 싶나요?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# [추가 기능] 대화 내용 복사 및 다운로드 도구
chat_summary_lines = []
for msg in st.session_state.messages:
    sender = "선생님(AI)" if msg["role"] == "assistant" else "나(학생)"
    chat_summary_lines.append(f"[{sender}]\n{msg['content']}\n")
full_chat_text = "\n".join(chat_summary_lines)

with st.expander("📋 지금까지 나눈 대화 복사 / 저장하기", expanded=False):
    st.info("오른쪽 상단 복사 아이콘을 누르거나 아래 파일 저장 버튼을 눌러보세요!")
    # 코드 블록 우측 상단의 기본 '복사' 버튼 활용
    st.code(full_chat_text, language="markdown")
    st.download_button(
        label="💾 대화 내용 텍스트 파일(.txt)로 다운로드",
        data=full_chat_text,
        file_name="발명_아이디어_대화내용.txt",
        mime="text/plain"
    )

st.divider()

# 5. 이전 대화 화면 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. 사용자 입력 및 최적화 스트리밍 호출
if user_input := st.chat_input("선생님께 답변이나 아이디어를 적어보세요!"):
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 전체 대화 대신 최근 6개 메시지만 문맥으로 전달 (비용 절감)
    recent_messages = st.session_state.messages[-6:]

    api_contents = []
    for m in recent_messages:
        role = "user" if m["role"] == "user" else "model"
        api_contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))

    with st.chat_message("assistant"):
        def response_generator():
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response_stream = client.models.generate_content_stream(
                        model="gemini-3.6-flash",
                        contents=api_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.7,
                            max_output_tokens=350,
                        )
                    )
                    for chunk in response_stream:
                        if chunk.text:
                            yield chunk.text
                    return
                except APIError as e:
                    if e.code == 429:
                        yield "⏳ 지금 많은 친구들이 동시에 질문하고 있어요! 약 20~30초 뒤에 다시 입력해 주세요."
                        return
                    elif e.code == 503 and attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                    else:
                        yield f"오류가 발생했습니다: {e}"
                        return
                except Exception as e:
                    yield f"오류가 발생했습니다: {e}"
                    return

        full_response = st.write_stream(response_generator)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()  # 복사 영역 텍스트를 최신 대화 상태로 즉시 갱신
