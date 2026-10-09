import streamlit as st
import pandas as pd
import re

from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Aws
SERVIDOR = r"mssql.csomccdkkzvk.us-east-1.rds.amazonaws.com"
BANCO = "hamburgueria"
DRIVER = "ODBC Driver 18 for SQL Server"

#OUTRO MÉTODO LOGIN
USUARIO = "dev"
SENHA = "ABC123xyz"


def conectar():    
    odbc = (
        f"DRIVER={{{DRIVER}}};SERVER={SERVIDOR};DATABASE={BANCO};"
        f"UID={USUARIO};PWD={SENHA};"
        "TrustServerCertificate=yes"
    )    
    return create_engine("mssql+pyodbc:///?odbc_connect="+ quote_plus(odbc))


def consultar(sql):    
    with conectar().connect() as conexao:
        return pd.read_sql(text(sql), conexao)


if __name__ == '__main__':

    query = '''
        SELECT @@VERSION
    '''

    st.title("MSSQL na AWS")
    st.write('Versão')
    st.dataframe(consultar(query))

    query_2 = '''
        SELECT name from sys.databases
    '''

    st.write('Bancos')
    st.dataframe(consultar(query_2))
