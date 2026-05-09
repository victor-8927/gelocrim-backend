path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

total = len(lines)
print(f'Total: {total} linhas')
print('\n=== ÚLTIMAS 15 LINHAS ===')
for i in range(max(0,total-15), total):
    print(f'{i+1}: {repr(lines[i][:100])}')

# Conta tags de abertura/fechamento de script
content = ''.join(lines)
opens = content.count('<script')
closes = content.count('</script>')
print(f'\n<script>: {opens}  </script>: {closes}')

# Se desbalanceado, fecha o script
if opens > closes:
    print('Script não fechado! Adicionando </script>...')
    # Adiciona antes do </body>
    last_body = content.rfind('</body>')
    content = content[:last_body] + '\n</script>\n' + content[last_body:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Corrigido!')
else:
    print('Scripts balanceados!')
