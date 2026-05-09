caminho = r"C:\fleet-cloud\gelocrim_v1.html"
with open(caminho, encoding="utf-8", errors="ignore") as f:
    data = f.read()

# Verificar se v-edit-id existe no HTML
if 'id="v-edit-id"' in data:
    idx = data.find('id="v-edit-id"')
    print("v-edit-id encontrado:")
    print(data[max(0,idx-100):idx+100])
else:
    print("v-edit-id NAO existe no HTML! Precisa adicionar.")
    # Adicionar campo oculto no modal
    antigo = '<div id="modal-veiculo-completo"'
    if antigo in data:
        # Encontrar o form dentro do modal e adicionar input hidden
        idx_modal = data.find('modal-veiculo-completo')
        idx_form = data.find('<div style="padding:20px 24px">', idx_modal)
        if idx_form > 0:
            data = data[:idx_form+30] + '\n            <input type="hidden" id="v-edit-id" value="">' + data[idx_form+30:]
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(data)
            print("OK - v-edit-id adicionado!")
