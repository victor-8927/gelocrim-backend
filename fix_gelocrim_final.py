import re

path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra a função gerarRomaneio e corrige o fechamento
# O problema: o html termina com </div>` mas falta `;\n  const w...`
old = '''    </div>
    </div>`;
</script>'''

new = '''    </div>
    </div>\`;
  const w = window.open('','_blank');
  if(w){w.document.write(html);w.document.close();}
}
</script>'''

if old in content:
    content = content.replace(old, new)
    print('Corrigido gerarRomaneio!')
else:
    # Tenta variação
    old2 = '    </div>`;\n</script>'
    if old2 in content:
        content = content.replace(old2, '    </div>`;\n  const w = window.open(\'\',\'_blank\');\n  if(w){w.document.write(html);w.document.close();}\n}\n</script>')
        print('Corrigido variação 2!')
    else:
        # Mostra contexto do </script> para diagnóstico
        idx = content.find('</script>')
        while idx != -1:
            line = content[:idx].count('\n') + 1
            ctx = content[max(0,idx-100):idx+15]
            print(f'</script> linha {line}: {repr(ctx[-80:])}')
            idx = content.find('</script>', idx+1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

import re
opens  = len(re.findall(r'<script[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f'Scripts: {opens} opens / {closes} closes')
print('Pronto!')
