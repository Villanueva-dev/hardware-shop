from producto_crud import InMemoryProductoRepository
import os

# Instancia del repositorio que se usará en toda la aplicación.
# La lógica de negocio (main.py) no sabe cómo se guardan los datos,
# solo se comunica a través del contrato definido en ProductoRepository.
repo = InMemoryProductoRepository()

def mostrar_menu():
    """Muestra el menú principal de opciones."""
    print("\n" + "="*50)
    print("SISTEMA DE GESTIÓN DE INVENTARIO - TECH STORE")
    print("="*50)
    print("1. 📦 Agregar producto")
    print("2. 📋 Ver todos los productos")
    print("3. 🔍 Buscar producto por ID")
    print("4. ✏️  Actualizar producto")
    print("5. 🗑️  Eliminar producto")
    print("6. 📄 Exportar inventario a archivo")
    print("7. 🟡 Consultar productos con stock bajo.")
    print("8. 🚪 Salir")
    print("="*50)

def main():
    """Función principal que ejecuta el sistema de inventario."""
    while True:
        mostrar_menu()
        
        opcion = input("Seleccione una opción (1-7): ").strip()
        
        # Limpiar pantalla después de seleccionar opción
        os.system("cls" if os.name == "nt" else "clear")

        if opcion == "1":
            print("📦 AGREGAR NUEVO PRODUCTO")
            print("-" * 30)
            nombre = input("Nombre del producto: ").strip()
            if not nombre:
                print("❌ El nombre no puede estar vacío.")
                continue
                
            try:
                precio = float(input("Precio del producto ($): "))
                stock = int(input("Cantidad en stock: "))
                if precio < 0 or stock < 0:
                    print("❌ El precio y stock deben ser valores positivos.")
                    continue
                
                nuevo_producto_data = {"nombre": nombre, "precio": precio, "stock": stock}
                producto_creado = repo.create(nuevo_producto_data)
                print(f"✅ Producto agregado con ID {producto_creado['id']}: {producto_creado['nombre']}")

            except ValueError:
                print("❌ Por favor ingrese valores numéricos válidos.")
            
        elif opcion == "2":
            print("\n📦 INVENTARIO COMPLETO:")
            print("-" * 60)
            productos = repo.get_all()
            if not productos:
                print("No hay productos en la base de datos.")
            else:
                for p in productos:
                    estado_stock = ""
                    if p['stock'] == 0:
                        estado_stock = "🔴 SIN STOCK"
                    elif p['stock'] <= 5:
                        estado_stock = "🟡 STOCK BAJO"
                    else:
                        estado_stock = "🟢 STOCK OK"
                    print(f"ID: {p['id']} | {p['nombre']} | Precio: ${p['precio']} | Stock: {p['stock']} | {estado_stock}")
            print("-" * 60)
            
        elif opcion == "3":
            print("🔍 BUSCAR PRODUCTO")
            print("-" * 30)
            try:
                id_producto = int(input("ID del producto a buscar: "))
                producto = repo.get_by_id(id_producto)
                if producto:
                    print("\n📋 DETALLE DEL PRODUCTO:")
                    print(f"ID: {producto['id']}")
                    print(f"Nombre: {producto['nombre']}")
                    print(f"Precio: ${producto['precio']}")
                    print(f"Stock: {producto['stock']} unidades")
                else:
                    print("❌ Producto no encontrado.")
            except ValueError:
                print("❌ Por favor ingrese un ID numérico válido.")
            
        elif opcion == "4":
            print("✏️  ACTUALIZAR PRODUCTO")
            print("-" * 30)
            try:
                id_producto = int(input("ID del producto a actualizar: "))
                producto_existente = repo.get_by_id(id_producto)

                if not producto_existente:
                    print("❌ Producto no encontrado.")
                    continue

                print("\n💡 Deje en blanco los campos que no desea cambiar:")
                nuevo_nombre = input(f"Nuevo nombre (actual: {producto_existente['nombre']}): ").strip() or producto_existente['nombre']
                
                precio_input = input(f"Nuevo precio (actual: {producto_existente['precio']}): ").strip()
                nuevo_precio = float(precio_input) if precio_input else producto_existente['precio']
                
                stock_input = input(f"Nuevo stock (actual: {producto_existente['stock']}): ").strip()
                nuevo_stock = int(stock_input) if stock_input else producto_existente['stock']
                
                if nuevo_precio < 0 or nuevo_stock < 0:
                    print("❌ El precio y el stock no pueden ser negativos.")
                    continue
                    
                datos_actualizados = {"nombre": nuevo_nombre, "precio": nuevo_precio, "stock": nuevo_stock}
                repo.update(id_producto, datos_actualizados)
                print("✅ Producto actualizado correctamente.")

            except ValueError:
                print("❌ Por favor ingrese valores numéricos válidos.")
            
        elif opcion == "5":
            print("🗑️  ELIMINAR PRODUCTO")
            print("-" * 30)
            try:
                id_producto = int(input("ID del producto a eliminar: "))
                if repo.delete(id_producto):
                    print("✅ Producto eliminado correctamente.")
                else:
                    print("❌ Producto no encontrado.")
            except ValueError:
                print("❌ Por favor ingrese un ID numérico válido.")
            
        elif opcion == "6":
            print("📄 EXPORTAR INVENTARIO")
            print("-" * 30)
            nombre_archivo = input("Nombre del archivo (sin extensión): ").strip()
            if not nombre_archivo:
                print("❌ El nombre del archivo no puede estar vacío.")
                continue
            
            exportar_directory = "exports-txt"
            os.makedirs(exportar_directory, exist_ok=True)
            filepath = os.path.join(exportar_directory, f"{nombre_archivo}.txt")

            try:
                with open(filepath, "w", encoding="utf-8") as archivo:
                    archivo.write("REPORTE DE INVENTARIO\n")
                    archivo.write("=" * 50 + "\n\n")
                    productos = repo.get_all()
                    for p in productos:
                        linea = f"ID: {p['id']} | {p['nombre']} | Precio: ${p['precio']} | Stock: {p['stock']}\n"
                        archivo.write(linea)
                print(f"✅ Productos exportados correctamente a {filepath}")
            except Exception as e:
                print(f"❌ Error al exportar productos: {e}")
                
        elif opcion == "7":
            productos = repo.get_all()
            
            if not productos:
                print("No hay productos en la base de datos.")
            else:
                productos_stock_bajo = repo.get_by_low_stock()
                
                if not productos_stock_bajo:
                    print("🟡 CONSULTAR PRODUCTOS CON STOCK BAJO (<5 unidades)")
                    print("-" * 60)
                    print("\tNo hay productos con stock bajo 👌🏼")
                else:
                    print("🟡 CONSULTAR PRODUCTOS CON STOCK BAJO (<5 unidades)")
                    print("-" * 60)
                    for producto in productos_stock_bajo:
                        estado_stock = ""
                        if producto['stock'] == 0:
                            estado_stock = "🔴 SIN STOCK"
                        elif producto['stock'] <= 5:
                            estado_stock = "🟡 STOCK BAJO"
                        print(f"ID: {producto['id']} | {producto['nombre']} | Precio: ${producto['precio']} | Stock: {producto['stock']} | {estado_stock}")
                    print("-" * 60)

        elif opcion == "8":
            print("¡Gracias por usar el Sistema de Inventario!")
            print("🔒 Cerrando aplicación...")
            break
            
        else:
            print("❌ Opción no válida. Por favor seleccione una opción del 1 al 7.")
            
        # Pausa para que el usuario pueda leer el resultado
        input("\n📱 Presione Enter para continuar...")
        os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    main()