# import openai
import streamlit as st
import requests
import time

st.set_page_config(
    page_title="OpenEyes",
    page_icon="👀",
)


st.title("OpenEyes")

API_KEY = st.secrets["OPENAI_API_KEY"]


def makeRequest(prompt):
    url = "http://3.88.181.187:8080/v1/"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"  # setting up a session state model

if "messages" not in st.session_state:
    # st.session_state.messages = [] # setting up a session state messages to store the messages
    # set a default message hi to the bot before the user types anything
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi, I'm OpenEyes. I'm here to help you with your queries related to Animals. What do you want to know?",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # creating a chat message with the role
        st.markdown(message["content"])  # adding the content to the chat message

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response = makeRequest(prompt)
        for chunk in response["choices"][0]["message"]["content"].split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

print(st.session_state.messages)