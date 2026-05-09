import re

path = r'C:\fleet-cloud\gelocrim_v1.html'
c = open(path, encoding='utf-8', errors='ignore').read()

# 1. Substituir a célula de foto única pelas 4 colunas
OLD = """        '<td style="padding:8px;text-align:center">'+
          (s.foto_url
            ? '<img src="'+s.foto_url+'" style="width:48px;height:48px;object-fit:cover;border-radius:6px;border:1px solid #1e3a5c;cursor:pointer" onclick="window.open(this.src)" title="Ver foto">'
            : (s.status==="completed"?'<span style="font-size:10px;color:#90afd4">sem foto</span>':''))+
        '</td>'+"""

NEW = """        '<td style="padding:6px;text-align:center">'+fotoCell(s.foto_nf,'NF')+'</td>'+
        '<td style="padding:6px;text-align:center">'+fotoCell(s.foto_boleto,'Boleto')+'</td>'+
        '<td style="padding:6px;text-align:center">'+fotoCell(s.foto_comodato,'Comodato')+'</td>'+
        '<td style="padding:6px;text-align:center">'+fotoCell(s.foto_outros,'Outros')+'</td>'+"""

c = c.replace(OLD, NEW)

# 2. Adicionar função fotoCell antes de verProgressoRota
FUNC = """function fotoCell(url, label) {
  if (url) {
    return '<div style="display:flex;flex-direction:column;align-items:center;gap:2px">' +
      '<img src="' + url + '" style="width:44px;height:44px;object-fit:cover;border-radius:6px;border:2px solid #10b981;cursor:pointer" ' +
      'onclick="abrirLightbox(\\'' + url + '\\')" title="Ver ' + label + '">' +
      '<span style="font-size:9px;color:#10b981;font-weight:700">' + label + '</span>' +
      '</div>';
  }
  return '<div style="display:flex;flex-direction:column;align-items:center;gap:2px">' +
    '<div style="width:44px;height:44px;border:1px dashed #1e3a5c;border-radius:6px;display:flex;align-items:center;justify-content:center">' +
    '<span style="font-size:14px">📷</span></div>' +
    '<span style="font-size:9px;color:#1e3a5c">' + label + '</span>' +
    '</div>';
}

function abrirLightbox(url) {
  var lb = document.getElementById('lightbox-fotos');
  if (!lb) {
    lb = document.createElement('div');
    lb.id = 'lightbox-fotos';
    lb.style = 'display:none;position:fixed;inset:0;background:rgba(0,0,0,.92);z-index:9999;align-items:center;justify-content:center;flex-direction:column;gap:16px';
    lb.innerHTML = '<img id="lb-img" style="max-width:90vw;max-height:75vh;border-radius:10px;border:2px solid #10b981">' +
      '<div style="display:flex;gap:12px">' +
      '<button onclick="baixarFoto()" style="padding:8px 18px;background:#10b981;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:700">⬇ Baixar</button>' +
      '<button onclick="compartilharWhats()" style="padding:8px 18px;background:#25D366;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:700">📲 WhatsApp</button>' +
      '<button onclick="document.getElementById(\'lightbox-fotos\').style.display=\'none\'" style="padding:8px 18px;background:#1e3a5c;color:#fff;border:none;border-radius:8px;cursor:pointer">✕ Fechar</button>' +
      '</div>';
    lb.onclick = function(e){ if(e.target===lb) lb.style.display='none'; };
    document.body.appendChild(lb);
  }
  document.getElementById('lb-img').src = url;
  lb.style.display = 'flex';
  lb._url = url;
}

function baixarFoto() {
  var url = document.getElementById('lightbox-fotos')._url;
  var a = document.createElement('a');
  a.href = url; a.download = 'foto_gelocrim.jpg'; a.click();
}

function compartilharWhats() {
  var url = document.getElementById('lightbox-fotos')._url;
  window.open('https://wa.me/?text=' + encodeURIComponent(url), '_blank');
}

async function verProgressoRota"""

c = c.replace('async function verProgressoRota', FUNC)

# 3. Atualizar cabeçalho da tabela — substituir coluna Foto por 4 colunas
c = c.replace(
  "'<th style=\"padding:8px;text-align:center\">Foto</th>'+",
  "'<th style=\"padding:8px;text-align:center\">NF</th>'+'<th style=\"padding:8px;text-align:center\">Boleto</th>'+'<th style=\"padding:8px;text-align:center\">Comodato</th>'+'<th style=\"padding:8px;text-align:center\">Outros</th>'+"
)

open(path, 'w', encoding='utf-8').write(c)
print("OK - fotos corrigidas!")
