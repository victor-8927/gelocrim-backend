path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. SUBSTITUI AS VARIÁVEIS CSS (TEMA AZUL MARINHO) ─────────────
old_root = ''':root {
  --bg: #f0f2f5;'''

new_root = ''':root {
  --bg: #0a1628;'''

content = content.replace(old_root, new_root, 1)

# Substitui as cores principais
replacements = [
    ('--border: #e2e6ea;',      '--border: #1e3a5c;'),
    ('--border2: #d0d5dd;',     '--border2: #2563a8;'),
    ('--text: #1a1d23;',        '--text: #e8f0fe;'),
    ('--text2: #4a5568;',       '--text2: #90afd4;'),
]
for old, new in replacements:
    content = content.replace(old, new)

# Substitui --white onde usado em backgrounds
content = content.replace('--white: #ffffff;', '--white: #0f2040;')
content = content.replace("background:var(--white);color:var(--text);font-family:'DM Sans'", "background:var(--bg);color:var(--text);font-family:'DM Sans'")

# Topbar azul escuro
content = content.replace(
    '.topbar{position:fixed;top:0;left:0;right:0;height:var(--topbar-h);background:var(--white);border-bottom:1px solid var(--border);',
    '.topbar{position:fixed;top:0;left:0;right:0;height:var(--topbar-h);background:#061020;border-bottom:1px solid #1e3a5c;'
)

# Sidebar azul escuro
content = content.replace(
    '.sidebar{position:fixed;top:var(--topbar-h);left:0;width:var(--sidebar-w);height:calc(100vh - var(--topbar-h));background:var(--white);border-right:1px solid var(--border);',
    '.sidebar{position:fixed;top:var(--topbar-h);left:0;width:var(--sidebar-w);height:calc(100vh - var(--topbar-h));background:#061020;border-right:1px solid #1e3a5c;'
)

# Cards
content = content.replace(
    '.card{background:var(--white);border:1px solid var(--border);border-radius:12px;',
    '.card{background:#0f2040;border:1px solid #1e3a5c;border-radius:12px;'
)

# Table headers
content = content.replace(
    'th{padding:10px 16px;text-align:left;font-size:11px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;color:var(--muted);background:#f8fafc;border-bottom:1px solid var(--border);}',
    'th{padding:10px 16px;text-align:left;font-size:11px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;color:var(--text2);background:#061828;border-bottom:1px solid #1e3a5c;}'
)

# Filters bar
content = content.replace(
    '.filters-bar{background:var(--white);border:1px solid var(--border);',
    '.filters-bar{background:#0f2040;border:1px solid #1e3a5c;'
)
content = content.replace(
    '.filter-input{padding:7px 12px;border:1.5px solid var(--border);border-radius:6px;font-family:\'DM Sans\',sans-serif;font-size:13px;color:var(--text);background:var(--white);',
    '.filter-input{padding:7px 12px;border:1.5px solid #1e3a5c;border-radius:6px;font-family:\'DM Sans\',sans-serif;font-size:13px;color:var(--text);background:#0a1628;'
)

# Modal
content = content.replace(
    '.modal-header{padding:20px 24px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;background:var(--white);',
    '.modal-header{padding:20px 24px;border-bottom:1px solid #1e3a5c;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;background:#0f2040;'
)

# Sidebar item hover
content = content.replace(
    '.sidebar-item:hover{background:var(--bg);color:var(--text);}',
    '.sidebar-item:hover{background:#1e3a5c;color:#64B4FF;}'
)

# Sidebar item active
content = content.replace(
    '.sidebar-item.active{background:var(--primary-light);color:var(--primary);font-weight:600;}',
    '.sidebar-item.active{background:#1e3a5c;color:#64B4FF;font-weight:600;}'
)

# btn-secondary
content = content.replace(
    '.btn-secondary{background:var(--white);color:var(--text2);border:1px solid var(--border2);}',
    '.btn-secondary{background:#0f2040;color:#90afd4;border:1px solid #1e3a5c;}'
)

# form controls
content = content.replace(
    '.form-control{width:100%;padding:9px 13px;border:1.5px solid var(--border2);border-radius:8px;font-family:\'DM Sans\',sans-serif;font-size:13px;color:var(--text);outline:none;transition:border-color .2s;}',
    '.form-control{width:100%;padding:9px 13px;border:1.5px solid #1e3a5c;border-radius:8px;font-family:\'DM Sans\',sans-serif;font-size:13px;color:var(--text);background:#0a1628;outline:none;transition:border-color .2s;}'
)

# Tela de login
content = content.replace(
    'background:linear-gradient(135deg,#002855 0%,#1a3a6e 100%)',
    'background:linear-gradient(135deg,#020c1b 0%,#0a1628 100%)'
)

# ── 2. REORGANIZA O DASHBOARD HTML ────────────────────────────────
old_dash = '''      <!-- ── LAYOUT PRINCIPAL: esquerda indicadores | direita mapa ── -->
      <div style="display:grid;grid-template-columns:1fr 380px;gap:16px;align-items:start">'''

if old_dash not in content:
    # Já tem o layout antigo, substitui tudo entre os kpis
    pass

print('Tema azul marinho aplicado!')
print('Faca Ctrl+Shift+R no navegador.')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
