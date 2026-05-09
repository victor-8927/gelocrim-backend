data = open(r'C:\fleet-cloud\gelocrim_v1.html', encoding='utf-8', errors='ignore').read()

# Procurar pela funcao que preenche modal-ped-body
termos = ['modal-ped-body', 'modal-pedido-detalhe', 'ped-body']

for termo in termos:
    idx = 0
    count = 0
    while count < 5:
        idx = data.find(termo, idx)
        if idx < 0:
            break
        print(f"\n=== '{termo}' ocorrencia {count+1} pos {idx} ===")
        print(data[max(0,idx-300):idx+500])
        print("---")
        idx += 1
        count += 1
