import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Configurações iniciais do app
st.set_page_config(page_title="Lista de Presença", layout="centered")

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

# Título principal
st.title("Lista de Presença")

# Subtítulo
st.subheader("Registro de Presença")

# Criar o formulário
with st.form(key="attendance_form"):
    # Nome
    name = st.text_input("Nome", placeholder="Digite seu nome completo")
    # CPF ou Matrícula
    cpf_matricula = st.text_input("CPF ou Matrícula", placeholder="Digite seu CPF ou matrícula")
    # Empresa
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
        if not name.strip():
            st.error("O campo Nome é obrigatório. Por favor, preencha-o.")
        elif not cpf_matricula.strip():
            st.error("O campo CPF ou Matrícula é obrigatório. Por favor, preencha-o.")
        elif not treinamentos:
            st.error("Selecione pelo menos um tipo de treinamento.")
        else:
            # Salvar dados no banco de dados
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_data(name, cpf_matricula, empresa, treinamentos, time_now)
            st.success(f"Presença registrada com sucesso às {time_now}!")
