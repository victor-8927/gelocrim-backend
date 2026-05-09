path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Renomeia Motoristas → Equipe de Entrega ────────────────────
trocas = [
    ('Motoristas e Equipe',        'Equipe de Entrega'),
    ('Motoristas e Ajudantes',     'Equipe de Entrega'),
    ('Gestão de equipes de entrega','Motoristas e ajudantes da operação'),
    ('>&#x1F464; Motoristas<',     '>&#x1F465; Equipe de Entrega<'),
    ('data-page="motoristas">\n        <span class="icon">👤</span> Motoristas',
     'data-page="motoristas">\n        <span class="icon">👥</span> Equipe de Entrega'),
]
for old, new in trocas:
    if old in content:
        content = content.replace(old, new)
        print(f'Renomeado: {old[:40]}')

# Sidebar
content = content.replace(
    '<span class="icon">👤</span> Motoristas',
    '<span class="icon">👥</span> Equipe de Entrega'
)
content = content.replace(
    'Motoristas e Ajudantes',
    'Equipe de Entrega'
)
print('Sidebar renomeado!')

# ── 2. Verifica se as funções de salvar estão presentes ───────────
funcs = [
    'function salvarVeiculoCompleto',
    'function salvarMotoristaCompleto',
    'function salvarPallet',
    'function salvarItem',
    'function salvarOcorrencia',
]
for f in funcs:
    if f in content:
        print(f'✅ {f} — PRESENTE')
    else:
        print(f'❌ {f} — AUSENTE')

# ── 3. Verifica os botões de salvar nos modais ────────────────────
btns = [
    ('salvarVeiculoCompleto()',   'Modal Veículo'),
    ('salvarMotoristaCompleto()', 'Modal Motorista'),
    ('salvarPallet()',            'Modal Pallet'),
    ('salvarItem()',              'Modal Item'),
    ('salvarOcorrencia()',        'Modal Ocorrência'),
]
for fn, label in btns:
    if fn in content:
        print(f'✅ Botão {label} — OK')
    else:
        print(f'❌ Botão {label} — AUSENTE')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Ctrl+Shift+R.')
