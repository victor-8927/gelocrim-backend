data = open(r'C:\gelocrim-motorista\screens\RotaScreen.js', encoding='utf-8', errors='ignore').read()
# Ver como a linha de rota e calculada
idx = data.find('routeCoords')
print(data[max(0,idx-200):idx+500])
