path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove a função do lugar errado
old_wrong = """      // Converte data serial do Excel para string DD/MM/YYYY
      function excelDateToStr(val) {
        if (!val) return '';
        if (typeof val === 'string' && val.includes('/')) return val;
        var num = parseInt(val);
        if (isNaN(num) || num < 1000) return String(val);
        // Serial Excel: dias desde 1/1/1900
        var d = new Date(Date.UTC(1899, 11, 30) + num * 86400000);
        return d.toISOString().slice(0,10);
      }"""

if old_wrong in content:
    content = content.replace(old_wrong, '')
    print('Função removida do lugar errado!')

# Adiciona no lugar certo - antes do forEach
old_right = """      // Filtra ORDEM DE CARGA = 0
      var filtradas = rows.filter(function(r) {"""

new_right = """      // Converte data serial do Excel para string
      function excelDateToStr(val) {
        if (!val) return '';
        if (typeof val === 'string' && val.match(/\d{2}\/\d{2}/)) return val;
        var num = parseInt(val);
        if (isNaN(num) || num < 1000) return String(val);
        var d = new Date(Date.UTC(1899, 11, 30) + num * 86400000);
        return d.toISOString().slice(0,10);
      }

      // Filtra ORDEM DE CARGA = 0
      var filtradas = rows.filter(function(r) {"""

if old_right in content:
    content = content.replace(old_right, new_right)
    print('Função adicionada no lugar certo!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Ctrl+Shift+R e reimporte!')
