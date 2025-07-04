# backend/core/file_operations.py
import os
import shutil
import logging

# Configura o logger para ser usado internamente ou por quem importar
# Você pode configurar isso de forma mais robusta no main.py ou em um módulo de configuração.
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def busca_e_copia(ano: int, mes: int, dia: int, protocolo: str, destino: str, raiz: str, com_horario: bool, log_callback=None) -> bool:
    """
    Busca arquivos de áudio com o protocolo especificado e os copia para o destino.
    Retorna True se algum arquivo foi encontrado e copiado, False caso contrário.
    O log_callback é uma função (e.g., um método da GUI) para enviar mensagens.
    """
    encontrado_nesta_raiz = False
    pastas_backup_antigas = ["Backup_Gravacoes_10_11", "Backup_Gravacoes_10_12"]

    def _log(message):
        if log_callback:
            log_callback(message)
        logging.info(message) # Mantém o log no console/arquivo

    if not com_horario: # Para as pastas antigas (2019-2021)
        for pasta in pastas_backup_antigas:
            caminho_base = os.path.join(raiz, pasta, str(ano), f"{int(mes):02}", f"{int(dia):02}")
            _log(f"Procurando em: {caminho_base}...")

            if not os.path.exists(caminho_base):
                continue

            for dirpath, _, filenames in os.walk(caminho_base):
                for filename in filenames:
                    if protocolo in filename:
                        origem = os.path.join(dirpath, filename)
                        try:
                            shutil.copy(origem, destino)
                            _log(f"Arquivo '{filename}' copiado para '{destino}'")
                            encontrado_nesta_raiz = True
                        except Exception as e:
                            _log(f"Erro ao copiar '{filename}': {e}")
    else: # Para as pastas com estrutura de horário (0.74 e 0.254)
        caminho_base = os.path.join(raiz, str(ano), str(int(mes)), str(int(dia)))
        
        _log(f"Procurando em: {caminho_base} (e subpastas de horário)...")

        if not os.path.exists(caminho_base):
            return False

        for dirpath, _, filenames in os.walk(caminho_base):
            for filename in filenames:
                if protocolo in filename:
                    origem = os.path.join(dirpath, filename)
                    try:
                        shutil.copy(origem, destino)
                        _log(f"Arquivo '{filename}' copiado para '{destino}'")
                        encontrado_nesta_raiz = True
                    except Exception as e:
                        _log(f"Erro ao copiar '{filename}': {e}")
    
    if not encontrado_nesta_raiz:
        _log(f"Protocolo NÃO encontrado nesta raiz: {raiz}.")
    
    return encontrado_nesta_raiz