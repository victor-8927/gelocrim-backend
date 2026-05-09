import re

# 1. Corrige routes.py para buscar o campo TOP do banco
routes_path = r'C:\fleet-cloud\app\routers\routes.py'
with open(routes_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona top na query de pedidos
old_query = '''            SELECT o.id, o.lat, o.lng, o.weight_kg, o.volume_m3,
                   o.tw_start, o.tw_end,
                   r.address, r.name AS recipient_name
            FROM orders o JOIN recipients r ON r.id = o.recipient_id
            WHERE o.status IN (\'pending\',\'queued\')
              AND o.nfe_status != \'rejected\'
              AND date(o.created_at) <= :d'''

new_query = '''            SELECT o.id, o.lat, o.lng, o.weight_kg, o.volume_m3,
                   o.tw_start, o.tw_end, o.recipient_id,
                   COALESCE(o.notes, \'\') as top,
                   r.address, r.name AS recipient_name
            FROM orders o JOIN recipients r ON r.id = o.recipient_id
            WHERE o.status IN (\'pending\',\'queued\')
              AND date(o.created_at) <= :d'''

content = content.replace(old_query, new_query)

# Corrige tambem a query com order_ids
old_query2 = '''            SELECT o.id, o.lat, o.lng, o.weight_kg, o.volume_m3,
                   o.tw_start, o.tw_end,
                   r.address, r.name AS recipient_name
            FROM orders o JOIN recipients r ON r.id = o.recipient_id
            WHERE o.id IN {ph} AND o.status IN (\'pending\',\'queued\')'''

new_query2 = '''            SELECT o.id, o.lat, o.lng, o.weight_kg, o.volume_m3,
                   o.tw_start, o.tw_end, o.recipient_id,
                   COALESCE(o.external_id, \'\') as top,
                   r.address, r.name AS recipient_name
            FROM orders o JOIN recipients r ON r.id = o.recipient_id
            WHERE o.id IN {ph} AND o.status IN (\'pending\',\'queued\')'''

content = content.replace(old_query2, new_query2)

with open(routes_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('routes.py query atualizada com TOP e recipient_id!')

# 2. Adiciona coluna top na tabela orders se nao existir
import sys, os
sys.path.insert(0, r'C:\fleet-cloud')
os.chdir(r'C:\fleet-cloud')

from app.database import engine_sync
from sqlalchemy import text

with engine_sync.begin() as conn:
    try:
        conn.execute(text("ALTER TABLE orders ADD COLUMN top TEXT"))
        print('Coluna top adicionada!')
    except:
        print('Coluna top ja existe!')
    try:
        conn.execute(text("ALTER TABLE orders ADD COLUMN recipient_id_orig TEXT"))
        print('OK')
    except:
        pass

# 3. Atualiza o HTML para mostrar TOPs na parada
html_path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Corrige a exibicao das paradas no resultado da roteirizacao
old_stop_row = '''                    <td style="padding:6px 10px;font-family:monospace;color:#2563eb;font-weight:600">${s.eta}</td>
                    <td style="padding:6px 10px;font-weight:600">${s.recipient_name}</td>
                    <td style="padding:6px 10px;color:var(--muted)">${s.address||\'\'}</td>
                    <td style="padding:6px 10px;text-align:right">${(s.weight_kg||0).toFixed(0)} kg</td>'''

new_stop_row = '''                    <td style="padding:6px 10px;font-family:monospace;color:#2563eb;font-weight:600">${s.eta}</td>
                    <td style="padding:6px 10px">
                      <div style="font-weight:600">${s.recipient_name}</div>
                      ${s.num_pedidos > 1 ? `<div style="font-size:10px;color:#7c3aed;margin-top:2px">${s.num_pedidos} pedidos: ${s.pedidos_info||\'\'}</div>` : \'\'}
                    </td>
                    <td style="padding:6px 10px;color:var(--muted);font-size:11px">${s.address||\'\'}</td>
                    <td style="padding:6px 10px;text-align:right">${(s.weight_kg||0).toFixed(0)} kg</td>'''

html = html.replace(old_stop_row, new_stop_row)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print('HTML atualizado com exibicao de TOPs!')
print('\nPronto! Reinicie a API e teste a roteirizacao.')
