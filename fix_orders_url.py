path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('Linha 3650 atual:')
print(repr(lines[3649]))

old = "const o = await api('GET', `/orders${status?'?status='+status:''}${limit?'&limit='+limit:''}`);"
new = """const _p=[]; if(status) _p.push('status='+status); if(limit) _p.push('limit='+limit);
    const o = await api('GET', '/orders'+(_p.length?'?'+_p.join('&'):''));"""

if old in lines[3649]:
    lines[3649] = lines[3649].replace(old, new)
    print('Corrigido!')
else:
    # Tenta substituição direta
    lines[3649] = "    const _p=[]; if(status) _p.push('status='+status); if(limit) _p.push('limit='+limit);\n    const o = await api('GET', '/orders'+(_p.length?'?'+_p.join('&'):''));\n"
    print('Substituído por posição!')

print('Linha 3650 nova:')
print(repr(lines[3649]))

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Pronto! Ctrl+Shift+R.')
