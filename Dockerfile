FROM python:3.12.2-slim

# Define o diretório de trabalho principal
WORKDIR /app

# Copia todos os arquivos para dentro do container
ADD . /app

# Define o diretório de trabalho onde está seu app Streamlit
WORKDIR /app/src

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Evita criação de arquivos .pyc e habilita logs no console
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Executa a aplicação Streamlit
ENTRYPOINT ["streamlit", "run", "main_with_rag.py", "--server.port=8501", "--server.address=0.0.0.0"]
