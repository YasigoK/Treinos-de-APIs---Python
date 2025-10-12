import requests
import pandas as pd
from IPython.display import display 
import os 


os.system('cls' if os.name=='nt' else 'clear')
def get_by_cep(cep):
    cep = cep.replace("-", "").replace(".","").replace(",","").replace(" ","")

    if len(cep)==8:
        url_request = f'https://viacep.com.br/ws/{cep}/json'

        requisition = requests.get(url_request)

        if requisition.status_code == 200:
            return requisition.json()
        else:
            print(f"Erro de requisição {requisition.status_code}")
    else:
        print(f"O valor de cep {cep} é invalido, numero de caracteres deve ser igual a 8")

def get_cep(uf,cidade,endereco):
    #viacep.com.br/ws/RS/Porto Alegre/Porto Alegre/son
    url_request =f'https://viacep.com.br/ws/{uf}/{cidade}/{endereco}/json/'
    requisition = requests.get(url_request)

    if requisition.status_code ==200:
        return requisition.json()
    else:
       print(f"Erro de requisição {requisition.status_code}") 

cepRJ = get_by_cep("2023-0010")
acharCep = get_cep("SP","São paulo","São paulo")


tabela01 = pd.DataFrame([cepRJ])
display(tabela01)

print("="*200)
tabela02 = pd.DataFrame(acharCep)
display(tabela02)



