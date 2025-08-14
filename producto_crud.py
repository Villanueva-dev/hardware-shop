import logging
from typing import List, Dict, Any
from repositorio import ProductoRepository
import os

# --- Configuración del Logger ---
logging.basicConfig(
    filename='operaciones.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# --- Datos en Memoria ---
# Esta sección simula una base de datos en memoria utilizando una lista de diccionarios.
# Es privada para este módulo y solo se accede a través de la clase InMemoryProductoRepository.
_fake_db: List[Dict[str, Any]] = [
    {"id": 1, "nombre": "NVIDIA RTX 4070", "precio": 599.99, "stock": 12},
    {"id": 2, "nombre": "AMD Ryzen 7 7700X", "precio": 349.99, "stock": 8},
    {"id": 3, "nombre": "Corsair Vengeance DDR5 32GB", "precio": 199.99, "stock": 15},
    {"id": 4, "nombre": "ASUS ROG Strix B650-E", "precio": 299.99, "stock": 3},
    {"id": 5, "nombre": "Monitor Samsung Odyssey G7 27\"", "precio": 449.99, "stock": 0},
    {"id": 6, "nombre": "Teclado Mecánico Logitech G Pro X", "precio": 129.99, "stock": 25}
]
_id_counter = 7

class InMemoryProductoRepository(ProductoRepository):
    """Implementación del repositorio de productos que usa una lista en memoria."""

    def get_all(self) -> List[Dict[str, Any]]:
        """Devuelve todos los productos."""
        logging.info(f"Consulta de la lista completa de productos. Total: {len(_fake_db)} productos")
        return _fake_db

    def get_by_id(self, id_producto: int) -> Dict[str, Any] | None:
        """Busca un producto por su ID."""
        logging.info(f"Buscando producto con ID: {id_producto}")
        for producto in _fake_db:
            if producto["id"] == id_producto:
                return producto
        logging.warning(f"Intento de obtener producto no existente con ID: {id_producto}")
        return None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo producto y lo añade a la base de datos en memoria."""
        global _id_counter
        nuevo_producto = {"id": _id_counter, **data}
        _fake_db.append(nuevo_producto)
        logging.info(f"Producto agregado con ID {_id_counter}: {nuevo_producto}")
        _id_counter += 1
        return nuevo_producto

    def update(self, id_producto: int, data: Dict[str, Any]) -> Dict[str, Any] | None:
        """Actualiza un producto existente."""
        producto = self.get_by_id(id_producto)
        if producto:
            datos_anteriores = producto.copy()
            producto.update(data)
            logging.info(f"Producto con ID {id_producto} actualizado. Datos anteriores: {datos_anteriores}. Datos nuevos: {producto}")
            return producto
        logging.warning(f"Intento de actualizar producto no existente con ID: {id_producto}")
        return None

    def delete(self, id_producto: int) -> bool:
        """Elimina un producto de la base de datos."""
        producto = self.get_by_id(id_producto)
        if producto:
            logging.info(f"Producto eliminado con ID {id_producto}: {producto}")
            _fake_db.remove(producto)
            return True
        logging.warning(f"Intento de eliminar producto no existente con ID: {id_producto}")
        return False

    def get_by_low_stock(self) -> List[Dict[str, Any]]:
        """Muestra los productos con Stock bajo (< 5 unds)."""
        productos_stock_bajo = []
        
        for producto in _fake_db:
            if producto.get("stock") <= 5:
                productos_stock_bajo.append(producto)
                logging.info(f"Producto con stock bajo: {producto}")
                
        if not productos_stock_bajo:
            logging.info(f"No hay productos con 5 o menos unidades en stock.")
            
        return productos_stock_bajo