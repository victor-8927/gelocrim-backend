path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige o push do _csvDados para incluir codparc e cruzar com base de clientes
old_push = '''      _csvDados.push({
        external_id:       'SNK-' + nunota,
        recipient_name:    get('cliente') || 'CODPARC ' + get('codparc'),
        address:           endFull,
        weight_kg:         peso,
        volume_m3:         parseFloat(get('volume').replace(/\\./g,'').replace(',','.')) || 0,
        total_value:       parseFloat(get('valor').replace(/\\./g,'').replace(',','.')) || 0,
        order_type:        get('top') || '1000',
        delivery_date:     get('data') || new Date().toISOString().slice(0,10),
        regiao:            get('regiao') || null,
        status:            'pending',
        priority:          1,
        lat:               null,
        lng:               null,
        time_window_start: '07:30',
        time_window_end:   '18:00',
      });'''

new_push = '''      // Cruza com base de clientes pelo CODPARC
      const codparcNum = parseInt(get('codparc'));
      const clienteBase = codparcNum ? buscarClientePorCodparc(codparcNum) : null;

      const nomeCliente = clienteBase?.nome || get('cliente') || 'CODPARC ' + get('codparc');
      const enderecoFinal = clienteBase?.endereco || endFull;
      const latFinal = clienteBase?.lat || null;
      const lngFinal = clienteBase?.lng || null;
      const regiaoFinal = clienteBase?.regiao || get('regiao') || null;

      _csvDados.push({
        external_id:       'SNK-' + nunota,
        recipient_name:    nomeCliente,
        address:           enderecoFinal,
        codparc:           codparcNum || null,
        weight_kg:         parseBR(get('peso')),
        volume_m3:         parseBR(get('volume')),
        total_value:       parseBR(get('valor')),
        order_type:        get('top') || '1000',
        delivery_date:     get('data') || new Date().toISOString().slice(0,10),
        regiao:            regiaoFinal,
        status:            'pending',
        priority:          1,
        lat:               latFinal,
        lng:               lngFinal,
        time_window_start: '07:30',
        time_window_end:   '18:00',
      });'''

if old_push in content:
    content = content.replace(old_push, new_push)
    print('Push do importador corrigido com codparc e cruzamento!')
else:
    print('Padrão não encontrado — buscando...')
    idx = content.find("external_id:       'SNK-' + nunota,")
    if idx != -1:
        print(content[max(0,idx-100):idx+500])

# Corrige também o POST para salvar codparc
old_post_js = "await api('POST', '/orders', pedido);"
new_post_js = "await api('POST', '/orders', pedido); // inclui codparc"
# Não muda nada aqui — o campo codparc vai no objeto pedido

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Salvo!')
