from Crypto.PublicKey import RSA, ECC
from Crypto.Signature import pkcs1_15, DSS
from Crypto.Hash import SHA256, SHA512
import base64

mensagem = b"Mensagem de teste ICP-Brasil"

# ===== RSA/SHA-256 =====
print("\n=== TESTE RSA/SHA-256 ===")

# Carregar chaves RSA
with open("keys/chave_privada_rsa.pem", "rb") as f:
    priv_rsa = RSA.import_key(f.read())
with open("keys/chave_publica_rsa.pem", "rb") as f:
    pub_rsa = RSA.import_key(f.read())

# Gera hash e assinatura
hash_rsa = SHA256.new(mensagem)
assinatura_rsa = pkcs1_15.new(priv_rsa).sign(hash_rsa)
print("Assinatura RSA (Base64):", base64.b64encode(assinatura_rsa).decode())

# Verificação
try:
    pkcs1_15.new(pub_rsa).verify(hash_rsa, assinatura_rsa)
    print("Resultado RSA: ✅ PASS - Assinatura válida")
except (ValueError, TypeError):
    print("Resultado RSA: ❌ FAIL - Assinatura inválida")

# ===== ECDSA/SHA-512 =====
print("\n=== TESTE ECDSA/SHA-512 ===")

# Carregar chaves ECC
with open("keys/chave_privada_ecdsa.pem", "rt") as f:
    priv_ecc = ECC.import_key(f.read())
with open("keys/chave_publica_ecdsa.pem", "rt") as f:
    pub_ecc = ECC.import_key(f.read())

# Gera hash e assinatura
hash_ecc = SHA512.new(mensagem)
assinatura_ecc = DSS.new(priv_ecc, 'fips-186-3').sign(hash_ecc)
print("Assinatura ECDSA (Base64):", base64.b64encode(assinatura_ecc).decode())

# Verificação
try:
    DSS.new(pub_ecc, 'fips-186-3').verify(hash_ecc, assinatura_ecc)
    print("Resultado ECDSA: ✅ PASS - Assinatura válida")
except ValueError:
    print("Resultado ECDSA: ❌ FAIL - Assinatura inválida")
