import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Configurações iniciais do app
st.set_page_config(page_title="Lista de Presença", layout="centered")

# Estilização personalizada
custom_style = """
    <style>
    /* Ocultar menus e rodapé */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Barra de título */
    .title-bar {
        background-color: #8B0000;
        padding: 10px;
        color: white;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    /* Centralizar o formulário */
    .form-container {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        max-width: 600px;
        margin: 0 auto;
    }

    /* Inputs e botões */
    input, select {
        border: 1px solid #D1D1D1;
        border-radius: 5px;
        padding: 10px;
        font-size: 14px;
        width: 100%;
        margin-bottom: 15px;
    }
    button {
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
    button:hover {
        background-color: #6A0000;
    }

    /* Tabela de presença */
    .dataframe {
        margin-top: 20px;
        border-radius: 8px;
        overflow: hidden;
    }
    .dataframe th {
        background-color: #8B0000;
        color: white;
        text-align: center;
        padding: 10px;
    }
    .dataframe td {
        text-align: center;
        padding: 8px;
    }
    </style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

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

# Função para buscar os dados do banco
def fetch_data():
    conn = sqlite3.connect("lista_presenca.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, cpf_matricula, empresa, treinamento, horario FROM presenca")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Criar a tabela no banco de dados
create_table()

# Barra de título
st.markdown('<div class="title-bar">Lista de Presença</div>', unsafe_allow_html=True)

# Criar o formulário
with st.container():
    with st.form(key="attendance_form"):
        st.markdown('<div class="form-container">', unsafe_allow_html=True)

        # Campos de entrada
        name = st.text_input("Nome", placeholder="Digite seu nome completo", key="name_input").strip()
        cpf_matricula = st.text_input("CPF ou Matrícula", placeholder="Digite seu CPF ou matrícula", key="cpf_input").strip()
        empresa = st.selectbox("Empresa", ["Loram", "Prioriza", "Outra"])
        
        # Checkboxes para treinamentos
        treinamentos = []
        if st.checkbox("Treinamento GQI e Relatório de Qualidade"):
            treinamentos.append("Treinamento GQI e Relatório de Qualidade")
        if st.checkbox("Treinamento de Gerenciamento de Dados do RIV"):
            treinamentos.append("Treinamento de Gerenciamento de Dados do RIV")

        # Botão para envio
        submit_button = st.form_submit_button("Registrar Presença")

        if submit_button:
            # Verificações
            if not name:
                st.error("O campo Nome é obrigatório. Por favor, preencha-o.")
            elif not cpf_matricula:
                st.error("O campo CPF ou Matrícula é obrigatório. Por favor, preencha-o.")
            elif not treinamentos:
                st.error("Selecione pelo menos um tipo de treinamento.")
            else:
                # Salvar dados no banco de dados
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_data(name, cpf_matricula, empresa, treinamentos, time_now)
                st.success(f"Presença registrada com sucesso às {time_now}!")
        st.markdown("</div>", unsafe_allow_html=True)

# Exibir os dados registrados
st.markdown("<h3 style='margin-top: 20px;'>Presenças Registradas</h3>", unsafe_allow_html=True)
data = fetch_data()
if data:
    df = pd.DataFrame(data, columns=["Nome", "CPF/Matrícula", "Empresa", "Treinamento", "Horário"])
    st.dataframe(df.style.set_properties(**{'text-align': 'center'}), use_container_width=True)
else:
    st.info("Nenhuma presença registrada ainda.")
