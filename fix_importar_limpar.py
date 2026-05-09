path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Adiciona opção de limpar pedidos antigos no modal ──────────
old_opcoes = '''              Ignorar pedidos já importados (mesmo NUNOTA)
            </label>
            <label style="display:flex;align-items:center;gap:8px;font-size:12px;color:#e8f0fe;cursor:pointer">
              <input type="checkbox" id="csv-opt-data-hoje" checked style="accent-color:#64B4FF">
              Usar data de hoje como data de entrega
            </label>'''

new_opcoes = '''              Ignorar pedidos já importados (mesmo NUNOTA)
            </label>
            <label style="display:flex;align-items:center;gap:8px;font-size:12px;color:#e8f0fe;cursor:pointer">
              <input type="checkbox" id="csv-opt-data-hoje" checked style="accent-color:#64B4FF">
              Usar data de hoje como data de entrega
            </label>
            <label style="display:flex;align-items:center;gap:8px;font-size:12px;color:#f59e0b;cursor:pointer;background:rgba(245,158,11,.08);padding:8px;border-radius:6px;border:1px solid rgba(245,158,11,.3)">
              <input type="checkbox" id="csv-opt-limpar" checked style="accent-color:#f59e0b">
              <span>⚠️ <b>Substituir pedidos pendentes</b> — apaga os anteriores e importa só desta planilha</span>
            </label>'''

if old_opcoes in content:
    content = content.replace(old_opcoes, new_opcoes)
    print('Opção de limpar adicionada no modal!')

# ── 2. Atualiza a função importarCSV para limpar antes ────────────
old_import_start = '''async function importarCSV() {
  if (_csvDados.length === 0) { toast('Nenhum dado!', 'error'); return; }
  const btn = document.getElementById('btn-importar-csv');
  btn.disabled=true; btn.textContent='⏳ Importando...';

  const ignorarDup = document.getElementById('csv-opt-duplicados').checked;
  const usarHoje   = document.getElementById('csv-opt-data-hoje').checked;
  const hoje       = new Date().toISOString().slice(0,10);

  let existentes = [];
  if (ignorarDup) {
    try { const ords=await api('GET','/orders'); existentes=ords.map(o=>o.external_id); } catch(e) {}
  }

  let importados=0, duplicados=0, erros=0;'''

new_import_start = '''async function importarCSV() {
  if (_csvDados.length === 0) { toast('Nenhum dado!', 'error'); return; }
  const btn = document.getElementById('btn-importar-csv');
  btn.disabled=true; btn.textContent='⏳ Importando...';

  const ignorarDup = document.getElementById('csv-opt-duplicados').checked;
  const usarHoje   = document.getElementById('csv-opt-data-hoje').checked;
  const limparAnt  = document.getElementById('csv-opt-limpar')?.checked ?? true;
  const hoje       = new Date().toISOString().slice(0,10);

  // Limpa pedidos pendentes antes de importar
  if (limparAnt) {
    try {
      btn.textContent = '⏳ Limpando pedidos antigos...';
      const ords = await api('GET', '/orders?status=pending&limit=500');
      let apagados = 0;
      for (const o of ords) {
        try { await api('DELETE', `/orders/${o.id}`); apagados++; } catch(e) {}
      }
      console.log(`${apagados} pedidos pendentes removidos`);
    } catch(e) { console.log('Erro ao limpar:', e.message); }
  }

  let existentes = [];
  if (ignorarDup && !limparAnt) {
    try { const ords=await api('GET','/orders'); existentes=ords.map(o=>o.external_id); } catch(e) {}
  }

  let importados=0, duplicados=0, erros=0;'''

if old_import_start in content:
    content = content.replace(old_import_start, new_import_start)
    print('Função importarCSV atualizada!')
else:
    print('Padrão não encontrado — buscando...')
    idx = content.find('async function importarCSV()')
    if idx != -1:
        print(content[idx:idx+400])

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
