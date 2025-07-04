# frontend/gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import getpass
import os
import datetime
import threading

# Importa as funções do backend
from backend.auth.permissions import tem_permissao
from backend.core.file_operations import busca_e_copia
from backend.utils.date_parser import parse_date_ddmmyyyy, format_date_d_m_yyyy, format_date_m_d_y

class GravacaoApp:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Buscador de Gravações")
        self.janela.geometry("600x600")

        self._configure_style()
        self._create_widgets()

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Segoe UI', 11))
        style.configure('TButton', font=('Segoe UI', 11, 'bold'), foreground='#ffffff', background='#0078d7')
        style.map('TButton',
                  foreground=[('active', '#ffffff')],
                  background=[('active', '#005a9e')])
        style.configure('TLabelframe', background='#f4f6fa', borderwidth=2, relief='ridge')
        style.configure('TLabelframe.Label', font=('Segoe UI', 12, 'bold'), background='#f4f6fa')
        # Estilo customizado para a Progressbar
        style.configure("blue.Horizontal.TProgressbar",
                        troughcolor='#e9ecf3',
                        background='#0078d7',
                        thickness=15,  # altura da barra
                        bordercolor='#0078d7',
                        lightcolor='#0078d7',
                        darkcolor='#0078d7')
        self.janela.configure(bg='#e9ecf3')

    def _create_widgets(self):
        # Frame de Input
        input_frame = ttk.LabelFrame(self.janela, text="🔎 Dados da Ligação", padding="15")
        input_frame.pack(padx=15, pady=15, fill="x", expand=True)

        lbl_data = ttk.Label(input_frame, text="📅 Data da Ligação (DD/MM/AAAA):")
        lbl_data.grid(row=0, column=0, padx=8, pady=8, sticky="w")

        self.entry_data = ttk.Entry(input_frame, width=20, font=('Segoe UI', 11))
        self.entry_data.grid(row=0, column=1, padx=8, pady=8, sticky="ew")

        btn_calendario = ttk.Button(input_frame, text="Abrir Calendário", command=self._selecionar_data)
        btn_calendario.grid(row=0, column=2, padx=8, pady=8)

        lbl_protocolo = ttk.Label(input_frame, text="🔑 Protocolo da Ligação:")
        lbl_protocolo.grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.entry_protocolo = ttk.Entry(input_frame, width=30, font=('Segoe UI', 11))
        self.entry_protocolo.grid(row=1, column=1, columnspan=2, padx=8, pady=8, sticky="ew")

        btn_buscar = ttk.Button(input_frame, text="🔍 Buscar Gravação", command=self._buscar_ligacao)
        btn_buscar.grid(row=2, column=0, columnspan=3, padx=8, pady=15, sticky="ew")

        input_frame.columnconfigure(1, weight=1)

        # Frame de Output
        output_frame = ttk.LabelFrame(self.janela, text="📋 Progresso da Busca", padding="15")
        output_frame.pack(padx=15, pady=5, fill="both", expand=True)

        # Progressbar sempre visível abaixo do campo de texto
        self.progress = ttk.Progressbar(output_frame, mode='determinate', style="blue.Horizontal.TProgressbar", maximum=100)
        self.progress.pack(fill="x", pady=(10, 0))

        # Sub-frame para texto e scrollbar
        text_frame = tk.Frame(output_frame, bg='#f4f6fa')
        text_frame.pack(fill="both", expand=True)

        self.output_text = tk.Text(text_frame, wrap=tk.WORD, height=10, state='normal', font=("Consolas", 10), bg='#f8fafc')
        self.output_text.pack(side=tk.LEFT, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(text_frame, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.output_text.config(yscrollcommand=scrollbar.set)

        # Botão para abrir a pasta de destino
        self.btn_abrir_pasta = ttk.Button(output_frame, text="Abrir Pasta de Destino", command=self._abrir_pasta_destino)


        
    
    def _log_to_gui(self, message: str):
        """Método para exibir mensagens na área de texto da GUI e atualizar progresso se necessário."""
        if message.startswith("PROGRESS:"):
            try:
                percent = int(message.split(":")[1])
                self.progress['value'] = percent
                self.janela.update_idletasks()
            except Exception:
                pass
        else:
            self.output_text.insert(tk.END, message + "\n")
            self.output_text.see(tk.END) # Auto-scroll

    def _selecionar_data(self):
        def set_date():
            data_selecionada_str = cal.get_date()
            # O tkcalendar retorna no formato 'MM/DD/YY'.
            # Precisamos converter para um objeto datetime e depois para 'DD/MM/YYYY' para o entry.
            try:
                data_obj = datetime.datetime.strptime(data_selecionada_str, '%m/%d/%y')
                data_formatada = format_date_d_m_yyyy(data_obj)
                self.entry_data.delete(0, tk.END)
                self.entry_data.insert(0, data_formatada)
                top.destroy()
            except ValueError:
                messagebox.showerror("Erro de Formato", "A data selecionada está em um formato inesperado. Tente novamente.")

        top = tk.Toplevel(self.janela)
        top.title("Selecionar Data")
        top.configure(bg='#e9ecf3')

        # Inicializa o calendário com a data atual ou a data já no entry
        initial_date = datetime.date.today()
        current_entry_date = self.entry_data.get()
        if current_entry_date:
            try:
                initial_date = parse_date_ddmmyyyy(current_entry_date).date()
            except ValueError:
                pass

        cal = Calendar(
            top,
            selectmode='day',
            date_pattern='mm/dd/yy',
            year=initial_date.year,
            month=initial_date.month,
            day=initial_date.day,
            background='#f4f6fa',         # Fundo dos dias
            foreground='#22223b',         # Cor dos números
            selectbackground='#0078d7',   # Fundo do dia selecionado
            selectforeground='#ffffff',   # Cor do número selecionado
            headersbackground='#e9ecf3',  # Fundo dos nomes dos dias
            headersforeground='#0078d7',  # Cor dos nomes dos dias
            bordercolor='#0078d7',        # Cor da borda
            othermonthbackground='#e9ecf3', # Dias de outros meses
            othermonthwebackground='#e9ecf3',
            font=('Segoe UI', 11)
        )
        cal.pack(pady=10)

        btn_ok = ttk.Button(top, text="Selecionar", command=set_date)
        btn_ok.pack(pady=5)

    def _abrir_pasta_destino(self):
        destino = os.path.join(os.path.expanduser("~"), "Desktop", "protocolos")
        if os.path.exists(destino):
            os.startfile(destino)
        else:
            tk.messagebox.showwarning("Pasta não encontrada", f"A pasta de destino não existe: {destino}")

    def _buscar_ligacao(self):
        self.progress['value'] = 0
        self.btn_abrir_pasta['state'] = 'disabled'
        self.btn_abrir_pasta.pack_forget()
        self.output_text.delete(1.0, tk.END)
        self._log_to_gui("Iniciando busca...\n")

        def tarefa():
            usuario = getpass.getuser()
            log_path = os.getenv("LOG_PATH")
            
            if not tem_permissao(usuario, log_path):
                self.janela.after(0, lambda: messagebox.showerror("Erro de Permissão", "Acesso negado! Você não possui permissão para usar este programa."))
                self._log_to_gui("Acesso negado!\n")
                self.progress.stop()
                return

            data_str = self.entry_data.get()
            protocolo = self.entry_protocolo.get().strip()

            if not data_str or not protocolo:
                self.janela.after(0, lambda: messagebox.showwarning("Entrada Inválida", "Por favor, preencha a data e o protocolo."))
                self._log_to_gui("Data ou protocolo não preenchidos.\n")
                self.progress.stop()
                return

            try:
                data_obj = parse_date_ddmmyyyy(data_str)
                dia, mes, ano = data_obj.day, data_obj.month, data_obj.year
            except ValueError as e:
                self.janela.after(0, lambda: messagebox.showerror("Erro de Data", str(e)))
                self._log_to_gui(f"Erro: {e}\n")
                self.progress.stop()
                return

            if not (2019 <= ano <= 2025):
                self.janela.after(0, lambda: messagebox.showwarning("Ano Inválido", "Por favor, digite um ano entre 2019 e 2025."))
                self._log_to_gui("Ano fora do intervalo permitido.\n")
                self.progress.stop()
                return

            raizes_a_buscar = self._determinar_raizes(ano)

            if not raizes_a_buscar:
                self.janela.after(0, lambda: messagebox.showinfo("Sem Caminhos", "Nenhum caminho de busca configurado para o ano especificado."))
                self._log_to_gui("Nenhum caminho de busca configurado.\n")
                self.progress.stop()
                return

            destino = os.path.join(os.path.expanduser("~"), "Desktop", "protocolos")
            os.makedirs(destino, exist_ok=True)

            self._log_to_gui(f"\nBuscando protocolo '{protocolo}' na data {dia}/{mes}/{ano}...\n")
            self._log_to_gui("PROGRESS:10")
            total_encontrado = False
            caminhos_buscados = []
            for raiz_path, com_horario in raizes_a_buscar:
                caminhos_buscados.append(raiz_path)
                if busca_e_copia(ano, mes, dia, protocolo, destino, raiz_path, com_horario, self._log_to_gui):
                    total_encontrado = True
            # Limpa o log e mostra apenas o resultado final
            self.output_text.delete(1.0, tk.END)
            if total_encontrado:
                self.progress['value'] = 100  # Mantém a barra cheia
                self._log_to_gui(f"Busca finalizada! Protocolo(s) encontrado(s) e copiado(s) para:\n{destino}\n")
                if not self.btn_abrir_pasta.winfo_ismapped():
                    self.btn_abrir_pasta.pack(pady=(8, 0), anchor="e")
                self.btn_abrir_pasta['state'] = 'normal'
            else:
                self.progress['value'] = 100  # Mantém a barra cheia mesmo se não encontrar
                self._log_to_gui("Protocolo NÃO encontrado em nenhum dos caminhos verificados.\n")
                self._log_to_gui("O sistema fez a busca nos seguintes caminhos:")
                for caminho in caminhos_buscados:
                    self._log_to_gui(f"- {caminho}")
                if not self.btn_abrir_pasta.winfo_ismapped():
                    self.btn_abrir_pasta.pack(pady=(8, 0), anchor="e")
                self.btn_abrir_pasta['state'] = 'normal'
            # Removido self.progress.stop() para não limpar a barra

        threading.Thread(target=tarefa, daemon=True).start()

    def _determinar_raizes(self, ano: int) -> list:
        """Determina as raízes de busca baseadas no ano."""
        raizes = []
        if 2019 <= ano <= 2021:
            raiz_info = os.getenv("RAIZ_2019_2021", "").split(",")
            if len(raiz_info) == 2:
                raizes.append((raiz_info[0], raiz_info[1].lower() == 'true'))
        if 2021 <= ano <= 2023:
            raiz_info = os.getenv("RAIZ_2021_2023", "").split(",")
            if len(raiz_info) == 2:
                raizes.append((raiz_info[0], raiz_info[1].lower() == 'true'))
        if 2023 <= ano <= 2025:
            raiz_info = os.getenv("RAIZ_2023_2025", "").split(",")
            if len(raiz_info) == 2:
                raizes.append((raiz_info[0], raiz_info[1].lower() == 'true'))
        return raizes

    def run(self):
        self.janela.mainloop()