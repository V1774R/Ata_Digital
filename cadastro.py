import streamlit as st
from utils import conn

st.write('# ATA GCMR - CADASTRO')

nome = st.text_input("Nome do agente")
matricula = st.text_input("Matricula do agente")
graduacao = st.selectbox("Graduação do agente", options=["GCM.", "SI.", "INSP."])
face = st.file_uploader("Imagem do agente.", type=["jpn", "jpeg", "png"])

if st.button("cadastrar"):
    conn.inserir_cadastro(nome, matricula, graduacao, face)

