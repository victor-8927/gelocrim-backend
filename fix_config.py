with open(r'C:\fleet-cloud\app\config.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'DATABASE_URL_SYNC = "sqlite:///C:/fleet-cloud/fleet.db"',
    'DATABASE_URL_SYNC = os.getenv("DATABASE_URL", "sqlite:///C:/fleet-cloud/fleet.db")'
)

with open(r'C:\fleet-cloud\app\config.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('config.py corrigido!')
print('DATABASE_URL_SYNC agora le do .env')
