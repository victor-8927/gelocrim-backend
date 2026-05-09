path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = r"""  var reader = new FileReader();
  reader.onload = function(e) {
    try {
      var wb = XLSX.read(e.target.result, { type: 'array' });
      var ws = wb.Sheets[wb.SheetNames[0]];
      var rows = XLSX.utils.sheet_to_json(ws, { defval: '' });

      // Filtra ORDEM DE CARGA = 0
      var filtradas = rows.filter(function(r) {
        var oc = r['ORDEM DE CARGA'] || r['ORDEMCARGA'] || 0;
        return parseInt(oc) === 0;
      });

      // Agrupa por NUMERO ÚNICO
      var pedidos = {};
      filtradas.forEach(function(r) {
        var numUnico = String(r['NUMERO ÚNICO'] || r['NUMERO UNICO'] || '').trim();
        var numDoc   = String(r['NUMERO DOCUMENTO'] || '').trim();
        var codNome  = String(r['CODPAR-NOME PARCEIROS'] || '').trim();
        var data     = String(r['DATA'] || '').trim();
        var itemStr  = String(r['ITEM'] || '').trim();
        var qtd      = parseInt(r['Q NEGOCIADA'] || 0);

        if (!numUnico || !codNome) return;

        // Extrai codparc e nome
        var partes = codNome.split(' - ');
        var codparc = parseInt(partes[0]) || 0;
        var nome = partes.slice(1).join(' - ').trim();

        // Extrai código do item
        var codItem = itemStr.split(' - ')[0].trim();
        var pesoUnit = PESOS_ITEM[codItem] || 0;
        var nomeItem = NOMES_ITEM[codItem] || itemStr;

        if (!pedidos[numUnico]) {
          pedidos[numUnico] = {
            external_id: numUnico,
            num_doc: numDoc,
            codparc: codparc,
            recipient_name: nome,
            data: data,
            itens: [],
            weight_kg: 0
          };
        }
        pedidos[numUnico].itens.push({ cod: codItem, nome: nomeItem, qtd: qtd, peso_unit: pesoUnit });
        pedidos[numUnico].weight_kg += qtd * pesoUnit;
      });"""

new = r"""  var reader = new FileReader();
  reader.onload = function(e) {
    try {
      var wb = XLSX.read(e.target.result, { type: 'array' });
      var ws = wb.Sheets[wb.SheetNames[0]];
      var rows = XLSX.utils.sheet_to_json(ws, { defval: '' });

      // Mostra colunas disponíveis no console para debug
      if (rows.length > 0) console.log('Colunas:', Object.keys(rows[0]));

      // Função para buscar coluna com variações de nome
      function col(row, nomes) {
        for (var i=0; i<nomes.length; i++) {
          var keys = Object.keys(row);
          for (var j=0; j<keys.length; j++) {
            if (keys[j].trim().toUpperCase() === nomes[i].toUpperCase()) {
              return String(row[keys[j]] || '').trim();
            }
          }
        }
        return '';
      }

      // Filtra ORDEM DE CARGA = 0
      var filtradas = rows.filter(function(r) {
        var oc = col(r, ['ORDEM DE CARGA','ORDEMCARGA','ORDEM CARGA','OC']);
        return !oc || parseInt(oc) === 0;
      });

      console.log('Linhas filtradas (OC=0):', filtradas.length, 'de', rows.length);

      // Agrupa por NUMERO ÚNICO
      var pedidos = {};
      filtradas.forEach(function(r) {
        var numUnico = col(r, ['NUMERO ÚNICO','NUMERO UNICO','NUM UNICO','NÚMERO ÚNICO','NUMERO_UNICO']);
        var numDoc   = col(r, ['NUMERO DOCUMENTO','NUM DOC','NUMERO DOC','DOCUMENTO']);
        var codNome  = col(r, ['CODPAR-NOME PARCEIROS','CODPARC','COD PARC','PARCEIRO','CODPAR NOME PARCEIROS']);
        var data     = col(r, ['DATA','DT NEG','DT_NEG','DATA NEG']);
        var itemStr  = col(r, ['ITEM','PRODUTO','DESCRICAO','DESC']);
        var qtd      = parseInt(col(r, ['Q NEGOCIADA','QTD','QUANTIDADE','Q NEG','QTDE'])) || 0;
        var top      = col(r, ['TOP','TOP APP','TOPAPP','TIPO']);
        var oc       = col(r, ['ORDEM DE CARGA','ORDEMCARGA','OC']);

        if (!numUnico || !codNome) return;

        // Extrai codparc e nome
        var partes = codNome.split(' - ');
        var codparc = parseInt(partes[0]) || 0;
        var nome = partes.slice(1).join(' - ').trim();
        if (!nome) nome = codNome;

        // Extrai código do item
        var codItem = itemStr.split(' - ')[0].trim();
        var pesoUnit = PESOS_ITEM[codItem] || 0;
        var nomeItem = NOMES_ITEM[codItem] || itemStr;

        if (!pedidos[numUnico]) {
          pedidos[numUnico] = {
            external_id: numUnico,
            num_doc: numDoc,
            codparc: codparc,
            recipient_name: nome,
            data: data,
            top_app: top || '1000',
            itens: [],
            weight_kg: 0
          };
        }
        pedidos[numUnico].itens.push({ cod: codItem, nome: nomeItem, qtd: qtd, peso_unit: pesoUnit });
        pedidos[numUnico].weight_kg += qtd * pesoUnit;
      });"""

if old in content:
    content = content.replace(old, new)
    print('Importador corrigido!')
else:
    print('Padrão não encontrado!')

# Atualiza também o preview para mostrar TOP
old2 = """        '<b style="color:#e8f0fe">' + p.recipient_name + '</b> (cod:'+p.codparc+') — ' +
          p.itens.map(function(i){return i.qtd+'x '+i.nome;}).join(', ') +
          ' = <b style="color:#64B4FF">' + p.weight_kg.toFixed(0) + 'kg</b></div>';"""

new2 = """        '<b style="color:#e8f0fe">' + p.recipient_name + '</b> (cod:'+p.codparc+') — ' +
          p.itens.map(function(i){return i.qtd+'x '+i.nome;}).join(', ') +
          ' = <b style="color:#64B4FF">' + p.weight_kg.toFixed(0) + 'kg</b>' +
          (p.top_app ? ' <span style="color:#f59e0b">TOP:'+p.top_app+'</span>' : '') +
          '</div>';"""

if old2 in content:
    content = content.replace(old2, new2)
    print('Preview com TOP atualizado!')

# Atualiza colunas esperadas no modal
old3 = 'Colunas esperadas:</b> NUMERO ÚNICO · NUMERO DOCUMENTO · CODPAR-NOME PARCEIROS · DATA · ITEM · Q NEGOCIADA · ORDEM DE CARGA'
new3 = 'Colunas esperadas:</b> NUMERO ÚNICO · NUMERO DOCUMENTO · CODPAR-NOME PARCEIROS · DATA · ITEM · Q NEGOCIADA · ORDEM DE CARGA · TOP (opcional)'

if old3 in content:
    content = content.replace(old3, new3)
    print('Descrição atualizada!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R e reimporte a planilha.')
