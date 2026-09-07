# 8. 사용자 입력 및 스트리밍 응답 (출력 끊김 방지 및 안정화)
if user_input := st.chat_input("선생님께 답변이나 새로운 생각을 적어보세요!"):
    # 1) 사용자 메시지 표시 및 저장
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2) 최근 6개 대화만 문맥으로 압축 전달 (비용 방어)
    recent_messages = st.session_state.messages[-6:]
    api_contents = []
    for m in recent_messages:
        role = "user" if m["role"] == "user" else "model"
        api_contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))

    # 3) 모델 답변 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        max_retries = 3

        for attempt in range(max_retries):
            try:
                response_stream = client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=api_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                        max_output_tokens=800,  # 문장 잘림 방지 (넉넉한 길이)
                    )
                )
                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                
                # 완성된 문장 최종 렌더링
                message_placeholder.markdown(full_response)
                break

            except APIError as e:
                if e.code == 429:
                    full_response = "⏳ 지금 많은 친구들이 질문하고 있어요! 약 20초 뒤에 다시 보내주세요."
                    message_placeholder.markdown(full_response)
                    break
                elif e.code == 503 and attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                else:
                    full_response = f"오류가 발생했습니다: {e}"
                    message_placeholder.markdown(full_response)
                    break
            except Exception as e:
                full_response = f"오류가 발생했습니다: {e}"
                message_placeholder.markdown(full_response)
                break

        # 완성된 텍스트 세션에 저장
        st.session_state.messages.append({"role": "assistant", "content": full_response})
