#!/bin/bash
# =========================================================
# Script: run_all_tests.sh
# Objetivo: Executar todos os testes funcionais (KAT)
# Autor: Robson Santos
# =========================================================

ROOT_DIR=$(pwd)
RESULTS_DIR="$ROOT_DIR/results"
LOG_FILE="$RESULTS_DIR/test_run_$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$RESULTS_DIR"

echo "======================================" | tee -a "$LOG_FILE"
echo "EXECUÇÃO AUTOMATIZADA DE TESTES KAT" | tee -a "$LOG_FILE"
echo "Data: $(date)" | tee -a "$LOG_FILE"
echo "======================================" | tee -a "$LOG_FILE"

# ===== Teste PyCryptodome =====
echo -e "\n>>> [1/3] Executando testes PyCryptodome..." | tee -a "$LOG_FILE"
cd "$ROOT_DIR/tests/pycryptodome"
python3 kat_test_pycryptodome_extended.py | tee -a "$LOG_FILE"

# ===== Teste OpenSSL =====
echo -e "\n>>> [2/3] Executando testes OpenSSL..." | tee -a "$LOG_FILE"
cd "$ROOT_DIR/tests/openssl"
bash kat_test_openssl_extended.sh | tee -a "$LOG_FILE"

# ===== Teste BouncyCastle =====
echo -e "\n>>> [3/3] Executando testes BouncyCastle..." | tee -a "$LOG_FILE"
cd "$ROOT_DIR/tests/bouncycastle"
javac -cp .:bcprov-jdk18on-176.jar KATTestBouncyCastleExtended.java
java -cp .:bcprov-jdk18on-176.jar KATTestBouncyCastleExtended | tee -a "$LOG_FILE"

# ===== Consolidação dos Resultados =====
cd "$RESULTS_DIR"
echo -e "\n>>> Consolidação de resultados finalizada."
echo "Resultados salvos em: $LOG_FILE"
