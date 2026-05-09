"""
vrp_solver_v2.py — Motor de Roteirização Gelocrim V2

Melhorias implementadas:
- Horário de saída fixo: 07:30
- Início e fim obrigatório no depósito
- Agrupamento geográfico Tipo 4 (K-Means por proximidade)
- Sequenciamento Tipo K (nearest neighbor + 2-opt)
- Score operacional por rota
- Suporte a prioridades
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import math
import logging

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

logger = logging.getLogger(__name__)

# ── Constantes ───────────────────────────────────────────────────────────────
DEPOT_START_MIN = 7 * 60 + 30   # 07:30 em minutos
DEPOT_END_MIN   = 18 * 60       # 18:00 em minutos
AVG_SPEED_KMH   = 35.0          # velocidade média Manaus
SERVICE_MIN_DEFAULT = 10        # minutos de atendimento por parada


# ── Modelos de entrada ───────────────────────────────────────────────────────

@dataclass
class DepotLocation:
    lat: float
    lng: float


@dataclass
class Vehicle:
    id: str
    capacity_kg: float
    capacity_m3: float
    shift_start: int = DEPOT_START_MIN
    shift_end: int   = DEPOT_END_MIN


@dataclass
class Delivery:
    id: str
    lat: float
    lng: float
    weight_kg: float     = 0.0
    volume_m3: float     = 0.0
    service_minutes: int = SERVICE_MIN_DEFAULT
    tw_start: int        = DEPOT_START_MIN
    tw_end: int          = DEPOT_END_MIN
    priority: int        = 1   # 1=normal, 2=alta, 3=urgente
    region: str          = ""


@dataclass
class Stop:
    delivery_id: str
    sequence: int
    arrival_min: int
    departure_min: int
    lat: float = 0.0
    lng: float = 0.0


@dataclass
class RouteResult:
    vehicle_id: str
    stops: list[Stop]
    total_distance_km: float
    total_time_min: int
    score: float = 0.0
    cluster_id: int = -1


@dataclass
class SolveResult:
    routes: list[RouteResult]
    unassigned: list[str]
    status: str
    wall_time_ms: int
    total_distance_km: float = 0.0


# ── Utilitários ──────────────────────────────────────────────────────────────

def _haversine_km(lat1, lng1, lat2, lng2) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi   = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _travel_min(km: float, speed: float = AVG_SPEED_KMH) -> int:
    return max(1, int((km / speed) * 60))


def _hhmm(minutes: int) -> str:
    minutes = max(0, minutes % 1440)
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


# ── Agrupamento Tipo 4 (K-Means Geográfico) ──────────────────────────────────

def cluster_deliveries(deliveries: list[Delivery], n_clusters: int) -> list[int]:
    """
    Agrupamento geográfico Tipo 4:
    Divide as entregas em clusters por proximidade geográfica.
    Retorna lista de cluster_id para cada delivery.
    """
    if not deliveries or n_clusters <= 1:
        return [0] * len(deliveries)

    n = len(deliveries)
    k = min(n_clusters, n)

    # Inicializa centróides com os pontos mais distantes entre si
    centroids = [(deliveries[0].lat, deliveries[0].lng)]
    for _ in range(1, k):
        max_dist = -1
        farthest = 0
        for i, d in enumerate(deliveries):
            min_dist = min(_haversine_km(d.lat, d.lng, c[0], c[1]) for c in centroids)
            if min_dist > max_dist:
                max_dist = min_dist
                farthest = i
        centroids.append((deliveries[farthest].lat, deliveries[farthest].lng))

    # K-Means iterativo (máx 20 iterações)
    assignments = [0] * n
    for _ in range(20):
        # Atribuir ao centróide mais próximo
        new_assignments = []
        for d in deliveries:
            dists = [_haversine_km(d.lat, d.lng, c[0], c[1]) for c in centroids]
            new_assignments.append(dists.index(min(dists)))

        if new_assignments == assignments:
            break
        assignments = new_assignments

        # Recalcular centróides
        for c_idx in range(k):
            members = [deliveries[i] for i, a in enumerate(assignments) if a == c_idx]
            if members:
                centroids[c_idx] = (
                    sum(m.lat for m in members) / len(members),
                    sum(m.lng for m in members) / len(members),
                )

    return assignments


# ── Sequenciamento Tipo K (Nearest Neighbor + 2-opt) ─────────────────────────

def sequence_tipo_k(deliveries: list[Delivery], depot: DepotLocation) -> list[int]:
    """
    Sequenciamento Tipo K:
    1. Nearest Neighbor a partir do depósito
    2. Melhoria 2-opt
    Retorna lista de índices na ordem otimizada.
    """
    if not deliveries:
        return []

    n = len(deliveries)
    unvisited = list(range(n))
    route = []

    # Nearest Neighbor a partir do depósito
    current_lat, current_lng = depot.lat, depot.lng
    while unvisited:
        nearest = min(unvisited,
                      key=lambda i: _haversine_km(current_lat, current_lng,
                                                   deliveries[i].lat, deliveries[i].lng))
        route.append(nearest)
        unvisited.remove(nearest)
        current_lat = deliveries[nearest].lat
        current_lng = deliveries[nearest].lng

    # 2-opt melhoria
    improved = True
    iterations = 0
    while improved and iterations < 100:
        improved = False
        iterations += 1
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                # Calcula custo atual
                a, b = deliveries[route[i-1]], deliveries[route[i]]
                c, d = deliveries[route[j]], deliveries[route[(j+1) % n]] if j+1 < n else None

                d1 = _haversine_km(a.lat, a.lng, b.lat, b.lng)
                d2 = _haversine_km(c.lat, c.lng, d.lat, d.lng) if d else 0

                # Custo após inversão
                d3 = _haversine_km(a.lat, a.lng, c.lat, c.lng)
                d4 = _haversine_km(b.lat, b.lng, d.lat, d.lng) if d else 0

                if d3 + d4 < d1 + d2 - 0.001:
                    route[i:j+1] = route[i:j+1][::-1]
                    improved = True

    return route


# ── Score Operacional ─────────────────────────────────────────────────────────

def calc_route_score(
    route: RouteResult,
    vehicles: list[Vehicle],
    deliveries: list[Delivery],
) -> float:
    """
    Score operacional da rota (0 a 10).
    Penaliza: km excessivo, tempo longo, capacidade ociosa, atrasos de janela.
    """
    if not route.stops:
        return 0.0

    score = 10.0
    delivery_map = {d.id: d for d in deliveries}
    vehicle = next((v for v in vehicles if v.id == route.vehicle_id), None)

    # Penaliza distância excessiva (>50km por rota)
    if route.total_distance_km > 50:
        score -= min(2.0, (route.total_distance_km - 50) / 50)

    # Penaliza tempo excessivo (>8h)
    if route.total_time_min > 480:
        score -= min(2.0, (route.total_time_min - 480) / 60 * 0.3)

    # Penaliza capacidade ociosa
    if vehicle:
        total_kg = sum(delivery_map.get(s.delivery_id, Delivery("",0,0)).weight_kg
                       for s in route.stops)
        ociosidade = 1 - (total_kg / max(vehicle.capacity_kg, 1))
        score -= ociosidade * 1.5

    # Penaliza violações de janela
    for stop in route.stops:
        d = delivery_map.get(stop.delivery_id)
        if d and stop.arrival_min > d.tw_end:
            score -= 0.5

    return max(0.0, round(score, 2))


# ── Solver Principal ──────────────────────────────────────────────────────────

class VRPSolver:
    """
    Motor de Roteirização Gelocrim V2

    Pipeline:
    1. Agrupamento Tipo 4 (K-Means geográfico)
    2. Alocação por capacidade
    3. Sequenciamento Tipo K (nearest neighbor + 2-opt)
    4. Otimização OR-Tools com VRPTW
    5. Score operacional por rota
    """

    def __init__(
        self,
        time_limit_sec: int = 30,
        avg_speed_kmh: float = AVG_SPEED_KMH,
        depot_start: int = DEPOT_START_MIN,
    ):
        self.time_limit_sec = time_limit_sec
        self.avg_speed_kmh  = avg_speed_kmh
        self.depot_start    = depot_start

    def solve(
        self,
        vehicles: list[Vehicle],
        deliveries: list[Delivery],
        depot: DepotLocation,
    ) -> SolveResult:

        if not vehicles:
            raise ValueError("Pelo menos um veículo é necessário.")
        if not deliveries:
            return SolveResult(routes=[], unassigned=[], status="optimal",
                               wall_time_ms=0, total_distance_km=0)

        # Ordena por prioridade (urgente primeiro)
        deliveries = sorted(deliveries, key=lambda d: -d.priority)

        # Agrupamento Tipo 4
        cluster_ids = cluster_deliveries(deliveries, len(vehicles))

        # Pré-sequenciamento Tipo K por cluster
        clusters: dict[int, list[int]] = {}
        for i, cid in enumerate(cluster_ids):
            clusters.setdefault(cid, []).append(i)

        # Reordena deliveries por cluster e sequência Tipo K
        reordered = []
        for cid in sorted(clusters.keys()):
            idxs = clusters[cid]
            cluster_deliveries_list = [deliveries[i] for i in idxs]
            seq = sequence_tipo_k(cluster_deliveries_list, depot)
            reordered.extend([cluster_deliveries_list[s] for s in seq])

        deliveries = reordered

        # OR-Tools VRPTW
        data = self._build_data(vehicles, deliveries, depot)
        manager, routing = self._build_model(data)
        solution = self._run_search(routing, manager, data)

        if solution is None:
            logger.warning("Solver não encontrou solução viável.")
            return SolveResult(
                routes=[],
                unassigned=[d.id for d in deliveries],
                status="infeasible",
                wall_time_ms=self.time_limit_sec * 1000,
            )

        result = self._extract_result(solution, manager, routing, data,
                                      vehicles, deliveries, cluster_ids)

        # Calcula score para cada rota
        for route in result.routes:
            route.score = calc_route_score(route, vehicles, deliveries)

        result.total_distance_km = round(
            sum(r.total_distance_km for r in result.routes), 2
        )

        return result

    def _build_data(self, vehicles, deliveries, depot) -> dict:
        nodes = [depot] + deliveries
        n = len(nodes)

        dist_matrix = []
        time_matrix = []

        for i in range(n):
            row_d, row_t = [], []
            for j in range(n):
                if i == j:
                    row_d.append(0); row_t.append(0)
                else:
                    lat_i = depot.lat if i == 0 else deliveries[i-1].lat
                    lng_i = depot.lng if i == 0 else deliveries[i-1].lng
                    lat_j = depot.lat if j == 0 else deliveries[j-1].lat
                    lng_j = depot.lng if j == 0 else deliveries[j-1].lng
                    km = _haversine_km(lat_i, lng_i, lat_j, lng_j)
                    row_d.append(int(km * 10))
                    row_t.append(_travel_min(km, self.avg_speed_kmh))
            dist_matrix.append(row_d)
            time_matrix.append(row_t)

        # Adiciona tempo de serviço
        for i, d in enumerate(deliveries, start=1):
            for j in range(n):
                if j != i:
                    time_matrix[i][j] += d.service_minutes

        return {
            "num_vehicles": len(vehicles),
            "depot": 0,
            "distance_matrix": dist_matrix,
            "time_matrix": time_matrix,
            "time_windows": [
                (self.depot_start, DEPOT_END_MIN),
                *[(d.tw_start, d.tw_end) for d in deliveries],
            ],
            "demands_kg": [0] + [d.weight_kg for d in deliveries],
            "demands_m3": [0] + [d.volume_m3 for d in deliveries],
            "vehicle_capacities_kg": [v.capacity_kg for v in vehicles],
            "vehicle_capacities_m3": [v.capacity_m3 for v in vehicles],
            "vehicle_time_windows": [
                (self.depot_start, v.shift_end) for v in vehicles
            ],
        }

    def _build_model(self, data):
        manager = pywrapcp.RoutingIndexManager(
            len(data["distance_matrix"]),
            data["num_vehicles"],
            data["depot"],
        )
        routing = pywrapcp.RoutingModel(manager)

        def dist_cb(fi, ti):
            return data["distance_matrix"][manager.IndexToNode(fi)][manager.IndexToNode(ti)]
        dc = routing.RegisterTransitCallback(dist_cb)
        routing.SetArcCostEvaluatorOfAllVehicles(dc)

        def time_cb(fi, ti):
            return data["time_matrix"][manager.IndexToNode(fi)][manager.IndexToNode(ti)]
        tc = routing.RegisterTransitCallback(time_cb)

        routing.AddDimension(tc, 60, 1440, False, "Time")
        time_dim = routing.GetDimensionOrDie("Time")

        for node_idx, (tw_s, tw_e) in enumerate(data["time_windows"]):
            idx = manager.NodeToIndex(node_idx)
            time_dim.CumulVar(idx).SetRange(tw_s, tw_e)

        for v_idx, (ts, te) in enumerate(data["vehicle_time_windows"]):
            time_dim.CumulVar(routing.Start(v_idx)).SetRange(ts, te)
            time_dim.CumulVar(routing.End(v_idx)).SetRange(ts, te)

        def dkg(fi):
            node = manager.IndexToNode(fi)
            return int(data["demands_kg"][node])
        kgc = routing.RegisterUnaryTransitCallback(dkg)
        routing.AddDimensionWithVehicleCapacity(
            kgc, 0, [int(c) for c in data["vehicle_capacities_kg"]], True, "CapKg"
        )

        def dm3(fi):
            node = manager.IndexToNode(fi)
            return int(data["demands_m3"][node] * 100)
        m3c = routing.RegisterUnaryTransitCallback(dm3)
        routing.AddDimensionWithVehicleCapacity(
            m3c, 0, [int(c * 100) for c in data["vehicle_capacities_m3"]], True, "CapM3"
        )

        for node in range(1, len(data["distance_matrix"])):
            routing.AddDisjunction([manager.NodeToIndex(node)], 100000)

        return manager, routing

    def _run_search(self, routing, manager, data):
        params = pywrapcp.DefaultRoutingSearchParameters()
        params.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        params.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        params.time_limit.seconds = self.time_limit_sec
        params.log_search = False
        return routing.SolveWithParameters(params)

    def _extract_result(self, solution, manager, routing, data,
                        vehicles, deliveries, cluster_ids) -> SolveResult:
        time_dim = routing.GetDimensionOrDie("Time")
        routes = []
        assigned = set()

        delivery_cluster = {d.id: cluster_ids[i] if i < len(cluster_ids) else -1
                            for i, d in enumerate(deliveries)}

        for v_idx, vehicle in enumerate(vehicles):
            if not routing.IsVehicleUsed(solution, v_idx):
                continue

            stops = []
            total_dist = 0
            idx = routing.Start(v_idx)
            seq = 0

            while not routing.IsEnd(idx):
                node = manager.IndexToNode(idx)
                if node != data["depot"]:
                    d = deliveries[node - 1]
                    arrival   = solution.Value(time_dim.CumulVar(idx))
                    departure = arrival + d.service_minutes
                    stops.append(Stop(
                        delivery_id=d.id,
                        sequence=seq,
                        arrival_min=arrival,
                        departure_min=departure,
                        lat=d.lat,
                        lng=d.lng,
                    ))
                    assigned.add(node)
                    seq += 1

                next_idx = solution.Value(routing.NextVar(idx))
                total_dist += routing.GetArcCostForVehicle(idx, next_idx, v_idx)
                idx = next_idx

            end_t   = solution.Value(time_dim.CumulVar(routing.End(v_idx)))
            start_t = solution.Value(time_dim.CumulVar(routing.Start(v_idx)))

            routes.append(RouteResult(
                vehicle_id=vehicle.id,
                stops=stops,
                total_distance_km=round(total_dist / 10, 2),
                total_time_min=end_t - start_t,
                cluster_id=v_idx,
            ))

        all_nodes = set(range(1, len(deliveries) + 1))
        unassigned = [deliveries[n - 1].id for n in (all_nodes - assigned)]
        status = "optimal" if routing.status() == 1 else "feasible"

        return SolveResult(
            routes=routes,
            unassigned=unassigned,
            status=status,
            wall_time_ms=routing.solver().WallTime(),
        )


# ── Exemplo ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)

    depot = DepotLocation(lat=-3.1019, lng=-60.0250)

    vehicles = [
        Vehicle(id="VH-001", capacity_kg=1000, capacity_m3=8),
        Vehicle(id="VH-002", capacity_kg=800,  capacity_m3=6),
        Vehicle(id="VH-003", capacity_kg=500,  capacity_m3=4),
    ]

    deliveries = [
        Delivery(id="PED-001", lat=-3.1300, lng=-60.0100, weight_kg=50,  volume_m3=0.5, priority=2),
        Delivery(id="PED-002", lat=-3.0800, lng=-60.0500, weight_kg=120, volume_m3=1.2, priority=1),
        Delivery(id="PED-003", lat=-3.1500, lng=-59.9800, weight_kg=30,  volume_m3=0.3, priority=3),
        Delivery(id="PED-004", lat=-3.0600, lng=-60.0200, weight_kg=200, volume_m3=2.0, priority=1),
        Delivery(id="PED-005", lat=-3.1200, lng=-60.0350, weight_kg=80,  volume_m3=0.8, priority=2),
    ]

    solver = VRPSolver(time_limit_sec=15)
    result = solver.solve(vehicles, deliveries, depot)

    print(f"\nStatus: {result.status}")
    print(f"Distância total: {result.total_distance_km} km")
    print(f"Não alocados: {result.unassigned or 'nenhum'}\n")

    for route in result.routes:
        print(f"Veículo {route.vehicle_id} | Score: {route.score}/10 | {route.total_distance_km} km")
        for stop in route.stops:
            print(f"  [{stop.sequence+1}] {stop.delivery_id} — {_hhmm(stop.arrival_min)}")
        print()
