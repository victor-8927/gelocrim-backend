path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona console.log no loadRotMapData
old = """async function loadRotMapData(){
  var statusEl=document.getElementById('rot-map-status');
  if(statusEl) statusEl.textContent='Carregando clientes...';
  try{
    // Carrega clientes com GPS para o mapa
    var clientes=await api('GET','/clientes');"""

new = """async function loadRotMapData(){
  var statusEl=document.getElementById('rot-map-status');
  if(statusEl) statusEl.textContent='Carregando clientes...';
  console.log('loadRotMapData iniciado!');
  try{
    // Carrega clientes com GPS para o mapa
    var clientes=await api('GET','/clientes');
    console.log('Clientes carregados:', clientes.length);"""

if old in content:
    content = content.replace(old, new)
    print('Log adicionado em loadRotMapData!')
else:
    print('Padrão não encontrado!')
    # Busca loadRotMapData
    idx = content.find('async function loadRotMapData()')
    if idx != -1:
        ln = content[:idx].count('\n')+1
        print(f'loadRotMapData na linha {ln}')
        print(repr(content[idx:idx+200]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
