import xmltodict
import json
import requests
import pprint
import os
import streamlit as st

os.system('cls')

def get_previsao(id):
    url =f"http://servicos.cptec.inpe.br/XML/cidade/{id}/previsao.xml"
    dados = requests.get(url)

    if dados.status_code ==200:
        xml_texto = dados.text
        dados_cidade = xmltodict.parse(xml_texto)
        return dados_cidade
    else:
        print("Erro ao acessar informação")



st.title("previsão de 4 dias")
entrada = st.text_input("Digite qual cidade quer saber a previsão",value="241")

previsao = get_previsao(entrada)

#pp = pprint.PrettyPrinter(indent=2)
nome_cidade = previsao['cidade']['nome']
previsao4dias = previsao['cidade']['previsao']
#pp.pprint(previsao4dias)

st.header(f"Previsão para : {nome_cidade}")
#print("-="*40)
for repet in previsao4dias:
    with st.container(border=True):
        dia = repet.get('dia', 'N/A')
        iuv = repet.get('iuv', 'N/A')
        maxima = repet.get('maxima', 'N/A')
        minima = repet.get('minima', 'N/A')
        tempo = repet.get('tempo', 'N/A')

        st.markdown(f"### PREVISÃO PARA O DIA : **{dia}**")

        temperatura,descricao = st.columns(2)
        with temperatura:
            st.metric(
                label="Temperatura (min/max)",
                value=f"{minima}°C   {maxima}°C {iuv} {tempo}" ,
            )
        



