# RAG_Agentes_AI

Sistema de perguntas e respostas utilizando **RAG (Retrieval-Augmented Generation)**, Python, LangChain, OpenAI e ChromaDB.

O projeto permite fazer perguntas em linguagem natural e obter respostas baseadas nos documentos armazenados em uma base de conhecimento vetorial.

## Objetivo

O objetivo do projeto é criar um assistente inteligente capaz de:

- Consultar documentos próprios;
- Encontrar informações semanticamente relevantes;
- Utilizar modelos de linguagem para gerar respostas;
- Evitar respostas sem relação com a base de conhecimento;
- Servir como base para futuras integrações com agentes e WhatsApp.

## Tecnologias utilizadas

- **Python** — linguagem principal;
- **LangChain** — integração e organização do fluxo de IA;
- **OpenAI Embeddings** — conversão de textos em vetores;
- **ChatOpenAI** — geração das respostas;
- **ChromaDB** — armazenamento e busca vetorial;
- **python-dotenv** — carregamento de variáveis de ambiente;
- **GPT-4o-mini** — modelo utilizado para gerar as respostas.

## Como o projeto funciona

O sistema segue o fluxo abaixo:

```text
Pergunta do usuário
        |
        v
Conversão da pergunta em embedding
        |
        v
Busca semântica no ChromaDB
        |
        v
Recuperação dos documentos mais relevantes
        |
        v
Montagem do prompt com o contexto
        |
        v
Geração da resposta pelo GPT-4o-mini
        |
        v
Resposta em português
```

O modelo recebe a pergunta junto com os documentos encontrados. Dessa forma, ele consegue responder com base no conteúdo disponível na base de conhecimento.

## Estrutura do projeto

```text
RAG_Agentes_AI/
├── db/                 # Banco vetorial persistido pelo ChromaDB
├── main.py             # Lógica RAG e modo de execução pelo terminal
├── app.py              # Interface de conversa com Streamlit
├── .env                # Variáveis de ambiente locais
├── .env.example        # Modelo das variáveis necessárias
├── .gitignore          # Arquivos ignorados pelo Git
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação
```

## Pré-requisitos

- Python 3.10 ou superior;
- Uma chave de API da OpenAI;
- Git, caso deseje clonar o repositório;
- Uma base vetorial criada na pasta `db`.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/Cleverson10C/rag-agentes-ai.git
cd RAG_Agentes_AI
```

Crie um ambiente virtual:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a ativação, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

## Configuração da API

Crie um arquivo chamado `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua_chave_da_openai
```

Também é possível criar um arquivo `.env.example` para documentar as variáveis necessárias:

```env
OPENAI_API_KEY=sua_chave_aqui
```

> Nunca compartilhe ou publique sua chave da OpenAI.

## Arquivo `.gitignore`

O arquivo `.gitignore` deve conter:

```gitignore
.env
.env.*
!.env.example
.venv/
__pycache__/
*.pyc
```

Se o arquivo `.env` já tiver sido adicionado ao Git, remova-o do controle de versão:

```powershell
git rm --cached .env
git commit -m "Remove arquivo .env do versionamento"
```

## Executando o projeto

Com o ambiente virtual ativado, você pode iniciar a interface de conversa:

```powershell
streamlit run app.py
```

O chatbot mantém o histórico durante a sessão e usa as mensagens anteriores
para interpretar perguntas de acompanhamento. A conversa pode ser reiniciada
pelo botão **Limpar conversa**.

Para fazer uma pergunta diretamente pelo terminal, execute:

```powershell
python main.py
```

O sistema solicitará uma pergunta:

```text
Qual é a sua pergunta?
```

Exemplo:

```text
Qual é a política de atendimento?
```

A aplicação consultará a base vetorial e exibirá a resposta gerada pela inteligência artificial.

## Funcionamento do código

A aplicação carrega as variáveis de ambiente:

```python
load_dotenv()
```

Depois, inicializa os embeddings e conecta-se ao banco vetorial:

```python
funcao_embeddings = OpenAIEmbeddings()

