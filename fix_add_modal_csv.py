path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

modal_html = '''
  <!-- MODAL IMPORTAÇÃO CSV SANKHYA -->
  <div id="modal-importacao-csv" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:3000;align-items:center;justify-content:center;padding:20px">
    <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:700px;max-height:90vh;overflow-y:auto">
      <div style="padding:18px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0">
        <div>
          <div style="font-size:16px;font-weight:700;color:#e8f0fe">📥 Importar Pedidos — CSV Sankhya</div>
          <div style="font-size:11px;color:#90afd4;margin-top:2px">Campos: NUNOTA, NOMEPARC, ENDERECO, PESO, VOLUME, CODTIPOPER, VLRNOTA</div>
        </div>
        <button onclick="document.getElementById('modal-importacao-csv').style.display='none'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">✕</button>
      </div>
      <div style="padding:20px 24px">
        <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:14px;margin-bottom:20px">
          <div style="font-size:11px;font-weight:700;color:#64B4FF;margin-bottom:6px">📋 FORMATO</div>
          <div style="font-size:11px;color:#90afd4;line-height:1.8;font-family:monospace">
            Obrigatórios: <span style="color:#10b981">NUNOTA, PESO</span><br>
            Usados: <span style="color:#f59e0b">NOMEPARC, ENDERECO, CIDADE, VOLUME, DTNEG, CODTIPOPER, VLRNOTA</span><br>
            Demais colunas: <span style="color:#64B4FF">ignoradas automaticamente</span>
          </div>
        </div>
        <div onclick="document.getElementById('csv-file-input').click()" style="border:2px dashed #1e3a5c;border-radius:10px;padding:30px;text-align:center;margin-bottom:20px;cursor:pointer">
          <div style="font-size:36px;margin-bottom:8px">📄</div>
          <div style="font-size:14px;color:#e8f0fe;font-weight:600">Clique para selecionar o arquivo CSV</div>
          <div style="font-size:11px;color:#90afd4;margin-top:4px" id="csv-nome-arquivo">Nenhum arquivo selecionado</div>
        </div>
        <input type="file" id="csv-file-input" accept=".csv,.txt" style="display:none" onchange="lerArquivoCSV(this)">
        <div id="csv-preview" style="display:none;margin-bottom:20px">
          <div style="font-size:11px;font-weight:700;color:#64B4FF;margin-bottom:8px">👁️ PRÉVIA DOS DADOS</div>
          <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;overflow-x:auto;max-height:200px;overflow-y:auto">
            <table id="csv-preview-table" style="font-size:11px;min-width:100%"></table>
          </div>
          <div style="margin-top:8px;font-size:12px;color:#90afd4">
            Total: <b style="color:#64B4FF" id="csv-total-linhas">0</b> linhas &nbsp;|&nbsp;
            Válidos: <b style="color:#10b981" id="csv-validos">0</b> &nbsp;|&nbsp;
            Erros: <b style="color:#f87171" id="csv-erros">0</b>
          </div>
        </div>
        <div id="csv-opcoes" style="display:none;margin-bottom:20px">
          <div style="display:grid;gap:8px">
            <label style="display:flex;align-items:center;gap:8px;font-size:12px;color:#e8f0fe;cursor:pointer">
              <input type="checkbox" id="csv-opt-duplicados" checked style="accent-color:#64B4FF">
              Ignorar pedidos já importados (mesmo NUNOTA)
            </label>
            <label style="display:flex;align-items:center;gap:8px;font-size:12px;color:#e8f0fe;cursor:pointer">
              <input type="checkbox" id="csv-opt-data-hoje" checked style="accent-color:#64B4FF">
              Usar data de hoje como data de entrega
            </label>
          </div>
        </div>
        <div id="csv-resultado" style="display:none;padding:12px;border-radius:8px;margin-bottom:20px"></div>
        <div style="display:flex;gap:10px;justify-content:flex-end;padding-top:12px;border-top:1px solid #1e3a5c">
          <button onclick="document.getElementById('modal-importacao-csv').style.display='none'" class="btn btn-secondary">Cancelar</button>
          <button id="btn-importar-csv" onclick="importarCSV()" disabled class="btn btn-primary" style="opacity:.5;cursor:not-allowed">📥 Importar Pedidos</button>
        </div>
      </div>
    </div>
  </div>
'''

if modal_html.strip()[:50] not in content:
    content = content.replace('</body>', modal_html + '\n</body>')
    print('Modal CSV adicionado ao HTML!')
else:
    print('Modal já existe!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
