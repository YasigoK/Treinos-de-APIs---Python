import requests
import pandas as pd
from IPython.display import display 
from tkinter import  *
from tkinter import messagebox
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

def get_cep_search():
   cep_digitado = cep_texto.get()
   busca = get_by_cep(cep_digitado)
   
   if isinstance(busca,dict):
        tabela = pd.DataFrame([busca])
        tabela_Trans = tabela.T
        
        tabela_String = tabela_Trans.to_string(header=False)
        resultado.insert(END,"=== Resultado da busca ===")
        for i in tabela_String.split('\n'):
            resultado.insert(END,i)
        
   else : 
       resultado.delete(0,END)
       resultado.insert(END, "Resultado desconhecido")


janela = Tk()
janela.title("Consulta de cep")
janela.geometry("800x600")

campo_texto= Label(janela, text="Digite o cep para realizar uma consulta", font=("Helvetica",16))
campo_texto.pack(pady=16)

cep_texto = StringVar()
entrada = Entry(janela, font=("Helvetica",16,"bold"), textvariable=cep_texto)
entrada.pack()

botao = Button(janela,command=get_cep_search ,text="Pesquisar", width=30,font=("Helvetica",10))
botao.pack(pady=2)

resultado = Listbox(janela, width=70)
resultado.pack(pady=9)


janela.mainloop()