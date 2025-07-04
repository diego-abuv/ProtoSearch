# ProtoSearch 🔎

Um sistema intuitivo para buscar e recuperar gravações de ligações por protocolo e data, organizadas em uma estrutura de pastas padronizada (`ANO/MÊS/DIA/HORA`). Facilite a localização de áudios importantes com esta ferramenta simples e eficiente.

---

## **Recursos** ✨

* **Busca por Protocolo e Data:** Localize rapidamente gravações usando o número do protocolo e a data exata da ligação.
* **Organização Automatizada:** Copia as gravações encontradas para uma pasta `protocolos` na Área de Trabalho do usuário.
* **Suporte a Múltiplas Raízes:** Configurações para buscar em diferentes caminhos de armazenamento de gravações, cobrindo diversos períodos.
* **Interface Gráfica (GUI):** Fácil de usar com uma interface amigável construída com Tkinter.
* **Gerenciamento de Permissões:** Controla o acesso de usuários ao sistema via um arquivo de log.

---

## **Como Rodar o Projeto** 🚀

Siga os passos abaixo para configurar e executar o ProtoSearch em sua máquina.

### **Requisitos** 🛠️

* **Python 3.x** (preferencialmente Python 3.8 ou superior)
* Uma IDE (ambiente de desenvolvimento integrado) que suporte Python (ex: VS Code, PyCharm).

### **Instalando Dependências** 📦

1. Certifique-se de ter o Python instalado (recomendado 3.8 ou superior).
2. Instale as dependências do projeto executando o comando abaixo no terminal, dentro da pasta do projeto:

    ```bash
    pip install -r requirements.txt
    ```

   > **Observação:**
   > - O `tkinter` já vem instalado por padrão no Python para Windows. Em algumas distribuições Linux, pode ser necessário instalar manualmente (exemplo: `sudo apt-get install python3-tk`).
   > - O `tkcalendar` e o `python-dotenv` são instalados automaticamente pelo comando acima.

### **Clonando o Repositório e Configurando Variáveis de Ambiente** ⬇️⚙️

1.  **Clone o projeto** para sua máquina local usando o Git:

    ```bash
    git clone git@github.com:diego-abuv/ProtoSearch.git
    ```

2.  **Navegue até o diretório do projeto:**

    ```bash
    cd ProtoSearch
    ```

3.  **Crie o arquivo de variáveis de ambiente:**
    Na raiz do projeto, crie um novo arquivo chamado `.env` (ou `.env.dev` se for para ambiente de testes e desenvolvimento). Este arquivo **não deve ser enviado para o Git** por conter informações sensíveis.

    * **Dica:** Verifique o `.gitignore` na raiz do projeto para garantir que `.env` e `.env.*` estão sendo ignorados.

### **Configurando o Arquivo `.env`** 🔑

O arquivo `.env` (ou `.env.dev`) precisa conter as variáveis que o sistema usará para autenticação e para localizar as raízes das gravações. Copie o exemplo abaixo e preencha com seus dados:

```ini
# .env.dev (Exemplo para ambiente de desenvolvimento)

# Caminho completo para o arquivo .log que contém a lista de usuários permitidos (um usuário por linha)
LOG_PATH="C:/caminho/para/seu/users.log"

# Caminho da pasta raiz onde ficam as gravações de 2019 a 2021
# O formato é "caminho/da/raiz,COM_HORARIO_BOOL".
# Use TRUE se as subpastas forem por hora (ex: 2019/10/26/10/arquivo.wav)
# Use FALSE se não houver subpastas de hora (ex: 2019/10/26/arquivo.wav)
RAIZ_2019_2021="C:/Raizes/GravacoesAntigas,FALSE"

# Caminho da pasta raiz onde ficam as gravações de 2021 a 2023
RAIZ_2021_2023="D:/Raizes/GravacoesIntermediarias,TRUE"

# Caminho da pasta raiz onde ficam as gravações de 2023 a 2025 (e futuras)
RAIZ_2023_2025="E:/Raizes/GravacoesAtuais,TRUE"
```

### **Rodando o Projeto** ▶️

Após instalar as dependências e configurar o arquivo `.env` ou `.env.dev`, execute o seguinte comando na raiz do projeto para iniciar a aplicação:

```bash
python main.py
```

A interface gráfica será aberta e você poderá utilizar normalmente.

---

### **Gerando Executável e Instalador (Opcional)** 🛠️

Se desejar distribuir o ProtoSearch como um executável para Windows, siga os passos abaixo:

#### 1. Gerando o Executável com PyInstaller

1. Instale o PyInstaller (caso ainda não tenha):
   ```bash
   pip install pyinstaller
   ```
2. Gere o executável (a partir da raiz do projeto):
   ```bash
   pyinstaller --onefile --noconsole --name BuscadorProtocolo main.py
   ```
   - O executável será criado na pasta `dist`.
   - Para incluir arquivos adicionais (como `.env`), copie-os manualmente para a mesma pasta do executável ou use a opção `--add-data` do PyInstaller.

#### 2. Organize os arquivos para o instalador

- Crie uma pasta (ex: `build_files`) e coloque dentro:
  - O executável gerado (`BuscadorProtocolo.exe`)
  - O arquivo `.env` de exemplo ou configuração

#### 3. Criando o Instalador com Inno Setup Compiler

1. Instale o [Inno Setup Compiler](https://jrsoftware.org/isinfo.php).
2. Use o script abaixo como base para gerar o instalador:

```ini
[Setup]
AppName=BuscadorProtocolo
AppVersion=1.0
DefaultDirName=C:\BuscadorProtocolo
DefaultGroupName=BuscadorProtocolo
OutputDir=.
OutputBaseFilename=BuscadorProtocoloSetup

[Files]
Source: "build_files\BuscadorProtocolo.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "build_files\.env"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{commondesktop}\BuscadorProtocolo"; Filename: "{app}\BuscadorProtocolo.exe"
```

3. Compile o script no Inno Setup para gerar o instalador `.exe`.

Pronto! Agora você pode distribuir o instalador para outros usuários.