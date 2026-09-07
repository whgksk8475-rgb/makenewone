import streamlit as st
import time
import random
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 페이지 기본 설정
st.set_page_config(page_title="발명 공모전 아이디어 도우미", page_icon="💡", layout="wide")

# 1. API 키 불러오기 및 클라이언트 초기화
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Streamlit Secrets에 GEMINI_API_KEY를 등록해 주세요.")
    st.stop()

client = genai.Client(api_key=api_key)

# 2. 상단 헤더 및 모드 선택
st.title("💡 발명 공모전 아이디어 도우미")
st.caption("대회 규정에 따라 AI는 글이나 만화를 대신 완성해주지 않아요! 나만의 아이디어를 구체화하는 발명 파트너로 활용해 보세요.")

col_mode, col_grade = st.columns([3, 2])
with col_mode:
    mode = st.selectbox("참여 분야를 선택하세요", ["글짓기 (타임머신 발명보고서)", "만화 (AI 파트너와 지구 복구)"])
with col_grade:
    grade = st.selectbox("학년을 선택하세요", ["초등학생", "중학생"])

# 3. 사이드바: 창작 지원 도구함
with st.sidebar:
    st.header("🛠️ 발명 지원 도구함")
    
    # 기능 1: 아이디어 씨앗 뽑기
    st.subheader("🌱 아이디어 씨앗 뽑기")
    if "글짓기" in mode:
        history_items = ["세종대왕의 측우기", "장영실의 자격루", "조선시대 온돌", "거북선 철갑", "봉수대 통신망"]
        future_tech = ["양자 시뮬레이터", "시공간 압축 엔진", "나노 입자 필터", "인공 중력장", "기후 복원 캡슐"]
        mission_items = ["가뭄과 홍수 예방", "깨끗한 식수 공급", "미래 기후 위기 극복", "안전한 도시 건설", "신종 질병 퇴치"]
        
        if st.button("🎲 영감 키워드 뽑기", use_container_width=True):
            s1, s2, s3 = random.choice(history_items), random.choice(future_tech), random.choice(mission_items)
            st.info(f"💡 **조합 힌트**\n* 배경: {s1}\n* 기술: {s2}\n* 목표: {s3}")
    else:
        ai_types = ["변신형 청소 로봇", "식물 대화형 AI 드론", "해양 정화 거북이 로봇", "탄소 흡수 반려 AI", "미세플라스틱 분해 젤리"]
        env_issues = ["태평양 플라스틱 쓰레기섬", "사막화와 가뭄", "바다 산호초 백화현상", "도심 열섬 현상", "음식물 쓰레기 배출"]
        actions = ["자원 업사이클링", "멸종위기 동물 구출", "스마트 숲 가꾸기", "친환경 청정 에너지 생성", "제로 웨이스트 마을 만들기"]
        
        if st.button("🎲 영감 키워드 뽑기", use_container_width=True):
            a1, a2, a3 = random.choice(ai_types), random.choice(env_issues), random.choice(actions)
            st.info(f"💡 **조합 힌트**\n* AI 파트너: {a1}\n* 해결할 문제: {a2}\n* 모험 미션: {a3}")

    st.divider()

    # 기능 2: 8컷 만화 양식지 (만화 모드 전용)
    if "만화" in mode:
        st.subheader("📄 만화 콘티 양식지")
        svg_template = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1130" width="100%" height="100%">
        <rect width="100%" height="100%" fill="#ffffff"/>
        <text x="400" y="45" font-size="22" font-weight="bold" text-anchor="middle" fill="#333">AI 파트너와 함께하는 지구 복구 프로젝트 (8컷 콘티)</text>
        <text x="50" y="75" font-size="14" fill="#666">제목: ___________________________ | 이름: _______________</text>
        <rect x="50" y="90" width="330" height="230" fill="none" stroke="#222" stroke-width="2"/>
        <text x="65" y="115" font-size="14" font-weight="bold" fill="#555">[컷 1]</text>
        <rect x="420" y="90" width="330" height="230" fill="none" stroke="#222" stroke-width="2"/>
        <text x="435" y="115" font-size="14" font-weight="bold" fill="#555">[컷 2]</text>
        <rect x="50" y="340" width="330" height="230" fill="none" stroke="#222" stroke-width="2"/>
        <text x="65" y="365" font-size="14" font-weight="bold" fill="#555">[컷 3]</text>
        <rect x="420" y="340" width="330" height="230" fill="none" stroke="#222" stroke-width="2"/>
        <text x="435" y="365" font-size="14" font-weight="bold" fill="#555">[컷 4]</text>
        <rect x="50" y="590" width="330" height="230" fill="none" stroke="#222" stroke-width="2"/>
        <text x="65" y="615" font-size="14" font-weight="bold" fill="#555">[컷 5]</text>
        <rect x="420" y="590" width="330" height="230" fill="none" stroke="#222" stroke-width="2"/>
        <text x="435" y="615" font-size="14" font-weight="bold" fill="#555">[컷 6]</text>
        <rect x="50" y="840" width="330" height="230" fill="none" stroke="#222" stroke-width="2"/>
        <text x="65" y="865" font-size="14" font-weight="bold" fill="#555">[컷 7]</text>
        <rect x="420" y="840" width="330" height="230" fill="none" stroke="#222" stroke-width="2"/>
        <text x="435" y="865" font-size="14" font-weight="bold" fill="#555">[컷 8 - 결말]</text>
        </svg>"""
        st.download_button(
            label="📥 A4 8컷 콘티 양식지 다운로드 (SVG)",
            data=svg_template,
            file_name="8컷_만화_콘티양식지.svg",
            mime="image/svg+xml",
            use_container_width=True
        )
        st.caption("💡 내려받은 파일을 웹 브라우저로 열어 바로 인쇄(Ctrl+P)할 수 있어요!")
        st.divider()

    # 기능 3: 글자 수 검사기 (글짓기 모드 전용)
    if "글짓기" in mode:
        st.subheader("📏 글자 수 진단기")
        sample_text = st.text_area("작성 중인 글을 넣어보세요", height=120, placeholder="여기에 작성한 글을 붙여넣으면 공모전 기준(1,500자~2,000자)을 검사해 줍니다.")
        char_count = len(sample_text)
        
        if char_count == 0:
            st.caption("글자 수: 0자 (공백 포함)")
        elif 1500 <= char_count < 2000:
            st.success(f"✅ 알맞은 분량이에요! 현재 {char_count:,}자 (1,500~2,000자 충족)")
        elif char_count < 1500:
            st.warning(f"⚠️ 분량이 부족해요! 현재 {char_count:,}자 ({1500 - char_count:,}자 더 필요)")
        else:
            st.error(f"❌ 2,000자를 넘겼어요! 현재 {char_count:,}자 ({char_count - 1999:,}자 초과)")

        st.markdown("**📝 자가 점검표**")
        st.checkbox("발명 동기와 배경이 드러났나요?")
        st.checkbox("발명품 이름과 작동 원리가 적혀있나요?")
        st.checkbox("과거 또는 미래 위기를 극복하는 내용인가요?")

# 4. 시스템 프롬프트 가드레일 (군더더기 배제 및 핵심 집중형)
system_instruction = f"""
당신은 대한민국 '제50회 전국 초·중학생 발명글짓기·만화 공모전' 아이디어 코치입니다.
대상: {grade}, 분야: {mode}

