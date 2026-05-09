import sqlite3 
conn = sqlite3.connect('fleet.db') 
cur = conn.cursor() 
cur.execute("DELETE FROM vehicles WHERE plate LIKE 'TOTAL%' OR plate='NAN'") 
print('Removidos:', cur.rowcount, 'registros invalidos') 
conn.commit() 
