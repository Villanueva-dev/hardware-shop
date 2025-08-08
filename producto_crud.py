import logging

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

fake_db : dict[int, Producto] = {}
id_counter = 1

def agregar_producto(nombre_producto, precio, stock=0):
    """
    Agrega un nuevo producto a la base de datos en memoria.
    Registra la operación en el log.
    """
    global id_counter
    producto = Producto(nombre_producto, precio, stock)
    fake_db[id_counter] = producto
    # Se registra la creación del producto, incluyendo el ID asignado.
    logging.info(f"Producto agregado con ID {id_counter}: {producto.nombre}, Precio: {producto.precio}, Stock: {producto.stock}")
    print(f"Producto agregado: {producto.nombre}")
    id_counter += 1
    
def eliminar_producto(id_producto):
    """
    Elimina un producto de la base de datos usando su ID.
    Registra la operación o el intento fallido en el log.
    """
    if id_producto in fake_db:
        producto = fake_db.pop(id_producto)
        # Se registra la eliminación del producto.
        logging.info(f"Producto eliminado con ID {id_producto}: {producto.nombre}")
        print(f"Producto eliminado: {producto.nombre}")
    else:
        # Se registra un intento de eliminación de un producto que no existe.
        logging.warning(f"Intento de eliminar producto no existente con ID: {id_producto}")
        print("Producto no encontrado.")
        
def leer_productos():
    """
    Muestra todos los productos en la base de datos.
    Registra la consulta en el log.
    """
    if not fake_db:
        # Se registra que se intentó leer pero no había productos.
        logging.info("Se consultó la lista de productos, pero la base de datos está vacía.")
        print("No hay productos en la base de datos.")
    else:
        # Se registra que se ha accedido a la lista completa de productos.
        logging.info("Consulta de la lista completa de productos.")
        for id_producto, producto in fake_db.items():
            print(f"ID: {id_producto}, Producto: {producto}")
            
def leer_producto(id_producto):
    """
    Busca y muestra un producto específico por su ID.
    Registra la consulta o el intento fallido en el log.
    """
    if id_producto in fake_db:
        producto = fake_db[id_producto]
        # Se registra la consulta de un producto específico.
        logging.info(f"Consulta del producto con ID {id_producto}: {producto.nombre}")
        print(f"Producto encontrado: {producto}")
    else:
        # Se registra un intento de consulta de un producto que no existe.
        logging.warning(f"Intento de leer producto no existente con ID: {id_producto}")
        print("Producto no encontrado.")
        
def actualizar_producto(id_producto, nuevo_nombre, nuevo_precio):
    """
    Actualiza el nombre y el precio de un producto existente.
    Registra la actualización con los datos antiguos y nuevos para auditoría.
    """
    if id_producto in fake_db:
        producto = fake_db[id_producto]
        # Se registra la actualización, guardando el estado anterior para auditoría.
        logging.info(
            f"Producto con ID {id_producto} actualizado. "
            f"Datos anteriores: (Nombre: '{producto.nombre}', Precio: '{producto.precio}'). "
            f"Datos nuevos: (Nombre: '{nuevo_nombre}', Precio: '{nuevo_precio}')"
        )
        producto.nombre = nuevo_nombre
        producto.precio = nuevo_precio
        print(f"Producto actualizado: {producto}")
    else:
        # Se registra un intento de actualización de un producto que no existe.
        logging.warning(f"Intento de actualizar producto no existente con ID: {id_producto}")
        print("Producto no encontrado.")