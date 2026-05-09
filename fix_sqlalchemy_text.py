# -*- coding: utf-8 -*-

import os
import re

BASE_DIR = r"C:\fleet-cloud"

def corrigir_arquivo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()

    original = conteudo

    conteudo = re.sub(
        r'(session\.execute\()\s*"(SELECT .*?)"',
        r'\1text("\2")',
        conteudo,
        flags=re.DOTALL | re.IGNORECASE
    )

    conteudo = re.sub(
        r'(db\.execute\()\s*"(SELECT .*?)"',
        r'\1text("\2")',
        conteudo,
        flags=re.DOTALL | re.IGNORECASE
    )

    if conteudo != original:
        print("Corrigido:", caminho)

        if "from sqlalchemy import text" not in conteudo:
            conteudo = "from sqlalchemy import text\n" + conteudo

        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)

def percorrer():
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".py"):
                caminho = os.path.join(root, file)
                corrigir_arquivo(caminho)

if __name__ == "__main__":
    percorrer()
    print("Correcao finalizada!")
