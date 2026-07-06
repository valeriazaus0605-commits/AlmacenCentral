import os
from modulos import pedidos
from modulos import stock
from modulos import despacho
from modulos import reportes

def limpiar_pantalla():
    # Limpia la pantalla de la consola según el sistema operativo
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    while True:
        limpiar_pantalla()
        print("==============================================")
        print("   SISTEMA DE GESTIÓN 'EL ALMACÉN CENTRAL'    ")
        print("==============================================")
        print("1. 📄 Gestión de Pedidos y Clientes (Estudiante 2)")
        print("2. 📦 Gestión de Inventario / Stock (Estudiante 3)")
        print("3. 🚚 Control de Despachos y Envíos (Estudiante 4)")
        print("4. 📊 Reportes y KPIs Gerenciales  (Estudiante 5)")
        print("5. ❌ Salir del Sistema")
        print("==============================================")
        
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        if opcion == "1":
            submenu_pedidos()
        elif opcion == "2":
            submenu_stock()
        elif opcion == "3":
            submenu_despacho()
        elif opcion == "4":
            submenu_reportes()
        elif opcion == "5":
            print("\nCerrando sistema. ¡Hasta luego!")
            break
        else:
            input("\n[!] Opción inválida. Presione Enter para continuar...")

def submenu_pedidos():
    while True:
        limpiar_pantalla()
        print("--- SUBMENÚ: PEDIDOS Y CLIENTES ---")
        print("1. Registrar nuevo cliente")
        print("2. Buscar datos de un cliente")
        print("3. Registrar una nueva orden de compra (Pedido)")
        print("4. Buscar orden por código ID")
        print("5. 🧾 Generar Boleta de Venta (Nueva Opción)")  # <-- Agregado
        print("6. Volver al menú principal")  # <-- Cambiado a opción 6
        
        opc = input("Seleccione una opción: ").strip()
        if opc == "1":
            dni = input("DNI/RUC del cliente: ").strip()
            nom = input("Nombre completo: ").strip()
            tel = input("Teléfono: ").strip()
            dir_c = input("Dirección de entrega: ").strip()
            pedidos.registrar_cliente(dni, nom, tel, dir_c)
            input("\nPresione Enter para continuar...")
        elif opc == "2":
            dni = input("Ingrese el DNI/RUC a buscar: ").strip()
            c = pedidos.buscar_cliente(dni)
            if c:
                print(f"\n[+] Encontrado: {c['nombre']} | Telf: {c['telefono']} | Dir: {c['direccion']}")
            else:
                print("\n[!] Cliente no registrado.")
            input("\nPresione Enter para continuar...")
        elif opc == "3":
            dni = input("DNI/RUC del cliente comprador: ").strip()
            stock.ver_inventario()
            lista_compra = []
            while True:
                print("\nEjemplos de códigos: PROD01 (Clavos), PROD04 (Taladro), PROD06 (Alicate)")
                prod = input("Código del producto a comprar (o 'FIN' para terminar): ").strip().upper()
                if prod == 'FIN': break
                try:
                    cant = int(input(f"Cantidad para {prod}: "))
                    precio = float(input(f"Precio unitario pactado para {prod}: S/. "))
                    lista_compra.append({"producto": prod, "cantidad": cant, "precio_unitario": precio})
                except ValueError:
                    print("[!] Error: Ingrese números válidos.")
            
            if lista_compra:
                id_generado = pedidos.registrar_pedido(dni, lista_compra)
                if id_generado:
                    print(f"\n[🚀] ¡ÉXITO! Orden guardada con el ID: {id_generado}")
            else:
                print("\n[!] No se agregaron productos al pedido.")
            input("\nPresione Enter para continuar...")
        elif opc == "4":
            id_p = input("Ingrese el ID de 8 caracteres del pedido: ").strip().upper()
            p = pedidos.buscar_pedido(id_p)
            if p:
                print(f"\nID: {p['id_pedido']} | Cliente: {p['cliente_nombre']} | Total: S/. {p['total']} | Estado: {p['estado']}")
                print("Productos solicitados:")
                for prod in p["productos"]:
                    print(f" -> {prod['producto']} x{prod['cantidad']}")
            else:
                print("\n[!] Pedido no encontrado.")
            input("\nPresione Enter para continuar...")
        elif opc == "5":  # ===================================================
            # LOGÍSTICA PARA LA NUEVA FUNCIÓN DE BOLETAS
            # =================================================================
            id_p = input("Ingrese el ID del pedido para facturar boleta: ").strip().upper()
            boleta_impresa = pedidos.generar_boleta_venta(id_p)
            print(boleta_impresa)  # Imprime el diseño visual directo en consola
            input("\nPresione Enter para continuar...")
        elif opc == "6":  # Cambiado a 6 para salir de este submenú
            break

