#!/bin/bash
MSG="mensagem.txt"
echo "Mensagem de teste ICP-Brasil" > $MSG

# ===== RSA/SHA-256 =====
echo -e "\n=== TESTE RSA/SHA-256 ==="
openssl dgst -sha256 -sign keys/chave_privada_rsa.pem -out rsa_assinatura.bin $MSG
openssl dgst -sha256 -verify keys/chave_publica_rsa.pem -signature rsa_assinatura.bin $MSG
if [ $? -eq 0 ]; then
  echo "Resultado RSA: ✅ PASS"
else
  echo "Resultado RSA: ❌ FAIL"
fi

# ===== ECDSA/SHA-512 =====
echo -e "\n=== TESTE ECDSA/SHA-512 ==="
openssl dgst -sha512 -sign keys/chave_privada_ecdsa.pem -out ecdsa_assinatura.bin $MSG
openssl dgst -sha512 -verify keys/chave_publica_ecdsa.pem -signature ecdsa_assinatura.bin $MSG
if [ $? -eq 0 ]; then
  echo "Resultado ECDSA: ✅ PASS"
else
  echo "Resultado ECDSA: ❌ FAIL"
fi
