from openai import OpenAI
import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_web_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    return text[:3000]  # limit characters to fit into prompt


st.title("ChatGPT-like clone")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

url = "https://draft5.gg/equipe/330-FURIA"
context = fetch_web_content(url)

print(context)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Set up messages with prompt engineering via a system message
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": f"Você é um assistente que vai ajudar os fãs do time furia de Counter Strike, provendo informações sobre os jogadores, competições, resultados e próximos eventos.Consulte esse material para dados gerais:{context}"
        }
    ]

# Display message history
for message in st.session_state.messages[1:]:  # skip system message in UI
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
