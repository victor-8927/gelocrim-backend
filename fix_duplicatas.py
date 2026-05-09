import re

path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Verifica linha 3503 ────────────────────────────────────────
lines = content.split('\n')
print('=== LINHAS 3498-3510 ===')
for i in range(3497, min(3510, len(lines))):
    print(f'{i+1}: {lines[i][:120]}')

# ── 2. Conta declarações de _clientesCache ────────────────────────
ocorr = [m.start() for m in re.finditer(r'let _clientesCache', content)]
print(f'\nlet _clientesCache encontrado: {len(ocorr)}x nas posições: {ocorr}')

# ── 3. Remove blocos <script> duplicados do _clientesCache ────────
# Encontra todos os blocos <script> que contêm _clientesCache
blocks = list(re.finditer(r'<script>\s*//\s*── BASE DE CLIENTES.*?</script>', content, re.DOTALL))
print(f'Blocos BASE DE CLIENTES: {len(blocks)}')

if len(blocks) > 1:
    # Remove todos menos o último
    for b in reversed(blocks[:-1]):
        content = content[:b.start()] + content[b.end():]
    print('Blocos duplicados removidos!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nVerificação e limpeza concluída!')
