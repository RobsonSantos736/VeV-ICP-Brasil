from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

# Mensagem fixa do vetor de teste
mensagem = b"Mensagem de teste ICP-Brasil"

# Carregar as chaves RSA (geradas previamente)
with open("chave_privada.pem", "rb") as f:
    chave_privada = RSA.import_key(f.read())
with open("chave_publica.pem", "rb") as f:
    chave_publica = RSA.import_key(f.read())

# Geração do hash
hash_msg = SHA256.new(mensagem)

# Assinatura digital
assinatura = pkcs1_15.new(chave_privada).sign(hash_msg)
assinatura_b64 = base64.b64encode(assinatura).decode()
print("Assinatura (Base64):", assinatura_b64)

# Verificação da assinatura
try:
    pkcs1_15.new(chave_publica).verify(hash_msg, assinatura)
    print("Resultado: ✅ PASS - Assinatura válida")
except (ValueError, TypeError):
    print("Resultado: ❌ FAIL - Assinatura inválida")
