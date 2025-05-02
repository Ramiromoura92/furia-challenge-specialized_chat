import os
from decouple import config
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import AsyncChromiumLoader 
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_extraction_chain

os.environ['OPENAI_API-KEY'] = config('OPENAI_API-KEY')

llm = ChatOpenAI(

    model = 'gpt-4o-mini',
    temperature = 0.5,
    
    )

schema = {

    'properties':{

        'line-up titular':{'type':'String'},
        'reservas':{'type':'string'},
        'coach':{'type':'string'},
        'resultados':{'type':'integer'}

    },

    'type': 'object',  # Obrigatório para o create_extraction_chain funcionar
    'required': ['line-up titular', 'reservas', 'coach', 'resultados']
}
def extract(content,schema):
    return create_extraction_chain(
        schema=schema,
        llm=llm
    ).invoke(content).get('text')
    
def scrape_with_playwright(urls, schema):

    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformed = BeautifulSoupTransformer()
    doc_transformed = bs_transformed.transform_documents(
        documents=docs,
        tags_to_extract=['table','a','div','h1','h2','p','svg']
    )
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(

        chunk_size = 2000,
        chunk_overlap = 0  
    )
    splits = splitter.split_documents(

        documents=doc_transformed,
    )

    extracted_content = []

    for split in splits:
        extracted_content.extend(
            extract(schema = schema,
            content = split.page_content,)
            
        )
    return extracted_content

if __name__== '__main__':
    urls = ['']

    extracted_contents = scrape_with_playwright(

        urls=urls,
        schema=schema
    )

    print(extracted_contents)