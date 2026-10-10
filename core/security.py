#CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')
from pwdlib import PasswordHash

CRIPTO = PasswordHash.recommended()

DUMMY_HASH = CRIPTO.hash("dummypassword")

def verificar_senha(senha: str, hash_senha: str) -> bool:
    return CRIPTO.verify(senha, hash_senha)

def gerar_hash_senha(senha: str) -> str:
    return CRIPTO.hash(senha)