path = r'C:\fleet-cloud\app\routers\vehicles.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona endpoint PATCH no final
patch_code = '''

@router.patch("/{vid}")
def update_vehicle(vid: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"vda","plate","model","type","capacity_kg","capacity_m3","status",
               "fuel_type","km_per_liter","fuel_price","ipva_anual","manut_mes","daily_cost",
               "pallets","bau_comp","bau_larg","bau_alt","oleo_ult_data","oleo_prox_data","oleo_custo"}
    updates = {k:v for k,v in body.items() if k in allowed}
    if not updates:
        raise HTTPException(status_code=400, detail="Nenhum campo válido")
    updates["updated_at"] = now_str()
    updates["id"] = vid
    sets = ", ".join(f"{k}=:{k}" for k in updates if k != "id")
    db.execute(text(f"UPDATE vehicles SET {sets} WHERE id=:id"), updates)
    db.commit()
    return {"message": "Veículo atualizado!"}

@router.delete("/{vid}", status_code=204)
def delete_vehicle(vid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(text("UPDATE vehicles SET status='deleted' WHERE id=:id"), {"id": vid})
    db.commit()
'''

if '@router.patch' not in content:
    content += patch_code
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('PATCH adicionado ao vehicles.py!')
else:
    print('PATCH já existe!')
