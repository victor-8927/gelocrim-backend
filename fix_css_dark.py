path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

css_fix = '''
/* ── FIX: inputs mantém tema escuro no focus/hover/autofill ── */
input, select, textarea {
  color-scheme: dark;
}
input:focus, select:focus, textarea:focus {
  background-color: #0a1628 !important;
  color: #e8f0fe !important;
  border-color: #64B4FF !important;
  outline: none !important;
  box-shadow: 0 0 0 2px rgba(100,180,255,.2) !important;
}
input:hover, select:hover, textarea:hover {
  border-color: #2d5a8e !important;
  background-color: #0a1628 !important;
}
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
  -webkit-box-shadow: 0 0 0 40px #0a1628 inset !important;
  -webkit-text-fill-color: #e8f0fe !important;
  caret-color: #e8f0fe !important;
}
select option {
  background: #0f2040;
  color: #e8f0fe;
}
.form-control:focus {
  background: #0a1628 !important;
  color: #e8f0fe !important;
  border-color: #64B4FF !important;
  outline: none !important;
}
/* Tabela rows hover */
tbody tr:hover {
  background: rgba(100,180,255,.05) !important;
}
/* Readonly inputs */
input[readonly]:focus {
  border-color: #1e3a5c !important;
  box-shadow: none !important;
  cursor: default;
}
'''

# Injeta antes de </style>
if 'color-scheme: dark' not in content:
    content = content.replace('</style>', css_fix + '\n</style>', 1)
    print('CSS de tema escuro adicionado!')
else:
    print('CSS já existe!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
