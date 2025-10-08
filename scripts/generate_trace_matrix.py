import csv
import os
import re
from datetime import datetime

# Caminhos principais
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
LOG_FILES = sorted(
    [f for f in os.listdir(RESULTS_DIR) if f.startswith("test_run_") and f.endswith(".log")],
    reverse=True
)

if not LOG_FILES:
    print("❌ Nenhum arquivo de log encontrado em /results.")
    exit(1)

latest_log = os.path.join(RESULTS_DIR, LOG_FILES[0])
trace_file = os.path.join(RESULTS_DIR, "matriz_rastreabilidade.csv")

print(f"📄 Processando log mais recente: {latest_log}")

# Padrões para extração de resultados
pattern = re.compile(
    r"=== TESTE (RSA|ECDSA)/(SHA-\d{3}) ===|Resultado (RSA|ECDSA):\s*(✅ PASS|❌ FAIL)"
)

# Mapeamento auxiliar
library_map = {
    "pycryptodome": "PyCryptodome",
    "openssl": "OpenSSL",
    "bouncycastle": "BouncyCastle"
}

# Detectar biblioteca com base no log
def detect_library(log_path):
    if "pycryptodome" in log_path:
        return "PyCryptodome"
    elif "openssl" in log_path:
        return "OpenSSL"
    elif "bouncycastle" in log_path:
        return "BouncyCastle"
    else:
        return "Desconhecida"

# Extrair resultados
results = []
with open(latest_log, "r", encoding="utf-8") as log:
    lines = log.readlines()

current_alg = None
current_hash = None
library = None
for line in lines:
    line_strip = line.strip()
    lib_detected = detect_library(latest_log)

    match = pattern.search(line_strip)
    if not match:
        continue

    # Identificação do início do teste
    if "===" in line_strip:
        parts = re.findall(r"(RSA|ECDSA)|(SHA-\d{3})", line_strip)
        alg = next((a for a, _ in parts if a), None)
        hash_type = next((h for _, h in parts if h), None)
        current_alg, current_hash, library = alg, hash_type, lib_detected

    # Resultado do teste
    if "Resultado" in line_strip:
        outcome = "PASS" if "PASS" in line_strip else "FAIL"
        results.append({
            "Biblioteca": library,
            "Algoritmo": current_alg,
            "Hash": current_hash,
            "Resultado": outcome
        })

# Criar arquivo CSV se não existir
header = [
    "Data",
    "Teste ID",
    "Biblioteca",
    "Algoritmo",
    "Hash",
    "Vetor de Teste",
    "Resultado",
    "Observações"
]

file_exists = os.path.exists(trace_file)
with open(trace_file, "a", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    if not file_exists:
        writer.writeheader()

    for i, result in enumerate(results, start=1):
        writer.writerow({
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Teste ID": f"KAT-{datetime.now().strftime('%y%m%d')}-{i:02d}",
            "Biblioteca": result["Biblioteca"],
            "Algoritmo": result["Algoritmo"],
            "Hash": result["Hash"],
            "Vetor de Teste": "Mensagem ICP-Brasil",
            "Resultado": result["Resultado"],
            "Observações": "Execução automatizada via script"
        })

print(f"✅ Matriz de rastreabilidade atualizada com {len(results)} registros.")
print(f"📊 Arquivo salvo em: {trace_file}")
