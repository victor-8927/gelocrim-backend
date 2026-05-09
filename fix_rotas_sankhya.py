path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Atualiza o select de região com as rotas do Sankhya
old_select = '''          <select class="filter-input" id="f-regiao" onchange="filterOrdersLocal()">
            <option value="">Todas</option>
            <option value="norte">Região Norte</option>
            <option value="sul">Região Sul</option>
            <option value="leste">Região Leste</option>
            <option value="oeste">Região Oeste</option>
            <option value="centro">Centro</option>
          </select>'''

new_select = '''          <select class="filter-input" id="f-regiao" onchange="filterOrdersLocal()">
            <option value="">Todas</option>
            <option value="801">ROTA 801</option>
            <option value="802">ROTA 802</option>
            <option value="803">ROTA 803</option>
            <option value="804">ROTA 804</option>
            <option value="805">ROTA 805</option>
            <option value="811">ROTA 811</option>
            <option value="822">ROTA 822</option>
          </select>'''

if old_select in content:
    content = content.replace(old_select, new_select)
    print('Select de região atualizado com rotas Sankhya!')
else:
    print('Padrao nao encontrado, tentando alternativa...')
    # Tenta localizar o select
    idx = content.find('id="f-regiao"')
    if idx != -1:
        print(content[idx-50:idx+300])

# Atualiza o filtro para usar o campo rota do Sankhya
old_zona_filter = '''    // Filtro de zona
    if (zona) {
      const addr = (o.address||'').toLowerCase();
      const bairros = zonaBairros[zona] || [];
      const naZona = bairros.some(b => addr.includes(b));
      if (!naZona) return false;
    }'''

new_zona_filter = '''    // Filtro de região (ROTA Sankhya)
    if (zona) {
      // Quando integrado com Sankhya, virá do campo o.regiao ou o.rota
      const regiao = (o.regiao || o.rota || o.region || '').toString();
      const endereco = (o.address||'').toLowerCase();
      // Verifica se o campo região contém o número da rota
      const naRegiao = regiao.includes(zona) || endereco.includes(zona);
      if (!naRegiao) return false;
    }'''

if old_zona_filter in content:
    content = content.replace(old_zona_filter, new_zona_filter)
    print('Filtro de região atualizado para rotas Sankhya!')

# Remove o mapeamento de bairros que não será mais usado
old_mapa_bairros = '''  // Mapeamento de bairros por zona de Manaus
  const zonaBairros = {
    norte: ['tarumã','cidade nova','colônia','novo israel','monte das oliveiras','santa etelvina','zumbi','mario ypiranga'],
    sul:   ['praça 14','cachoeirinha','petrópolis','raiz','morro da liberdade','educandos','coroado','distrito industrial'],
    leste: ['flores','aleixo','adrianópolis','parque 10','tancredo neves','gilberto mestrinho','jorge teixeira'],
    oeste: ['compensa','lírio','redenção','santo agostinho','santo antonio','glória','da paz','sao raimundo'],
    centro:['centro','aparecida','chapada','nossa senhora das gracas']
  };'''

content = content.replace(old_mapa_bairros, '''  // Regiões = Rotas Sankhya (801/802/803/804/805/811/822)
  // Quando integrado, virá do campo o.regiao do cadastro de clientes''')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R.')
