path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix linha do verDetalhePedido - aspas quebradas
old = "      '<td><button class=\"btn btn-sm btn-secondary\" onclick=\"verDetalhePedido(''+o.id+'')\">"
new = "      '<td><button class=\"btn btn-sm btn-secondary\" onclick=\"verDetalhePedido(\\''+o.id+'\\')\">"
if old in content:
    content = content.replace(old, new)
    print('Fix verDetalhePedido aplicado!')

# Fix linha do toggleOrderChk - aspas duplas escapadas que viram erro
old2 = 'onchange="toggleOrderChk(\\"\\'+o.id+\'\\",this.checked)"'
new2 = "onchange=\\'toggleOrderChk(\\\\\"'+o.id+'\\\\\",this.checked)\\'"
# Abordagem mais simples: substitui a função renderOrders inteira
old_render = """      '<td><input type="checkbox" class="order-chk" data-id="'+o.id+'" onchange="toggleOrderChk(\\"'+o.id+'\\"\"'+"""
# Vamos só substituir a linha problemática pelo índice
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'toggleOrderChk' in line and 'order-chk' in line:
        print(f'Linha {i+1}: {repr(line[:100])}')
        lines[i] = "      '<td><input type=\"checkbox\" class=\"order-chk\" data-id=\"'+o.id+'\" onchange=\"toggleOrderChk(this.dataset.id,this.checked)\" data-id=\"'+o.id+'\"></td>' +"
        print(f'Corrigido: {repr(lines[i][:100])}')
        break
    if 'verDetalhePedido' in line and "btn-sm" in line:
        print(f'Linha {i+1}: {repr(line[:100])}')
        lines[i] = "      '<td><button class=\"btn btn-sm btn-secondary\" onclick=\"verDetalhePedido(this.dataset.id)\" data-id=\"'+o.id+'\">👁</button></td>' +"
        print(f'Corrigido: {repr(lines[i][:100])}')

content = '\n'.join(lines)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
