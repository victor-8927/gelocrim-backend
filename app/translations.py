"""
Dicionario central de traducao PT <-> EN
Usado por todos os routers para normalizar campos
"""

# Campos PT -> EN
PT_TO_EN = {
    # clients
    "nome": "name",
    "nome_fantasia": "trade_name",
    "razao_social": "legal_name",
    "cpf_cnpj": "tax_id",
    "telefone": "phone",
    "endereco": "address",
    "endereço": "address",
    "bairro": "district",
    "cidade": "city",
    "cep": "zip_code",
    "estado": "state",
    "segmento": "segment",
    "rota": "route",
    "zona_geo": "geo_zone",
    "tempo_entrega": "service_time",
    "comodatos": "loans",
    "ativo": "status",

    # drivers
    "tipo": "type",
    "veiculo_fixo": "fixed_vehicle",
    "cnh": "license_number",
    "cnh_category": "license_category",
    "cnh_foto": "license_photo",
    "data_admissao": "hire_date",
    "observacoes": "notes",
    "dia_folga": "day_off",
    "carga_horaria": "work_hours",
    "hora_almoco": "lunch_time",
    "ajudante_id": "assistant_id",
    "jornada": "shift",
    "custo_dia": "daily_cost",

    # vehicles
    "ipva_anual": "annual_tax",
    "manut_mes": "monthly_maintenance",
    "bau_comp": "box_length",
    "bau_larg": "box_width",
    "bau_alt": "box_height",
    "oleo_ult_data": "last_oil_date",
    "oleo_prox_data": "next_oil_date",
    "oleo_custo": "oil_cost",

    # routes
    "km_inicial": "km_start",
    "km_final": "km_end",
    "ajudante1_id": "assistant1_id",
    "ajudante2_id": "assistant2_id",

    # stops
    "foto_url": "photo_nf",
    "foto_boleto_url": "photo_receipt",
    "foto_comodato_url": "photo_loan",
    "foto_outros_url": "photo_other",
    "lat_confirmacao": "lat_confirmed",
    "lng_confirmacao": "lng_confirmed",

    # orders
    "regiao": "region",
    "região": "region",
    "nunota": "invoice_number",
    "nfe_status": "invoice_status",
    "peso_kg": "weight_kg",

    # order_items
    "item_tipo": "item_type",
    "item_nome": "item_name",
    "peso_unit": "weight_unit",
    "qtd": "qty",
    "dt_neg": "negotiation_date",

    # status values
    "pendente": "pending",
    "roteado": "routed",
    "entregue": "delivered",
    "entrega": "delivered",
    "concluido": "completed",
    "falhou": "failed",
    "liberada": "released",
    "executando": "executing",
    "ativo": "active",
    "inativo": "inactive",
    "motorista": "driver",
    "ajudante": "assistant",
}

# Campos EN -> PT (inverso)
EN_TO_PT = {v: k for k, v in PT_TO_EN.items()}

# Aliases SQL para queries - retorna campos com nomes PT para o app mae
SQL_ALIASES_CLIENTS = """
    id, codparc, name,
    name AS nome,
    trade_name AS nome_fantasia,
    legal_name AS razao_social,
    tax_id AS cpf_cnpj,
    phone AS telefone,
    address AS endereco,
    district AS bairro,
    city AS cidade,
    zip_code AS cep,
    state AS estado,
    lat, lng,
    segment AS segmento,
    route AS rota,
    geo_zone AS zona_geo,
    service_time AS tempo_entrega,
    loans AS comodatos,
    CASE WHEN status=\'active\' THEN \'S\' ELSE \'N\' END AS ativo,
    status, created_at, updated_at
"""

SQL_ALIASES_STOPS = """
    stop_id, route_id, order_id, sequence,
    recipient_name, address, lat, lng, weight_kg,
    status, eta, ata, atd, failure_reason, codparc,
    segment AS segmento,
    photo_nf AS foto_url,
    photo_receipt AS foto_boleto_url,
    photo_loan AS foto_comodato_url,
    photo_other AS foto_outros_url,
    lat_confirmed AS lat_confirmacao,
    lng_confirmed AS lng_confirmacao,
    created_at
"""

SQL_ALIASES_ROUTES = """
    id AS route_id, trip_number,
    route_date AS date,
    status, planned_start, planned_end,
    total_distance_km,
    km_start AS km_inicial,
    km_end AS km_final,
    last_lat, last_lng, last_seen,
    created_at, updated_at
"""

def normalizar(data: dict) -> dict:
    """Converte campos PT->EN em um dicionario"""
    resultado = {}
    for k, v in data.items():
        chave_en = PT_TO_EN.get(k, k)
        resultado[chave_en] = v
    return resultado

def normalizar_status(status: str) -> str:
    """Converte status PT->EN"""
    return PT_TO_EN.get(status, status)

def normalizar_codparc(codparc) -> int:
    """Remove espacos e converte para int"""
    try:
        return int(str(codparc).strip())
    except:
        return None
