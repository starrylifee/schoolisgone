import openai
import streamlit as st
import time
import random
import pathlib
import toml

hide_github_icon = """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK{ display: none; }
    #MainMenu{ visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    </style>
"""

st.markdown(hide_github_icon, unsafe_allow_html=True)

def load_css():
    css = """
    <style>
        body, .stApp, .stChatFloatingInputContainer {
            background-color: #E0F7FA !important; /* 옅은 하늘색으로 전체 배경색 변경 */
        }
        .stChatInputContainer {
            background-color: #E0F7FA !important; /* 입력 필드의 배경색도 변경 */
        }
        textarea {
            background-color: #FFFFFF !important; /* 실제 입력 필드의 배경색도 흰색으로 변경 */
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def main():
    load_css()  # 배경색 스타일 로드

    # 초기화 조건 수정
    if "initialized" not in st.session_state:
        st.session_state.thread_id = ""  # 스레드 ID 초기화
        st.session_state.messages = [{"role": "assistant", "content": "안녕하세요, 저는 우리 학교가 없어졌어요 챗봇입니다. 먼저 왼쪽의 '대화 시작'버튼을 눌러주세요. 무엇을 도와드릴까요?"}]  # 초기 메시지 설정
        st.session_state.initialized = True

    # secrets.toml 파일 경로
    secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

    # secrets.toml 파일 읽기
    with open(secrets_path, "r", encoding="utf-8") as f:
        secrets = toml.load(f)

    # secrets.toml 파일에서 여러 API 키 값 가져오기
    api_keys = [
        secrets.get("api_key1"),
        secrets.get("api_key2"),
        secrets.get("api_key3"),
        secrets.get("api_key4"),
        secrets.get("api_key5"),
        secrets.get("api_key6"),
        secrets.get("api_key7"),
        secrets.get("api_key8"),
        secrets.get("api_key9"),
        secrets.get("api_key10"),
        secrets.get("api_key11"),
        secrets.get("api_key12")
    ]

    # 유효한 API 키 필터링
    api_keys = [key for key in api_keys if key is not None]

    # 랜덤하게 API 키를 선택하여 OpenAI 클라이언트 초기화
    selected_api_key = random.choice(api_keys)
    client = openai.OpenAI(api_key=selected_api_key)

    with st.sidebar:
        # 스레드 ID 관리
        thread_btn = st.button("대화 시작")
        if thread_btn:
            try:
                thread = client.beta.threads.create()
                st.session_state.thread_id = thread.id  # 스레드 ID를 session_state에 저장
                st.success("대화가 시작되었습니다!")
            except Exception as e:
                st.error("대화 시작에 실패했습니다. 다시 시도해주세요.")
                st.error(str(e))

        st.divider()
        if "show_examples" not in st.session_state:
            st.session_state.show_examples = True

        if st.session_state.show_examples:
            st.subheader("질문 예시")
            st.info("미정")
            st.info("몰랑")

    # 스레드 ID 입력란을 자동으로 업데이트
    thread_id = st.session_state.thread_id

    st.title("우리 학교가 없어졌어요.")
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not thread_id:
            st.error("왼쪽의 대화시작 버튼을 눌러주세요.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("응답을 기다리는 중..."):
            response = client.beta.threads.messages.create(
                thread_id,
                role="user",
                content=prompt,
            )

            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=secrets["assistant_api_key1"]
            )

            run_id = run.id

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run_id
                )
                if run.status == "completed":
                    break
                else:
                    time.sleep(2)

            thread_messages = client.beta.threads.messages.list(thread_id)

            msg = thread_messages.data[0].content[0].text.value

            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)

if __name__ == "__main__":
    main()
