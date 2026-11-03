import streamlit as st
from main import perguntar


st.set_page_config(page_title="Assistente IA", page_icon="🤖")
st.title("Assistente IA - EstiloBot")
st.caption("Faça perguntas sobre a nossa empresa que nosso assistente de IA vai te responder.")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

with st.sidebar:
    st.subheader("Conversa")
    if st.button("Limpar conversa", use_container_width=True):
        st.session_state.mensagens = []
        st.rerun()

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

pergunta_usuario = st.chat_input("Digite sua pergunta...")
if pergunta_usuario:
    st.session_state.mensagens.append(
        {"role": "user", "content": pergunta_usuario}
    )
    with st.chat_message("user"):
        st.markdown(pergunta_usuario)

    with st.chat_message("assistant"):
        with st.spinner("Consultando a base de conhecimento..."):
            resposta = perguntar(
                pergunta_usuario,
                historico=st.session_state.mensagens[:-1],
            )
        st.markdown(resposta)

    st.session_state.mensagens.append(
        {"role": "assistant", "content": resposta}
    )
