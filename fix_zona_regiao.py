path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Renomeia label Zona para Região
content = content.replace(
    '<span class="filter-label">Zona</span>',
    '<span class="filter-label">Região</span>'
)

# Renomeia as options
content = content.replace(
    '<option value="norte">Zona Norte</option>',
    '<option value="norte">Região Norte</option>'
)
content = content.replace(
    '<option value="sul">Zona Sul</option>',
    '<option value="sul">Região Sul</option>'
)
content = content.replace(
    '<option value="leste">Zona Leste</option>',
    '<option value="leste">Região Leste</option>'
)
content = content.replace(
    '<option value="oeste">Zona Oeste</option>',
    '<option value="oeste">Região Oeste</option>'
)
content = content.replace(
    '<option value="centro">Centro</option>',
    '<option value="centro">Centro</option>'
)

# Renomeia o id do campo
content = content.replace('id="f-zona"', 'id="f-regiao"')
content = content.replace("document.getElementById('f-zona')", "document.getElementById('f-regiao')")

# Atualiza o feedback do filtro
content = content.replace("zona && `zona: ${zona}`", "zona && `região: ${zona}`")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Campo renomeado para Região!')
print('Faca Ctrl+Shift+R.')
