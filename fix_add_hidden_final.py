path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica se o hidden existe no HTML (fora de scripts)
import re
# Pega só o HTML sem scripts
html_sem_script = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
count_html = html_sem_script.count('id="v-edit-id"')
count_total = content.count('id="v-edit-id"')
print(f'v-edit-id no HTML puro: {count_html}')
print(f'v-edit-id total: {count_total}')

if count_html == 0:
    # Adiciona o hidden logo antes do botão Cancelar do modal veículo
    old = '''              <button onclick="document.getElementById('modal-veiculo-completo').style.display='none'" class="btn btn-secondary">Cancelar</button>
              <button onclick="salvarVeiculoCompleto()" class="btn btn-primary">💾 Salvar Veículo</button>'''
    new = '''              <input type="hidden" id="v-edit-id" value="">
              <button onclick="document.getElementById('modal-veiculo-completo').style.display='none'" class="btn btn-secondary">Cancelar</button>
              <button onclick="salvarVeiculoCompleto()" class="btn btn-primary">💾 Salvar Veículo</button>'''
    if old in content:
        content = content.replace(old, new)
        print('Hidden adicionado no HTML!')
    else:
        print('Botão não encontrado! Procurando...')
        idx = content.find('salvarVeiculoCompleto()')
        while idx != -1:
            ln = content[:idx].count('\n')+1
            ctx = content[max(0,idx-100):idx+50]
            # Só pega o que está no HTML (não em script)
            before = content[:idx]
            opens = before.count('<script')
            closes = before.count('</script>')
            if opens == closes:  # fora de script
                print(f'Botão salvar no HTML linha {ln}')
                # Insere hidden antes
                insert = content.rfind('\n', 0, idx)
                content = content[:insert] + '\n              <input type="hidden" id="v-edit-id" value="">' + content[insert:]
                print('Hidden inserido!')
                break
            idx = content.find('salvarVeiculoCompleto()', idx+1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verifica novamente
html_sem_script2 = re.sub(r'<script[^>]*>.*?</script>', '', ''.join(open(path).readlines()), flags=re.DOTALL)
print(f'v-edit-id no HTML após fix: {html_sem_script2.count("id=\\"v-edit-id\\"")}')
print('Pronto! Ctrl+Shift+R.')