db = Chroma(
    persist_directory="db",
    embedding_function=funcao_embeddings
)
```

A pergunta é comparada com os documentos armazenados no ChromaDB:

```python
resultado_similaridade = db.similarity_search_with_score(
    pergunta,
    k=7
)
```

Nesse caso, são recuperados até sete documentos semelhantes à pergunta.

Em seguida, os conteúdos encontrados são reunidos e enviados ao modelo por meio de um prompt:

```python
base_conhecimento = "\n".join(
    doc.page_content for doc, _ in resultado_similaridade
)
```

O modelo recebe a instrução para responder somente com base no contexto recuperado. Quando a informação não está disponível, ele deve informar:

```text
Desculpe, não sei a resposta para isso.
```

## Banco de dados vetorial

A pasta `db` contém a base vetorial utilizada pelo sistema.

Para que o projeto funcione corretamente, essa pasta precisa conter documentos previamente processados e transformados em embeddings.

O ChromaDB permite realizar buscas por similaridade semântica. Isso significa que a aplicação não procura apenas palavras iguais, mas também conteúdos com significado semelhante.

## Geração da base de conhecimento

A base de conhecimento deve ser criada antes da execução da aplicação principal.

Um processo de ingestão pode incluir:

1. Leitura dos documentos;
2. Divisão dos textos em trechos menores;
3. Geração dos embeddings;
4. Armazenamento dos vetores no ChromaDB;
5. Persistência dos dados na pasta `db`.

Essa etapa ainda pode ser automatizada em um módulo específico de carregamento de documentos.

## Principais benefícios

- Permite consultar documentos próprios;
- Reduz respostas genéricas;
- Facilita a atualização da base de conhecimento;
- Utiliza busca semântica;
- Pode ser adaptado para diferentes áreas;
- Possibilita integração com aplicações web e mensageria;
- Serve como base para criação de agentes especializados.

## Limitações atuais

O projeto mantém algumas limitações:

- A base de conhecimento precisa ser preparada previamente;
- O histórico do chatbot existe apenas enquanto a sessão do Streamlit estiver ativa;
- Não existe autenticação de usuários;
- A integração com WhatsApp ainda não foi implementada;
- O sistema ainda não possui avaliação automática das respostas;
- O projeto ainda não possui testes automatizados completos.

## Próximos passos

As principais melhorias planejadas são:

- Implementar integração com WhatsApp;
- Criar uma API utilizando FastAPI;
- Desenvolver uma interface web;
- Automatizar o upload e processamento de documentos;
- Implementar histórico de conversas;
- Adicionar autenticação de usuários;
- Exibir as fontes utilizadas na resposta;
- Criar testes automatizados;
- Adicionar tratamento avançado de erros;
- Melhorar a avaliação da busca semântica;
- Implementar agentes especializados;
- Adicionar monitoramento e registro das interações;
- Permitir o uso de diferentes modelos de linguagem.

## Possível integração com WhatsApp

A integração futura com WhatsApp poderá utilizar uma API oficial ou um provedor compatível.

O fluxo planejado será:

```text
Mensagem recebida no WhatsApp
        |
        v
API recebe a mensagem
        |
        v
Sistema realiza a busca no ChromaDB
        |
        v
Modelo gera a resposta
        |
        v
Resposta enviada ao WhatsApp
```

Essa integração permitirá transformar o projeto em um assistente acessível diretamente por mensagens.

## Segurança

Algumas práticas importantes:

- Nunca publique o arquivo `.env`;
- Não compartilhe chaves da OpenAI;
- Utilize variáveis de ambiente;
- Não armazene dados sensíveis sem proteção;
- Revogue uma chave imediatamente caso ela seja exposta;
- Controle o acesso aos documentos da base de conhecimento;
- Valide as entradas recebidas pelo sistema.

## Gerando o arquivo de dependências

Para gerar ou atualizar o arquivo `requirements.txt`:

```powershell
python -m pip freeze > requirements.txt
```

Para instalar as dependências posteriormente:

```powershell
python -m pip install -r requirements.txt
```

## Contribuição

Contribuições são bem-vindas.

Para contribuir:

1. Faça um fork do projeto;
2. Crie uma nova branch:

```bash
git checkout -b minha-melhoria
```

3. Faça as alterações;
4. Teste o projeto;
5. Realize o commit:

```bash
git commit -m "Adiciona nova melhoria"
```

6. Envie a branch:

```bash
git push origin minha-melhoria
```

7. Abra um Pull Request.

## Licença

Este projeto pode ser distribuído sob a licença MIT. Caso essa licença seja escolhida, adicione um arquivo chamado `LICENSE` ao repositório.

## Autor

Desenvolvido por **Cleverson** como projeto prático de estudos e desenvolvimento em:

- Inteligência Artificial Generativa;
- Arquitetura RAG;
- Busca semântica;
- Bancos de dados vetoriais;
- Engenharia de prompts;
- Integração com modelos de linguagem;
- Desenvolvimento de agentes inteligentes.