[답변 원칙 - 불필요한 사족 절대 금지]
1. 인사말, 긴 감탄사, 불필요한 칭찬, 교훈적인 서론을 일절 쓰지 마세요.
2. 답변은 반드시 아래 2단계 구조로 3문장 이내로만 간결하게 끝내세요:
   - [핵심 피드백]: 학생 아이디어의 과학적 핵심 원리나 적용 포인트를 1문장으로 명확히 짚어주기
   - [생각할 질문]: 글이나 만화 장면을 구체화할 수 있는 짧고 날카로운 질문 1~2개 던지기
3. 학생 대신 완성된 본문(1,500자 이상)이나 대본을 써주는 것은 엄격히 금지됩니다.
4. 문장이 중간에 잘리지 않도록 핵심만 말하고 즉시 마침표를 찍으세요.
"""

# 5. 대화 세션 초기화
if "current_mode" not in st.session_state or st.session_state.current_mode != mode:
    st.session_state.current_mode = mode
    st.session_state.messages = []
    
    if "글짓기" in mode:
        welcome_msg = f"반가워요! '타임머신 발명보고서'를 쓰기 위해 과거 우리 과학 역사로 갈지, 미래 50년 뒤로 갈지 정해볼까요?"
    else:
        welcome_msg = f"반가워요! '지구 복구 프로젝트' 만화에서 어떤 환경 문제를 가장 먼저 해결해보고 싶나요?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# 6. 상단 도구: 대화 복사 및 기획서 카드 정리 버튼
c_left, c_right = st.columns([1, 1])
with c_left:
    chat_summary_lines = []
    for msg in st.session_state.messages:
        sender = "선생님" if msg["role"] == "assistant" else "나"
        chat_summary_lines.append(f"[{sender}]\n{msg['content']}\n")
    full_chat_text = "\n".join(chat_summary_lines)

    with st.expander("📋 대화 내용 복사 / 저장하기"):
        st.code(full_chat_text, language="markdown")
        st.download_button(
            label="💾 대화 텍스트 다운로드 (.txt)",
            data=full_chat_text,
            file_name="발명_대화기록.txt",
            mime="text/plain",
            use_container_width=True
        )

with c_right:
    if st.button("📊 지금까지 나눈 아이디어 기획서 카드로 정리하기", use_container_width=True):
        if len(st.session_state.messages) < 4:
            st.warning("아이디어를 조금 더 나눈 뒤에 정리 버튼을 눌러주세요! (최소 2~3회 대화 필요)")
        else:
            with st.spinner("아이디어를 표로 요약 정리하고 있어요..."):
                summary_prompt = f"""
                다음 대화를 바탕으로 학생이 작품을 제작할 수 있는 '발명 기획 카드'를 표로 정리하세요. 
                본문은 대신 쓰지 말고 핵심 개요만 마크다운 표로 요약하세요.
                
                분야: {mode}
                - 발명품(또는 AI 파트너) 명칭:
                - 해결하려는 문제:
                - 핵심 과학 원리:
                - 뼈대 구성: (글짓기 4단락 개요 또는 만화 8컷 요약)
                """
                
                try:
                    summary_resp = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=[types.Content(role="user", parts=[types.Part.from_text(text=full_chat_text + "\n\n" + summary_prompt)])],
                        config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=700)
                    )
                    st.session_state.summary_card = summary_resp.text
                except Exception as e:
                    st.error(f"요약 중 오류가 발생했습니다: {e}")

if "summary_card" in st.session_state and st.session_state.summary_card:
    st.success("🎯 나만의 발명 기획서 카드가 완성되었습니다!")
    st.markdown(st.session_state.summary_card)
    st.divider()

# 7. 이전 채팅 내역 렌더링
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 8. 사용자 입력 및 스트리밍 응답 (초기 글자 수 제한 복구 및 UI 렌더링 안정화)
if user_input := st.chat_input("선생님께 답변이나 새로운 생각을 적어보세요!"):
    # 사용자 메시지 즉시 렌더링 및 세션 저장
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 최근 6개 대화만 문맥으로 압축
    recent_messages = st.session_state.messages[-6:]
    api_contents = []
    for m in recent_messages:
        role = "user" if m["role"] == "user" else "model"
        api_contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))

    with st.chat_message("assistant"):
        def generate_response():
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response_stream = client.models.generate_content_stream(
                        model="gemini-3.6-flash",
                        contents=api_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.5,
                            max_output_tokens=350,  # 요청하신 최초 글자 수 제한으로 복구
                        )
                    )
                    for chunk in response_stream:
                        if chunk.text:
                            yield chunk.text
                    return
                except APIError as e:
                    if e.code == 429:
                        yield "⏳ 잠시 이용자가 많아요. 15초 뒤 다시 질문해 주세요."
                        return
                    elif e.code == 503 and attempt < max_retries - 1:
                        time.sleep(1.5)
                        continue
                    else:
                        yield f"오류: {e}"
                        return
                except Exception as e:
                    yield f"오류: {e}"
                    return

        # 문장 잘림 없는 안전한 스트리밍 출력
        full_response = st.write_stream(generate_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
