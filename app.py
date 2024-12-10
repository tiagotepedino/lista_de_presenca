import streamlit as st
import pandas as pd
from datetime import datetime

# Configurações iniciais do app
st.set_page_config(page_title="Lista de Presença", layout="centered")

# Função para salvar os dados no arquivo CSV
def save_data(name, email, time):
    data = {"Nome": name, "Email": email, "Horário": time}
    df = pd.DataFrame([data])
    try:
        # Verifica se o arquivo já existe
        df_existing = pd.read_csv("lista_presenca.csv")
        df = pd.concat([df_existing, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv("lista_presenca.csv", index=False)

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
try:
    df = pd.read_csv("lista_presenca.csv")
    st.dataframe(df)
except FileNotFoundError:
    st.info("Nenhuma presença registrada ainda.")