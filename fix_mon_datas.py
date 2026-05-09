path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = "    var rotas=await api('GET','/routes?date='+date);"

new = (
    "    // Busca rotas dos últimos 3 dias se hoje não tiver\n"
    "    var rotas=await api('GET','/routes?date='+date);\n"
    "    if(!rotas.length){\n"
    "      for(var di=1;di<=3;di++){\n"
    "        var d2=new Date(Date.now()-di*86400000).toISOString().slice(0,10);\n"
    "        var r2=await api('GET','/routes?date='+d2);\n"
    "        if(r2.length){rotas=r2;break;}\n"
    "      }\n"
    "    }\n"
)

if old in content:
    content = content.replace(old, new, 1)
    print('Busca de datas corrigida!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Ctrl+Shift+R -> Monitoramento')
