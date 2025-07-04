# backend/auth/permissions.py
import os

def tem_permissao(usuario: str, log_path: str) -> bool:
    """Verifica se o usuário tem permissão para usar o buscador."""
    try:
        if not os.path.exists(log_path):
            return False
        with open(log_path, 'r') as f:
            permissoes = [u.strip().lower() for u in f]
        return usuario.lower() in permissoes
    except Exception:
        # Idealmente, logar o erro aqui para depuração
        return False