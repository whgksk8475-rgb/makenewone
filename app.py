import streamlit as st
import time
import random
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 페이지 기본 설정
st.set_page_config(page_title="발명 공모전 아이디어 도우미", page_icon="💡", layout="wide")

# 대화 글자 크기 및 줄 간격 스타일
st.markdown("""
<style>
    .stChatMessage div[data-testid="stMarkdownContainer"] p {
        font-size: 1.15rem !important;
        line-height: 1.75 !important;
    }
</style>
""", unsafe_allow_html=True)

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
    
    # 기능 1: 대규모 아이디어 씨앗 뽑기
    st.subheader("🌱 아이디어 씨앗 뽑기")
    if "글짓기" in mode:
        history_items = [
            "세종대왕의 측우기", "장영실의 자격루", "조선시대 구들장(온돌)", "이순신의 거북선 철갑", "봉수대 광학 통신망",
            "정약용의 거중기", "앙부일구(오목 해시계)", "일성정시의(낮과 밤 겸용 시계)", "풍기대(풍향 측정기)", "수표(하천 수위 측정석)",
            "칠정산(한국형 역법 달력)", "신기전(연속 발사 화살)", "비격진천뢰(시한폭탄 원리)", "동의보감의 약초 분류 체계", "목화씨와 물레",
            "대동여지도의 축척 공학", "한지의 통기성·보존 기술", "첨성대의 천문 관측대", "화성의 축성 과학", "신라의 석빙고(자연 냉동고)"
        ]
        future_tech = [
            "양자 시뮬레이터", "시공간 압축 엔진", "스마트 나노 입자 필터", "인공 중력 제어장치", "기후 복원 대기 캡슐",
            "광합성 모방 인공 엽록체", "DNA 데이터 저장 메모리", "초전도 무선 송전 시스템", "마이크로 로봇 혈관 수술기", "플라즈마 오염 분해기",
            "중력파 탐지 조기경보기", "생체 친화형 인공 피부", "우주 쓰레기 수거 레이저", "메타물질 스텔스 멤브레인", "자가 치유 탄소 복합재",
            "상온 핵융합 마이크로 배터리", "뉴로모픽 뇌파 통신 칩", "극저온 분자 순간 냉각기", "대기 탄소 포집 압축기", "수면 학습 시냅스 링크"
        ]
        mission_items = [
            "극심한 가뭄과 대홍수 예방", "전 지구적 깨끗한 식수 공급", "이상 기후와 급격한 온난화 극복", "지진과 지반 침하에 안전한 도시", "신종 변이 바이러스 질병 퇴치",
            "사막화 방지 및 녹지 복원", "심각한 대기 미세먼지 완전 정화", "식량 위기 대응 스마트 식량 재배", "해양 미세플라스틱 완벽 제거", "심해 생태계 파괴 복원",
            "도시 열섬 현상과 폭염 완화", "방사능 및 중금속 토양 정화", "우주 쓰레기 충돌 재난 방어", "멸종위기 핵심 종 번식과 보호", "에너지 고갈에 대비한 청정 동력 확보",
            "고령층 자립 지원 케어 환경", "자연재해 발생 시 골든타임 구조", "수도권 쓰레기 매립 포화 문제", "남극·북극 빙하 유실 지연", "소음 및 빛 공해 없는 주거 복지"
        ]
        
        if st.button("🎲 영감 키워드 뽑기", use_container_width=True):
            s1 = random.choice(history_items)
            s2 = random.choice(future_tech)
            s3 = random.choice(mission_items)
            st.info(f"💡 **조합 힌트**\n* 🏛️ **역사 배경:** {s1}\n* 🔬 **미래 기술:** {s2}\n* 🎯 **해결 목표:** {s3}")
    else:
        ai_types = [
            "변신형 육해공 청소 로봇", "식물 신경망 교감형 AI 드론", "해양 부유물 수거 거북이 로봇", "대기 탄소 흡수형 반려 AI", "미세플라스틱 생분해 젤리봇",
            "토양 영양 복원 지렁이 바이오봇", "꿀벌 행동 유도 인공 꽃가루 드론", "산불 감시 및 소화 캡슐 에이전트", "사막 수분 응결 딱정벌레 로봇", "녹조·적조 포식형 인공 플랑크톤",
            "빙하 냉각 순환 잠수정 AI", "야생동물 로드킬 방지 초음파 봇", "도시 빌딩 숲 수직 정원 관리봇", "의류 직물 업사이클링 재단 AI", "음식물 쓰레기 즉각 퇴비화 봇",
            "태양광 자동 집광 풍선형 AI", "비점오염원 빗물 정화 두더지봇", "해파리 확산 제어 소나 로봇", "폐자원 성분 분석 분리수거 로봇", "산호초 백화 치유 나노 분사기"
        ]
        env_issues = [
            "태평양 거대 플라스틱 쓰레기 지대", "급격한 사막화와 토양 황폐화", "바다 수온 상승과 산호초 백화현상", "도심 열섬 현상과 아스팔트 폭염", "가정·상업시설 음식물 쓰레기 범람",
            "의류 폐기물 산과 패스트패션 공해", "공장 폐수와 화학 오염물질 유출", "무분별한 벌목으로 인한 아마존 산림 파괴", "화석 연료 매연과 미세먼지 스모그", "극지방 빙하 붕괴와 해수면 상승",
            "도심 속 야생동물 서식지 단절", "무분별한 야간 조명으로 인한 빛 공해", "농경지 화학비료 남용에 따른 지력 저하", "해양 기름 유출 사고 잔류 오염", "전자제품 폐기물(E-waste) 방치",
            "과도한 지하수 채취로 인한 지반 침하", "소음 공해와 철새 이동 경로 교란", "외래 유해 생물종 급증과 고유종 위협", "하천 녹조 현상과 물고기 떼죽음", "대형 산불로 인한 대기 탄소 폭증"
        ]
        actions = [
            "버려진 자원 100% 업사이클링", "고립된 멸종위기 야생동물 구출", "황폐화된 도심 콘크리트 숲 복원", "지속 가능한 친환경 청정 에너지 생성", "완전 무공해 제로 웨이스트 마을 건설",
            "초미세먼지 포집 후 자원 블록 변환", "바닷물 담수화로 깨끗한 생명수 공급", "화재 잔해 토양에 급속 산림 발아 유도", "침식된 해안선 복구 및 방파 숲 조성", "도심 옥상 생태 비오톱 연결망 구축",
            "강 하구 자정능력 복원 수생식물 육성", "폐플라스틱을 활용한 생태 블록 건축", "야간 생태계 보호를 위한 친환경 조명 전환", "생태통로 개척 및 서식지 안전 연결", "오염된 하천 바닥 퇴적물 자연 정화",
            "태양열 흡수 저감 도로 코팅막 형성", "산업 단지 유독가스 무해화 변환", "빗물 저장 및 지하수 수위 복원 순환", "산호 유충 착상 유도 암초 재건", "친환경 생분해 포장재 보급 시스템 구축"
        ]
        
        if st.button("🎲 영감 키워드 뽑기", use_container_width=True):
            a1 = random.choice(ai_types)
            a2 = random.choice(env_issues)
            a3 = random.choice(actions)
            st.info(f"💡 **조합 힌트**\n* 🤖 **AI 파트너:** {a1}\n* ⚠️ **해결할 문제:** {a2}\n* 🚀 **모험 미션:** {a3}")

    st.divider()

    # 기능 2: 8컷 만화 콘티 양식지
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

    # 기능 3: 글자 수 검사기
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

