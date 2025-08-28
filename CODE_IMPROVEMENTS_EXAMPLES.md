# 🔧 Ejemplos de Mejoras de Código

Este documento complementa el code review principal con ejemplos específicos de código mostrando problemas actuales y soluciones propuestas.

## 🚨 Problema 1: Función `main()` Muy Larga

### ❌ Código Actual (Problemático)
```python
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
                # ... más líneas ...
```

### ✅ Código Mejorado (Propuesto)
```python
class InventoryController:
    def __init__(self, repository: ProductoRepository, validator: InputValidator):
        self.repository = repository
        self.validator = validator
        self.logger = logging.getLogger('hardware_shop.controller')
    
    def add_product(self):
        """Maneja la adición de un nuevo producto."""
        print("📦 AGREGAR NUEVO PRODUCTO")
        print("-" * 30)
        
        try:
            product_data = self._get_product_input()
            product = self.repository.create(product_data)
            
            if product:
                self.logger.info(f"Producto agregado con ID {product['id']}: {product['nombre']}")
                print(f"✅ Producto agregado con ID {product['id']}: {product['nombre']}")
            else:
                self._handle_creation_error()
                
        except InvalidInputError as e:
            self.logger.warning(f"Entrada inválida al agregar producto: {e}")
            print(f"❌ {e}")
        except Exception as e:
            self.logger.error(f"Error inesperado al agregar producto: {e}")
            print("❌ Error inesperado al agregar el producto.")
    
    def _get_product_input(self) -> Dict[str, Any]:
        """Obtiene y valida los datos del producto del usuario."""
        nombre = self.validator.validate_non_empty_string(
            input("Nombre del producto: ").strip(), 
            "nombre del producto"
        )
        precio = self.validator.validate_positive_float(
            input("Precio del producto ($): "), 
            "precio"
        )
        stock = self.validator.validate_positive_int(
            input("Cantidad en stock: "), 
            "stock"
        )
        
        return {"nombre": nombre, "precio": precio, "stock": stock}

def main():
    """Función principal simplificada."""
    controller = InventoryController(repo, InputValidator())
    menu_handler = MenuHandler(controller)
    
    while True:
        try:
            menu_handler.show_menu()
            option = menu_handler.get_user_choice()
            menu_handler.handle_option(option)
            
            if option == "8":  # Salir
                break
                
        except KeyboardInterrupt:
            print("\n🔒 Cerrando aplicación...")
            break
        except Exception as e:
            logger.error(f"Error inesperado en main: {e}")
            print("❌ Error inesperado. Intente nuevamente.")
        
        input("\n📱 Presione Enter para continuar...")
        os.system("cls" if os.name == "nt" else "clear")
```

## 🚨 Problema 2: Validación Repetitiva

### ❌ Código Actual (Repetitivo)
```python
# En opción "3" - Buscar producto
try:
    id_producto = int(input("ID del producto a buscar: "))
    # ...
except ValueError:
    logger.warning("Entrada no válida para buscar producto por ID.")
    print("❌ Por favor ingrese un ID numérico válido.")

# En opción "4" - Actualizar producto  
try:
    id_producto = int(input("ID del producto a actualizar: "))
    # ...
except ValueError:
    logger.warning("Error de valor al actualizar producto.")
    print("❌ Por favor ingrese valores numéricos válidos para precio y stock.")

# En opción "5" - Eliminar producto
try:
    id_producto = int(input("ID del producto a eliminar: "))
    # ...
except ValueError:
    logger.warning("Entrada no válida para eliminar producto.")
    print("❌ Por favor ingrese un ID numérico válido.")
```

