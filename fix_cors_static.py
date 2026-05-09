main_path = r'C:\fleet-cloud\app\main.py'

with open(main_path, 'r') as f:
    content = f.read()

# Adiciona servico de arquivo estático
old_imports = 'from fastapi import FastAPI'
new_imports = '''from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os'''

if 'FileResponse' not in content:
    content = content.replace(old_imports, new_imports)
    print('Imports adicionados!')

# Adiciona rota para servir o HTML
old_root = '''@app.get("/")
def root():
    return {"app": "Gelocrim Fleet API", "docs": "/docs"}'''

new_root = '''@app.get("/")
def root():
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gelocrim_v1.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"app": "Gelocrim Fleet API", "docs": "/docs"}

@app.get("/app")
def app_html():
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gelocrim_v1.html")
    return FileResponse(html_path)'''

if '@app.get("/app")' not in content:
    content = content.replace(old_root, new_root)
    print('Rota HTML adicionada!')

with open(main_path, 'w') as f:
    f.write(content)

print('\nPronto! Reinicie o servidor e acesse:')
print('http://localhost:8000/  (em vez de http://127.0.0.1:8080)')
print('\nAssim o HTML e a API ficam na mesma origem — sem CORS!')
