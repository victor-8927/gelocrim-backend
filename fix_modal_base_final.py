import re

path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Remove modais duplicados — deixa só o primeiro ─────────────
pattern = r'<!--\s*MODAL BASE DE CLIENTES\s*-->.*?</div>\s*\n\s*</div>\s*\n\s*</div>'
matches = list(re.finditer(pattern, content, re.DOTALL))
print(f'Modais encontrados: {len(matches)}')

if len(matches) > 1:
    # Remove do último para o segundo (mantém o primeiro)
    for m in reversed(matches[1:]):
        content = content[:m.start()] + content[m.end():]
    print('Duplicatas removidas!')

# ── 2. Injeta função abrirImportacaoBaseClientes ──────────────────
func = '''
// ── BASE DE CLIENTES ─────────────────────────────────────────────
let _clientesCache = {};

async function carregarBaseClientes() {
  try {
    const lista = await api('GET', '/clientes');
    _clientesCache = {};
    lista.forEach(c => { _clientesCache[c.codparc] = c; });
    console.log('Base de clientes:', lista.length, 'registros');
    return lista.length;
  } catch(e) { return 0; }
}

function buscarClientePorCodparc(codparc) {
  return _clientesCache[parseInt(codparc)] || null;
}

function abrirImportacaoBaseClientes() {
  const modal = document.getElementById('modal-base-clientes');
  if (modal) {
    modal.style.display = 'flex';
  } else {
    toast('Modal não encontrado!', 'error');
    console.error('modal-base-clientes não existe no DOM');
  }
}

function lerBaseClientesXLS(input) {
  const file = input.files[0];
  if (!file) return;
  document.getElementById('base-clientes-nome').textContent = file.name;

  const reader = new FileReader();
  reader.onload = e => {
    try {
      const wb   = XLSX.read(e.target.result, {type:'binary'});
      const ws   = wb.Sheets[wb.SheetNames[0]];
      const rows = XLSX.utils.sheet_to_json(ws, {header:1, defval:''});

      let headerIdx = 0;
      for (let r = 0; r < Math.min(5, rows.length); r++) {
        const norm = rows[r].map(h => String(h||'').toUpperCase());
        if (norm.some(h => h.includes('PARCEIRO') || h.includes('COD'))) {
          headerIdx = r; break;
        }
      }

      const header = rows[headerIdx].map(h =>
        String(h||'').trim().toUpperCase()
          .normalize('NFD').replace(/[\\u0300-\\u036f]/g,'')
          .replace(/[^A-Z0-9 ().+]/g,'').trim()
      );
      console.log('Colunas base clientes:', header);

      const m = {
        codparc:  ['COD. PARCEIRO','CODPARCEIRO','COD PARCEIRO','CODIGO'],
        nome:     ['NOME PARCEIRO','NOME','NOMEPARCEIRO'],
        bairro:   ['NOME (BAIRRO)','BAIRRO','NOME BAIRRO'],
        cidade:   ['NOME + UF (CIDADE)','CIDADE','NOME CIDADE'],
        regiao:   ['NOME (REGIAO)','REGIAO','NOME (REGIÃO)'],
        cep:      ['CEP'],
        endereco: ['NOME (ENDERECO)','ENDERECO','NOME ENDERECO','NOME (ENDERE+O)','NOME (ENDERE O)'],
        numero:   ['NUMERO','NÚMERO'],
        telefone: ['TELEFONE','CELULAR/FAX'],
        lat:      ['LATITUDE'],
        lng:      ['LONGITUDE'],
      };

      const idx = {};
      for (const [campo, opcoes] of Object.entries(m)) {
        idx[campo] = opcoes.map(o => header.indexOf(o)).find(i => i !== -1) ?? -1;
      }
      console.log('Mapeamento:', idx);

      const clientes = [];
      let sem_gps = 0;

      for (let i = headerIdx + 1; i < rows.length; i++) {
        const cols = rows[i].map(c => String(c||'').trim());
        if (cols.join('').length === 0) continue;
        const get = (campo) => idx[campo] !== -1 ? cols[idx[campo]] || '' : '';

        const codparc = parseInt(get('codparc'));
        if (!codparc || isNaN(codparc)) continue;

        const parseCoord = (v) => parseFloat(String(v).replace(',','.').replace(/[^\\d.\\-]/g,'')) || null;
        const lat = parseCoord(get('lat'));
        const lng = parseCoord(get('lng'));
        if (!lat || !lng) sem_gps++;

        const rua    = get('endereco');
        const num    = get('numero');
        const bairro = get('bairro');
        const cidade = get('cidade').replace(/ - AM$/,'') || 'Manaus';
        const endFull = [rua, num].filter(Boolean).join(', ')
          + (bairro ? ', ' + bairro : '') + ', ' + cidade + ' - AM';

        clientes.push({codparc, nome:get('nome'), bairro, cidade:get('cidade'),
          regiao:get('regiao'), cep:get('cep'), endereco:endFull, numero:num,
          lat, lng, telefone:get('telefone'), ativo:'S'});
      }

      document.getElementById('base-clientes-count').textContent =
        clientes.length + ' clientes (' + sem_gps + ' sem GPS)';
      const btn = document.getElementById('btn-importar-base');
      btn.disabled = false; btn.style.opacity = '1'; btn.style.cursor = 'pointer';
      window._clientesParaImportar = clientes;
      toast(clientes.length + ' clientes prontos!', 'success');
    } catch(err) {
      toast('Erro: ' + err.message, 'error');
    }
  };
  reader.readAsBinaryString(file);
}

async function importarBaseClientes() {
  const clientes = window._clientesParaImportar;
  if (!clientes || !clientes.length) { toast('Nenhum dado!','error'); return; }
  const btn = document.getElementById('btn-importar-base');
  btn.disabled = true; btn.textContent = '⏳ Importando...';
  try {
    const loteSize = 500; let total = 0;
    for (let i = 0; i < clientes.length; i += loteSize) {
      const res = await api('POST', '/clientes/bulk', clientes.slice(i, i+loteSize));
      total += (res.inserted||0) + (res.updated||0);
      btn.textContent = '⏳ ' + total + '/' + clientes.length + '...';
    }
    await carregarBaseClientes();
    toast('✅ ' + total + ' clientes importados com GPS!', 'success');
    btn.textContent = '✅ Importado';
    setTimeout(()=>{ document.getElementById('modal-base-clientes').style.display='none'; }, 2000);
  } catch(e) {
    toast('Erro: ' + e.message, 'error');
    btn.textContent = '📥 Importar Base'; btn.disabled = false;
  }
}

document.addEventListener('DOMContentLoaded', () => { carregarBaseClientes(); });
'''

if 'function abrirImportacaoBaseClientes' not in content:
    content = content.replace('</script>\n</body>', func + '\n</script>\n</body>')
    print('Função injetada!')
else:
    print('Função já existe!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
