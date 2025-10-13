import requests
import pandas as pd
import json
import os 
from IPython.display import display 
from tkinter import  *
from tkinter import filedialog


salvar_resultado = None

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
   global salvar_resultado
   cep_digitado = cep_texto.get()
   busca = get_by_cep(cep_digitado)
   
   if isinstance(busca,dict):
        salvar_resultado = busca
        tabela = pd.DataFrame([busca])
        tabela_Trans = tabela.T
        
        tabela_String = tabela_Trans.to_string(header=False)
        resultado.delete(0,END)
        resultado.insert(END,"=== Resultado da busca ===")
        for i in tabela_String.split('\n'):
            resultado.insert(END,i)
        
   else : 
       salvar_resultado = None
       resultado.delete(0,END)
       resultado.insert(END, "Resultado desconhecido")

def save_file():
    if not salvar_resultado:
        resultado.delete(0,END)
        resultado.insert(END, "Error ao salvar, nenhum Cep consultado") 
        return
    
    local_salvar = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Arquivos JSON", "*.json"),("todos os arquivos", "*.")],
        initialfile=f"cep_{salvar_resultado.get('cep','resultado')}.json"
    )
    
    if local_salvar:
        try:
            with open(local_salvar, 'w', encoding='utf-8') as f:
                json.dump(salvar_resultado , f, indent=4,ensure_ascii=False)
            resultado.insert(END, "Arquivo salvado com sucesso")
        except Exception as e:
             resultado.insert(END, "Error ao salvar, não foi possível salvar o arquivo")

janela = Tk()
janela.title("Consulta de cep")
janela.geometry("800x600")

campo_texto= Label(janela, text="Digite o cep para realizar uma consulta", font=("Helvetica",16))
campo_texto.pack(pady=16)

frame_busca = Frame(janela)
frame_busca.pack(pady=5)

cep_texto = StringVar()
entrada = Entry(frame_busca, font=("Helvetica",16,"bold"), textvariable=cep_texto)
entrada.pack(side=LEFT, padx=(0, 10))

botao = Button(frame_busca,command=get_cep_search ,text="Pesquisar", width=15,font=("Helvetica",10))
botao.pack(side=LEFT)

resultado = Listbox(janela, width=63)
resultado.pack(pady=9)

salvar = Button(janela, command=save_file, text="Salvar", width=30,font=("Helvetica",10) )
salvar.pack(pady=10)


janela.mainloop()