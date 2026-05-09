path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'id="modal-base-clientes"' in content:
    print('Modal JÁ EXISTE!')
    import re
    ocorr = [m.start() for m in re.finditer('id="modal-base-clientes"', content)]
    print(f'Encontrado {len(ocorr)}x')
else:
    print('Modal NAO existe — adicionando...')

    modal = '''
  <!-- MODAL IMPORTAR PARCEIROS -->
  <div id="modal-base-clientes" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:3000;align-items:center;justify-content:center;padding:20px">
    <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:560px;max-height:90vh;overflow-y:auto">
      <div style="padding:16px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0">
        <div>
          <div style="font-size:15px;font-weight:700;color:#e8f0fe">&#x1F91D; Importar Parceiros</div>
          <div style="font-size:11px;color:#90afd4;margin-top:2px">Planilha com CODIGO_ERP, LATITUDE, LONGITUDE e demais campos</div>
        </div>
        <button onclick="document.getElementById('modal-base-clientes').style.display='none'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">&#x2715;</button>
      </div>
      <div style="padding:20px 24px">
        <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:12px;margin-bottom:16px;font-size:11px;color:#90afd4;line-height:1.8">
          <b style="color:#64B4FF">Colunas esperadas:</b><br>
          <span style="color:#10b981">CODIGO_ERP, NOME_FANTASIA, RAZAO_SOCIAL, ENDERECO, CEP, BAIRRO, CIDADE/UF</span><br>
          <span style="color:#f59e0b">LATITUDE, LONGITUDE, CPF/CNPJ, SEGMENTO, ZONA_GEO, Comodatos, Tempo Medio Entrega, Rota</span>
        </div>
        <div onclick="document.getElementById('base-clientes-input').click()" style="border:2px dashed #1e3a5c;border-radius:10px;padding:28px;text-align:center;cursor:pointer;margin-bottom:16px;transition:.2s" onmouseover="this.style.borderColor='#64B4FF'" onmouseout="this.style.borderColor='#1e3a5c'">
          <div style="font-size:32px;margin-bottom:8px">&#x1F4C4;</div>
          <div style="font-size:14px;color:#e8f0fe;font-weight:600">Clique para selecionar o arquivo XLS/XLSX</div>
          <div style="font-size:11px;color:#90afd4;margin-top:4px" id="base-clientes-nome">Nenhum arquivo selecionado</div>
          <div style="font-size:12px;color:#64B4FF;margin-top:6px;font-weight:600" id="base-clientes-count"></div>
        </div>
        <input type="file" id="base-clientes-input" accept=".xls,.xlsx,.csv" style="display:none" onchange="lerBaseClientesXLS(this)">
        <div style="display:flex;gap:10px;justify-content:flex-end;padding-top:12px;border-top:1px solid #1e3a5c">
          <button onclick="document.getElementById('modal-base-clientes').style.display='none'" class="btn btn-secondary">Cancelar</button>
          <button id="btn-importar-base" onclick="importarBaseClientes()" disabled class="btn btn-primary" style="opacity:.5;cursor:not-allowed">&#x1F4E5; Importar Parceiros</button>
        </div>
      </div>
    </div>
  </div>
'''
    last_body = content.rfind('\n</body>')
    content = content[:last_body] + modal + content[last_body:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Modal adicionado! Ctrl+Shift+R.')
