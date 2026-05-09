path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Verifica se ja existe
content = ''.join(lines)
if 'sel-motorista' in content:
    print('Campos ja existem!')
else:
    # Encontra a linha que fecha o rot-cap-info e o card-body
    # Linha 543 tem </div> fechando rot-cap-info
    # Precisamos inserir ANTES do fechamento do card-body (linha ~545)
    insert_after = None
    for i, line in enumerate(lines):
        if 'rot-cap-info' in line and i > 510:
            # Encontra o fechamento deste div (3 fechamentos)
            depth = 1
            j = i + 1
            while j < len(lines) and depth > 0:
                depth += lines[j].count('<div')
                depth -= lines[j].count('</div>')
                j += 1
            insert_after = j - 1
            break

    if insert_after:
        print(f'Inserindo na linha {insert_after + 1}')
        print(f'Contexto: {lines[insert_after].strip()}')

        equipe_html = '''
          <!-- EQUIPE DA ROTA -->
          <div style="margin-top:10px;padding-top:10px;border-top:1px solid var(--border)">
            <div style="font-weight:700;font-size:11px;color:var(--muted);margin-bottom:8px">EQUIPE DA ROTA</div>
            <div style="margin-bottom:6px">
              <label style="font-size:11px;color:var(--muted);display:block;margin-bottom:4px">&#x1F468;&#x200D;&#x1F4BC; Motorista</label>
              <select id="sel-motorista" style="width:100%;padding:8px;border:1px solid var(--border);border-radius:6px;font-size:12px;background:var(--bg)">
                <option value="">-- Selecione --</option>
              </select>
            </div>
            <div style="margin-bottom:6px">
              <label style="font-size:11px;color:var(--muted);display:block;margin-bottom:4px">&#x1F477; Ajudante 1</label>
              <select id="sel-ajudante1" style="width:100%;padding:8px;border:1px solid var(--border);border-radius:6px;font-size:12px;background:var(--bg)">
                <option value="">-- Nenhum --</option>
              </select>
            </div>
            <div>
              <label style="font-size:11px;color:var(--muted);display:block;margin-bottom:4px">&#x1F477; Ajudante 2</label>
              <select id="sel-ajudante2" style="width:100%;padding:8px;border:1px solid var(--border);border-radius:6px;font-size:12px;background:var(--bg)">
                <option value="">-- Nenhum --</option>
              </select>
            </div>
          </div>
'''
        lines.insert(insert_after, equipe_html)

        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print('Campos inseridos com sucesso!')
    else:
        print('Nao encontrou posicao para inserir!')
        # Debug: mostra linhas 519-550
        for i in range(518, 550):
            print(f'{i+1}: {lines[i].rstrip()}')
