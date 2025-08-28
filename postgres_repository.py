import psycopg2
import os
from typing import List, Dict, Any
from repositorio import ProductoRepository
import logging

# La configuración del logger se realiza en el punto de entrada de la aplicación (main.py)

class PostgresProductoRepository(ProductoRepository):
    """Implementación del repositorio de productos que usa una base de datos PostgreSQL."""
    def __init__(self):
        """Inicializa la conexión a la base de datos."""
        self.conn = None
        try:
            # Idealmente, estos datos de conexión deberían venir de variables de entorno o un archivo de configuración
            self.conn = psycopg2.connect(
                dbname="hardware_shop_db", 
                user="postgres", 
                password="postgres", 
                host="localhost", 
                port="5432"
            )
            self._create_table_if_not_exists()
            logging.info("Conexión a PostgreSQL exitosa.")
        except psycopg2.OperationalError as e:
            logging.error(f"Error al conectar con PostgreSQL: {e}")
            # Si no se puede conectar, self.conn será None y las operaciones fallarán controladamente.
            raise ConnectionError(f"No se pudo conectar a la base de datos: {e}")

    def _create_table_if_not_exists(self):
        """Crea la tabla de productos si no existe."""
        if not self.conn:
            return
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS productos (
                        id SERIAL PRIMARY KEY,
                        nombre VARCHAR(255) NOT NULL,
                        precio NUMERIC(10, 2) NOT NULL,
                        stock INTEGER NOT NULL
                    );
                """)
                self.conn.commit()
        except psycopg2.Error as e:
            logging.error(f"Error al crear la tabla 'productos': {e}")
            self.conn.rollback()

    def _to_dict(self, cur, row) -> Dict[str, Any] | None:
        """Convierte una fila de la base de datos a un diccionario."""
        if row is None:
            return None
        try:
            desc = [d[0] for d in cur.description]
            return dict(zip(desc, row))
        except Exception as e:
            logging.error(f"Error al convertir fila a diccionario: {e}")
            return None

    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todos los productos de la base de datos."""
        if not self.conn:
            return []
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, nombre, precio, stock FROM productos ORDER BY id;")
                logging.info("Se han obtenido todos los productos.")
                return [self._to_dict(cur, row) for row in cur.fetchall()]
        except psycopg2.Error as e:
            logging.error(f"Error al obtener todos los productos: {e}")
            return []

    def get_by_id(self, id_producto: int) -> Dict[str, Any] | None:
        """Obtiene un producto por su ID."""
        if not self.conn:
            return None
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, nombre, precio, stock FROM productos WHERE id = %s;", (id_producto,))
                producto = self._to_dict(cur, cur.fetchone())
                if producto:
                    logging.info(f"Producto con ID {id_producto} obtenido.")
                else:
                    logging.warning(f"No se encontró producto con ID {id_producto}.")
                return producto
        except psycopg2.Error as e:
            logging.error(f"Error al obtener producto con ID {id_producto}: {e}")
            return None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo producto en la base de datos."""
        if not self.conn:
            return None
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s) RETURNING id, nombre, precio, stock;",
                    (data['nombre'], data['precio'], data['stock'])
                )
                new_product = self._to_dict(cur, cur.fetchone())
                self.conn.commit()
                logging.info(f"Producto creado: {new_product}")
                return new_product
        except psycopg2.Error as e:
            logging.error(f"Error al crear producto con datos {data}: {e}")
            self.conn.rollback()
            return None

    def update(self, id_producto: int, data: Dict[str, Any]) -> Dict[str, Any] | None:
        """Actualiza un producto existente en la base de datos."""
        if not self.conn:
            return None
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id = %s RETURNING id, nombre, precio, stock;",
                    (data['nombre'], data['precio'], data['stock'], id_producto)
                )
                updated_product = self._to_dict(cur, cur.fetchone())
                self.conn.commit()
                if updated_product:
                    logging.info(f"Producto con ID {id_producto} actualizado.")
                else:
                    logging.warning(f"Intento de actualizar producto no existente con ID {id_producto}.")
                return updated_product
        except psycopg2.Error as e:
            logging.error(f"Error al actualizar producto con ID {id_producto}: {e}")
            self.conn.rollback()
            return None

    def delete(self, id_producto: int) -> bool:
        """Elimina un producto de la base de datos."""
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM productos WHERE id = %s;", (id_producto,))
                self.conn.commit()
                if cur.rowcount > 0:
                    logging.info(f"Producto con ID {id_producto} eliminado.")
                    return True
                else:
                    logging.warning(f"Intento de eliminar producto no existente con ID {id_producto}.")
                    return False
        except psycopg2.Error as e:
            logging.error(f"Error al eliminar producto con ID {id_producto}: {e}")
            self.conn.rollback()
            return False

    def get_by_low_stock(self) -> List[Dict[str, Any]]:
        """Obtiene productos con stock bajo (<= 5)."""
        if not self.conn:
            return []
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, nombre, precio, stock FROM productos WHERE stock <= 5 ORDER BY stock;")
                productos = [self._to_dict(cur, row) for row in cur.fetchall()]
                logging.info(f"Se han obtenido {len(productos)} productos con stock bajo.")
                return productos
        except psycopg2.Error as e:
            logging.error(f"Error al obtener productos con stock bajo: {e}")
            return []

    def __del__(self):
        """Cierra la conexión a la base de datos cuando el objeto es destruido."""
        if self.conn:
            self.conn.close()
            logging.info("Conexión a PostgreSQL cerrada.")