def submenu_stock():
    while True:
        limpiar_pantalla()
        print("--- SUBMENÚ: CONTROL DE STOCK ---")
        print("1. Ver Inventario Completo")
        print("2. Agregar Stock (Ingreso de Proveedor)")
        print("3. Volver al menú principal")
        
        opc = input("Seleccione una opción: ").strip()
        if opc == "1":
            stock.ver_inventario()
            input("\nPresione Enter para continuar...")
        elif opc == "2":
            id_p = input("Código del producto a reabastecer (PROD01 - PROD10): ").strip().upper()
            try:
                cant = int(input("Cantidad recibida del proveedor: "))
                if stock.agregar_stock(id_p, cant):
                    print("[+] Inventario actualizado con éxito.")
                else:
                    print("[!] Error: No se pudo actualizar. Verifique el código.")
            except ValueError:
                print("[!] Error: Ingrese una cantidad entera válida.")
            input("\nPresione Enter para continuar...")
        elif opc == "3":
            break

def submenu_despacho():
    while True:
        limpiar_pantalla()
        print("--- SUBMENÚ: DESPACHO Y LOGÍSTICA ---")
        print("1. Asignar Repartidor a Pedido (Cambia a 'En Camino')")
        print("2. Actualizar Estado de Entrega Final")
        print("3. Volver al menú principal")
        
        opc = input("Seleccione una opción: ").strip()
        if opc == "1":
            id_p = input("ID del pedido a despachar: ").strip().upper()
            rep = input("Nombre del repartidor / Empresa de carga: ").strip()
            res = despacho.asignar_despacho(id_p, rep)
            print(res)
            input("\nPresione Enter para continuar...")
        elif opc == "2":
            id_p = input("ID del pedido entregado/observado: ").strip().upper()
            print("Estados posibles: [Entregado] [Retrasado] [No Entregado]")
            nuevo_est = input("Ingrese el nuevo estado: ").strip()
            res = despacho.actualizar_estado_nuevo(id_p, nuevo_est)
            print(res)
            input("\nPresione Enter para continuar...")
        elif opc == "3":
            break

def submenu_reportes():
    while True:
        limpiar_pantalla()
        print("--- SUBMENÚ: REPORTES Y KPIS ---")
        print("1. Ver Alertas de Reabastecimiento Crítico")
        print("2. Ver Tasa (%) de Pedidos Retrasados")
        print("3. Listar Pedidos por Estado")
        print("4. Ver Auditoría de Ingresos Totales (Solo Entregados)")
        print("5. Volver al menú principal")
        
        opc = input("Seleccione una opción: ").strip()
        if opc == "1":
            reportes.obtener_alertas_reabastecimiento()
            input("\nPresione Enter para continuar...")
        elif opc == "2":
            reportes.calcular_porcentaje_pedidos_retrasados()
            input("\nPresione Enter para continuar...")
        elif opc == "3":
            est = input("¿Qué estado desea filtrar? (Pendiente / En Camino / Entregado / Retrasado / No Entregado): ").strip()
            reportes.listar_pedidos_por_estado(est)
            input("\nPresione Enter para continuar...")
        elif opc == "4":
            reportes.calcular_ingresos_totales_acumulados()
            input("\nPresione Enter para continuar...")
        elif opc == "5":
            break

if __name__ == "__main__":
    menu_principal()
