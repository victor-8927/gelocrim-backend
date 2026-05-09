import sqlite3
conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')

print('=== ROUTES ===')
for r in conn.execute("SELECT id, trip_number, status, vehicle_id, driver_id FROM routes").fetchall():
    print(r)

print('\n=== ROUTE_STOPS ===')
count = conn.execute("SELECT COUNT(*) FROM route_stops").fetchone()[0]
print(f'Total stops: {count}')

conn.close()
