from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings  
from dotenv import load_dotenv

load_dotenv()

PASTA_BASE = "base"

# Função principal para criar a base de dados
def criar_db():
    documentos = carregar_pdf()
    chunks = dividir_documentos(documentos)
    vetorizar_chunks(chunks)

# Função para carregar os PDFs da pasta base
def carregar_pdf():
    carregador = PyPDFDirectoryLoader(PASTA_BASE, glob="**/*.pdf")
    documentos = carregador.load()
    return documentos

# Função para dividir os documentos em chunks menores
def dividir_documentos(documentos):
    separador_texto = RecursiveCharacterTextSplitter(
        chunk_size=900, 
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = separador_texto.split_documents(documentos)
    return chunks

# Função para vetorizar os chunks usando embeddings
def vetorizar_chunks(chunks):
    # Aqui você pode adicionar a lógica para vetorizar os chunks usando o modelo de sua escolha
    embeddings = OpenAIEmbeddings()
    Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory="db")
    print(f"Documentos divididos em {len(chunks)} chunks.")
    print("Vetorizações concluídas e armazenadas no banco de dados.")
    
criar_db()

