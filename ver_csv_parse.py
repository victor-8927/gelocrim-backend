path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('_csvDados.push({')
if idx != -1:
    print(repr(content[max(0,idx-300):idx+600]))
else:
    print('_csvDados.push nao encontrado')
    idx2 = content.find('_csvDados')
    print(f'_csvDados em: {idx2}')
    print(content[idx2:idx2+200])
