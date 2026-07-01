import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DATA = os.path.join(BASE_DIR, "datos", "productos.json")

def cargar_productos():
    """Carga los productos del JSON."""
    try:
        with open(RUTA_DATA, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def guardar_productos(productos):
    """Guarda los productos asegurando la creación automática de la carpeta."""
    directorio = os.path.dirname(RUTA_DATA)
    os.makedirs(directorio, exist_ok=True)
        
    with open(RUTA_DATA, "w", encoding="utf-8") as archivo:
        json.dump(productos, archivo, indent=4, ensure_ascii=False)
    return True

def verificar_stock(lista_productos_solicitados):
    """Compara las cantidades pedidas contra las disponibles en almacén."""
    productos_db = cargar_productos()
    for item in lista_productos_solicitados:
        codigo_p = item["producto"].upper()
        cantidad_solicitada = item["cantidad"]
        if codigo_p not in productos_db or productos_db[codigo_p]["cantidad"] < cantidad_solicitada:
            return False
    return True

def descontar_stock(lista_productos_solicitados):
    """Disminuye las unidades vendidas de nuestro inventario central."""
    productos_db = cargar_productos()
    for item in lista_productos_solicitados:
        codigo_p = item["producto"].upper()
        if codigo_p in productos_db:
            box = productos_db[codigo_p]
            # Soporta tanto llaves antiguas como nuevas de datos
            cant_actual = box.get("cantidad", box.get("stock", 0))
            box["cantidad"] = cant_actual - item["cantidad"]
    guardar_productos(productos_db)
    return True

def agregar_stock(id_producto, quantity):
    """Permite registrar ingresos de nuevos lotes de proveedores."""
    id_producto = id_producto.upper()
    if quantity <= 0: return False
    productos_db = cargar_productos()
    if id_producto in productos_db:
        box = productos_db[id_producto]
        cant_actual = box.get("cantidad", box.get("stock", 0))
        box["cantidad"] = cant_actual + quantity
        guardar_productos(productos_db)
        print(f"\n[+] Stock actualizado para '{productos_db[id_producto]['nombre']}'.")
        return True
    return False

def ver_inventario():
    """Muestra de forma bonita y tabulada todo el stock actual."""
    productos_db = cargar_productos()
    print("\n" + "="*85)
    print(f"{'CÓDIGO':<10} | {'DESCRIPCIÓN DEL PRODUCTO':<35} | {'STOCK REAL':<12} | {'PRECIO UNIT.':<12}")
    print("="*85)
    for cod, info in productos_db.items():
        cant = info.get("cantidad", info.get("stock", 0))
        prec = info.get("precio", info.get("precio_unitario", 0.0))
        print(f"{cod:<10} | {info['nombre']:<35} | {cant:<12} | S/. {prec:.2f}")
    print("="*85)