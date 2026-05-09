path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_goto = "if(page==='roteirizacao') { const today=new Date().toISOString().slice(0,10); document.getElementById('opt-date').value=today; loadRotMapData(); }"

new_goto = "if(page==='roteirizacao') { const today=new Date().toISOString().slice(0,10); document.getElementById('opt-date').value=today; loadRotMapData(); carregarFrota(); carregarVeiculosSelect(); }"

if old_goto in content:
    content = content.replace(old_goto, new_goto)
    print('carregarFrota adicionada ao abrir roteirização!')
else:
    print('Padrão não encontrado, tentando variação...')
    idx = content.find("page==='roteirizacao'")
    print(content[idx:idx+200])

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
