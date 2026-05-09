path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Mostra todos os tr:hover
import re
for m in re.finditer(r'tr:hover[^}]*}', content):
    print(f'Pos {m.start()}: {m.group()}')

print('---')

# Remove TODOS os tr:hover existentes
content = re.sub(r'tr:hover\s*\{[^}]*\}', '', content)
content = re.sub(r'tbody\s+tr:hover\s*\{[^}]*\}', '', content)

# Adiciona o correto antes de </style>
css_correto = '''
/* ── HOVER TABELA TEMA ESCURO ── */
table tbody tr:hover {
  background-color: #1a3a5c !important;
}
table tbody tr:hover td,
table tbody tr:hover td * {
  color: #e8f0fe !important;
}
table tbody tr:hover td b { color: #64B4FF !important; }
table tbody tr:hover td .badge { opacity: 1 !important; }
'''

content = content.replace('</style>', css_correto + '</style>', 1)
print('CSS hover corrigido!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
