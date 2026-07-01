import json
import os

RUTA_PEDIDOS = "datos/pedidos.json"

def _cargar_pedidos():
    if not os.path.exists(RUTA_PEDIDOS): return []
    with open(RUTA_PEDIDOS, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except json.JSONDecodeError: return []

def _guardar_pedidos(pedidos):
    with open(RUTA_PEDIDOS, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, indent=4, ensure_ascii=False)

def asignar_despacho(codigo_pedido, repartidor):
    """Asigna un motorizado a una orden que esté en estado 'Pendiente'."""
    codigo_pedido = codigo_pedido.upper().strip()
    pedidos = _cargar_pedidos()
    for p in pedidos:
        if p["id_pedido"] == codigo_pedido:
            if p["estado"].lower() == "pendiente":
                p.update({"estado": "En Camino", "repartidor": repartidor})
                _guardar_pedidos(pedidos)
                return f"\n[+] Pedido {codigo_pedido} asignado a {repartidor} con éxito."
            return f"\n[!] No se puede despachar. Estado actual: [{p['estado']}]."
    return f"\n[!] Pedido '{codigo_pedido}' no encontrado."

def actualizar_estado_nuevo(codigo_pedido, nuevo_estado):
    """Modifica el tracking de entrega y exige motivo si la entrega falló."""
    codigo_pedido = codigo_pedido.upper().strip()
    pedidos = _cargar_pedidos()
    for p in pedidos:
        if p["id_pedido"] == codigo_pedido:
            p["estado"] = nuevo_estado
            if nuevo_estado == "No Entregado":
                p["motivo_fallo"] = input("Ingrese la razón de la no entrega: ").strip()
            _guardar_pedidos(pedidos)
            return f"\n[+] Pedido {codigo_pedido} actualizado a '{nuevo_estado}'."
    return f"\n[!] Pedido no encontrado."