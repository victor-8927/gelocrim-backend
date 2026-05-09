path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ver rotVeiculoChanged atual
idx = content.find('function rotVeiculoChanged()')
depth=0; i=idx
while i < len(content):
    if content[i]=='{': depth+=1
    elif content[i]=='}':
        depth-=1
        if depth==0: end=i+1; break
    i+=1
print('rotVeiculoChanged atual:')
print(content[idx:end])

# Ver carregarFrota - como salva os dados do veículo
idx2 = content.find('async function carregarFrota()')
print('\ncarregarFrota (trecho):')
print(content[idx2:idx2+800])
