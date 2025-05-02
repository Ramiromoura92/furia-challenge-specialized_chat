import os
import json
from decouple import config
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import AsyncChromiumLoader 
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel, Field  # Novo import


os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

llm = ChatOpenAI(
    model='gpt-4o',
    temperature=0.5,
)

# ✅ Novo schema usando Pydantic
class TimeInfo(BaseModel):
    lineup_titular: str = Field(..., description="Line-up Titular")
    reservas: str = Field(..., description="Reservas")
    coach: str = Field(..., description="Coach")
    jogos: str = Field(...,description="Jogos")
    resultados: str = Field(..., description="Resultados")
    estatisticas_da_partida: float = Field(...,description="Estatísticas da partida")
    o_jogo:str = Field(...,description="O jogo")
    mapas:str = Field(...,description="Mapas")
    vetos:str = Field(...,description="Vetos")
    confontros:str = Field(...,description="Confrontos diretos")
    resultados_recentes:str = Field(...,description="Resultados recentes")
    noticias:str = Field(...,description="Noticias")
    campeonatos:str = Field(...,description="Próximos Campeonatos")
    partidas:str = Field(...,description="quarta-feira, 9 de abril de 2025, ")


# ✅ Atualizado: usando with_structured_output
structured_llm = llm.with_structured_output(TimeInfo)

def extract(content):
    return structured_llm.invoke(content)

def scrape_with_playwright(urls):

    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformed = BeautifulSoupTransformer()
    doc_transformed = bs_transformed.transform_documents(
        documents=docs,
        tags_to_extract=['table','a','div','h1','h2','p','svg','script']
    )
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=2000,
        chunk_overlap=0  
    )
    splits = splitter.split_documents(doc_transformed)

    extracted_content = []

    for split in splits:
        result = extract(split.page_content)
        extracted_content.append(result)

    return extracted_content

if __name__ == '__main__':
    urls = ['https://draft5.gg/equipe/330-FURIA',
            'https://draft5.gg/equipe/330-FURIA/resultados',
            'https://draft5.gg/equipe/330-FURIA/campeonatos',
            'https://draft5.gg/partida/36342-FURIA-vs-The-MongolZ-PGL-Bucharest-2025',
            'https://draft5.gg/partida/36349-FURIA-vs-Virtus.pro-PGL-Bucharest-2025,'
            'https://draft5.gg/partida/36328-FURIA-vs-Complexity-PGL-Bucharest-2025',
            'https://draft5.gg/partida/36197-FURIA-vs-Apogee-PGL-Bucharest-2025',
            'https://draft5.gg/partida/35425-M80-vs-FURIA-BLAST-Open-Lisbon-2025',
            'https://draft5.gg/noticia/furia-apresenta-ex-falcons-como-novo-auxiliar-tecnico',
             
            ]  # Adicione uma URL válida

    extracted_contents = scrape_with_playwright(urls)
    print(extracted_contents)

with open('results2.json','w',encoding='utf-8') as f:
    json.dump([res.model_dump()for res in extracted_contents],f, ensure_ascii=False, indent=4)