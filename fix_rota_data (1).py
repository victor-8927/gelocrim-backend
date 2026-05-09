path = r'C:\gelocrim-motorista\screens\RotaScreen.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove filtro de data - motorista ve todas as rotas liberadas para ele
old_hoje = "  const hoje = new Date().toISOString().slice(0, 10);"
new_hoje = "  // Busca rotas dos ultimos 2 dias para cobrir mudancas de data\n  const hoje = new Date().toISOString().slice(0, 10);\n  const ontem = new Date(Date.now() - 86400000).toISOString().slice(0, 10);"

content = content.replace(old_hoje, new_hoje)

# Busca rotas de hoje e ontem
old_fetch = "      const res = await fetch(`${API_URL}/routes?date=${hoje}`, { headers });"
new_fetch = """      // Busca rotas de hoje e ontem
      const [res1, res2] = await Promise.all([
        fetch(`${API_URL}/routes?date=${hoje}`, { headers }),
        fetch(`${API_URL}/routes?date=${ontem}`, { headers }),
      ]);
      const [rotas1, rotas2] = await Promise.all([res1.json(), res2.json()]);
      const rotasTodas = [...(Array.isArray(rotas1) ? rotas1 : []), ...(Array.isArray(rotas2) ? rotas2 : [])];
      const res = { ok: true };
      // Usa rotasTodas no lugar de rotas"""

old_rotas = "      const rotas = await res.json();"
new_rotas = "      const rotas = rotasTodas;"

content = content.replace(old_fetch, new_fetch)
content = content.replace(old_rotas, new_rotas)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('RotaScreen corrigido - busca rotas de hoje e ontem!')
print('Pressione r no Expo!')
