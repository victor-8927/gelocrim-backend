path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'modal-base-clientes' in content:
    import re
    ocorr = [m.start() for m in re.finditer('id="modal-base-clientes"', content)]
    print(f'Modal encontrado {len(ocorr)}x')
else:
    print('Modal NAO existe! Adicionando...')

    modal = '''
  <!-- MODAL BASE DE CLIENTES -->
  <div id="modal-base-clientes" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:3000;align-items:center;justify-content:center;padding:20px">
    <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:560px">
      <div style="padding:16px 20px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center">
        <div>
          <div style="font-size:15px;font-weight:700;color:#e8f0fe">&#128101; Importar Base de Clientes</div>
          <div style="font-size:11px;color:#90afd4">Relatorio de Parceiros do Sankhya (com GPS)</div>
        </div>
        <button onclick="document.getElementById('modal-base-clientes').style.display='none'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">&#x2715;</button>
      </div>
      <div style="padding:20px">
        <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:12px;margin-bottom:16px;font-size:11px;color:#90afd4;line-height:1.8">
          Exporte o relatorio <b style="color:#64B4FF">Parceiro</b> do Sankhya com as colunas:<br>
          <span style="color:#10b981">Cod. Parceiro, Nome Parceiro, Bairro, Cidade, Endereco, Numero, Latitude, Longitude</span><br>
          Apos importar, os pedidos do CSV terao <b style="color:#f59e0b">endereco e GPS automaticos</b>!
        </div>
        <div onclick="document.getElementById('base-clientes-input').click()" style="border:2px dashed #1e3a5c;border-radius:8px;padding:24px;text-align:center;cursor:pointer;margin-bottom:16px">
          <div style="font-size:28px;margin-bottom:6px">&#128101;</div>
          <div style="font-size:13px;color:#e8f0fe;font-weight:600">Clique para selecionar o XLS de Parceiros</div>
          <div style="font-size:11px;color:#90afd4;margin-top:4px" id="base-clientes-nome">Nenhum arquivo</div>
          <div style="font-size:12px;color:#64B4FF;margin-top:6px" id="base-clientes-count"></div>
        </div>
        <input type="file" id="base-clientes-input" accept=".xls,.xlsx,.csv" style="display:none" onchange="lerBaseClientesXLS(this)">
        <div style="display:flex;gap:8px;justify-content:flex-end">
          <button onclick="document.getElementById('modal-base-clientes').style.display='none'" class="btn btn-secondary">Cancelar</button>
          <button id="btn-importar-base" onclick="importarBaseClientes()" disabled class="btn btn-primary" style="opacity:.5;cursor:not-allowed">&#128229; Importar Base</button>
        </div>
      </div>
    </div>
  </div>
'''
    # Adiciona antes do último </body>
    last_body = content.rfind('\n</body>')
    content = content[:last_body] + modal + content[last_body:]
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Modal adicionado! Ctrl+Shift+R.')