### ✅ Código Mejorado (DRY)
```python
class InputValidator:
    """Centraliza toda la validación de entrada de usuario."""
    
    @staticmethod
    def validate_positive_int(input_str: str, field_name: str) -> int:
        """Valida que la entrada sea un entero positivo."""
        try:
            value = int(input_str)
            if value < 0:
                raise InvalidInputError(f"El {field_name} debe ser un número positivo.")
            return value
        except ValueError:
            raise InvalidInputError(f"El {field_name} debe ser un número entero válido.")
    
    @staticmethod
    def validate_positive_float(input_str: str, field_name: str) -> float:
        """Valida que la entrada sea un float positivo."""
        try:
            value = float(input_str)
            if value < 0:
                raise InvalidInputError(f"El {field_name} debe ser un número positivo.")
            return value
        except ValueError:
            raise InvalidInputError(f"El {field_name} debe ser un número decimal válido.")
    
    @staticmethod
    def validate_non_empty_string(input_str: str, field_name: str) -> str:
        """Valida que la entrada no esté vacía."""
        if not input_str or not input_str.strip():
            raise InvalidInputError(f"El {field_name} no puede estar vacío.")
        return input_str.strip()
    
    @staticmethod
    def validate_product_id(input_str: str) -> int:
        """Valida un ID de producto."""
        return InputValidator.validate_positive_int(input_str, "ID del producto")

# Uso simplificado
class InventoryController:
    def search_product(self):
        """Busca un producto por ID."""
        print("🔍 BUSCAR PRODUCTO")
        print("-" * 30)
        
        try:
            product_id = self.validator.validate_product_id(
                input("ID del producto a buscar: ")
            )
            product = self.repository.get_by_id(product_id)
            
            if product:
                self._display_product_details(product)
            else:
                print("❌ Producto no encontrado.")
                
        except InvalidInputError as e:
            print(f"❌ {e}")
        except Exception as e:
            self.logger.error(f"Error al buscar producto: {e}")
            print("❌ Ocurrió un error al buscar el producto.")
```

## 🚨 Problema 3: Configuración Hard-codeada

### ❌ Código Actual (Hard-coded)
```python
# En postgres_repository.py
def __init__(self):
    self.conn = None
    try:
        self.conn = psycopg2.connect(
            dbname="hardware_shop_db", 
            user="postgres", 
            password="postgres", 
            host="localhost", 
            port="5432"
        )
        # ...
```

### ✅ Código Mejorado (Configurable)
```python
# config.py
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class DatabaseConfig:
    """Configuración de la base de datos."""
    host: str = os.getenv('DB_HOST', 'localhost')
    port: str = os.getenv('DB_PORT', '5432')
    name: str = os.getenv('DB_NAME', 'hardware_shop_db')
    user: str = os.getenv('DB_USER', 'postgres')
    password: str = os.getenv('DB_PASSWORD', 'postgres')
    
    @property
    def connection_string(self) -> str:
        """Genera la cadena de conexión."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

@dataclass
class AppConfig:
    """Configuración general de la aplicación."""
    log_file: str = os.getenv('LOG_FILE', 'operaciones.log')
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    export_directory: str = os.getenv('EXPORT_DIR', 'exports-txt')
    
    database: DatabaseConfig = DatabaseConfig()

# postgres_repository.py (mejorado)
class PostgresProductoRepository(ProductoRepository):
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.conn = None
        self._connect()
    
    def _connect(self):
        """Establece la conexión usando la configuración."""
        try:
            self.conn = psycopg2.connect(
                dbname=self.config.name,
                user=self.config.user,
                password=self.config.password,
                host=self.config.host,
                port=self.config.port
            )
            self._create_table_if_not_exists()
            logging.info("Conexión a PostgreSQL exitosa.")
        except psycopg2.OperationalError as e:
            logging.error(f"Error al conectar con PostgreSQL: {e}")
            raise ConnectionError(f"No se pudo conectar a la base de datos: {e}")

# main.py (inicialización mejorada)
def inicializar_repositorio():
    """Inicializa el repositorio con configuración."""
    config = AppConfig()
    try:
        return PostgresProductoRepository(config.database)
    except ConnectionError as e:
        logger.error(f"CRÍTICO: No se pudo conectar a la base de datos. {e}")
        print("Error fatal: No se pudo establecer la conexión con la base de datos.")
        sys.exit(1)
```

## 🚨 Problema 4: Logging Duplicado

### ❌ Código Actual (Duplicado)
```python
# En main.py
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file_handler = logging.FileHandler('operaciones.log', encoding='utf-8')
log_file_handler.setFormatter(log_formatter)
log_console_handler = logging.StreamHandler(sys.stdout)
log_console_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_file_handler)
logger.addHandler(log_console_handler)

# En postgres_repository.py
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
```

