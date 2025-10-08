import os
import re
import csv
from datetime import datetime
from base64 import b64encode

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
comparison_file = os.path.join(RESULTS_DIR, "comparativo_resultados.csv")

print(f"📄 Analisando arquivo de log: {latest_log}")

# Padrões de captura
pattern_alg = re.compile(r"=== TESTE (RSA|ECDSA)/(SHA-\d{3}) ===")
pattern_sig = re.compile(r"Assinatura (RSA|ECDSA).*?:\s*([A-Za-z0-9+/=]+)")
pattern_result = re.compile(r"Resultado (RSA|ECDSA).*?(PASS|FAIL)")

# Armazenamento de resultados
entries = []
current_library = None
if "pycryptodome" in latest_log:
    current_library = "PyCryptodome"
elif "openssl" in latest_log:
    current_library = "OpenSSL"
elif "bouncycastle" in latest_log:
    current_library = "BouncyCastle"

with open(latest_log, "r", encoding="utf-8") as f:
    data = f.read()

# Detectar múltiplos blocos (PyCryptodome, OpenSSL, BouncyCastle)
logs = data.split(">>> [")
libraries = ["PyCryptodome", "OpenSSL", "BouncyCastle"]

# Estrutura: {algoritmo: {biblioteca: assinatura}}
results_map = {}

for block, lib in zip(logs[1:], libraries):
    algos = pattern_alg.findall(block)
    sigs = pattern_sig.findall(block)
    outcomes = pattern_result.findall(block)

    for i, algo in enumerate(algos):
        algoritmo, hash_type = algo
        key = f"{algoritmo}/{hash_type}"
        assinatura = sigs[i][1] if i < len(sigs) else None
        resultado = outcomes[i][1] if i < len(outcomes) else None

        if key not in results_map:
            results_map[key] = {}
        results_map[key][lib] = {
            "assinatura": assinatura,
            "resultado": resultado
        }

# Criar/atualizar CSV
header = [
    "Data",
    "Algoritmo",
    "Implementação 1",
    "Implementação 2",
    "Assinatura_1",
    "Assinatura_2",
    "Comparativo",
    "Observações"
]

with open(comparison_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()

    for algoritmo, bibliotecas in results_map.items():
        libs = list(bibliotecas.keys())
        if len(libs) < 2:
            continue  # Não há comparações possíveis

        for i in range(len(libs) - 1):
            lib1, lib2 = libs[i], libs[i + 1]
            sig1 = bibliotecas[lib1].get("assinatura")
            sig2 = bibliotecas[lib2].get("assinatura")

            if sig1 and sig2:
                comparativo = "✅ Iguais" if sig1 == sig2 else "❌ Diferentes"
            else:
                comparativo = "⚠️ Incompleto"

            writer.writerow({
                "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Algoritmo": algoritmo,
                "Implementação 1": lib1,
                "Implementação 2": lib2,
                "Assinatura_1": sig1,
                "Assinatura_2": sig2,
                "Comparativo": comparativo,
                "Observações": "Comparação entre saídas baseadas no mesmo vetor de teste"
            })

print(f"✅ Comparativo de resultados gerado com sucesso!")
print(f"📊 Arquivo salvo em: {comparison_file}")
