from postgres_repository import PostgresProductoRepository
import os
import logging
import sys

# --- Configuración del Logger ---
# Configura el logger para que escriba en un archivo y también en la consola.
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file_handler = logging.FileHandler('operaciones.log', encoding='utf-8')
log_file_handler.setFormatter(log_formatter)
log_console_handler = logging.StreamHandler(sys.stdout)
log_console_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_file_handler)
logger.addHandler(log_console_handler)

def inicializar_repositorio():
    """Inicializa el repositorio de productos y maneja errores de conexión."""
    try:
        return PostgresProductoRepository()
    except ConnectionError as e:
        logger.error(f"CRÍTICO: No se pudo conectar a la base de datos. {e}")
        print("Error fatal: No se pudo establecer la conexión con la base de datos.")
        print("Por favor, verifique la configuración y que el servicio de PostgreSQL esté en ejecución.")
        sys.exit(1) # Termina la aplicación si no hay conexión

# Instancia del repositorio que se usará en toda la aplicación.
repo = inicializar_repositorio()

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
        
        opcion = input("Seleccione una opción (1-8): ").strip()
        
        # Limpiar pantalla después de seleccionar opción
        os.system("cls" if os.name == "nt" else "clear")

        if opcion == "1":
            print("📦 AGREGAR NUEVO PRODUCTO")
            print("-" * 30)
            nombre = input("Nombre del producto: ").strip()
            if not nombre:
                logger.warning("Intento de crear producto con nombre vacío.")
                print("❌ El nombre no puede estar vacío.")
                continue
                
            try:
                precio = float(input("Precio del producto ($): "))
                stock = int(input("Cantidad en stock: "))
                if precio < 0 or stock < 0:
                    logger.warning(f"Intento de crear producto con valores negativos: Precio {precio}, Stock {stock}")
                    print("❌ El precio y stock deben ser valores positivos.")
                    continue
                
                nuevo_producto_data = {"nombre": nombre, "precio": precio, "stock": stock}
                producto_creado = repo.create(nuevo_producto_data)
                if producto_creado:
                    logger.info(f"Producto agregado con ID {producto_creado['id']}: {producto_creado['nombre']}")
                    print(f"✅ Producto agregado con ID {producto_creado['id']}: {producto_creado['nombre']}")
                else:
                    logger.error("No se pudo crear el producto en la base de datos.")
                    print("❌ Error: No se pudo crear el producto.")

            except ValueError:
                logger.error("Error de valor al agregar producto: entrada no válida.")
                print("❌ Por favor ingrese valores numéricos válidos para precio y stock.")
            
        elif opcion == "2":
            print("\n📦 INVENTARIO COMPLETO:")
            print("-" * 60)
            try:
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
                        print(f"ID: {p['id']} | {p['nombre']} | Precio: ${p['precio']:.2f} | Stock: {p['stock']} | {estado_stock}")
                print("-" * 60)
            except Exception as e:
                logger.error(f"Error al obtener todos los productos: {e}")
                print("❌ Ocurrió un error al consultar el inventario.")
            
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
                    print(f"Precio: ${producto['precio']:.2f}")
                    print(f"Stock: {producto['stock']} unidades")
                else:
                    print("❌ Producto no encontrado.")
            except ValueError:
                logger.warning("Entrada no válida para buscar producto por ID.")
                print("❌ Por favor ingrese un ID numérico válido.")
            except Exception as e:
                logger.error(f"Error al buscar producto por ID: {e}")
                print("❌ Ocurrió un error al buscar el producto.")
            
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
                    logger.warning(f"Intento de actualizar con valores negativos para ID {id_producto}.")
                    print("❌ El precio y el stock no pueden ser negativos.")
                    continue
                    
                datos_actualizados = {"nombre": nuevo_nombre, "precio": nuevo_precio, "stock": nuevo_stock}
                producto_actualizado = repo.update(id_producto, datos_actualizados)
                if producto_actualizado:
                    logger.info(f"Producto ID {id_producto} actualizado.")
                    print("✅ Producto actualizado correctamente.")
                else:
                    logger.error(f"No se pudo actualizar el producto con ID {id_producto}.")
                    print("❌ Error: No se pudo actualizar el producto.")

            except ValueError:
                logger.warning("Error de valor al actualizar producto.")
                print("❌ Por favor ingrese valores numéricos válidos para precio y stock.")
            except Exception as e:
                logger.error(f"Error inesperado al actualizar producto: {e}")
                print("❌ Ocurrió un error inesperado al actualizar.")
            
        elif opcion == "5":
            print("🗑️  ELIMINAR PRODUCTO")
            print("-" * 30)
            try:
                id_producto = int(input("ID del producto a eliminar: "))
                if repo.delete(id_producto):
                    logger.info(f"Producto con ID {id_producto} eliminado.")
                    print("✅ Producto eliminado correctamente.")
                else:
                    logger.warning(f"Intento de eliminar producto no existente con ID {id_producto}.")
                    print("❌ Producto no encontrado o no se pudo eliminar.")
            except ValueError:
                logger.warning("Entrada no válida para eliminar producto.")
                print("❌ Por favor ingrese un ID numérico válido.")
            except Exception as e:
                logger.error(f"Error al eliminar producto: {e}")
                print("❌ Ocurrió un error al eliminar el producto.")
            
        elif opcion == "6":
            print("📄 EXPORTAR INVENTARIO")
            print("-" * 30)
            nombre_archivo = input("Nombre del archivo (sin extensión): ").strip()
            if not nombre_archivo:
                logger.warning("Intento de exportar con nombre de archivo vacío.")
                print("❌ El nombre del archivo no puede estar vacío.")
                continue
            
            exportar_directory = "exports-txt"
            try:
                os.makedirs(exportar_directory, exist_ok=True)
                filepath = os.path.join(exportar_directory, f"{nombre_archivo}.txt")

                with open(filepath, "w", encoding="utf-8") as archivo:
                    archivo.write("REPORTE DE INVENTARIO\n")
                    archivo.write("=" * 50 + "\n\n")
                    productos = repo.get_all()
                    for p in productos:
                        linea = f"ID: {p['id']} | {p['nombre']} | Precio: ${p['precio']:.2f} | Stock: {p['stock']}\n"
                        archivo.write(linea)
                logger.info(f"Inventario exportado a {filepath}")
                print(f"✅ Productos exportados correctamente a {filepath}")
            except IOError as e:
                logger.error(f"Error de I/O al exportar a {filepath}: {e}")
                print(f"❌ Error al escribir en el archivo: {e}")
            except Exception as e:
                logger.error(f"Error inesperado al exportar productos: {e}")
                print(f"❌ Error inesperado al exportar productos: {e}")
                
        elif opcion == "7":
            print("🟡 CONSULTAR PRODUCTOS CON STOCK BAJO (<5 unidades)")
            print("-" * 60)
            try:
                productos_stock_bajo = repo.get_by_low_stock()
                
                if not productos_stock_bajo:
                    print("\tNo hay productos con stock bajo 👌🏼")
                else:
                    for producto in productos_stock_bajo:
                        estado_stock = "🔴 SIN STOCK" if producto['stock'] == 0 else "🟡 STOCK BAJO"
                        print(f"ID: {producto['id']} | {producto['nombre']} | Precio: ${producto['precio']:.2f} | Stock: {producto['stock']} | {estado_stock}")
                print("-" * 60)
            except Exception as e:
                logger.error(f"Error al consultar productos con stock bajo: {e}")
                print("❌ Ocurrió un error al realizar la consulta.")

        elif opcion == "8":
            print("¡Gracias por usar el Sistema de Inventario!")
            logger.info("Cerrando aplicación.")
            print("🔒 Cerrando aplicación...")
            break
            
        else:
            print("❌ Opción no válida. Por favor seleccione una opción del 1 al 8.")
            
        # Pausa para que el usuario pueda leer el resultado
        input("\n📱 Presione Enter para continuar...")
        os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    main()