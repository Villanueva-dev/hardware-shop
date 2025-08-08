from producto_crud import agregar_producto, leer_productos, eliminar_producto, leer_producto, actualizar_producto, exportar_productos_txt
import os

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
    print("7. 🚪 Salir")
    print("="*50)

def main():
    """Función principal que ejecuta el sistema de inventario."""
    # Los productos están precargados directamente en fake_db
    
    while True:
        mostrar_menu()
        
        try:
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
                    agregar_producto(nombre, precio, stock)
                except ValueError:
                    print("❌ Por favor ingrese valores numéricos válidos.")
                
            elif opcion == "2":
                leer_productos()
                
            elif opcion == "3":
                print("🔍 BUSCAR PRODUCTO")
                print("-" * 30)
                try:
                    id_producto = int(input("ID del producto a buscar: "))
                    leer_producto(id_producto)
                except ValueError:
                    print("❌ Por favor ingrese un ID numérico válido.")
                
            elif opcion == "4":
                print("✏️  ACTUALIZAR PRODUCTO")
                print("-" * 30)
                try:
                    id_producto = int(input("ID del producto a actualizar: "))
                    
                    print("\n💡 Deje en blanco los campos que no desea cambiar:")
                    nuevo_nombre = input("Nuevo nombre (actual se mantiene si vacío): ").strip() or None
                    
                    precio_input = input("Nuevo precio (actual se mantiene si vacío): ").strip()
                    nuevo_precio = float(precio_input) if precio_input else None
                    
                    stock_input = input("Nuevo stock (actual se mantiene si vacío): ").strip()
                    nuevo_stock = int(stock_input) if stock_input else None
                    
                    if nuevo_precio is not None and nuevo_precio < 0:
                        print("❌ El precio debe ser positivo.")
                        continue
                    if nuevo_stock is not None and nuevo_stock < 0:
                        print("❌ El stock debe ser positivo.")
                        continue
                        
                    actualizar_producto(id_producto, nuevo_nombre, nuevo_precio, nuevo_stock)
                except ValueError:
                    print("❌ Por favor ingrese valores numéricos válidos.")
                
            elif opcion == "5":
                print("🗑️  ELIMINAR PRODUCTO")
                print("-" * 30)
                try:
                    id_producto = int(input("ID del producto a eliminar: "))
                    eliminar_producto(id_producto)
                except ValueError:
                    print("❌ Por favor ingrese un ID numérico válido.")
                
            elif opcion == "6":
                print("📄 EXPORTAR INVENTARIO")
                print("-" * 30)
                nombre_archivo = input("Nombre del archivo (sin extensión): ").strip()
                if not nombre_archivo:
                    print("❌ El nombre del archivo no puede estar vacío.")
                    continue
                exportar_productos_txt(nombre_archivo)

            elif opcion == "7":
                print("¡Gracias por usar el Sistema de Inventario!")
                print("🔒 Cerrando aplicación...")
                break
            
            else:
                print("❌ Opción no válida. Por favor seleccione una opción del 1 al 7.")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Aplicación cerrada por el usuario!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            
        # Pausa para que el usuario pueda leer el resultado
        input("\n📱 Presione Enter para continuar...")
        os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    main()