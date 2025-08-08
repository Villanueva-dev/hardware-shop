import logging
import os

# --- Configuración del Logger ---
# Se configura el sistema de logging para que registre los eventos en un archivo.
# - filename: 'operaciones.log' es el archivo donde se guardarán los logs.
# - level: logging.INFO indica que se registrarán todos los mensajes de nivel INFO y superiores (WARNING, ERROR, CRITICAL).
# - format: Define el formato de cada línea de log.
#   - %(asctime)s: Fecha y hora del evento.
#   - %(levelname)s: Nivel del log (ej. INFO, WARNING).
#   - %(message)s: El mensaje del log.
# - encoding: 'utf-8' para asegurar que los caracteres especiales se guarden correctamente.
logging.basicConfig(
    filename='operaciones.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

class Producto:
    def __init__(self, nombre:str, precio:str, stock:int=0):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        
    def __str__(self):
        return f"{self.nombre} - Precio: ${self.precio} - Stock: {self.stock}"

fake_db : dict[int, Producto] = {
    1: Producto("NVIDIA RTX 4070", "599.99", 12),
    2: Producto("AMD Ryzen 7 7700X", "349.99", 8),
    3: Producto("Corsair Vengeance DDR5 32GB", "199.99", 15),
    4: Producto("ASUS ROG Strix B650-E", "299.99", 3),
    5: Producto("Monitor Samsung Odyssey G7 27\"", "449.99", 0),
    6: Producto("Teclado Mecánico Logitech G Pro X", "129.99", 25)
}
id_counter = 7  # Empezar desde 7 para nuevos productos

def agregar_producto(nombre_producto, precio, stock):
    """
    Agrega un nuevo producto a la base de datos en memoria.
    Requiere especificar la cantidad de stock inicial.
    Registra la operación en el log.
    """
    global id_counter
    producto = Producto(nombre_producto, precio, stock)
    fake_db[id_counter] = producto
    # Se registra la creación del producto, incluyendo el ID asignado.
    logging.info(f"Producto agregado con ID {id_counter}: {producto.nombre}, Precio: {producto.precio}, Stock: {producto.stock}")
    print(f"Producto agregado: {producto.nombre} - Stock: {producto.stock} unidades")
    id_counter += 1
    
def eliminar_producto(id_producto):
    """
    Elimina un producto de la base de datos usando su ID.
    Muestra advertencia si el producto tiene stock > 0.
    Registra la operación o el intento fallido en el log.
    """
    if id_producto in fake_db:
        producto = fake_db[id_producto]
        
        # Verificar si el producto tiene stock antes de eliminar
        if producto.stock > 0:
            # Advertencia al gerente sobre pérdida de inventario
            print(f"⚠️  ADVERTENCIA: El producto '{producto.nombre}' tiene {producto.stock} unidades en stock.")
            confirmacion = input("¿Está seguro de que desea eliminarlo? Esto resultará en pérdida de inventario. (s/n): ").lower()
            
            if confirmacion != 's':
                logging.info(f"Eliminación cancelada para producto con ID {id_producto}: {producto.nombre} (Stock: {producto.stock})")
                print("❌ Eliminación cancelada.")
                return
        
        # Proceder con la eliminación
        producto_eliminado = fake_db.pop(id_producto)
        # Se registra la eliminación del producto con información completa.
        logging.info(f"Producto eliminado con ID {id_producto}: {producto_eliminado.nombre}, Stock perdido: {producto_eliminado.stock} unidades")
        print(f"✅ Producto eliminado: {producto_eliminado.nombre} - Stock eliminado: {producto_eliminado.stock} unidades")
    else:
        # Se registra un intento de eliminación de un producto que no existe.
        logging.warning(f"Intento de eliminar producto no existente con ID: {id_producto}")
        print("❌ Producto no encontrado.")
        
def leer_productos():
    """
    Muestra todos los productos en la base de datos incluyendo información de stock.
    Registra la consulta en el log.
    """
    if not fake_db:
        # Se registra que se intentó leer pero no había productos.
        logging.info("Se consultó la lista de productos, pero la base de datos está vacía.")
        print("No hay productos en la base de datos.")
    else:
        # Se registra que se ha accedido a la lista completa de productos.
        logging.info(f"Consulta de la lista completa de productos. Total: {len(fake_db)} productos")
        print("\n📦 INVENTARIO COMPLETO:")
        print("-" * 60)
        for id_producto, producto in fake_db.items():
            # Mostrar indicador visual del estado del stock
            if producto.stock == 0:
                estado_stock = "🔴 SIN STOCK"
            elif producto.stock <= 5:
                estado_stock = "🟡 STOCK BAJO"
            else:
                estado_stock = "🟢 STOCK OK"
            
            print(f"ID: {id_producto} | {producto} | {estado_stock}")
        print("-" * 60)
            
def leer_producto(id_producto):
    """
    Busca y muestra un producto específico por su ID incluyendo información detallada de stock.
    Registra la consulta o el intento fallido en el log.
    """
    if id_producto in fake_db:
        producto = fake_db[id_producto]
        # Se registra la consulta de un producto específico.
        logging.info(f"Consulta del producto con ID {id_producto}: {producto.nombre}, Stock actual: {producto.stock}")
        
        # Mostrar información detallada del producto
        print(f"\n📋 DETALLE DEL PRODUCTO:")
        print(f"ID: {id_producto}")
        print(f"Nombre: {producto.nombre}")
        print(f"Precio: ${producto.precio}")
        print(f"Stock: {producto.stock} unidades")
        
        # Análisis del stock
        if producto.stock == 0:
            print("⚠️  Estado: SIN STOCK - ¡Necesita reabastecimiento urgente!")
        elif producto.stock <= 5:
            print("⚠️  Estado: STOCK BAJO - Considere realizar pedido")
        else:
            print("✅ Estado: Stock suficiente")
            
    else:
        # Se registra un intento de consulta de un producto que no existe.
        logging.warning(f"Intento de leer producto no existente con ID: {id_producto}")
        print("❌ Producto no encontrado.")
        
def actualizar_producto(id_producto, nuevo_nombre=None, nuevo_precio=None, nuevo_stock=None):
    """
    Actualiza el nombre, precio y/o stock de un producto existente.
    Registra la actualización con los datos antiguos y nuevos para auditoría.
    """
    if id_producto in fake_db:
        producto = fake_db[id_producto]
        
        # Guardar valores anteriores para el log
        datos_anteriores = {
            'nombre': producto.nombre,
            'precio': producto.precio,
            'stock': producto.stock
        }
        
        # Actualizar solo los campos que se proporcionaron
        if nuevo_nombre is not None:
            producto.nombre = nuevo_nombre
        if nuevo_precio is not None:
            producto.precio = nuevo_precio
        if nuevo_stock is not None:
            producto.stock = nuevo_stock
        
        # Determinar qué campos se actualizaron para el log
        cambios = []
        if nuevo_nombre is not None:
            cambios.append(f"Nombre: '{datos_anteriores['nombre']}' → '{producto.nombre}'")
        if nuevo_precio is not None:
            cambios.append(f"Precio: '{datos_anteriores['precio']}' → '{producto.precio}'")
        if nuevo_stock is not None:
            cambios.append(f"Stock: {datos_anteriores['stock']} → {producto.stock} unidades")
        
        # Se registra la actualización con los cambios específicos.
        logging.info(f"Producto con ID {id_producto} actualizado. Cambios: {' | '.join(cambios)}")
        print(f"✅ Producto actualizado: {producto}")
        
        # Alerta si el stock queda bajo
        if producto.stock <= 5 and producto.stock > 0:
            print("⚠️  Advertencia: El stock está bajo, considere realizar un pedido.")
        elif producto.stock == 0:
            print("⚠️  Advertencia: ¡El producto se ha quedado sin stock!")
            
    else:
        # Se registra un intento de actualización de un producto que no existe.
        logging.warning(f"Intento de actualizar producto no existente con ID: {id_producto}")
        print("❌ Producto no encontrado.")
        
def exportar_productos_txt(nombre_archivo:str):
    """
    Exporta todos los productos de la base de datos a un archivo de texto.
    Registra la operación de exportación en el log.
    """
    # Salir si no hay productos creados
    if not fake_db:
        # Se registra que se intentó exportar pero no había productos.
        logging.warning("Intento de exportar productos: no hay productos en el inventario.")
        print("No hay productos en el inventario")
        return

    # Crear directorio dentro del proyecto, si no existe
    exportar_directory = "exports-txt"
    os.makedirs(exportar_directory, exist_ok=True)

    # Ruta donde se guardara el archivo exportado
    filepath = os.path.join(exportar_directory, f"{nombre_archivo}.txt")

    try:
        # Generar el archivo txt con los datos existentes en fake_db
        with open(filepath, "w", encoding="utf-8") as archivo:
            archivo.write("REPORTE DE INVENTARIO\n")
            archivo.write("=" * 50 + "\n\n")
            for id_producto, producto in fake_db.items():
                estado_stock = ""
                if producto.stock == 0:
                    estado_stock = " [SIN STOCK]"
                elif producto.stock <= 5:
                    estado_stock = " [STOCK BAJO]"
                
                linea = f"ID: {id_producto} | {producto.nombre} | Precio: ${producto.precio} | Stock: {producto.stock} unidades{estado_stock}\n"
                archivo.write(linea)
        # Se registra la exportación exitosa con detalles del archivo y cantidad de productos.
        logging.info(f"Productos exportados exitosamente. Archivo: '{filepath}', Cantidad de productos: {len(fake_db)}")
        print(f"✅ Productos exportados correctamente a {filepath}")
    except Exception as e:
        # Se registra cualquier error que ocurra durante la exportación.
        logging.error(f"Error al exportar productos al archivo '{filepath}': {e}")
        print(f"❌ Error al exportar productos: {e}")

# Demostración cuando se ejecuta directamente
if __name__ == "__main__":
    print("\n🏪 SISTEMA DE GESTIÓN DE INVENTARIO")
    print("=" * 50)
    print("📦 Productos precargados en el sistema:")
    leer_productos()
    
    print("\n💡 Para usar el sistema completo, ejecute: python main.py")
    print("=" * 50)