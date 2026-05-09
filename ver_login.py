data = open(r'C:\fleet-cloud\gelocrim_v1.html', encoding='utf-8', errors='ignore').read()
idx = data.find('async function doLogin')
if idx < 0:
    idx = data.find('function doLogin')
print(data[idx:idx+600])
