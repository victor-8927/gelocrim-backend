path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Corrige URL de orders (& → ?) ──────────────────────────────
content = content.replace(
    "api('GET', '/orders&limit=100')",
    "api('GET', '/orders?limit=100')"
)
content = content.replace(
    '"/orders&limit=100"',
    '"/orders?limit=100"'
)
content = content.replace(
    "`/orders&limit=100`",
    "`/orders?limit=100`"
)
print('URL de orders verificada!')

# ── 2. Corrige processarLinhas para encontrar linha de cabeçalho ───
old_process = '''function processarLinhas(rows) {
  // Normaliza header
  const header = rows[0].map(h => String(h).trim().toUpperCase().replace(/[^A-Z0-9_]/g,''));
  console.log('Colunas encontradas:', header);'''

new_process = '''function processarLinhas(rows) {
  // Encontra a linha real do cabeçalho
  // O Sankhya às vezes tem linhas de título antes do cabeçalho real
  let headerRowIdx = 0;
  const camposConhecidos = ['NROUNICO','NRO','VLRNOTA','VLR','PARCEIRO','PESO','NOME','NOTA','NUNOTA'];
  for (let r = 0; r < Math.min(10, rows.length); r++) {
    const rowNorm = rows[r].map(h => String(h||'').trim().toUpperCase().replace(/[^A-Z0-9]/g,''));
    const matches = camposConhecidos.filter(c => rowNorm.some(h => h.includes(c)));
    if (matches.length >= 2) {
      headerRowIdx = r;
      console.log(`Cabeçalho encontrado na linha ${r+1}:`, rows[r]);
      break;
    }
  }
  const header = rows[headerRowIdx].map(h => String(h||'').trim().toUpperCase().replace(/[^A-Z0-9 ().]/g,'').trim());
  console.log('Colunas encontradas:', header);'''

if old_process in content:
    content = content.replace(old_process, new_process)
    print('processarLinhas corrigido para detectar linha de cabeçalho!')
else:
    print('Padrão não encontrado, buscando...')
    idx = content.find('function processarLinhas(rows)')
    if idx != -1:
        print(content[idx:idx+300])

# ── 3. Corrige o loop de dados para começar após o cabeçalho ───────
old_loop = '''  for (let i = 1; i < rows.length; i++) {
    const cols = rows[i].map(c => String(c||'').trim());
    if (cols.join('').length === 0) continue;'''

new_loop = '''  for (let i = headerRowIdx + 1; i < rows.length; i++) {
    const cols = rows[i].map(c => String(c||'').trim());
    if (cols.join('').length === 0) continue;'''

if old_loop in content:
    content = content.replace(old_loop, new_loop)
    print('Loop de dados corrigido!')

# ── 4. Corrige contador de linhas ─────────────────────────────────
old_count = "document.getElementById('csv-total-linhas').textContent = rows.length - 1;"
new_count = "document.getElementById('csv-total-linhas').textContent = rows.length - headerRowIdx - 1;"

if old_count in content:
    content = content.replace(old_count, new_count)
    print('Contador corrigido!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Ctrl+Shift+R e teste o XLS novamente.')
