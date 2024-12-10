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
        background-color: #8B0000;
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
    }
    .section-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Função para criar a tabela no SQLite
def create_table():
    conn = sqlite3.connect("lista_presenca.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS presenca_gqi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf_matricula TEXT NOT NULL,
            empresa TEXT NOT NULL,
            horario TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS presenca_riv (
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
def save_data(table_name, name, cpf_matricula, empresa, time):
    conn = sqlite3.connect("lista_presenca.db")
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} (nome, cpf_matricula, empresa, horario) VALUES (?, ?, ?, ?)", 
                   (name, cpf_matricula, empresa, time))
    conn.commit()
    conn.close()

# Função para obter os dados do banco
def get_data(table_name):
    conn = sqlite3.connect("lista_presenca.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT nome, cpf_matricula, empresa, horario FROM {table_name}")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Criar as tabelas no banco de dados
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

# Escolher o treinamento
st.markdown("<h2 style='text-align: center;'>Selecione o Treinamento</h2>", unsafe_allow_html=True)
treinamento = st.selectbox("Treinamento:", 
                           ["Treinamento GQI e Relatório de Qualidade", "Treinamento de Gerenciamento de Dados do RIV"])

# Nome da tabela no banco de dados
table_name = "presenca_gqi" if treinamento == "Treinamento GQI e Relatório de Qualidade" else "presenca_riv"

# Layout em colunas para o formulário
st.markdown("<h3 class='section-title'>Registro de Presença</h3>", unsafe_allow_html=True)
with st.container():
    with st.form(key="attendance_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nome", placeholder="Digite seu nome completo")
            cpf_matricula = st.text_input("CPF ou Matrícula", placeholder="Digite seu CPF ou matrícula")
        with col2:
            empresa = st.selectbox("Empresa", ["Loram", "Prioriza", "Outra"])
            submit_button = st.form_submit_button("Registrar Presença")

        if submit_button:
            if name and cpf_matricula and empresa:
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_data(table_name, name, cpf_matricula, empresa, time_now)
                st.success(f"Presença registrada com sucesso às {time_now}!")
            else:
                st.error("Por favor, preencha todos os campos.")

# Exibir a lista de presença
st.markdown("<h3 class='section-title'>Lista de Presença Registrada</h3>", unsafe_allow_html=True)
data = get_data(table_name)
if data:
    df = [{"Nome": row[0], "CPF/Matrícula": row[1], "Empresa": row[2], "Horário": row[3]} for row in data]
    st.dataframe(df)
else:
    st.info("Nenhuma presença registrada ainda.")
