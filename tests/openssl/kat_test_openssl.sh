#!/bin/bash
# Teste Funcional (KAT) - OpenSSL

MSG_FILE="mensagem.txt"
PRIV_KEY="chave_privada.pem"
PUB_KEY="chave_publica.pem"
SIGN_FILE="assinatura.bin"

echo "Mensagem de teste ICP-Brasil" > $MSG_FILE

# Gerar hash e assinatura digital com SHA-256
openssl dgst -sha256 -sign $PRIV_KEY -out $SIGN_FILE $MSG_FILE

# Verificar assinatura
openssl dgst -sha256 -verify $PUB_KEY -signature $SIGN_FILE $MSG_FILE

# Exibir resultado
if [ $? -eq 0 ]; then
  echo "Resultado: ✅ PASS - Assinatura válida"
else
  echo "Resultado: ❌ FAIL - Assinatura inválida"
fi
