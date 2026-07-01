import json

RUTA_PRODUCTOS = "datos/productos.json"
RUTA_PEDIDOS = "datos/pedidos.json"

def _cargar_json(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f: return json.load(f)
    except:
        return {} if "productos" in ruta_archivo else []

def obtener_alertas_reabastecimiento(limite_minimo=5):
    """Genera alertas gerenciales de productos con bajo inventario."""
    productos_db = _cargar_json(RUTA_PRODUCTOS)
    print("\n⚠️ ALERTAS DE REABASTECIMIENTO CRÍTICO ⚠️")
    for id_prod, info in productos_db.items():
        if info.get("cantidad", 0) <= limite_minimo:
            print(f" -> {id_prod}: {info['nombre']} | Quedan: {info['cantidad']} uds")

def calcular_porcentaje_pedidos_retrasados():
    """Calcula el KPI de efectividad y retrasos logísticos."""
    pedidos = _cargar_json(RUTA_PEDIDOS)
    if not pedidos: return 0.0
    retrasados = sum(1 for p in pedidos if p.get("estado") == "Retrasado")
    print(f"\n📊 TASA DE PEDIDOS RETRASADOS: {round((retrasados/len(pedidos))*100, 2)}%")

def listar_pedidos_por_estado(estado_consultado):
    """Filtra y extrae el historial de ventas por el estado solicitado."""
    pedidos = _cargar_json(RUTA_PEDIDOS)
    print(f"\n📋 ÓRDENES FILTRADAS POR: [{estado_consultado.upper()}]")
    for p in pedidos:
        if p.get("estado", "").lower() == estado_consultado.lower().strip():
            print(f"ID: {p['id_pedido']} | Cliente: {p['cliente_nombre']} | Total: S/. {p['total']:.2f}")

def calcular_ingresos_totales_acumulados():
    """Auditoría contable del flujo de caja (solo toma órdenes entregadas con éxito)."""
    pedidos = _cargar_json(RUTA_PEDIDOS)
    ingresos = sum(float(p.get("total", 0.0)) for p in pedidos if p.get("estado") == "Entregado")
    print(f"\n💰 REPORTE FINANCIERO: S/. {round(ingresos, 2):.2f}")