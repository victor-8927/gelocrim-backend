path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige o botao atualizar na roteirizacao
content = content.replace(
    "if(page==='roteirizacao') { const today=new Date().toISOString().slice(0,10); document.getElementById('opt-date').value=today; loadPreSummary(); }",
    "if(page==='roteirizacao') { const today=new Date().toISOString().slice(0,10); document.getElementById('opt-date').value=today; loadRotMapData(); }"
)

# Tambem corrige o onclick do botao atualizar na tela
content = content.replace(
    "onclick=\"loadPreSummary()\"",
    "onclick=\"loadRotMapData()\""
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Corrigido! Faca Ctrl+Shift+R no navegador.')
