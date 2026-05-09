import sqlite3
conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')

print('=== BANCO DE DADOS ===')
print(f'Clientes: {conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]}')
print(f'Orders pending: {conn.execute("SELECT COUNT(*) FROM orders WHERE status=\'pending\'").fetchone()[0]}')
print(f'Orders total: {conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]}')
print(f'Routes: {conn.execute("SELECT COUNT(*) FROM routes").fetchone()[0]}')
print(f'Route stops: {conn.execute("SELECT COUNT(*) FROM route_stops").fetchone()[0]}')
print(f'Drivers: {conn.execute("SELECT COUNT(*) FROM drivers").fetchone()[0]}')
print(f'Vehicles: {conn.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0]}')
print(f'Order items: {conn.execute("SELECT COUNT(*) FROM order_items").fetchone()[0]}')

print('\n=== ORDERS SEM GPS ===')
sem_gps = conn.execute("SELECT COUNT(*) FROM orders WHERE (lat IS NULL OR lat=0) AND status='pending'").fetchone()[0]
print(f'Pedidos sem GPS: {sem_gps}')

print('\n=== PESO TOTAL PENDENTE ===')
peso = conn.execute("SELECT SUM(weight_kg) FROM orders WHERE status='pending'").fetchone()[0]
print(f'Peso total pendente: {peso:.0f if peso else 0} kg')

conn.close()
