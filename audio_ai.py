from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Carregando a chave da API do OpenAI a partir das variáveis de ambiente
api_key = os.getenv("OPENAI_API_KEY")
if not api_key: 
    raise RuntimeError("Defina a variável OPENAI_API_KEY no ambiente ou no arquivo .env.")

# Criando o cliente OpenAI com a chave da API
client = OpenAI(api_key=api_key)

# Exemplo de uso: Gerar uma resposta em texto e convertê-la em áudio
prompt = "Qual o roadmap que preciso estudar para me tornar um desenvolvedor Python backend?"

# Gerando a resposta em texto usando o modelo de linguagem
resposta_texto = client.chat.completions.create(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    messages=[{"role": "user", "content": prompt}],
)

# Extraindo o texto da resposta
texto_para_falar = resposta_texto.choices[0].message.content.strip()

# Convertendo o texto em áudio usando o modelo de TTS (Text-to-Speech)
resposta_audio = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=texto_para_falar,
)

# Salvando o áudio em um arquivo WAV
resposta_audio.write_to_file("audio.wav")
 