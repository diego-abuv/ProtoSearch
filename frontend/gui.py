# frontend/gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import getpass
import os
import datetime

# Importa as funções do backend
from backend.auth.permissions import tem_permissao
from backend.core.file_operations import busca_e_copia
from backend.utils.date_parser import parse_date_ddmmyyyy, format_date_d_m_yyyy, format_date_m_d_y

class GravacaoApp:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Buscador de Gravações")
        self.janela.geometry("600x450")

        self._configure_style()
        self._create_widgets()

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use('clam')

    def _create_widgets(self):
        # Frame de Input
        input_frame = ttk.LabelFrame(self.janela, text="Dados da Ligação", padding="10")
        input_frame.pack(padx=10, pady=10, fill="x", expand=True)

        lbl_data = ttk.Label(input_frame, text="Data da Ligação (DD/MM/AAAA):")
        lbl_data.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.entry_data = ttk.Entry(input_frame, width=20)
        self.entry_data.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        btn_calendario = ttk.Button(input_frame, text="Abrir Calendário", command=self._selecionar_data)
        btn_calendario.grid(row=0, column=2, padx=5, pady=5)

        lbl_protocolo = ttk.Label(input_frame, text="Protocolo da Ligação:")
        lbl_protocolo.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_protocolo = ttk.Entry(input_frame, width=30)
        self.entry_protocolo.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        btn_buscar = ttk.Button(input_frame, text="Buscar Gravação", command=self._buscar_ligacao)
        btn_buscar.grid(row=2, column=0, columnspan=3, padx=5, pady=10)

        input_frame.columnconfigure(1, weight=1)

        # Frame de Output
        output_frame = ttk.LabelFrame(self.janela, text="Progresso da Busca", padding="10")
        output_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.output_text = tk.Text(output_frame, wrap=tk.WORD, height=10, state='normal', font=("Arial", 9))
        self.output_text.pack(side=tk.LEFT, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(output_frame, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.output_text.config(yscrollcommand=scrollbar.set)
    
    def _log_to_gui(self, message: str):
        """Método para exibir mensagens na área de texto da GUI."""
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
        # Inicializa o calendário com a data atual ou a data já no entry
        initial_date = datetime.date.today()
        current_entry_date = self.entry_data.get()
        if current_entry_date:
            try:
                initial_date = parse_date_ddmmyyyy(current_entry_date).date()
            except ValueError:
                pass # Ignora se a data no entry for inválida e usa a data atual

        cal = Calendar(top, selectmode='day', date_pattern='mm/dd/yy',
                       year=initial_date.year, month=initial_date.month, day=initial_date.day)
        cal.pack(pady=10)

        btn_ok = ttk.Button(top, text="Selecionar", command=set_date)
        btn_ok.pack(pady=5)

    def _buscar_ligacao(self):
        self.output_text.delete(1.0, tk.END) # Limpa a área de output
        self._log_to_gui("Iniciando busca...\n")
        
        usuario = getpass.getuser()
        log_path = os.getenv("LOG_PATH")
        
        if not tem_permissao(usuario, log_path):
            messagebox.showerror("Erro de Permissão", "Acesso negado! Você não possui permissão para usar este programa.")
            self._log_to_gui("Acesso negado!\n")
            return

        data_str = self.entry_data.get()
        protocolo = self.entry_protocolo.get().strip()

        if not data_str or not protocolo:
            messagebox.showwarning("Entrada Inválida", "Por favor, preencha a data e o protocolo.")
            self._log_to_gui("Data ou protocolo não preenchidos.\n")
            return

        try:
            data_obj = parse_date_ddmmyyyy(data_str)
            dia, mes, ano = data_obj.day, data_obj.month, data_obj.year
        except ValueError as e:
            messagebox.showerror("Erro de Data", str(e))
            self._log_to_gui(f"Erro: {e}\n")
            return

        if not (2019 <= ano <= 2025):
            messagebox.showwarning("Ano Inválido", "Por favor, digite um ano entre 2019 e 2025.")
            self._log_to_gui("Ano fora do intervalo permitido.\n")
            return

        raizes_a_buscar = self._determinar_raizes(ano)

        if not raizes_a_buscar:
            messagebox.showinfo("Sem Caminhos", "Nenhum caminho de busca configurado para o ano especificado.")
            self._log_to_gui("Nenhum caminho de busca configurado.\n")
            return

        destino = os.path.join(os.path.expanduser("~"), "Desktop", "protocolos")
        os.makedirs(destino, exist_ok=True)

        self._log_to_gui(f"\nBuscando protocolo '{protocolo}' na data {dia}/{mes}/{ano}...\n")
        total_encontrado = False
        for raiz_path, com_horario in raizes_a_buscar:
            if busca_e_copia(ano, mes, dia, protocolo, destino, raiz_path, com_horario, self._log_to_gui):
                total_encontrado = True
        
        if total_encontrado:
            messagebox.showinfo("Busca Concluída", f"Busca finalizada! Protocolo(s) encontrado(s) e copiado(s) para:\n{destino}")
            self._log_to_gui("\nBusca finalizada! Verifique a pasta 'protocolos' na sua Área de Trabalho.\n")
        else:
            messagebox.showinfo("Busca Concluída", "Protocolo NÃO encontrado em nenhum dos caminhos verificados.")
            self._log_to_gui("\nProtocolo NÃO encontrado.\n")

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