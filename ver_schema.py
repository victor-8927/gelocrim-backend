import sqlite3 
c = sqlite3.connect('fleet.db') 
cur = c.cursor() 
cur.execute("SELECT sql FROM sqlite_master WHERE name='order_items'") 
print(cur.fetchone()[0]) 
