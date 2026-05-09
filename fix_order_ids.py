path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adiciona order_ids real no objeto clienteMap
old1 = """          order_type: o.order_type||'',
          status: 'pending'
        };
      }
      clienteMap[key].weight_kg += parseFloat(o.weight_kg)||0;
      clienteMap[key].pedidos.push(o.external_id||o.id);"""

new1 = """          order_type: o.order_type||'',
          status: 'pending',
          order_ids: []
        };
      }
      clienteMap[key].weight_kg += parseFloat(o.weight_kg)||0;
      clienteMap[key].pedidos.push(o.external_id||o.id);
      clienteMap[key].order_ids.push(o.id);"""

if old1 in content:
    content = content.replace(old1, new1)
    print('order_ids adicionado ao clienteMap!')
else:
    print('Padrão 1 não encontrado!')

# 2. Corrige gravarCarga para usar order_ids reais de todos os clientes selecionados
old2 = """    var orderIds=confOrdem.map(function(o){return o.id;}).filter(function(x){return !!x;});
    console.log('Gravando carga:', orderIds.length, 'pedidos', orderIds);"""

new2 = """    var orderIds=[];
    confOrdem.forEach(function(o){
      if(o.order_ids && o.order_ids.length) {
        o.order_ids.forEach(function(id){ if(id) orderIds.push(id); });
      } else if(o.id && !o.id.startsWith('cli-')) {
        orderIds.push(o.id);
      }
    });
    console.log('Gravando carga:', confOrdem.length, 'clientes,', orderIds.length, 'pedidos', orderIds);"""

if old2 in content:
    content = content.replace(old2, new2)
    print('gravarCarga corrigido para usar order_ids reais!')
else:
    print('Padrão 2 não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R')
