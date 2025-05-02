from openai import OpenAI
import streamlit as st
import faiss
import numpy as np
import json

st.title("ChatGPT com RAG")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Carregar índice FAISS
index = faiss.read_index("docs.index")

# Carregar os documentos
with open("documents.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

#import ipdb; ipdb.set_trace()
def get_relevant_chunks(query, k=10):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=query
    )
    query_embedding = np.array(response.data[0].embedding).astype("float32")
    D, I = index.search(np.array([query_embedding]), k)
    
    # Aqui garantimos que retornamos apenas strings
    return [str(documents[i]) for i in I[0] if i < len(documents)]

# Mensagens da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Faça sua pergunta:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Recupera os trechos relevantes
    retrieved_docs = get_relevant_chunks(prompt)
    context = "\n\n".join(retrieved_docs)
    print(context)

    # Monta a prompt com contexto recuperado
    full_messages = [
        {
            "role": "system",
            "content": f"Você é um assistente que vai ajudar os fãs do time furia de counter strike, provendo informações sobre os jogadores, competições, resultados e próximos eventos. Use o seguinte contexto para responder:\n\n{context}"
        },
        *st.session_state.messages
    ]

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=full_messages,
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
