from collections.abc import Sequence
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


ROOT_DIR = Path(__file__).resolve().parent
CAMINHO_DB = ROOT_DIR / "db"
load_dotenv(ROOT_DIR / ".env")

PROMPT_TEMPLATE = """
Você responde perguntas somente com base no contexto dos documentos abaixo.
Use o histórico apenas para entender referências e perguntas de acompanhamento;
ele não é uma fonte de fatos. Se a resposta não estiver nos documentos, diga:
"Desculpe, não sei a resposta para isso."

Interprete a intenção da pergunta, mesmo quando ela usar palavras diferentes
das utilizadas nos documentos. Quando perguntarem como agendar um horário,
marcar uma visita ou solicitar um orçamento, procure no contexto por telefones,
WhatsApp e e-mail. Se houver contatos, informe-os como canais para consultar
ou solicitar o agendamento e esclareça quando o documento não descreve um
procedimento específico. Não responda apenas que não sabe se houver contatos
relevantes disponíveis. Não afirme que um agendamento foi confirmado nem
invente etapas, horários disponíveis ou serviços.

<historico>
{historico}
</historico>

<contexto>
{base_conhecimento}
</contexto>

Pergunta atual: {pergunta}

Responda diretamente em português.
"""

RESPOSTA_SEM_CONTEXTO = "Desculpe, não sei a resposta para isso."


@lru_cache(maxsize=1)
def _carregar_banco() -> Chroma:
    if not CAMINHO_DB.is_dir():
        raise FileNotFoundError(
            f"A base vetorial não foi encontrada em: {CAMINHO_DB}"
        )

    return Chroma(
        persist_directory=str(CAMINHO_DB),
        embedding_function=OpenAIEmbeddings(),
    )


@lru_cache(maxsize=1)
def _carregar_modelo() -> ChatOpenAI:
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.3, max_tokens=500)


def perguntar(
    pergunta: str,
    historico: Sequence[dict[str, str]] | None = None,
) -> str:
    """Busca informações na base e responde à pergunta em português."""
    pergunta = pergunta.strip()
    if not pergunta:
        raise ValueError("A pergunta não pode estar vazia.")

    mensagens_validas = [
        mensagem
        for mensagem in (historico or [])
        if mensagem.get("role") in {"user", "assistant"}
        and mensagem.get("content", "").strip()
    ]
    historico_prompt = "\n".join(
        f"{mensagem['role']}: {mensagem['content']}"
        for mensagem in mensagens_validas[-6:]
    )
    consulta_busca = "\n".join(
        [mensagem["content"] for mensagem in mensagens_validas[-4:]]
        + [pergunta]
    )

    banco = _carregar_banco()
    resultados = banco.similarity_search_with_score(consulta_busca, k=7)
    if not resultados:
        return RESPOSTA_SEM_CONTEXTO

    base_conhecimento = "\n".join(
        documento.page_content for documento, _ in resultados
    )
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    mensagens = prompt.invoke(
        {
            "historico": historico_prompt,
            "base_conhecimento": base_conhecimento,
            "pergunta": pergunta,
        }
    )

    resposta = _carregar_modelo().invoke(mensagens)
    if not isinstance(resposta.content, str):
        raise TypeError("O modelo retornou uma resposta em formato inesperado.")
    return resposta.content


def main() -> None:
    pergunta_usuario = input("Qual é a sua pergunta? ").strip()
    if not pergunta_usuario:
        print("Digite uma pergunta para continuar.")
        return

    print(perguntar(pergunta_usuario))


if __name__ == "__main__":
    main()
