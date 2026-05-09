path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''function abrirImportacaoCSV() {
  _csvDados = [];
  document.getElementById('csv-nome-arquivo').textContent = 'Nenhum arquivo selecionado';
  document.getElementById('csv-preview').style.display = 'none';
  document.getElementById('csv-opcoes').style.display = 'none';
  document.getElementById('csv-resultado').style.display = 'none';
  const btn = document.getElementById('btn-importar-csv');
  if (btn) { btn.disabled=true; btn.style.opacity='.5'; btn.textContent='📥 Importar Pedidos'; }
  document.getElementById('csv-file-input').value = '';
  document.getElementById('modal-importacao-csv').style.display = 'flex';
}'''

new_func = '''function abrirImportacaoCSV() {
  _csvDados = [];
  const safe = (id, fn) => { const e=document.getElementById(id); if(e) fn(e); };
  safe('csv-nome-arquivo', e => e.textContent='Nenhum arquivo selecionado');
  safe('csv-preview',      e => e.style.display='none');
  safe('csv-opcoes',       e => e.style.display='none');
  safe('csv-resultado',    e => e.style.display='none');
  safe('btn-importar-csv', e => { e.disabled=true; e.style.opacity='.5'; e.textContent='📥 Importar Pedidos'; });
  safe('csv-file-input',   e => e.value='');
  const modal = document.getElementById('modal-importacao-csv');
  if (modal) modal.style.display='flex';
  else { toast('Modal não encontrado!','error'); console.log('modal-importacao-csv não existe'); }
}'''

if old_func in content:
    content = content.replace(old_func, new_func)
    print('Função corrigida!')
else:
    print('Padrão não encontrado, corrigindo por posição...')
    idx = content.find('function abrirImportacaoCSV()')
    if idx != -1:
        depth=0; started=False; i=idx
        for i in range(idx, len(content)):
            if content[i]=='{': depth+=1; started=True
            elif content[i]=='}': depth-=1
            if started and depth==0: break
        content = content[:idx] + new_func + content[i+1:]
        print('Corrigido por posição!')

# Também corrige o 404 de orders - URL incorreta
old_url = "api('GET', '/orders&limit=100')"
new_url = "api('GET', '/orders?limit=100')"
if old_url in content:
    content = content.replace(old_url, new_url)
    print('URL de orders corrigida!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
