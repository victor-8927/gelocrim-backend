path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona console.log logo no início de lerArquivoCSV
old = "function lerArquivoCSV(input) {\n  var file=input.files[0];\n  if(!file) return;"
new = "function lerArquivoCSV(input) {\n  console.log('lerArquivoCSV chamado!', input.files[0]);\n  var file=input.files[0];\n  if(!file) return;"

if old in content:
    content = content.replace(old, new)
    print('Log adicionado em lerArquivoCSV!')

# Adiciona log no processarLinhas
old2 = "function processarLinhas(rows) {\n  var headerIdx=0;"
new2 = "function processarLinhas(rows) {\n  console.log('processarLinhas chamado! rows:', rows.length, 'primeira linha:', rows[0]);\n  var headerIdx=0;"

if old2 in content:
    content = content.replace(old2, new2)
    print('Log adicionado em processarLinhas!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R, reimporte e veja o console.')
