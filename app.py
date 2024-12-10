import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Configurações iniciais do app
st.set_page_config(page_title="Lista de Presença", layout="centered", initial_sidebar_state="collapsed")

# Estilização personalizada
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Barra fixa no topo */
    .title-bar {
        background-color: #8B0000;
        padding: 10px 20px;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000; /* Garante que fique acima de tudo */
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
        height: 60px; /* Altura fixa */
    }

    /* Ajusta o conteúdo para ficar abaixo da barra */
    .content {
        margin-top: 65px; /* Reduzido para minimizar a distância */
    }

    /* Formulário estilizado */
    .form-container {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        max-width: 600px; /* Limita a largura do formulário */
        margin: 0 auto; /* Centraliza o formulário */
    }
    .form-container input, .form-container select {
        border: 1px solid #D1D1D1;
        border-radius: 5px;
        padding: 10px;
        font-size: 14px;
        width: 100%;
        margin-bottom: 15px;
    }
    .form-container button {
        background-color: #8B0000;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease;
        width: 100%;
        margin-top: 20px;
    }
    .form-container button:hover {
        background-color: #6A0000;
    }
    </style>
"""
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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
            treinamento TEXT NOT NULL,
            horario TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Função para salvar dados no SQLite
def save_data(name, cpf_matricula, empresa, treinamentos, time):
    conn = sqlite3.connect("lista_presenca.db")
    cursor = conn.cursor()
    treinamentos_str = ", ".join(treinamentos)
    cursor.execute(
        "INSERT INTO presenca (nome, cpf_matricula, empresa, treinamento, horario) VALUES (?, ?, ?, ?, ?)",
        (name, cpf_matricula, empresa, treinamentos_str, time)
    )
    conn.commit()
    conn.close()

# Criar a tabela no banco de dados
create_table()

# Barra fixa no topo
st.markdown(
    """
    <div class="title-bar">Lista de Presença</div>
    """,
    unsafe_allow_html=True
)

# Certificar que o conteúdo começa abaixo da barra fixa
st.markdown("<div class='content'>", unsafe_allow_html=True)

# Título e formulário
st.markdown("<h3 style='margin-top: 0;'>Registro de Presença</h3>", unsafe_allow_html=True)
with st.container():
    with st.form(key="attendance_form"):
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        
        # Campos de entrada
        name = st.text_input("Nome", placeholder="Digite seu nome completo")
        cpf_matricula = st.text_input("CPF ou Matrícula", placeholder="Digite seu CPF ou matrícula")
        empresa = st.selectbox("Empresa", ["Loram", "Prioriza", "Outra"])
        
        # Checkboxes para seleção dos tipos de treinamento
        treinamentos = []
        if st.checkbox("Treinamento GQI e Relatório de Qualidade"):
            treinamentos.append("Treinamento GQI e Relatório de Qualidade")
        if st.checkbox("Treinamento de Gerenciamento de Dados do RIV"):
            treinamentos.append("Treinamento de Gerenciamento de Dados do RIV")

        # Botão de registro
        submit_button = st.form_submit_button("Registrar Presença", type="primary")
        
        if submit_button:
            if not name.strip():
                st.error("O campo Nome é obrigatório. Por favor, preencha-o.")
            elif not cpf_matricula.strip():
                st.error("O campo CPF ou Matrícula é obrigatório. Por favor, preencha-o.")
            elif not treinamentos:
                st.error("Selecione pelo menos um tipo de treinamento.")
            else:
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_data(name, cpf_matricula, empresa, treinamentos, time_now)
                st.success(f"Presença registrada com sucesso às {time_now}!")
        st.markdown("</div>", unsafe_allow_html=True)

# Fechar o div de conteúdo
st.markdown("</div>", unsafe_allow_html=True)
