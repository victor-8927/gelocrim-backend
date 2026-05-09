import subprocess

# Verifica versoes
r = subprocess.run(['C:\\fleet-cloud\\venv\\Scripts\\pip.exe', 'show', 'fastapi'], capture_output=True, text=True)
print(r.stdout)

r2 = subprocess.run(['C:\\fleet-cloud\\venv\\Scripts\\pip.exe', 'show', 'pydantic'], capture_output=True, text=True)
print(r2.stdout)
