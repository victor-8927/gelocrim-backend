path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Função auxiliar de parse BR — injeta no JS
parse_fn = '''
function parseBR(v) {
  // Converte formato BR: 1.234,56 → 1234.56
  if (!v) return 0;
  const s = String(v).trim();
  // Se tem vírgula E ponto: ponto é milhar, vírgula é decimal
  if (s.includes(',') && s.includes('.')) {
    return parseFloat(s.replace(/\\./g,'').replace(',','.')) || 0;
  }
  // Se só vírgula: vírgula é decimal
  if (s.includes(',')) {
    return parseFloat(s.replace(',','.')) || 0;
  }
  return parseFloat(s) || 0;
}
'''

# Injeta a função se não existir
if 'function parseBR(' not in content:
    content = content.replace(
        'function processarLinhas(rows)',
        parse_fn + '\nfunction processarLinhas(rows)'
    )
    print('Função parseBR injetada!')

# Substitui todos os parses de peso/volume/valor por parseBR
replacements = [
    # peso
    ("get('peso').replace(/\\./g,'').replace(',','.')", "parseBR(get('peso'))"),
    ("get('peso').replace(',','.').replace(/[^\\d.]/g,'')", "parseBR(get('peso'))"),
    ("parseFloat(get('peso').replace(',','.').replace(/[^\\d.]/g,'')) || 0", "parseBR(get('peso'))"),
    # volume
    ("parseFloat(get('volume').replace(/\\./g,'').replace(',','.')) || 0", "parseBR(get('volume'))"),
    ("parseFloat(get('volume').replace(',','.').replace(/[^\\d.]/g,'')) || 0", "parseBR(get('volume'))"),
    # valor
    ("parseFloat(get('valor').replace(/\\./g,'').replace(',','.')) || 0", "parseBR(get('valor'))"),
    ("parseFloat(get('valor').replace(',','.').replace(/[^\\d.]/g,'')) || 0", "parseBR(get('valor'))"),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f'Substituído: {old[:50]}...')

# Corrige também o peso no push final
old_push_peso = "weight_kg:         peso,"
new_push_peso = "weight_kg:         parseBR(get('peso')),"
# Mantém como está — peso já foi calculado corretamente

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Ctrl+Shift+R e reimporte o XLS.')
print('Formato 1.234,56 → parseBR → 1234.56 ✅')
