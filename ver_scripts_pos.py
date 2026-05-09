path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Mostra o que tem em cada abertura de script
opens  = [334, 17189, 149673, 197227, 206600]
closes = [466, 17271, 210250, 210262]

print('Script na pos 149673:')
print(content[149673:149773])
print('\n---')
print('Script na pos 197227:')
print(content[197227:197327])
print('\n---')
print('Script na pos 206600:')
print(content[206600:206700])