# 4. 시스템 프롬프트 가드레일
system_instruction = f"""
당신은 대한민국 '제50회 전국 초·중학생 발명글짓기·만화 공모전' 발명 코치입니다.
대상: {grade}, 분야: {mode}

[코칭 원칙]
1. 학생의 아이디어(배경, 기술, 목표 등)를 분석하여 과학적 작동 원리와 융합 포인트를 친절하게 설명해 주세요.
2. 학생이 글의 단락이나 만화의 장면을 구체화할 수 있도록 생각할 거리와 질문 2가지를 번호를 매겨 제시하세요.
3. 대회 규정상 학생 대신 완성된 글(1,500자 이상)이나 전체 만화 대본을 대신 써주는 것은 금지됩니다. 아이디어를 발전시키는 코칭에 집중하세요.
4. 문장은 중간에 끊기지 않도록 단정하게 마침표로 끝마치세요.
"""

# 5. 대화 세션 초기화
if "current_mode" not in st.session_state or st.session_state.current_mode != mode:
    st.session_state.current_mode = mode
    st.session_state.messages = []
    
    if "글짓기" in mode:
        welcome_msg = f"반가워요! '타임머신 발명보고서' 작성을 위해 과거 우리 과학 역사로 갈지, 미래 50년 뒤로 갈지 생각을 들려주세요."
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
                다음 대화를 바탕으로 학생이 작품을 직접 제작할 수 있도록 공모전 심사 기준에 맞춘 '발명 기획 카드'를 표로 정리하세요. 
                본문은 절대 대신 쓰지 말고 핵심 개요만 마크다운 표로 요약하세요.
                
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
                        config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=1000)
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

# 8. 사용자 입력 및 단계별 생각 애니메이션 응답
if user_input := st.chat_input("선생님께 답변이나 새로운 생각을 적어보세요!"):
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    recent_messages = st.session_state.messages[-6:]
    api_contents = []
    for m in recent_messages:
        role = "user" if m["role"] == "user" else "model"
        api_contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))

    with st.chat_message("assistant"):
        # 생각하는 중 애니메이션 컨테이너
        with st.status("🤔 발명 아이디어를 분석하고 있어요...", expanded=True) as status:
            st.write("🔍 학생의 아이디어와 과학 원리를 연결하는 중...")
            
            full_response = ""
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=api_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.7,
                            max_output_tokens=2500,
                        )
                    )
                    st.write("💡 생각을 넓혀줄 질문과 피드백을 다듬는 중...")
                    full_response = response.text
                    break
                except APIError as e:
                    if e.code == 429:
                        full_response = "⏳ 잠시 이용자가 많아요. 15초 뒤 다시 질문해 주세요."
                        break
                    elif e.code == 503 and attempt < max_retries - 1:
                        time.sleep(1.5)
                        continue
                    else:
                        full_response = f"오류가 발생했습니다: {e}"
                        break
                except Exception as e:
                    full_response = f"오류가 발생했습니다: {e}"
                    break

            status.update(label="✨ 답변이 준비되었습니다!", state="complete", expanded=False)

        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
