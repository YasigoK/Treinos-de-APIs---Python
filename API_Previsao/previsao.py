import xmltodict
import json
import requests
import pprint
import os
import streamlit as st
import numpy as np

def get_previsao(id):
    url =f"http://servicos.cptec.inpe.br/XML/cidade/{id}/previsao.xml"
    dados = requests.get(url)

    if dados.status_code ==200:
        xml_texto = dados.text
        dados_cidade = xmltodict.parse(xml_texto)
        return dados_cidade
    else:
        print("Erro ao acessar informação")
        return None

st.set_page_config(layout="wide")

st.title("previsão de 4 dias")
entrada = st.text_input("Digite qual cidade quer saber a previsão",value="241")

previsao = get_previsao(entrada)

nome_cidade = previsao['cidade']['nome']
previsao4dias = previsao['cidade']['previsao']
st.header(f"Previsão para : {nome_cidade}")

num_dias = len(previsao4dias)
colunas = st.columns(num_dias)
atual_max = np.zeros(num_dias)
atual_min = np.zeros(num_dias)
for i, repet in enumerate(previsao4dias):

    with colunas[i]:
        dia = repet.get('dia', 'N/A')
        iuv = repet.get('iuv', 'N/A')
        maxima = repet.get('maxima', 'N/A')
        minima = repet.get('minima', 'N/A')
        tempo = repet.get('tempo', 'N/A')
        atual_min[i] = float(minima)
        atual_max[i] = float(maxima)
        if i == 0:
            variacao_min = None 
            variacao_max = None
        else:
            variacao_min = atual_min[i] - atual_min[i-1]
            variacao_max = atual_max[i] - atual_max[i-1]
  
        with st.container(border=True):
                
                st.markdown(f"### PREVISÃO PARA O DIA :\n  ### **{dia}**")

                temperatura1,temperatura2,descricao = st.columns(3)
                with temperatura1:
                    st.metric(
                        label="Temperatura Min",
                        value=f"{minima}°C",
                        delta=f"{variacao_min:+.1f}" if variacao_min is not None else None, 
                        delta_color="inverse",
                    )
                with temperatura2:
                    st.metric(
                        label="Temperatura Max",
                        value=f"{maxima}°C",
                        delta=f"{variacao_min:+.1f}" if variacao_min is not None else None, 
                        delta_color="inverse",
                    )
            
                with descricao:
                    st.metric(
                        label="Tempo",
                        value=f"{tempo}",
                    )




