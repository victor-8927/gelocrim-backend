HTML_PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Remover a linha duplicada const custoTotal
OLD_DUP = """  const custoTotal = custoDia + custoDiesel + custoManut + ipvaDia;
  const custoTotal = custoDia + custoDiesel + custoManut;"""

NEW_DUP = """  const custoTotal = custoDia + custoDiesel + custoManut + ipvaDia;"""

if OLD_DUP in content:
    content = content.replace(OLD_DUP, NEW_DUP)
    print("✅ custoTotal duplicado corrigido")
else:
    # Tentar outra ordem
    OLD_DUP2 = """  const custoTotal = custoDia + custoDiesel + custoManut;
  const custoTotal = custoDia + custoDiesel + custoManut + ipvaDia;"""
    if OLD_DUP2 in content:
        content = content.replace(OLD_DUP2, NEW_DUP)
        print("✅ custoTotal duplicado corrigido (ordem 2)")
    else:
        # Buscar todas as ocorrencias de custoTotal
        import re
        ocorrencias = [(m.start(), m.group()) for m in re.finditer(r'const custoTotal[^\n]+', content)]
        print(f"Encontradas {len(ocorrencias)} ocorrencias de custoTotal:")
        for pos, txt in ocorrencias:
            print(f"  pos {pos}: {txt}")
        
        if len(ocorrencias) == 2:
            # Remover a segunda ocorrencia
            segunda_pos = ocorrencias[1][0]
            segunda_txt = ocorrencias[1][1]
            content = content[:segunda_pos] + content[segunda_pos:].replace(segunda_txt + '\n', '', 1)
            print("✅ Segunda declaração de custoTotal removida")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Arquivo salvo! Recarregue com Ctrl+Shift+R")
