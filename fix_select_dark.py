path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

css_select = '''
/* ── FIX SELECT DROPDOWN TEMA ESCURO ── */
select {
  background-color: #0a1628 !important;
  color: #e8f0fe !important;
  border-color: #1e3a5c !important;
  color-scheme: dark !important;
}
select:focus {
  background-color: #0a1628 !important;
  color: #e8f0fe !important;
  border-color: #64B4FF !important;
  outline: none !important;
}
select option {
  background-color: #0f2040 !important;
  color: #e8f0fe !important;
}
select option:hover,
select option:focus,
select option:checked {
  background-color: #1e3a5c !important;
  color: #64B4FF !important;
}
/* Fix filter-input selects */
.filter-input {
  background-color: #0a1628 !important;
  color: #e8f0fe !important;
}
/* Fix form-control selects */
.form-control {
  background-color: #0a1628 !important;
  color: #e8f0fe !important;
  border-color: #1e3a5c !important;
}
.form-control:focus {
  background-color: #0a1628 !important;
  color: #e8f0fe !important;
  border-color: #64B4FF !important;
}
'''

if 'FIX SELECT DROPDOWN TEMA ESCURO' not in content:
    content = content.replace('</style>', css_select + '\n</style>', 1)
    print('CSS select corrigido!')
else:
    print('CSS já existe, atualizando...')
    content = content.replace(
        '/* ── FIX SELECT DROPDOWN TEMA ESCURO ── */',
        '/* ── FIX SELECT DROPDOWN TEMA ESCURO UPDATED ── */'
    )
    content = content.replace('</style>', css_select + '\n</style>', 1)
    print('CSS atualizado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
