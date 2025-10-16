import requests
import json
import os 
import pyodbc
from tkinter import  *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox


salvar_resultado = None
       
conexao_bd = (
    "Driver={SQL Server};"
    "Server=.;"  #localhost
    "Database=TabelaCep;"
    "Trusted_Connection=yes;"
)

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
   global resultado_tabela
   
   cep_digitado = cep_texto.get()
   busca = get_by_cep(cep_digitado)
   if isinstance(busca,dict):
        salvar_resultado = busca
        
        ordem_campos = [
            'cep', 'logradouro', 'complemento', 'bairro','localidade', 'uf', 'ibge', 'gia', 'ddd', 'siafi'
        ]

        valores = [
            str(busca.get(campo,'N/A')) 
            for campo in ordem_campos
            ]
        
        resultado_tabela.insert('', END,values=valores)
   else:
       salvar_resultado=None
       resultado_tabela.insert('', END, values=(busca, '', '', '', '', '', '', '', '', ''))
            
    

def save_file():
    if not salvar_resultado:
        messagebox.showerror("Erro", "Não foi possível salvar, nenhum CEP consultado") 
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
            messagebox.showinfo("Salvo", "Arquivo salvado com sucesso")
        except Exception as e:
            messagebox.showerror("Error", "Erro ao salvar, não foi possível salvar o arquivo")

def insert_data_bd():
    global salvar_resultado
    if not salvar_resultado:
        messagebox.showerror("Error", "Erro ao adicionar, nenhum CEP consultado") 
        return
    
    ordem_campos_sql = [
        'CEP', 'Logradouro', 'Complemento', 'Bairro', 'Localidade','UF', 'IBGE', 'GIA', 'DDD', 'SIAFI'
    ]

    valores_sql=[
        salvar_resultado.get(campo.lower(),None)
        for campo in ordem_campos_sql

    ]
    insert_sql = f"""
        INSERT INTO dadosCEP({', '.join(ordem_campos_sql)})
        VALUES ({', '.join(['?']*len(ordem_campos_sql))})
    """

    conexao = pyodbc.connect(conexao_bd)
    cursor = conexao.cursor()

    cursor.execute(insert_sql,valores_sql)
    conexao.commit()
    messagebox.showinfo("Sucesso", "dado adicionado ao banco de dados com sucesso!")
    conexao.close()


janela = Tk()
janela.title("Consulta de cep")
janela.geometry("1000x500")

campo_texto= Label(janela, text="Digite o cep para realizar uma consulta", font=("Helvetica",16))
campo_texto.pack(pady=16)

frame_busca = Frame(janela)
frame_busca.pack(pady=5)

cep_texto = StringVar()
entrada = Entry(frame_busca, font=("Helvetica",16,"bold"), textvariable=cep_texto)
entrada.pack(side=LEFT, padx=(0, 10))

botao = Button(frame_busca,command=get_cep_search ,text="Pesquisar", width=15,font=("Helvetica",10))
botao.pack(side=LEFT)

colunas = ('cep', 'logradouro', 'complemento', 'bairro','localidade', 'uf', 'ibge', 'gia', 'ddd', 'siafi')

resultado_tabela = ttk.Treeview(janela, columns=colunas, show = 'headings')
resultado_tabela.pack(pady=10, padx=10, fill='x', expand=True)

larguras_campos = [70, 150, 120, 120, 150, 20, 50, 50, 20, 50]

for i, nome_coluna in enumerate(colunas):
    resultado_tabela.heading(nome_coluna, text=nome_coluna.capitalize())
    resultado_tabela.column(nome_coluna, width=larguras_campos[i], minwidth=larguras_campos[i],anchor=CENTER)

salvar = Button(janela, command=save_file, text="Salvar", width=30,font=("Helvetica",10) )
salvar.pack(pady=10)

inserirBd = Button(janela, command=insert_data_bd, text="Adicionar ao BD",width=30,font=("Helvetica",10))
inserirBd.pack(pady=10)


janela.mainloop()