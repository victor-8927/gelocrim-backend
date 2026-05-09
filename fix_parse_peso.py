path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui o filtro rígido por um mais permissivo com log
old_filter = '''      const nunota = get('id');
      const pesoStr = get('peso').replace(',','.').replace(/[^\\d.]/g,'');
      const peso = parseFloat(pesoStr) || 0;

      if (!nunota || peso === 0) { erros++; continue; }'''

new_filter = '''      const nunota = get('id');
      const pesoRaw = get('peso');
      const pesoStr = pesoRaw.replace(',','.').replace(/[^\\d.]/g,'');
      const peso = parseFloat(pesoStr) || 0;

      // Log de pedidos descartados para diagnóstico
      if (!nunota) {
        console.warn(`Linha ${i} descartada: NUNOTA vazio`, cols.slice(0,5));
        erros++; continue;
      }
      if (peso === 0) {
        console.warn(`Linha ${i} PESO=0 (raw: "${pesoRaw}") NUNOTA=${nunota} - importando com peso 1`);
        // Importa mesmo com peso 0 para não perder pedidos
      }'''

if old_filter in content:
    content = content.replace(old_filter, new_filter)
    print('Filtro atualizado — pedidos com peso 0 agora são importados!')
else:
    print('Padrão não encontrado, buscando...')
    idx = content.find("if (!nunota || peso === 0)")
    if idx != -1:
        print(content[max(0,idx-300):idx+200])

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Ctrl+Shift+R — abra o F12/Console antes de importar para ver os logs!')
