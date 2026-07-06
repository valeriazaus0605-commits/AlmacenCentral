import json
import uuid
import os
from datetime import datetime  # <-- Esencial para capturar la fecha de la boleta

# Definimos dónde se guardarán los archivos de datos
RUTA_CLIENTES = "datos/clientes.json"
RUTA_PEDIDOS = "datos/pedidos.json"
RUTA_BOLETAS = "datos/boletas.json"  # <-- La nueva ruta para el historial de boletas

def _cargar_json(ruta_archivo):
    """Lee archivos JSON. Si no existen, devuelve un diccionario o lista vacía."""
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si busca clientes o boletas devuelve diccionario {}, si busca pedidos devuelve lista []
        if "pedidos" in ruta_archivo:
            return []
        return {}

def _guardar_json(ruta_archivo, datos):
    """Guarda los datos en formato JSON creando la carpeta automáticamente."""
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def registrar_cliente(dni_ruc, nombre, telefono, direccion):
    """Registra un cliente validando que el DNI/RUC no esté repetido."""
    clientes = _cargar_json(RUTA_CLIENTES)
    if dni_ruc in clientes:
        print(f"\n[!] Error: El cliente con DNI/RUC {dni_ruc} ya existe.")
        return False
    
    clientes[dni_ruc] = {"nombre": nombre, "telefono": telefono, "direccion": direccion}
    _guardar_json(RUTA_CLIENTES, clientes)
    print(f"\n[+] Cliente '{nombre}' registrado correctamente.")
    return True

def buscar_cliente(dni_ruc):
    """Busca un cliente por su DNI en el archivo."""
    clientes = _cargar_json(RUTA_CLIENTES)
    return clientes.get(dni_ruc, None)

def registrar_pedido(dni_cliente, lista_productos_solicitados):
    """Crea una orden de compra verificando primero el stock en tiempo real."""
    from . import stock # Importación interna para conectar con stock.py
    
    cliente = buscar_cliente(dni_cliente)
    if not cliente:
        print(f"\n[!] Error: El cliente {dni_cliente} no existe.")
        return None

    if not stock.verificar_stock(lista_productos_solicitados):
        print("\n[!] Pedido cancelado: No hay stock suficiente.")
        return None

    stock.descontar_stock(lista_productos_solicitados)
    
    total_pedido = sum(p["cantidad"] * p["precio_unitario"] for p in lista_productos_solicitados)
    id_pedido = str(uuid.uuid4())[:8].upper() # Genera un ID único corto de 8 dígitos

    nuevo_pedido = {
        "id_pedido": id_pedido,
        "dni_cliente": dni_cliente,
        "cliente_nombre": cliente["nombre"],
        "productos": lista_productos_solicitados,
        "total": round(total_pedido, 2),
        "estado": "Pendiente"
    }

    pedidos = _cargar_json(RUTA_PEDIDOS)
    pedidos.append(nuevo_pedido)
    _guardar_json(RUTA_PEDIDOS, pedidos)
    return id_pedido

def buscar_pedido(id_pedido):
    """Busca un pedido guardado mediante su ID único."""
    pedidos = _cargar_json(RUTA_PEDIDOS)
    for p in pedidos:
        if p["id_pedido"] == id_pedido:
            return p
    return None

# =====================================================================
# CÓDIGO AGREGADO: SISTEMA DE BOLETAS ELECTRÓNICAS (AL FINAL)
# =====================================================================

def generar_boleta_venta(id_pedido):
    """Genera, registra en JSON y formatea una boleta con IGV del 18% para impresión."""
    id_pedido = id_pedido.strip().upper()
    
    # Buscamos el pedido usando tu función existente arriba
    p = buscar_pedido(id_pedido)
    if not p:
        return f"[!] No se puede generar boleta. Pedido {id_pedido} no existe."
        
    # Obtenemos los datos extendidos del cliente (como la dirección)
    clientes = _cargar_json(RUTA_CLIENTES)
    cli = clientes.get(p["dni_cliente"], {"nombre": p["cliente_nombre"], "direccion": "No registrada"})
    
    # Cálculos económicos formales (Perú: IGV 18%)
    total = p["total"]
    subtotal = total / 1.18
    igv = total - subtotal
    
    # Cargar historial de boletas existentes para calcular el nuevo número correlativo
    boletas_db = _cargar_json(RUTA_BOLETAS)
    num_boleta = len(boletas_db) + 1
    id_boleta = f"BOL-{num_boleta:04d}"
    
    # Guardamos el registro si es una boleta nueva
    if id_boleta not in boletas_db:
        boletas_db[id_boleta] = {
            "id_pedido": id_pedido,
            "cliente": cli["nombre"],
            "fecha_emision": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "monto_total": total
        }
        _guardar_json(RUTA_BOLETAS, boletas_db)

    # Construcción del diseño visual de la boleta de texto para consola/impresión
    out = []
    out.append("\n" + "==================================================")
    out.append("         BOLETA DE VENTA ELECTRÓNICA              ")
    out.append("             'EL ALMACÉN CENTRAL'                 ")
    out.append("         RUC: 20123456789 - AREQUIPA              ")  # Ajustado a tu localidad local
    out.append("==================================================")
    out.append(f" N° COMPROBANTE: {id_boleta}")
    out.append(f" REF. PEDIDO:    {id_pedido}")
    out.append(f" Fecha Emisión:  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    out.append("--------------------------------------------------")
    out.append(f" SEÑOR(ES): {cli['nombre']}")
    out.append(f" DNI/RUC:   {p['dni_cliente']}")
    out.append(f" Dirección: {cli['direccion']}")
    out.append("--------------------------------------------------")
    out.append(f"{'CANT':<5} | {'DESCRIPCIÓN':<25} | {'SUBTOTAL':<12}")
    out.append("--------------------------------------------------")
    
    # Iteramos sobre tus productos guardados en el pedido
    for item in p["productos"]:
        sub_item = item["cantidad"] * item["precio_unitario"]
        # Buscamos 'producto' o 'nombre' según cómo guardes el texto en tu lista
        nombre_producto = item.get("producto", item.get("nombre", "Producto"))
        out.append(f"{item['cantidad']:<5} | {nombre_producto[:25]:<25} | S/. {sub_item:<10.2f}")
        
    out.append("--------------------------------------------------")
    out.append(f" SUB-TOTAL:                     S/. {subtotal:<10.2f}")
    out.append(f" IGV (18%):                     S/. {igv:<10.2f}")
    out.append(f" TOTAL A PAGAR:                 S/. {total:<10.2f}")
    out.append("==================================================")
    out.append("     ¡Gracias por su compra mayorista!           ")
    out.append("    Este documento puede ser impreso en PDF       ")
    out.append("==================================================")
    
    return "\n".join(out)
