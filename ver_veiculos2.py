path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Modal de veículo
idx = content.find('modal-vehicle')
print('=== MODAL VEHICLE ===')
print(content[idx:idx+1500])

# saveVehicle
idx2 = content.find('async function saveVehicle(')
print('\n=== saveVehicle ===')
print(content[idx2:idx2+600])

# loadVehicles
idx3 = content.find('async function loadVehicles(')
print('\n=== loadVehicles ===')
print(content[idx3:idx3+600])
