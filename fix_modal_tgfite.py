path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adiciona modal TGFITE após o modal de importação CSV existente
old_modal_end = "  <!-- MODAL IMPORTAÇÃO CSV SANKHYA -->"
new_modal = """  <!-- MODAL IMPORTAÇÃO ITENS TGFITE -->
  <div id="modal-importacao-itens" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:3000;display:none;align-items:center;justify-content:center;padding:20px">
    <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:680px;max-height:90vh;overflow-y:auto">
      <div style="padding:18px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0">
        <div>
          <div style="font-size:16px;font-weight:700;color:#e8f0fe">📦 Importar Itens — TGFITE Sankhya</div>
          <div style="font-size:11px;color:#90afd4;margin-top:2px">Importe as 4 planilhas separadamente, uma por tipo de gelo</div>
        </div>
        <button onclick="fecharModalItens()" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">✕</button>
      </div>
      <div style="padding:20px 24px">
        <!-- Seletor de tipo de gelo -->
        <div style="margin-bottom:16px">
          <div style="font-size:11px;font-weight:700;color:#64B4FF;margin-bottom:8px">1. SELECIONE O TIPO DE GELO DESTA PLANILHA</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
            <button onclick="selecionarTipoGelo('gelo5','Gelo 5kg',6)" id="btn-gelo5"
              style="padding:12px;border:2px solid #1e3a5c;background:#0a1628;color:#90afd4;border-radius:8px;cursor:pointer;font-weight:600;font-size:13px">
              🧊 Gelo 5kg <span style="font-size:10px;color:#64B4FF">(6kg real)</span>
            </button>
            <button onclick="selecionarTipoGelo('gelo10','Gelo 10kg',11)" id="btn-gelo10"
              style="padding:12px;border:2px solid #1e3a5c;background:#0a1628;color:#90afd4;border-radius:8px;cursor:pointer;font-weight:600;font-size:13px">
              🧊 Gelo 10kg <span style="font-size:10px;color:#64B4FF">(11kg real)</span>
            </button>
            <button onclick="selecionarTipoGelo('gelo20','Gelo 20kg',23)" id="btn-gelo20"
              style="padding:12px;border:2px solid #1e3a5c;background:#0a1628;color:#90afd4;border-radius:8px;cursor:pointer;font-weight:600;font-size:13px">
              🧊 Gelo 20kg <span style="font-size:10px;color:#64B4FF">(23kg real)</span>
            </button>
            <button onclick="selecionarTipoGelo('gelo40','Gelo 40kg',45)" id="btn-gelo40"
              style="padding:12px;border:2px solid #1e3a5c;background:#0a1628;color:#90afd4;border-radius:8px;cursor:pointer;font-weight:600;font-size:13px">
              🧊 Gelo 40kg <span style="font-size:10px;color:#64B4FF">(45kg real)</span>
            </button>
          </div>
        </div>
        <!-- Upload arquivo -->
        <div style="margin-bottom:16px">
          <div style="font-size:11px;font-weight:700;color:#64B4FF;margin-bottom:8px">2. SELECIONE A PLANILHA</div>
          <div onclick="document.getElementById('tgfite-file-input').click()" style="border:2px dashed #1e3a5c;border-radius:10px;padding:24px;text-align:center;cursor:pointer">
            <div style="font-size:32px;margin-bottom:6px">📄</div>
            <div style="font-size:13px;color:#e8f0fe;font-weight:600">Clique para selecionar (XLS ou XLSX)</div>
            <div style="font-size:11px;color:#90afd4;margin-top:4px" id="tgfite-nome-arquivo">Nenhum arquivo selecionado</div>
          </div>
          <input type="file" id="tgfite-file-input" accept=".xls,.xlsx,.csv" style="display:none" onchange="lerArquivoTGFITE(this)">
        </div>
        <!-- Preview -->
        <div id="tgfite-preview" style="display:none;margin-bottom:16px">
          <div style="font-size:11px;font-weight:700;color:#64B4FF;margin-bottom:8px">👁️ PRÉVIA</div>
          <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;overflow-x:auto;max-height:180px;overflow-y:auto">
            <table id="tgfite-preview-table" style="font-size:11px;min-width:100%"></table>
          </div>
          <div style="margin-top:8px;font-size:12px;color:#90afd4">
            Total: <b style="color:#64B4FF" id="tgfite-total">0</b> linhas &nbsp;|&nbsp;
            Válidos: <b style="color:#10b981" id="tgfite-validos">0</b> &nbsp;|&nbsp;
            Erros: <b style="color:#f87171" id="tgfite-erros">0</b>
          </div>
        </div>
        <!-- Botão importar -->
        <button id="btn-importar-itens" onclick="importarItensTGFITE()" disabled
          style="width:100%;padding:14px;background:#10b981;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;opacity:0.5">
          📦 Importar Itens
        </button>
        <!-- Status dos 4 tipos -->
        <div style="margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:6px">
          <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:6px;padding:8px;text-align:center">
            <div id="status-gelo5" style="font-size:20px">⬜</div>
            <div style="font-size:10px;color:#90afd4">Gelo 5kg</div>
            <div id="count-gelo5" style="font-size:11px;color:#10b981"></div>
          </div>
          <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:6px;padding:8px;text-align:center">
            <div id="status-gelo10" style="font-size:20px">⬜</div>
            <div style="font-size:10px;color:#90afd4">Gelo 10kg</div>
            <div id="count-gelo10" style="font-size:11px;color:#10b981"></div>
          </div>
          <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:6px;padding:8px;text-align:center">
            <div id="status-gelo20" style="font-size:20px">⬜</div>
            <div style="font-size:10px;color:#90afd4">Gelo 20kg</div>
            <div id="count-gelo20" style="font-size:11px;color:#10b981"></div>
          </div>
          <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:6px;padding:8px;text-align:center">
            <div id="status-gelo40" style="font-size:20px">⬜</div>
            <div style="font-size:10px;color:#90afd4">Gelo 40kg</div>
            <div id="count-gelo40" style="font-size:11px;color:#10b981"></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL IMPORTAÇÃO CSV SANKHYA -->"""

content = content.replace(old_modal_end, new_modal)
print('Modal TGFITE adicionado!')

# 2. Adiciona botão na tela de Pedidos (junto ao botão de importar CSV)
old_btn_import = '''onclick="document.getElementById('csv-file-input').click()"'''
# Busca o botão de importar na tela pedidos (não no modal)
idx = content.find('Importar CSV')
ln = content[:idx].count('\n')+1
print(f'Botão Importar CSV linha {ln}')

# Adiciona botão Importar Itens após botão Importar CSV na toolbar
old_toolbar = '''<button class="btn btn-primary" onclick="document.getElementById('modal-importacao-csv').style.display='flex'">📥 Importar CSV</button>'''
new_toolbar = '''<button class="btn btn-primary" onclick="document.getElementById('modal-importacao-csv').style.display='flex'">📥 Importar CSV</button>
      <button class="btn btn-secondary" onclick="abrirModalItens()" style="background:rgba(16,185,129,.15);border-color:#10b981;color:#10b981">📦 Importar Itens</button>'''

if old_toolbar in content:
    content = content.replace(old_toolbar, new_toolbar)
    print('Botão Importar Itens adicionado na toolbar!')
else:
    # Tenta variação
    idx2 = content.find("'modal-importacao-csv'")
    ln2 = content[:idx2].count('\n')+1
    print(f'Modal CSV ref linha {ln2}: {repr(content[max(0,idx2-80):idx2+50])}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Agora adicionando JS...')
