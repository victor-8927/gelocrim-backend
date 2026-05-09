import subprocess, os

files = [
    r'C:\gelocrim-motorista\App.js',
    r'C:\gelocrim-motorista\screens\LoginScreen.js',
    r'C:\gelocrim-motorista\screens\RotaScreen.js',
    r'C:\gelocrim-motorista\screens\EntregaScreen.js',
    r'C:\gelocrim-motorista\screens\ResumoScreen.js',
]

for f in files:
    r = subprocess.run(
        ['node', '--check', f],
        capture_output=True
    )
    stderr = r.stderr.decode('utf-8', errors='replace')
    if r.returncode == 0:
        print(f'{os.path.basename(f)}: OK')
    else:
        print(f'{os.path.basename(f)}: ERRO')
        print(f'  {stderr[:200]}')
