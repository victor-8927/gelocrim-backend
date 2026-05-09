caminho = r"C:\fleet-cloud\gelocrim_v1.html"
with open(caminho, encoding="utf-8", errors="ignore") as f:
    data = f.read()

# Adicionar div resumo antes do thead da tabela
antigo = """<th>TOP</th>
                <th>T. ATEND.</th>
                <th>GPS</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody id="orders-tbody">"""

novo = """<th>TOP</th>
                <th>T. ATEND.</th>
                <th>GPS</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody id="orders-tbody">"""

# Buscar o elemento pai da tabela para inserir o div antes
antigo2 = '<th>Nº\n                Pedido</th>'
idx = data.find('orders-tbody')
# Encontrar abertura da tabela
idx_table = data.rfind('<table', 0, idx)
print(f"Table encontrada em pos {idx_table}")
print(repr(data[idx_table:idx_table+30]))

# Inserir div antes da table
antigo_table = data[idx_table:idx_table+7]
novo_div = '''<div id="resumo-quantidades" style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:8px 16px;margin-bottom:12px;display:flex;gap:12px;align-items:center;flex-wrap:wrap">
              <span style="font-size:11px;color:#90afd4;font-weight:700">📦 RESUMO DIA:</span>
              <span id="resumo-texto" style="font-size:12px;color:#e8f0fe;font-weight:600">—</span>
            </div>
            ''' + antigo_table

data = data[:idx_table] + novo_div + data[idx_table+7:]
with open(caminho, "w", encoding="utf-8") as f:
    f.write(data)
print("OK - div resumo adicionado!")
