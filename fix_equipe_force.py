path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica o que realmente existe
print('sel-motorista no HTML:', content.count('sel-motorista'))
print('id="sel-motorista":', content.count('id="sel-motorista"'))

# Insere logo antes do fechamento do card-sel-veiculo
# O card fecha com </div>\n      </div> depois do rot-cap-info
target = '''          </div>
        </div>
      </div>

      <!-- PASSO 3'''

equipe = '''          </div>

          <!-- EQUIPE -->
          <div style="margin-top:10px;padding-top:10px;border-top:1px solid #e5e7eb">
            <div style="font-weight:700;font-size:11px;color:#6b7280;margin-bottom:8px">EQUIPE DA ROTA</div>
            <div style="margin-bottom:6px">
              <div style="font-size:11px;color:#6b7280;margin-bottom:4px">Motorista</div>
              <select id="sel-motorista" style="width:100%;padding:8px;border:1px solid #e5e7eb;border-radius:6px;font-size:12px">
                <option value="">-- Selecione --</option>
              </select>
            </div>
            <div style="margin-bottom:6px">
              <div style="font-size:11px;color:#6b7280;margin-bottom:4px">Ajudante 1</div>
              <select id="sel-ajudante1" style="width:100%;padding:8px;border:1px solid #e5e7eb;border-radius:6px;font-size:12px">
                <option value="">-- Nenhum --</option>
              </select>
            </div>
            <div>
              <div style="font-size:11px;color:#6b7280;margin-bottom:4px">Ajudante 2</div>
              <select id="sel-ajudante2" style="width:100%;padding:8px;border:1px solid #e5e7eb;border-radius:6px;font-size:12px">
                <option value="">-- Nenhum --</option>
              </select>
            </div>
          </div>

        </div>
      </div>

      <!-- PASSO 3'''

if target in content:
    content = content.replace(target, equipe, 1)
    print('Campos inseridos!')
else:
    print('Padrao nao encontrado, tentando alternativa...')
    # Tenta encontrar o fechamento do card
    idx = content.find('id="card-sel-veiculo"')
    if idx != -1:
        # Pega 2000 chars apos o card
        trecho = content[idx:idx+2000]
        print('Trecho do card:')
        print(trecho[:800])

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nVerificando resultado:')
print('sel-motorista:', content.count('id="sel-motorista"'))
