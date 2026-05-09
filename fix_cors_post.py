from sqlalchemy import text
import os

# ── 1. Corrige o CORS no main.py para aceitar qualquer origem ─────
main_path = r'C:\fleet-cloud\app\main.py'
with open(main_path, 'r') as f:
    main = f.read()

old_cors = '''app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)'''

new_cors = '''app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)'''

if old_cors in main:
    main = main.replace(old_cors, new_cors)
    print('CORS corrigido!')

with open(main_path, 'w') as f:
    f.write(main)

# ── 2. Verifica o POST /orders e corrige o 500 ────────────────────
orders_path = r'C:\fleet-cloud\app\routers\orders.py'
with open(orders_path, 'r') as f:
    content = f.read()

print('\n=== POST /orders atual ===')
import re
m = re.search(r'@router\.post\(""\).*?(?=@router)', content, re.DOTALL)
if m:
    print(m.group()[:500])

# Substitui o POST por versão robusta que aceita dict livre
old_post = '''@router.post("", status_code=201)
def create_order(order: dict, db: sqlite3.Connection = Depends(get_db)):
    cols = ["external_id","recipient_name","address","weight_kg","volume_m3",
            "total_value","order_type","delivery_date","regiao","status","priority",
            "lat","lng","time_window_start","time_window_end"]
    vals = [order.get(c) for c in cols]
    cur = db.execute(
        f"INSERT INTO orders ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})",
        vals
    )
    db.commit()
    row = db.execute(text("SELECT * FROM orders WHERE id=?"), (cur.lastrowid,)).fetchone()
    desc = db.execute(text("SELECT * FROM orders LIMIT 0"))
    return dict(zip([d[0] for d in desc], row))'''

new_post = '''@router.post("", status_code=201)
def create_order(order: dict, db: sqlite3.Connection = Depends(get_db)):
    try:
        cols = ["external_id","recipient_name","address","weight_kg","volume_m3",
                "total_value","order_type","delivery_date","regiao","status","priority",
                "lat","lng","time_window_start","time_window_end"]
        vals = [order.get(c) for c in cols]
        cur = db.execute(
            f"INSERT INTO orders ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})",
            vals
        )
        db.commit()
        return {"id": cur.lastrowid, "external_id": order.get("external_id"), "status": "created"}
    except Exception as e:
        import traceback
        print("ERRO POST /orders:", traceback.format_exc())
        raise'''

if old_post in content:
    content = content.replace(old_post, new_post)
    print('\nPOST /orders corrigido!')
else:
    print('\nPadrão POST não encontrado exato — verificando...')
    if '@router.post("")' in content:
        print('POST existe mas com código diferente')

with open(orders_path, 'w') as f:
    f.write(content)

print('\nReinicie o servidor!')
