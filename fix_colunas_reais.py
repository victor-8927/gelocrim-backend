path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = """        var numUnico = col(r, ['NUMERO ÚNICO','NUMERO UNICO','NUM UNICO','NÚMERO ÚNICO','NUMERO_UNICO']);
        var numDoc   = col(r, ['NUMERO DOCUMENTO','NUM DOC','NUMERO DOC','DOCUMENTO']);
        var codNome  = col(r, ['CODPAR-NOME PARCEIROS','CODPARC','COD PARC','PARCEIRO','CODPAR NOME PARCEIROS']);
        var data     = col(r, ['DATA','DT NEG','DT_NEG','DATA NEG']);
        var itemStr  = col(r, ['ITEM','PRODUTO','DESCRICAO','DESC']);
        var qtd      = parseInt(col(r, ['Q NEGOCIADA','QTD','QUANTIDADE','Q NEG','QTDE'])) || 0;
        var top      = col(r, ['TOP','TOP APP','TOPAPP','TIPO']);
        var oc       = col(r, ['ORDEM DE CARGA','ORDEMCARGA','OC']);"""

new = """        var numUnico = col(r, ['Nro. Único','NUMERO ÚNICO','NUMERO UNICO','NUM UNICO','NÚMERO ÚNICO']);
        var numDoc   = col(r, ['Nro. Doc','NUMERO DOCUMENTO','NUM DOC','NUMERO DOC','DOCUMENTO']);
        var codNome  = col(r, ['Parceiro','CODPAR-NOME PARCEIROS','CODPARC','COD PARC','CODPAR NOME PARCEIROS']);
        var data     = col(r, ['Data','DATA','DT NEG','DT_NEG','DATA NEG']);
        var itemStr  = col(r, ['Item','ITEM','PRODUTO','DESCRICAO','DESC']);
        var qtd      = parseInt(col(r, ['Quantidade','Q NEGOCIADA','QTD','QUANTIDADE','Q NEG','QTDE'])) || 0;
        var top      = col(r, ['TOP','Top','TOP APP','TOPAPP','TIPO']);
        var oc       = col(r, ['Ordem de Carga','ORDEM DE CARGA','ORDEMCARGA','OC']);"""

if old in content:
    content = content.replace(old, new)
    print('Colunas corrigidas!')
else:
    print('Padrão não encontrado!')

# Corrige também o filtro de OC=0
old2 = """      var filtradas = rows.filter(function(r) {
        var oc = col(r, ['ORDEM DE CARGA','ORDEMCARGA','ORDEM CARGA','OC']);
        return !oc || parseInt(oc) === 0;
      });"""

new2 = """      var filtradas = rows.filter(function(r) {
        var oc = col(r, ['Ordem de Carga','ORDEM DE CARGA','ORDEMCARGA','ORDEM CARGA','OC']);
        return !oc || parseInt(oc) === 0;
      });"""

if old2 in content:
    content = content.replace(old2, new2)
    print('Filtro OC corrigido!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R e reimporte.')
