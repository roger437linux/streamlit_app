import streamlit as st
from supabase import create_client
import pandas as pd

supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    supabase_url,
    supabase_key
)

#----------------------------------------

response = (
    supabase
    .table("clientes")
    .select("*")
    .execute()
)

dados = response.data
# st.dataframe(dados)

# Teste
from random import randint

for i in range(5):
    r = randint(0, len(dados)-5)
    print(dados[r])
print()

#----------------------------------------

# Convertendo para dataframe

# df = pd.DataFrame(response.data)

# st.dataframe(df)
# print(df)

#####################
#    Exercício 1    #
#####################
           
if st.button("Query 1"):
    st.write('A Dona Marta quer saber quantos clientes cadastrados moram no bairro Centro.')
    
    response = (
        supabase.table("vw_q1").select("*").execute()
    )

    q1 = response.data
    st.dataframe(q1)


#####################
#    Exercício 2    #
#####################
           
if st.button("Query 2"):
    st.write('Liste o nome e o preço dos produtos da categoria Hambúrguer que custam \
                 mais de R$ 30,00, do mais caro para o mais barato.')
    
    response = (
        supabase.table("vw_q2").select("*").execute()
    )

    q2 = response.data
    st.dataframe(q2)

    