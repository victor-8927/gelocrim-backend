
caminho = r"C:\fleet-cloud\gelocrim_v1.html"
with open(caminho, encoding="utf-8", errors="ignore") as f:
    data = f.read()

antigo = "'<td style=\"font-size:11px;color:#90afd4\">'+(o.time_window_start||'07:30')+'-'+(o.time_window_end||'18:00')+'</td>'+"
novo   = "'<td style=\"font-size:11px;color:#90afd4\">'+(o.tempo_entrega?o.tempo_entrega+' min':'—')+'</td>'+"

if antigo in data:
    data = data.replace(antigo, novo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(data)
    print("OK - coluna Janela corrigida para mostrar tempo de atendimento!")
else:
    print("Trecho nao encontrado, tentando alternativa...")
    # Alternativa com aspas simples
    antigo2 = """'<td style="font-size:11px;color:#90afd4">'+(o.time_window_start||'07:30')+'-'+(o.time_window_end||'18:00')+'</td>'+"""
    novo2   = """'<td style="font-size:11px;color:#90afd4">'+(o.tempo_entrega?o.tempo_entrega+' min':'—')+'</td>'+"""
    if antigo2 in data:
        data = data.replace(antigo2, novo2)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(data)
        print("OK - corrigido (alternativa)!")
    else:
        print("ERRO - nao encontrou o trecho")
