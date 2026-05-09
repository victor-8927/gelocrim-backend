path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Linha 3395 (idx 3394): '    \n'  <- aqui precisa fechar o backtick e a função
# Linha 3396 (idx 3395): '</script>\n' <- esse é o fechamento do script principal

# Substitui linha 3394 para fechar o template literal e a função
lines[3394] = "    </div>`;\n  const w = window.open('','_blank');\n  if(w){w.document.write(html);w.document.close();}\n}\n"

print(f'Linha 3395 após: {repr(lines[3394][:80])}')
print(f'Total: {len(lines)}')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Pronto! Ctrl+Shift+R.')
