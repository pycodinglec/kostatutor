from openai import OpenAI
import streamlit as st
import os
import hashlib

GPT_MODEL = 'gpt-4-1106-preview'

def initialize_conversation():
    system_message = '너는 통계 학습을 도와주는 튜터야. 너는 통계 산출에 관련된 모든 질문에 항상 친절하게 대답해. 그러나 통계와 관련 없는 요청은 정중히 거절해.'
    hello_message = '오늘은 어떤 데이터를 분석해볼까요?'
    return [
        {'role': 'system', 'content': system_message},
        {'role': 'assistant', 'content': hello_message}
    ]

def chatbot_page():
    client = OpenAI()
    st.title('통계 학습 튜터')
     
    if 'msgs' not in st.session_state:
        st.session_state['msgs'] = initialize_conversation()

    for msg in st.session_state['msgs'][1:]:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])
    
    if prompt:= st.chat_input("Prompt"):
        st.session_state['msgs'].append({'role':'user', 'content': prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            
            message_placeholder = st.empty()
            full_response = ""
            try:
                responses = client.chat.completions.create(
                    model=GPT_MODEL,
                    messages=st.session_state['msgs'],
                    stream=True,
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")
            for response in responses:
                if response.choices[0].delta.content:
                    full_response += response.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state['msgs'].append({"role": "assistant", "content": full_response})

def verify_password(input_password):
    correct_password_hash = os.getenv('PASSWORD_HASH')
    password_hash = hashlib.md5(input_password.encode()).hexdigest()
    return password_hash == correct_password_hash

def main():
    with st.container():
        input_password = st.text_input("패스워드를 입력하세요", type="password")
        if st.button("로그인"):
            if verify_password(input_password):
                st.session_state['authenticated'] = True
            else:
                st.error("패스워드가 잘못되었습니다.")

    if st.session_state.get('authenticated', False):
        chatbot_page()

if __name__=='__main__':
    main()
