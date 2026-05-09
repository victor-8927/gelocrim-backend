import os
for nome in ['iniciar.bat', 'start.bat', 'iniciar_servidor.bat', 'run.bat']:
    p = r'C:\fleet-cloud\\' + nome
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8', errors='replace') as f:
            print(f'=== {nome} ===')
            print(f.read())
