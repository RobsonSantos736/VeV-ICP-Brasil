# VeV-ICP-Brasil
Estudo de modelos de teste adequados à Verificação e Validação de bibliotecas de assinaturas digitais em conformidade com padrões de certificação digital ICP-Brasil.

Procedimentos Práticos de Execução dos Testes de Conformidade
1. Teste Funcional – Known Answer Test (KAT)
Objetivo:
Confirmar se as bibliotecas geram e validam assinaturas digitais corretamente, reproduzindo vetores de teste com resultados previamente conhecidos.
Procedimentos:
    1. Selecionar pares de chaves (RSA e ECDSA) com tamanhos compatíveis aos definidos no DOC-ICP-01.01 (2048 bits para RSA e curvas P-256 e P-384 para ECDSA).
    2. Gerar mensagens de entrada fixas (exemplo: "Mensagem de teste ICP-Brasil") e calcular seus hashes com SHA-256 e SHA-512.
    3. Assinar as mensagens utilizando cada biblioteca:
        ◦ OpenSSL: openssl dgst -sha256 -sign chave_privada.pem -out assinatura.bin mensagem.txt
        ◦ PyCryptodome (Python):
          from Crypto.Signature import pkcs1_15
          from Crypto.Hash import SHA256
          from Crypto.PublicKey import RSA
          
          key = RSA.import_key(open('chave_privada.pem').read())
          h = SHA256.new(b'Mensagem de teste ICP-Brasil')
          assinatura = pkcs1_15.new(key).sign(h)
        ◦ BouncyCastle (Java): utilizar Signature.getInstance("SHA256withRSA").
    4. Verificar as assinaturas com as respectivas chaves públicas e comparar os resultados com os vetores conhecidos (KATs).
    5. Registrar no log: entrada, saída, algoritmo, resultado (pass/fail).
Evidência gerada:
Log de execução contendo o valor do hash, a assinatura gerada e o resultado da verificação (pass/fail).
1.1 PyCryptodome (Python)
1.1.1. PyCryptodome (Python) — RSA e ECDSA
       Geração de chaves:
       # RSA 2048 bits
openssl genrsa -out keys/chave_privada_rsa.pem 2048
openssl rsa -in keys/chave_privada_rsa.pem -pubout -out keys/chave_publica_rsa.pem

        # ECDSA P-256
openssl ecparam -genkey -name prime256v1 -noout -out keys/chave_privada_ecdsa.pem
openssl ec -in keys/chave_privada_ecdsa.pem -pubout -out keys/chave_publica_ecdsa.pem

1.2. OpenSSL (Shell Script / Bash)
Pré-requisito: As chaves RSA devem ser previamente geradas, por exemplo:
openssl genrsa -out chave_privada.pem 2048
openssl rsa -in chave_privada.pem -pubout -out chave_publica.pem
1.2.2. OpenSSL (Shell Script) — RSA e ECDSA


1.3. BouncyCastle (Java)
Dependência: adicionar o BouncyCastle ao classpath, por exemplo:
javac -cp bcprov-jdk18on-176.jar KATTestBouncyCastle.java
java -cp .:bcprov-jdk18on-176.jar KATTestBouncyCastle
1.3.3. BouncyCastle (Java) — RSA e ECDSA
Para gerar chaves DER a partir das PEM:
openssl pkcs8 -topk8 -inform PEM -outform DER -in chave_privada_rsa.pem -out chave_privada_rsa.der -nocrypt
openssl rsa -in chave_privada_rsa.pem -pubout -outform DER -out chave_publica_rsa.der

openssl pkcs8 -topk8 -inform PEM -outform DER -in chave_privada_ecdsa.pem -out chave_privada_ecdsa.der -nocrypt
openssl ec -in chave_privada_ecdsa.pem -pubout -outform DER -out chave_publica_ecdsa.der



2. Teste de Conformidade – Independent Algorithm Verification (IAV)
Objetivo:
Avaliar se as bibliotecas seguem corretamente os parâmetros e tamanhos de chave exigidos pelos padrões da ICP-Brasil.
Procedimentos:
    1. Configurar o ambiente de teste com chaves e algoritmos conforme o DOC-ICP-01.01:
        ◦ RSA: 2048 ou 4096 bits
        ◦ ECDSA: curvas P-256 e P-384
        ◦ Hashes: SHA-1, SHA-256, SHA-512
    2. Tentar gerar chaves fora dos tamanhos permitidos (ex.: RSA 1024 bits) e verificar se a biblioteca bloqueia ou emite erro.
    3. Analisar o formato dos certificados ou assinaturas (DER/PEM) para validar se seguem o padrão ASN.1 e OIDs corretos (sha256WithRSAEncryption, etc.).
    4. Registrar resultados em uma Matriz de Aderência (Apêndice A), marcando:
        ◦ Algoritmo testado
        ◦ Parâmetro aplicado
        ◦ Resultado esperado
        ◦ Resultado obtido
        ◦ Status: Conforme / Parcial / Não Conforme
Evidência gerada:
Relatório de conformidade e matriz de aderência, contendo parâmetros aceitos e rejeitados, e respectiva análise normativa.

3. Teste Estrutural – CAVP-like
Objetivo:
Simular os testes de validação do NIST/CAVP, analisando o comportamento interno das funções criptográficas e o desempenho em múltiplas execuções.
Procedimentos:
    1. Definir um conjunto de vetores CAVP-like, com entradas controladas (mensagens, chaves e hashes pré-gerados).
    2. Executar séries de assinaturas e verificações em ciclos repetidos (ex.: 100 execuções por biblioteca).
    3. Medir os tempos médios de:
        ◦ Geração de chaves
        ◦ Assinatura
        ◦ Verificação
    4. Coletar resultados intermediários, avaliando:
        ◦ Correção do resultado
        ◦ Desvios de tempo significativos
        ◦ Consistência entre execuções
    5. Comparar os resultados obtidos com padrões de desempenho de bibliotecas certificadas no CAVP/CMVP (NIST).
Evidência gerada:
Tabela de desempenho (tempo médio, desvio-padrão, sucesso de verificação), acompanhada de registros intermediários e logs.
