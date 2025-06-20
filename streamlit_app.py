import streamlit as st
from openai import OpenAI

st.title("FaithFam-Chatbot")
st.write(
    "Faith's Family를 위한 챗봇 서비스입니다. "
    "이 앱을 사용하려면 OpenAI API 키가 필요합니다. [여기](https://platform.openai.com/account/api-keys)에서 API 키를 발급받을 수 있습니다. "
    "이 앱을 단계별로 직접 만들어보고 싶으시다면 [이 튜토리얼](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)을 참고하세요."
)

openai_api_key = st.text_input("OpenAI API 키", type="password")
if not openai_api_key:
    st.info("써보고 싶다면 당신의 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 시스템 프롬프트 (한국어 기본 설정)
    system_prompt = "당신은 항상 한국어로 답변하는 친절하고 명확한 챗봇입니다. 복사해서 활용할 내용은 코드블럭에 먼저 출력하세요. 코드블럭 안에는 마크다운 문법(##, ** 등)을 사용하지 마세요. "

    # 이전 대화 불러오기 + 시스템 메시지 맨 앞에 추가
    messages = [{"role": "system", "content": system_prompt}]
    messages += [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("메시지를 입력해 주세요."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 답변 생성
        stream = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            temperature=0.9,  # 창의성 높임
            stream=True,
        )

        # 답변 출력
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
