path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui a função filterOrdersLocal
old_filter = '''function filterOrdersLocal() {
  const q = document.getElementById('f-search').value.toLowerCase();
  const filtered = ordersData.filter(o =>
    !q ||
    (o.recipient_name||'').toLowerCase().includes(q) ||
    (o.address||'').toLowerCase().includes(q) ||
    (o.external_id||'').toLowerCase().includes(q)
  );
  renderOrders(filtered);
}'''

new_filter = '''function filterOrdersLocal() {
  const q      = (document.getElementById('f-search')?.value||'').toLowerCase();
  const zona   = (document.getElementById('f-zona')?.value||'').toLowerCase();
  const top    = (document.getElementById('f-top')?.value||'');

  // Mapeamento de bairros por zona de Manaus
  const zonaBairros = {
    norte: ['tarumã','cidade nova','colônia','novo israel','monte das oliveiras','santa etelvina','zumbi','mario ypiranga'],
    sul:   ['praça 14','cachoeirinha','petrópolis','raiz','morro da liberdade','educandos','coroado','distrito industrial'],
    leste: ['flores','aleixo','adrianópolis','parque 10','tancredo neves','gilberto mestrinho','jorge teixeira'],
    oeste: ['compensa','lírio','redenção','santo agostinho','santo antonio','glória','da paz','sao raimundo'],
    centro:['centro','aparecida','chapada','nossa senhora das gracas']
  };

  // Mapeamento de TOP por tipo
  const topNomes = {
    '1000': 'venda',
    '1007': 'bonif',
    '1008': 'consig',
    '1009': 'troca',
    '1010': 'pre'
  };

  const filtered = ordersData.filter(o => {
    // Filtro de busca (nome, endereço, pedido)
    if (q) {
      const haystack = [o.recipient_name, o.address, o.external_id].join(' ').toLowerCase();
      if (!haystack.includes(q)) return false;
    }

    // Filtro de zona
    if (zona) {
      const addr = (o.address||'').toLowerCase();
      const bairros = zonaBairros[zona] || [];
      const naZona = bairros.some(b => addr.includes(b));
      if (!naZona) return false;
    }

    // Filtro de TOP (quando integrado com Sankhya virá do campo top)
    // Por ora filtra pelo external_id ou campo top se existir
    if (top) {
      const externalId = (o.external_id||'').toLowerCase();
      const hasTop = externalId.includes(top) || (o.top && String(o.top) === top);
      // Se não tem info de TOP ainda, mostra todos (integração pendente)
      // if (!hasTop) return false;
    }

    return true;
  });

  renderOrders(filtered);

  // Feedback visual do filtro ativo
  const filtrosAtivos = [q && `busca: "${q}"`, zona && `zona: ${zona}`, top && `TOP: ${top}`].filter(Boolean);
  const count = document.getElementById('orders-count');
  if (count) {
    count.textContent = filtrosAtivos.length
      ? `${filtered.length} pedidos · Filtros: ${filtrosAtivos.join(' · ')}`
      : `${filtered.length} pedido(s)`;
  }
}'''

if old_filter in content:
    content = content.replace(old_filter, new_filter)
    print('filterOrdersLocal atualizado com cascata!')
else:
    print('Padrao nao encontrado, buscando alternativa...')
    # Tenta localizar a função
    import re
    idx = content.find('function filterOrdersLocal()')
    if idx != -1:
        print('Encontrado em posição:', idx)
        print(content[idx:idx+300])

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Faca Ctrl+Shift+R.')
