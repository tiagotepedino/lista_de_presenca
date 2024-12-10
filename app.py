import streamlit as st
import sqlite3
from datetime import datetime

# Configurações iniciais do app
st.set_page_config(page_title="Lista de Presença", layout="centered")

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

# Escolher o treinamento
treinamento = st.selectbox("Selecione o treinamento:", 
                           ["Treinamento GQI e Relatório de Qualidade", "Treinamento de Gerenciamento de Dados do RIV"])

# Título do app
st.title(f"Lista de Presença - {treinamento}")

# Nome da tabela no banco de dados
table_name = "presenca_gqi" if treinamento == "Treinamento GQI e Relatório de Qualidade" else "presenca_riv"

# Formulário de registro
with st.form(key="attendance_form"):
    name = st.text_input("Nome", placeholder="Digite seu nome completo")
    cpf_matricula = st.text_input("CPF ou Matrícula", placeholder="Digite seu CPF ou matrícula")
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
st.subheader(f"Lista de Presença Registrada - {treinamento}")
data = get_data(table_name)
if data:
    df = [{"Nome": row[0], "CPF/Matrícula": row[1], "Empresa": row[2], "Horário": row[3]} for row in data]
    st.dataframe(df)
else:
    st.info("Nenhuma presença registrada ainda.")
