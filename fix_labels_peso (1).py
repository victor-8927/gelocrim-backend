PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(PATH, encoding='utf-8', errors='ignore') as f:
    content = f.read()

changes = 0

replacements = [
    ('PESO TOTAL', 'PESO BRUTO'),
    ('Peso Total', 'Peso Bruto'),
    ('peso total', 'peso bruto'),
    ('ENTREGA', 'PESO LÍQUIDO'),
    ('>Entrega<', '>Peso Líquido<'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"OK: '{old}' -> '{new}'")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes} substituicoes! Ctrl+Shift+R no navegador!")
