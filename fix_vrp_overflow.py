path = r'C:\fleet-cloud\vrp_solver.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige a funcao dkg para retornar int simples
old_dkg = '''        def dkg(fi):
            return data["demands_kg"][manager.IndexToNode(fi)]
        kgc = routing.RegisterUnaryTransitCallback(dkg)
        routing.AddDimensionWithVehicleCapacity(
            kgc, 0, [int(c) for c in data["vehicle_capacities_kg"]], True, "CapKg"
        )'''

new_dkg = '''        def dkg(fi):
            node = manager.IndexToNode(fi)
            return int(data["demands_kg"][node])
        kgc = routing.RegisterUnaryTransitCallback(dkg)
        routing.AddDimensionWithVehicleCapacity(
            kgc, 0, [int(c) for c in data["vehicle_capacities_kg"]], True, "CapKg"
        )'''

if old_dkg in content:
    content = content.replace(old_dkg, new_dkg)
    print('dkg corrigido!')
else:
    print('Padrao dkg nao encontrado, tentando alternativa...')
    # Tenta substituicao mais simples
    content = content.replace(
        'return data["demands_kg"][manager.IndexToNode(fi)]',
        'node = manager.IndexToNode(fi)\n            return int(data["demands_kg"][node])'
    )
    content = content.replace(
        'return data["demands_kg"][manager.IndexToNode(fi) * 10]',
        'node = manager.IndexToNode(fi)\n            return int(data["demands_kg"][node])'
    )
    print('Substituicao alternativa aplicada!')

# Corrige dm3 tambem
old_dm3 = '''        def dm3(fi):
            return int(data["demands_m3"][manager.IndexToNode(fi)] * 1000)
        m3c = routing.RegisterUnaryTransitCallback(dm3)
        routing.AddDimensionWithVehicleCapacity(
            m3c, 0, [int(c * 1000) for c in data["vehicle_capacities_m3"]], True, "CapM3"
        )'''

new_dm3 = '''        def dm3(fi):
            node = manager.IndexToNode(fi)
            return int(data["demands_m3"][node] * 100)
        m3c = routing.RegisterUnaryTransitCallback(dm3)
        routing.AddDimensionWithVehicleCapacity(
            m3c, 0, [int(c * 100) for c in data["vehicle_capacities_m3"]], True, "CapM3"
        )'''

if old_dm3 in content:
    content = content.replace(old_dm3, new_dm3)
    print('dm3 corrigido!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('vrp_solver.py corrigido!')
print('Reinicie a API com Ctrl+C e venv\\Scripts\\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000')
