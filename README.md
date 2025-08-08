# 🛒 Sistema de Gestión de Inventario - Tienda de Hardware

Un sistema completo de gestión de inventario desarrollado en Python para tiendas de hardware tecnológico. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre productos con control de stock inteligente y sistema de logging para auditoría.

## 📋 Características

- ✅ **Gestión completa de productos** (CRUD)
- 📊 **Control de stock inteligente** con alertas automáticas
- 🔍 **Sistema de logging** para auditoría y trazabilidad
- 📤 **Exportación de reportes** en formato TXT
- ⚠️ **Alertas de stock bajo** y productos sin stock
- 🛡️ **Protección contra eliminación accidental** de productos con inventario
- 🎯 **Datos de ejemplo** preconfigurados para pruebas

## 🚀 Instalación

### Requisitos del Sistema
- Python 3.7 o superior
- Sistema operativo: Windows, macOS, Linux

### Configuración del Proyecto

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/proyecto-tienda.git
   cd proyecto-tienda
   ```

2. **Verificar instalación de Python**
   ```bash
   python --version
   ```

3. **Ejecutar el sistema**
   ```bash
   python producto_crud.py
   ```

## 📁 Estructura del Proyecto

```
proyecto-tienda/
├── README.md                 # Documentación principal
├── producto_crud.py          # Módulo principal del sistema
├── main.py                   # Archivo principal de ejecución
├── operaciones.log           # Archivo de logs (generado automáticamente)
├── exports-txt/              # Carpeta de exportaciones (generada automáticamente)
├── __pycache__/              # Cache de Python (ignorado por Git)
├── uml/                      # Diagramas UML del proyecto
│   └── final-project-m3.plantuml
├── Contributors.md           # Lista de contribuidores
└── .gitignore               # Archivos ignorados por Git
```

## 🛠️ Uso del Sistema

### Funciones Principales

#### 1. Agregar Producto
```python
agregar_producto("NVIDIA RTX 4070", "599.99", 12)
```

#### 2. Consultar Todos los Productos
```python
leer_productos()
```
**Salida esperada:**
```
📦 INVENTARIO COMPLETO:
------------------------------------------------------------
ID: 1 | NVIDIA RTX 4070 - Precio: $599.99 - Stock: 12 | 🟢 STOCK OK
ID: 2 | AMD Ryzen 7 7700X - Precio: $349.99 - Stock: 8 | 🟢 STOCK OK
------------------------------------------------------------
```

#### 3. Consultar Producto Específico
```python
leer_producto(1)
```

#### 4. Actualizar Producto
```python
# Actualizar solo el precio
actualizar_producto(1, nuevo_precio="649.99")

# Actualizar múltiples campos
actualizar_producto(1, nuevo_nombre="NVIDIA RTX 4070 Ti", nuevo_precio="699.99", nuevo_stock=8)
```

#### 5. Eliminar Producto
```python
eliminar_producto(1)
```
*Nota: El sistema alertará si el producto tiene stock > 0*

#### 6. Exportar Inventario
```python
exportar_productos_txt("reporte_mensual")
```

### Sistema de Alertas de Stock

| Estado | Indicador | Descripción |
|--------|-----------|-------------|
| Stock OK | 🟢 | Stock > 5 unidades |
| Stock Bajo | 🟡 | Stock ≤ 5 unidades |
| Sin Stock | 🔴 | Stock = 0 unidades |

## 📊 Sistema de Logging

El sistema registra automáticamente todas las operaciones en `operaciones.log`:

- **INFO**: Operaciones exitosas (agregar, actualizar, consultar)
- **WARNING**: Intentos de operaciones sobre productos inexistentes
- **ERROR**: Errores durante exportaciones u otras operaciones

### Ejemplo de Log
```
2025-08-06 10:30:15 - INFO - Producto agregado con ID 1: NVIDIA RTX 4070, Precio: 599.99, Stock: 12
2025-08-06 10:35:22 - WARNING - Intento de eliminar producto no existente con ID: 99
2025-08-06 10:40:18 - INFO - Productos exportados exitosamente. Archivo: 'exports-txt/reporte.txt', Cantidad de productos: 6
```

## 🎯 Datos de Ejemplo

El sistema incluye 6 productos de hardware precargados:

1. **NVIDIA RTX 4070** - $599.99 (12 unidades)
2. **AMD Ryzen 7 7700X** - $349.99 (8 unidades)
3. **Corsair Vengeance DDR5 32GB** - $199.99 (15 unidades)
4. **ASUS ROG Strix B650-E** - $299.99 (3 unidades) ⚠️ Stock bajo
5. **Monitor Samsung Odyssey G7 27"** - $449.99 (0 unidades) 🔴 Sin stock
6. **Teclado Mecánico Logitech G Pro X** - $129.99 (25 unidades)

## 📤 Exportación de Reportes

Los reportes se generan en la carpeta `exports-txt/` con el siguiente formato:

```
REPORTE DE INVENTARIO
==================================================

ID: 1 | NVIDIA RTX 4070 | Precio: $599.99 | Stock: 12 unidades
ID: 4 | ASUS ROG Strix B650-E | Precio: $299.99 | Stock: 3 unidades [STOCK BAJO]
ID: 5 | Monitor Samsung Odyssey G7 27" | Precio: $449.99 | Stock: 0 unidades [SIN STOCK]
```

## 🔧 Configuración

### Variables de Configuración

- **Umbral de stock bajo**: 5 unidades (configurable en el código)
- **Archivo de logs**: `operaciones.log`
- **Directorio de exportación**: `exports-txt/`
- **Encoding**: UTF-8 para caracteres especiales

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Estándares de Código

- Seguir PEP 8 para Python
- Documentar todas las funciones con docstrings
- Incluir logging para operaciones importantes
- Mantener cobertura de pruebas > 80%

## 📝 Registro de Cambios

### v1.0.0 (2025-08-06)
- ✅ Implementación completa del sistema CRUD
- ✅ Sistema de control de stock con alertas
- ✅ Logging completo para auditoría
- ✅ Exportación de reportes TXT
- ✅ Datos de ejemplo precargados
- ✅ Protección contra eliminación accidental

## 🐛 Problemas Conocidos

- Los datos se almacenan en memoria (se pierden al cerrar el programa)
- No hay autenticación de usuarios
- Exportación limitada a formato TXT

## 🗺️ Roadmap

- [ ] Persistencia en base de datos
- [ ] Interfaz gráfica (GUI)
- [ ] Exportación en múltiples formatos (CSV, JSON, PDF)
- [ ] Sistema de usuarios y roles
- [ ] API REST
- [ ] Dashboard web
- [ ] Notificaciones automáticas de stock bajo