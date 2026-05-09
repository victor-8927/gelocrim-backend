data = open(r'C:\fleet-cloud\gelocrim_v1.html', encoding='utf-8', errors='ignore').read()
idx = data.find('async function salvarMotoristaCompleto')
print(data[idx:idx+800])
