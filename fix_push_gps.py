path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = """      codparc:parseInt(get('codparc'))||null,
      weight_kg:peso,volume_m3:parseBR(get('volume')),total_value:parseBR(get('valor')),
      order_type:get('top')||'1000',delivery_date:get('data')||new Date().toISOString().slice(0,10),
      regiao:(clienteBase&&clienteBase.regiao)||get('regiao')||null,
      status:'pen"""

new = """      codparc:parseInt(get('codparc'))||null,
      lat:(clienteBase&&clienteBase.lat)||null,
      lng:(clienteBase&&clienteBase.lng)||null,
      time_window_end:(clienteBase&&clienteBase.tempo_entrega)?String(parseInt(clienteBase.tempo_entrega)):'60',
      weight_kg:peso,volume_m3:parseBR(get('volume')),total_value:parseBR(get('valor')),
      order_type:get('top')||'1000',delivery_date:get('data')||new Date().toISOString().slice(0,10),
      regiao:(clienteBase&&clienteBase.regiao)||(clienteBase&&clienteBase.rota)||get('regiao')||null,
      status:'pen"""

if old in content:
    content = content.replace(old, new)
    print('GPS adicionado no push!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto!')
print('Agora reimporte a planilha TGFCAB em Pedidos -> Importar CSV')
