path = r'C:\fleet-cloud\app\routers\order_items.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'router = APIRouter()',
    'router = APIRouter(prefix="/api/v1/order_items", tags=["OrderItems"])'
)

# Corrige os endpoints removendo /order_items do path (já está no prefix)
content = content.replace('@router.get("/order_items")', '@router.get("")')
content = content.replace('@router.post("/order_items/bulk")', '@router.post("/bulk")')
content = content.replace('@router.delete("/order_items/{item_tipo}")', '@router.delete("/{item_tipo}")')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Prefix adicionado! Reinicie o servidor.')
