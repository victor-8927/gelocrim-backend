path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona campos motorista e ajudantes logo apos o rot-cap-info
old_tag = '''          </div>
        </div>
      </div>

      <!-- PASSO 2: Selecionar veiculo -->'''

# Essa abordagem nao funciona bem, vamos usar o fechamento do card-sel-veiculo
# Procura o fim do card-body do card-sel-veiculo
old_end = '''          </div>
        </div>
      </div>'''

# Melhor abordagem: adicionar antes do fechamento do card-body
old_card_body_end = '''          </div>
        </div>
      </div>

      <!-- PASSO 3'''

new_card_body = '''          </div>

          <!-- EQUIPE DA ROTA -->
          <div style="margin-top:10px;padding-top:10px;border-top:1px solid var(--border)">
            <div style="font-weight:700;font-size:11px;color:var(--muted);margin-bottom:8px">EQUIPE DA ROTA</div>
            <div style="margin-bottom:6px">
              <label style="font-size:11px;color:var(--muted);display:block;margin-bottom:4px">👨‍💼 Motorista</label>
              <select id="sel-motorista" style="width:100%;padding:8px;border:1px solid var(--border);border-radius:6px;font-size:12px;background:var(--bg)">
                <option value="">-- Selecione --</option>
              </select>
            </div>
            <div style="margin-bottom:6px">
              <label style="font-size:11px;color:var(--muted);display:block;margin-bottom:4px">👷 Ajudante 1</label>
              <select id="sel-ajudante1" style="width:100%;padding:8px;border:1px solid var(--border);border-radius:6px;font-size:12px;background:var(--bg)">
                <option value="">-- Nenhum --</option>
              </select>
            </div>
            <div>
              <label style="font-size:11px;color:var(--muted);display:block;margin-bottom:4px">👷 Ajudante 2</label>
              <select id="sel-ajudante2" style="width:100%;padding:8px;border:1px solid var(--border);border-radius:6px;font-size:12px;background:var(--bg)">
                <option value="">-- Nenhum --</option>
              </select>
            </div>
          </div>

        </div>
      </div>

      <!-- PASSO 3'''

if 'sel-motorista' not in content:
    if old_card_body_end in content:
        content = content.replace(old_card_body_end, new_card_body)
        print('Campos equipe adicionados!')
    else:
        # Tenta outro padrao
        old2 = '        </div>\n      </div>\n\n      <!-- PASSO 3'
        if old2 in content:
            content = content.replace(old2, new_card_body.replace('<!-- PASSO 3', '<!-- PASSO 3'), 1)
            print('Campos equipe adicionados (alternativo)!')
        else:
            print('Padrao nao encontrado!')
            # Mostra o contexto para debug
            idx = content.find('rot-cap-info')
            print(content[idx:idx+500])
else:
    print('Campos ja existem!')

# Atualiza carregarFrota para ser chamada quando o card de veiculo aparecer
old_rotVeiculoChanged = 'function rotVeiculoChanged()'
if old_rotVeiculoChanged in content:
    old_fn = 'function rotVeiculoChanged() {'
    new_fn = 'function rotVeiculoChanged() {\n  carregarFrota();'
    if 'carregarFrota' not in content[content.find(old_fn):content.find(old_fn)+200]:
        content = content.replace(old_fn, new_fn, 1)
        print('carregarFrota chamada em rotVeiculoChanged!')

# Adiciona driver_id e ajudantes no payload de roteirizacao
old_payload = '"vehicle_id": veiculoId,'
new_payload = '''"vehicle_id": veiculoId,
        "driver_id": document.getElementById("sel-motorista")?.value || null,
        "ajudante1_id": document.getElementById("sel-ajudante1")?.value || null,
        "ajudante2_id": document.getElementById("sel-ajudante2")?.value || null,'''

if old_payload in content and 'driver_id' not in content[content.find(old_payload)-5:content.find(old_payload)+300]:
    content = content.replace(old_payload, new_payload, 1)
    print('Payload atualizado com equipe!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R no navegador.')