### ✅ Código Mejorado (Centralizado)
```python
# logging_config.py
import logging
import sys
from typing import Optional

class LoggingConfig:
    """Configuración centralizada de logging."""
    
    @staticmethod
    def setup_logging(
        log_file: str = 'operaciones.log',
        log_level: str = 'INFO',
        console_output: bool = True
    ) -> logging.Logger:
        """Configura el sistema de logging para toda la aplicación."""
        
        # Crear logger principal
        logger = logging.getLogger('hardware_shop')
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # Evitar duplicación de handlers
        if logger.handlers:
            logger.handlers.clear()
        
        # Formato común
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Handler para archivo
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Handler para consola (opcional)
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        return logger

# main.py (uso simplificado)
from logging_config import LoggingConfig

# Configurar logging una sola vez
logger = LoggingConfig.setup_logging()

# postgres_repository.py (uso del logger configurado)
class PostgresProductoRepository(ProductoRepository):
    def __init__(self, config: DatabaseConfig):
        self.logger = logging.getLogger('hardware_shop.repository')
        # ... resto del código
    
    def get_all(self) -> List[Dict[str, Any]]:
        try:
            # ... código de consulta
            self.logger.info("Se han obtenido todos los productos.")
            return productos
        except psycopg2.Error as e:
            self.logger.error(f"Error al obtener todos los productos: {e}")
            return []
```

## 🚨 Problema 5: Manejo de Excepciones Genérico

### ❌ Código Actual (Genérico)
```python
except Exception as e:
    logger.error(f"Error inesperado al actualizar producto: {e}")
    print("❌ Ocurrió un error inesperado al actualizar.")
```

### ✅ Código Mejorado (Específico)
```python
# exceptions.py
class HardwareShopError(Exception):
    """Excepción base para la aplicación."""
    pass

class ProductNotFoundError(HardwareShopError):
    """Producto no encontrado."""
    pass

class InvalidInputError(HardwareShopError):
    """Entrada de usuario inválida."""
    pass

class DatabaseConnectionError(HardwareShopError):
    """Error de conexión a la base de datos."""
    pass

class ValidationError(HardwareShopError):
    """Error de validación de datos."""
    pass

# Uso en el código
class InventoryController:
    def update_product(self):
        """Actualiza un producto existente."""
        try:
            product_id = self.validator.validate_product_id(
                input("ID del producto a actualizar: ")
            )
            
            existing_product = self.repository.get_by_id(product_id)
            if not existing_product:
                raise ProductNotFoundError(f"No se encontró producto con ID {product_id}")
            
            updated_data = self._get_update_data(existing_product)
            updated_product = self.repository.update(product_id, updated_data)
            
            if updated_product:
                self.logger.info(f"Producto ID {product_id} actualizado.")
                print("✅ Producto actualizado correctamente.")
            else:
                raise DatabaseConnectionError("No se pudo actualizar el producto en la base de datos")
                
        except InvalidInputError as e:
            print(f"❌ Entrada inválida: {e}")
        except ProductNotFoundError as e:
            print(f"❌ {e}")
        except DatabaseConnectionError as e:
            self.logger.error(f"Error de base de datos: {e}")
            print("❌ Error de conexión. Intente nuevamente.")
        except Exception as e:
            self.logger.error(f"Error inesperado al actualizar producto: {e}")
            print("❌ Error inesperado. Contacte al administrador.")
```

## 📊 Resumen de Beneficios

| Mejora | Beneficio | Impacto |
|--------|-----------|---------|
| Refactorización de `main()` | Código más mantenible y testeable | Alto |
| Validación centralizada | Elimina duplicación, facilita cambios | Alto |
| Configuración externa | Flexibilidad en diferentes entornos | Medio |
| Logging centralizado | Consistencia y mejor debugging | Medio |
| Excepciones específicas | Mejor manejo de errores y UX | Alto |

Estas mejoras transformarían el código de un estado funcional pero difícil de mantener a un código de calidad profesional, fácil de extender y mantener.