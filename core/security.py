#from passlib.context import CryptContext

#CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')

from pwdlib import PasswordHash

CRIPTO = PasswordHash.recommended()

def verificar_senha(senha: str, hash_senha: str) -> bool:
    return CRIPTO.verify(senha, hash_senha)

def gerar_hash_senha(senha: str) -> str:
    return CRIPTO.hash(senha)