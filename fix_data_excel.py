path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona conversão de data serial Excel após a função col()
old = """      console.log('Colunas:', Object.keys(rows[0]));"""

new = """      console.log('Colunas:', Object.keys(rows[0]));

      // Converte data serial do Excel para string DD/MM/YYYY
      function excelDateToStr(val) {
        if (!val) return '';
        if (typeof val === 'string' && val.includes('/')) return val;
        var num = parseInt(val);
        if (isNaN(num) || num < 1000) return String(val);
        // Serial Excel: dias desde 1/1/1900
        var d = new Date(Date.UTC(1899, 11, 30) + num * 86400000);
        return d.toISOString().slice(0,10);
      }"""

if old in content:
    content = content.replace(old, new)
    print('Conversão de data adicionada!')
else:
    print('Padrão não encontrado!')

# Aplica a conversão na leitura da data
old2 = """        var data     = col(r, ['Data','DATA','DT NEG','DT_NEG','DATA NEG']);"""
new2 = """        var data     = excelDateToStr(col(r, ['Data','DATA','DT NEG','DT_NEG','DATA NEG']));"""

if old2 in content:
    content = content.replace(old2, new2)
    print('Data convertida na leitura!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto!')
