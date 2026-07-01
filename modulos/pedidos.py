import json
import uuid
import os

# Definimos dónde se guardarán los archivos de datos
RUTA_CLIENTES = "datos/clientes.json"
RUTA_PEDIDOS = "datos/pedidos.json"

def _cargar_json(ruta_archivo):
    """Lee archivos JSON. Si no existen, devuelve un diccionario o lista vacía."""
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si busca clientes devuelve diccionario {}, si busca pedidos devuelve lista []
        return {} if "clientes" in ruta_archivo else []

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