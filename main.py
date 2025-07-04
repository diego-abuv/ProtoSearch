# main.py
from dotenv import load_dotenv
import os
from frontend.gui import GravacaoApp # Importa a classe da sua GUI

def main():
    # Carrega variaveis de ambiente. A condicao e para evitar carregar em prod
    # se o .env.dev existir irá carregá-lo ao invés do .env
    if os.path.exists(".env.dev"):
        load_dotenv(".env.dev")
    else: 
        load_dotenv(".env")
    
    app = GravacaoApp() # Instancia sua aplicativo Tkinter
    app.run() # Inicia o loop principal da Tkinter

if __name__ == "__main__":
    main()
