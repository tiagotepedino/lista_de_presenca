import sqlite3
import pandas as pd

# Conexão com o banco de dados
conn = sqlite3.connect("lista_presenca.db")

# Consulta SQL
df = pd.read_sql_query("SELECT * FROM presenca", conn)

# Exibição dos dados
print(df)