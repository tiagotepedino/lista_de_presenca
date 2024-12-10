import streamlit as st
import sqlite3
from datetime import datetime

# Configurações iniciais do app
st.set_page_config(page_title="Lista de Presença", layout="wide", initial_sidebar_state="collapsed")

# Estilização personalizada
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .css-18e3th9 {padding-top: 50px;}
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 20px;
    }
    .top-bar {
        background-color: #4A7A8C;
        padding: 20px;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
    }
    .top-bar .title {
        text-align: center;
        color: white;
    }
    .form-container {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        margin-top: 20px;
    }
    .form-container input, .form-container select {
        border: 1px solid #D1D1D1;
        border-radius: 5px;
        padding: 10px;
        font-size: 14px;
        width: 100%;
    }
    .form-container button {
        background-color: #4A7A8C;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease;
        width: 100%;
    }
    .form-container button:hover {
        background-color: #376075;
    }
    .form-container .col {
        display: inline-block;
        width: 48%;
        margin-right: 2%;
        vertical-align: top;
    }
    .form-container .col:last-child {
        margin-right: 0;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Função para criar a tabela no SQLite
def create_table():
    conn = sqlite3.connect("lista_presenca.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS presenca (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf_matricula TEXT NOT NULL,
            empresa TEXT NOT NULL,
            horario TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Função para salvar dados no SQLite
def save_data(name, cpf_matricula, empresa, time):
    conn = sqlite3.connect("lista_presenca.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO presenca (nome, cpf_matricula, empresa, horario) VALUES (?, ?, ?, ?)",
                   (name, cpf_matricula, empresa, time))
    conn.commit()
    conn.close()

# Criar a tabela no banco de dados
create_table()

# Barra fixa no topo
st.markdown(
    """
    <div class="top-bar">
        <div class="title">Lista de Presença</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Layout em contêiner
st.markdown("<h3 class='section-title' style='margin-top: 80px;'>Registro de Presença</h3>", unsafe_allow_html=True)
with st.container():
    with st.form(key="attendance_form"):
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nome", placeholder="Digite seu nome completo")
            cpf_matricula = st.text_input("CPF ou Matrícula", placeholder="Digite seu CPF ou matrícula")
        with col2:
            empresa = st.selectbox("Empresa", ["Loram", "Prioriza", "Outra"])
            st.markdown("<br>", unsafe_allow_html=True)  # Espaçamento antes do botão
            submit_button = st.form_submit_button("Registrar Presença", type="primary")

        if submit_button:
            if name and cpf_matricula and empresa:
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_data(name, cpf_matricula, empresa, time_now)
                st.success(f"Presença registrada com sucesso às {time_now}!")
            else:
                st.error("Por favor, preencha todos os campos.")
        st.markdown("</div>", unsafe_allow_html=True)
