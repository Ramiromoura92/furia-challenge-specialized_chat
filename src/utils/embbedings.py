import faiss
import numpy as np
import streamlit as st
from openai import OpenAI
import json

# Cliente novo da OpenAI
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Carrega documentos do JSON
with open("../data/documents.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

# Função para gerar embedding de texto
def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

# Filtrar e embutir apenas o texto desejado (exemplo: 'lineup_titular')
doc_embeddings = [embed_text(f"{doc.get('campeonatos_em_andamento', '')} {doc.get('resultados_2025', '')}{doc.get('integrantes_time', '')} {doc.get('lineup_titular', '')} {doc.get('reservas', '')} {doc.get('coach', '')} {doc.get('resultados', '')} {doc.get('estatisticas_da_partida', '')} {doc.get('o_jogo', '')} {doc.get('mapas', '')} {doc.get('vetos', '')} {doc.get('confontros', '')} {doc.get('resultados_recentes', '')} {doc.get('noticias', '')} {doc.get('campeonatos', '')} {doc.get('redes_sociais_furia', '')} {doc.get('redes_sociais_jogadores', '')} {doc.get('redes_sociais_coach', '')}") for doc in documents]

# Criar índice FAISS
index = faiss.IndexFlatL2(len(doc_embeddings[0]))
index.add(np.array(doc_embeddings).astype("float32"))

# Salvar índice em disco
faiss.write_index(index, "docs.index")
