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
        CREATE TABLE IF NOT EXISTS presenca (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            horario TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Função para salvar dados no SQLite
def save_data(name, email, time):
    conn = sqlite3.connect("lista_presenca.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO presenca (nome, email, horario) VALUES (?, ?, ?)", (name, email, time))
    conn.commit()
    conn.close()

# Função para obter os dados do banco
def get_data():
    conn = sqlite3.connect("lista_presenca.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email, horario FROM presenca")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Criar a tabela no banco de dados
create_table()

# Título do app
st.title("Lista de Presença")

# Formulário de registro
with st.form(key="attendance_form"):
    name = st.text_input("Nome", placeholder="Digite seu nome completo")
    email = st.text_input("Email", placeholder="Digite seu email")
    submit_button = st.form_submit_button("Registrar Presença")

    if submit_button:
        if name and email:
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_data(name, email, time_now)
            st.success(f"Presença registrada com sucesso às {time_now}!")
        else:
            st.error("Por favor, preencha todos os campos.")

# Exibir a lista de presença
st.subheader("Lista de Presença Registrada")
data = get_data()
if data:
    df = [{"Nome": row[0], "Email": row[1], "Horário": row[2]} for row in data]
    st.dataframe(df)
else:
    st.info("Nenhuma presença registrada ainda.")
