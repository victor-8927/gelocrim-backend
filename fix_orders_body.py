path = r'C:\fleet-cloud\app\routers\orders.py'

with open(path, 'r') as f:
    content = f.read()

# Garante que imports necessários existem
if 'from fastapi import' in content:
    import re
    old_import = re.search(r'from fastapi import[^\n]+', content).group()
    if 'Body' not in old_import:
        new_import = old_import.rstrip() + ', Body'
        content = content.replace(old_import, new_import)
        print('Body adicionado ao import!')

if 'from typing import' not in content:
    content = 'from typing import Any, Dict\n' + content
    print('typing importado!')

# Substitui o POST para usar Body corretamente
old_post = '''@router.post("", status_code=201)
def create_order(order: dict, db: sqlite3.Connection = Depends(get_db)):'''

new_post = '''@router.post("", status_code=201)
def create_order(order: Dict[str, Any] = Body(...), db: sqlite3.Connection = Depends(get_db)):'''

if old_post in content:
    content = content.replace(old_post, new_post)
    print('POST corrigido com Body!')
else:
    # Tenta padrão alternativo
    import re
    content = re.sub(
        r'@router\.post\("", status_code=201\)\ndef create_order\(order: dict,',
        '@router.post("", status_code=201)\ndef create_order(order: Dict[str, Any] = Body(...),',
        content
    )
    print('POST corrigido via regex!')

with open(path, 'w') as f:
    f.write(content)

print('\nPronto! Agora FECHE o servidor e reinicie:')
print('Ctrl+C no terminal do servidor')
print('venv\\Scripts\\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000')
