with open(r'C:\fleet-cloud\.env', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'DATABASE_URL=postgresql+psycopg2://postgres.xxbywtumosrukfyedvcc:Fleet2026!@aws-0-sa-east-1.pooler.supabase.com:6543/postgres',
    'DATABASE_URL=sqlite:///C:/fleet-cloud/fleet.db'
)

with open(r'C:\fleet-cloud\.env', 'w', encoding='utf-8') as f:
    f.write(content)

print('DATABASE_URL voltou para SQLite local!')
print('Reinicie a API para aplicar.')
