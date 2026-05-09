path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Corrige o normalize do header para preservar letras ────────
old_norm = "const header = rows[headerRowIdx].map(h => String(h||'').trim().toUpperCase().replace(/[^A-Z0-9 ().]/g,'').trim());"
new_norm = """const header = rows[headerRowIdx].map(h => {
    return String(h||'').trim().toUpperCase()
      .normalize('NFD').replace(/[\\u0300-\\u036f]/g,'')  // remove acentos
      .replace(/[^A-Z0-9 ().]/g,'').trim();
  });"""

if old_norm in content:
    content = content.replace(old_norm, new_norm)
    print('Normalização corrigida para remover acentos corretamente!')
else:
    print('Padrão não encontrado, tentando alternativa...')
    # Tenta encontrar qualquer versão do normalize
    import re
    idx = content.find("rows[headerRowIdx].map(h =>")
    if idx != -1:
        end = content.find(';', idx) + 1
        old = content[idx:end]
        print(f'Encontrado: {old}')
        new_code = """rows[headerRowIdx].map(h => {
    const s = String(h||'').trim().toUpperCase();
    return s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^A-Z0-9 ().]/g,'').trim();
  })"""
        content = content[:idx] + new_code + content[end:]
        print('Corrigido via regex!')

# ── 2. Atualiza mapeamento com colunas normalizadas (sem acento) ───
old_mapa = """  // Mapeamento Sankhya → campos do app (colunas reais do TGFCAB)
  const mapa = {
    id:       ['NRO UNICO','NROUNICO','NRO. UNICO','NUNOTA','NUMNOTA','PEDIDO','NOTA'],
    cliente:  ['NOME PARCEIRO (PARCEIRO)','NOMEPARC','NOME PARCEIRO','NOMECLIENTE','CLIENTE','NOME FANTASIA (EMPRESA)'],
    endereco: ['ENDERECO','ENDCOB','LOGRADOURO','END'],
    cidade:   ['CIDADE','MUNICIPIO','NOMECIDADE'],
    bairro:   ['BAIRRO'],
    peso:     ['PESO','PESOLIQ','PESOBRUTO','PESONOTA'],
    volume:   ['VOLUME','VOL','CUBAGEM'],
    data:     ['DT. NEG.','DTNEG','DTNEGOCIACAO','DATA','DT NEG'],
    top:      ['DESCRICAO (TIPO DE OPERACAO)','TIPO OPERACAO','CODTIPOPER','TIPOPER','TOP','TIPO OPERAÇÃO','DESCRICÃO (TIPO DE OPERAÇÃO)'],
    valor:    ['VLR. NOTA','VLRNOTA','VALOR','VLR NOTA','VLRTOTAL'],
    codparc:  ['PARCEIRO','CODPARC','CODCLIENTE'],
    nronota:  ['NRO. NOTA','NRONOTA','NRO NOTA'],
    regiao:   ['ROTA','REGIAO','ZONA','CENTRO RESULTADO','DESCRICAO (CENTRO DE RESULTADO)'],
  };"""

new_mapa = """  // Mapeamento Sankhya → campos do app (sem acentos, normalizados)
  const mapa = {
    id:       ['NRO. UNICO','NRO UNICO','NROUNICO','NUNOTA','NUMNOTA','PEDIDO','NOTA'],
    cliente:  ['NOME PARCEIRO (PARCEIRO)','NOME PARCEIRO','NOMEPARC','NOMECLIENTE','CLIENTE','NOME FANTASIA (EMPRESA)'],
    endereco: ['ENDERECO','ENDCOB','LOGRADOURO','END'],
    cidade:   ['CIDADE','MUNICIPIO','NOMECIDADE'],
    bairro:   ['BAIRRO'],
    peso:     ['PESO','PESOLIQ','PESOBRUTO','PESONOTA'],
    volume:   ['VOLUME','VOL','CUBAGEM'],
    data:     ['DT. NEG.','DTNEG','DTNEGOCIACAO','DATA','DT NEG'],
    top:      ['DESCRICAO (TIPO DE OPERACAO)','TIPO OPERACAO','CODTIPOPER','TOP'],
    valor:    ['VLR. NOTA','VLRNOTA','VALOR','VLR NOTA'],
    codparc:  ['PARCEIRO','CODPARC','CODCLIENTE'],
    nronota:  ['NRO. NOTA','NRONOTA','NRO NOTA'],
    regiao:   ['CENTRO RESULTADO','DESCRICAO (CENTRO DE RESULTADO)','ROTA','REGIAO'],
  };"""

if old_mapa in content:
    content = content.replace(old_mapa, new_mapa)
    print('Mapeamento atualizado!')
else:
    print('Mapeamento não encontrado, buscando...')
    idx = content.find("id:       ['NRO UNICO'")
    if idx != -1:
        print(content[max(0,idx-50):idx+300])

# ── 3. Corrige URL de orders ───────────────────────────────────────
# Busca e corrige todas as ocorrências de orders&limit
import re
count = len(re.findall(r'orders&limit', content))
print(f'Ocorrências de orders&limit: {count}')
content = re.sub(r'orders&limit=(\d+)', r'orders?limit=\1', content)
content = re.sub(r'/orders&', '/orders?', content)
print('URLs de orders corrigidas!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Ctrl+Shift+R e teste o XLS novamente.')
