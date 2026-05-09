path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra inicio e fim da função renderClientes
start = None
end = None
for i, line in enumerate(lines):
    if 'function renderClientes(' in line:
        start = i
    if start and i > start and line.strip() == '}' and end is None:
        end = i
        break

print(f'renderClientes: linhas {start+1} a {end+1}')

# Substitui a função inteira por versão correta
nova_func = [
    'function renderClientes(lista) {\n',
    '  var tbody = document.getElementById("clientes-tbody");\n',
    '  var rodape = document.getElementById("clientes-rodape");\n',
    '  if (!tbody) return;\n',
    '  if (!lista.length) {\n',
    '    tbody.innerHTML = "<tr><td colspan=\'9\' class=\'loading-state\'>Nenhum parceiro encontrado</td></tr>";\n',
    '    return;\n',
    '  }\n',
    '  var rows = lista.map(function(c) {\n',
    '    var gps = c.lat && c.lng ? "<span style=\'color:#10b981\'>&#10003;</span>" : "<span style=\'color:#f87171\'>&#10007;</span>";\n',
    '    var ativo = c.ativo === "S" ? "active" : "inactive";\n',
    '    var aLabel = c.ativo === "S" ? "Ativo" : "Inativo";\n',
    '    var cidade = (c.cidade || "").replace(" - AM", "");\n',
    '    return "<tr>" +\n',
    '      "<td style=\'font-family:monospace;color:#64B4FF;font-weight:700\'>" + (c.codparc||"—") + "</td>" +\n',
    '      "<td><b>" + (c.nome||"—") + "</b></td>" +\n',
    '      "<td style=\'font-size:11px;color:#90afd4;max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap\' title=\'" + (c.endereco||"") + "\'>" + (c.endereco||"—") + "</td>" +\n',
    '      "<td style=\'font-size:11px\'>" + (c.bairro||"—") + "</td>" +\n',
    '      "<td style=\'font-size:11px\'>" + cidade + "</td>" +\n',
    '      "<td><span class=\'badge active\' style=\'font-size:9px\'>" + (c.regiao||"—") + "</span></td>" +\n',
    '      "<td style=\'text-align:center\'>" + gps + "</td>" +\n',
    '      "<td style=\'font-size:11px\'>" + (c.telefone||"—") + "</td>" +\n',
    '      "<td><span class=\'badge " + ativo + "\'>" + aLabel + "</span></td>" +\n',
    '      "</tr>";\n',
    '  });\n',
    '  tbody.innerHTML = rows.join("");\n',
    '  if (rodape) rodape.textContent = lista.length + " parceiros exibidos";\n',
    '}\n',
]

lines[start:end+1] = nova_func

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('renderClientes reescrita! Ctrl+Shift+R.')
