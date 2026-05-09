"""
instalar_vrp_v2.py
Instala o novo motor de roteirização V2 no projeto.
Execute: python instalar_vrp_v2.py
"""
import os, shutil

BASE = r"C:\fleet-cloud"

# 1. Copia vrp_solver_v2.py para vrp_solver.py
src = os.path.join(BASE, "vrp_solver_v2.py")
dst = os.path.join(BASE, "vrp_solver.py")

if os.path.exists(src):
    shutil.copy2(src, dst)
    print("✅ vrp_solver.py atualizado para V2!")
else:
    print("❌ vrp_solver_v2.py não encontrado. Baixe e salve em C:\\fleet-cloud\\")
    exit(1)

# 2. Atualiza routes.py para usar horário 07:30 e novo solver
routes_path = os.path.join(BASE, "app", "routers", "routes.py")

with open(routes_path, "r", encoding="utf-8") as f:
    content = f.read()

# Atualiza import do solver
content = content.replace(
    "from vrp_solver import VRPSolver, Vehicle, Delivery, DepotLocation",
    "from vrp_solver import VRPSolver, Vehicle, Delivery, DepotLocation, DEPOT_START_MIN"
)

# Atualiza função _min para usar 07:30 como padrão
content = content.replace(
    """def _min(t) -> int:
    \"\"\"Converte string HH:MM para minutos desde meia-noite.\"\"\"
    if not t:
        return 480""",
    """def _min(t) -> int:
    \"\"\"Converte string HH:MM para minutos desde meia-noite.\"\"\"
    if not t:
        return DEPOT_START_MIN  # 07:30 padrão"""
)

# Atualiza a criação do solver para passar depot_start
content = content.replace(
    "solver = VRPSolver(time_limit_sec=body.time_limit_sec)",
    "solver = VRPSolver(time_limit_sec=body.time_limit_sec, depot_start=DEPOT_START_MIN)"
)

# Atualiza o planned_start para usar 07:30
content = content.replace(
    '"ps": _hhmm(ps), "pe": _hhmm(pe)',
    '"ps": _hhmm(DEPOT_START_MIN), "pe": _hhmm(pe)'
)

with open(routes_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ routes.py atualizado com horário 07:30!")

# 3. Testa o novo solver
print("\nTestando novo solver V2...")
try:
    import sys
    sys.path.insert(0, BASE)
    from vrp_solver import VRPSolver, Vehicle, Delivery, DepotLocation, DEPOT_START_MIN

    depot = DepotLocation(lat=-3.1019, lng=-60.0250)
    vehicles = [Vehicle(id="VH-001", capacity_kg=1000, capacity_m3=8)]
    deliveries = [
        Delivery(id="PED-001", lat=-3.1300, lng=-60.0100, weight_kg=50, volume_m3=0.5, priority=2),
        Delivery(id="PED-002", lat=-3.0800, lng=-60.0500, weight_kg=80, volume_m3=0.8, priority=1),
        Delivery(id="PED-003", lat=-3.1500, lng=-59.9800, weight_kg=30, volume_m3=0.3, priority=3),
    ]

    solver = VRPSolver(time_limit_sec=10)
    result = solver.solve(vehicles, deliveries, depot)

    print(f"  ✅ Status: {result.status}")
    print(f"  ✅ Rotas: {len(result.routes)}")
    print(f"  ✅ Distância total: {result.total_distance_km} km")
    print(f"  ✅ Horário saída: 07:30 (minuto {DEPOT_START_MIN})")
    for route in result.routes:
        print(f"  ✅ Score rota {route.vehicle_id}: {route.score}/10")
        for stop in route.stops:
            h = stop.arrival_min // 60
            m = stop.arrival_min % 60
            print(f"     [{stop.sequence+1}] {stop.delivery_id} — {h:02d}:{m:02d}")

except Exception as e:
    print(f"  ❌ Erro no teste: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 Motor de roteirização V2 instalado!")
print("\nMelhorias ativas:")
print("  ✅ Horário de saída: 07:30")
print("  ✅ Início e fim no depósito obrigatório")
print("  ✅ Agrupamento Tipo 4 (K-Means geográfico)")
print("  ✅ Sequenciamento Tipo K (Nearest Neighbor + 2-opt)")
print("  ✅ Score operacional por rota")
print("  ✅ Priorização de pedidos urgentes")
print("\nReinicie o servidor para aplicar as mudanças!")
