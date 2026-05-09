path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

opens  = [334, 17189, 149673, 197227, 206600]
closes = [466, 17271, 210250, 210262]

# Mostra contexto ao redor de cada close
print('=== CLOSES ===')
for c in closes:
    print(f'Pos {c}: {repr(content[c-30:c+15])}')

print('\n=== SEQUÊNCIA ESPERADA ===')
# open 334   -> close 466     ✓ (SheetJS CDN script)
# open 17189 -> close 17271   ✓ (outro script pequeno)  
# open 149673 -> precisa close depois de 206600
# open 197227 -> close 210250 ✓
# open 206600 -> close 210262 ✓
# Falta: close para 149673 antes de 197227

print('Script 149673 vai até onde?')
# Encontra o conteúdo entre 149673 e 197227
trecho = content[149673:197227]
print(f'Tamanho: {len(trecho)} chars')
print('Final do trecho:')
print(repr(trecho[-200:]))
