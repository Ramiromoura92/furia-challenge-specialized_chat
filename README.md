## Challenge #1 **🧩**


🎯 Esse projeto foi desenvolvido com o objetivo de resolver um desafio proposto pela FURIA na criação de um ambiente onde os fãs da FURIA CS pudessem usufruir.


### **Tecnologias utilizadas 💡**

---

O projeto foi todo desenvolvido em python, utilizando Streamlit, OpenAI, Faiss, LangChain, Pydantic, Playwright, BeautifulSoup e Docker


├── Dockerfile
├── README.md
├── requirements.txt
└── src
    ├── data
    │   ├── docs.index
    │   ├── documents.json
    │   ├── results2.json
    ├── images
    │   ├── avatar.png
    ├── utils
    │   ├── embbedings.py
    │   ├── web_scraping.py
    └── main_with_rag.py


- **Dockerfile:** contém as definições do container (Docker).
- **requirements.txt:** arquivo com todos os pacotes necessários para rodar este projeto.
- **docs.index:** contém o índice de documentos, que pode ser usado para mapear o conteúdo e facilitar a busca e análise de documentos no sistema.
- **documents.json:** contém os dados brutos dos documentos.
- **result2.json:** armazena os resultados do processamento dos documentos.
- **avatar.png:** imagem utilizada para estilizar o chat.
- **embbedings.py:** arquivo que utiliza a API da OpenAI para fazer embbeding dos textos a partir de um arquivo JSON.
- **web_scraping.py:** arquivo que que realiza o scraping das informações das páginas webs de uma forma estruturada.
- **main_with_rag.py:** arquivo principal que cria um assistente interativo.

1. Abra o terminal dentro do diretório do projeto.

2. Instale as dependências do projeto, aqui o ideal é ter um ambiente virtual já criado.
    `pip install -r requirements.txt`

3. Após a isntalação das depências, rodar os seguintes comandos:
    ` 1 -Para fazer o scraping da página: python3 web_scraping.py`

    ` 2 -Após o scraping, realizar o embbeding: python3 embbedings.py`

    ` 2 -Após o embedding, subir a interação: streamlit run main_with_rag.py`

Esta aplicação foi testa nas versões Python 3.10.0.
Caso não tenha a versões acima disponível e/ou prefira rodar em docker, criei um Dockerfile para executar a aplicação. Execute os seguintes comandos na raíz do repositório para subir a aplicação:

`docker build -t myapp .`

`docker run -d -p 8501:8501 myapp:1.0 `

**Obs.:** Após rodar o último comando aparecerá um código do tipo: 6d7f3f69d0820f9c720a729bb8c4b6303cac170fe03a747aa71cd8a26f2b6e7d

![Arquitetura solução](arquitetura_proposta.png)