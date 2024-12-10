import sqlite3
import pandas as pd

# Conexão com o banco de dados
conn = sqlite3.connect("lista_presenca.db")

# Exportar os dados para CSV
df = pd.read_sql_query("SELECT * FROM presenca", conn)
df.to_csv("dados_presenca.csv", index=False)

# Fechar a conexão
conn.close()
print("Arquivo CSV criado: dados_presenca.csv")