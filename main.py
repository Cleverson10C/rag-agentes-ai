from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv 

load_dotenv()

CAMINHO_DB = "db"  

# Função para realizar a busca semântica e responder à pergunta do usuário
prompt_template = """
Você responde perguntas somente com base no contexto abaixo.

<contexto>
{base_conhecimento}
</contexto>

Pergunta: 

{pergunta}

Responda diretamente em português. Se a resposta não estiver no contexto, diga:
"Desculpe, não sei a resposta para isso."
"""


# função para realizar a busca semântica e responder à pergunta do usuário
def perguntar(pergunta):
    # Carregar a base de conhecimento do banco de dados
    funcao_embeddings = OpenAIEmbeddings()
    db = Chroma(
        persist_directory=CAMINHO_DB,
        embedding_function=funcao_embeddings
    )
    
    # Comparar a pergunta do usuário com os documentos da base de conhecimento
    resultado_similaridade = db.similarity_search_with_score(pergunta, k=7)

    if not resultado_similaridade:
        return "Desculpe, não sei a resposta para isso."

    base_conhecimento = "\n".join(
        doc.page_content for doc, _ in resultado_similaridade
    )
    
    # Extrair o conteúdo dos documentos mais semelhantes
    prompt = ChatPromptTemplate.from_template(prompt_template)
    mensagens = prompt.invoke({
        "pergunta": pergunta,
        "base_conhecimento": base_conhecimento
    })

    # Criar um modelo de linguagem para gerar a resposta
    modelo = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, max_tokens=150)
    resposta = modelo.invoke(mensagens)
    return resposta.content

# A função principal para interação do usuário faz a pergunta e resposta da IA
pergunta_usuario = input("Qual é a sua pergunta? ")
print(perguntar(pergunta_usuario))