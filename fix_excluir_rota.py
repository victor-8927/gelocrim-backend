path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adiciona endpoint DELETE no router (via script separado)
# 2. Adiciona botão Excluir na tabela de rotas
old_btn = """          btnLiberar+
          '<button class="btn btn-sm btn-secondary" data-id="'+r.route_id+'" onclick="verProgressoRota(this.dataset.id)">👁 Ver</button>'+"""

new_btn = """          btnLiberar+
          '<button class="btn btn-sm btn-secondary" data-id="'+r.route_id+'" onclick="verProgressoRota(this.dataset.id)">👁 Ver</button>'+
          (r.status!=='executing'&&r.status!=='done'?'<button class="btn btn-sm btn-danger" onclick="excluirRota(\''+r.route_id+'\')" title="Excluir viagem">🗑️</button>':'')+"""

if old_btn in content:
    content = content.replace(old_btn, new_btn)
    print('Botão excluir adicionado!')
else:
    print('Padrão não encontrado!')

# 3. Adiciona função excluirRota
old_liberar = """async function liberarRota(routeId) {
  if(!confirm('Liberar esta rota para o motorista?')) return;
  try{
    await api('POST', '/routes/'+routeId+'/liberar');
    toast('✅ Rota liberada! Motorista já pode ver no app.','success');
    loadRoutes();
  }catch(e){toast('Erro: '+e.message,'error');}
}"""

new_liberar = """async function liberarRota(routeId) {
  if(!confirm('Liberar esta rota para o motorista?')) return;
  try{
    await api('POST', '/routes/'+routeId+'/liberar');
    toast('✅ Rota liberada! Motorista já pode ver no app.','success');
    loadRoutes();
  }catch(e){toast('Erro: '+e.message,'error');}
}

async function excluirRota(routeId) {
  if(!confirm('Excluir esta viagem? Os pedidos voltarão para a fila de roteirização.')) return;
  try{
    await api('DELETE', '/routes/'+routeId);
    toast('🗑️ Viagem excluída! Pedidos devolvidos à roteirização.','success');
    loadRoutes();
  }catch(e){toast('Erro: '+e.message,'error');}
}"""

if old_liberar in content:
    content = content.replace(old_liberar, new_liberar)
    print('Função excluirRota adicionada!')
else:
    print('liberarRota não encontrada!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('HTML atualizado!')
