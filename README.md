# 🛒 Sistema de Gestión de Inventario - Tienda de Hardware

Un sistema de gestión de inventario desarrollado en Python, diseñado con una arquitectura limpia y escalable. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre productos, con un enfoque en la separación de responsabilidades y buenas prácticas de desarrollo.

## 📋 Características Principales

- ✅ **Arquitectura Limpia:** Implementación del **Patrón Repositorio** que separa la lógica de negocio de la capa de acceso a datos.
- 📦 **Gestión Completa de Productos (CRUD):** Operaciones robustas para manejar el ciclo de vida de los productos.
- 🔍 **Sistema de Logging:** Todas las operaciones de la base de datos se registran en `operaciones.log` para auditoría.
- 📤 **Exportación de Reportes:** Genera reportes de inventario en formato `.txt`.
- ⚠️ **Alertas de Stock:** Indicadores visuales para productos con stock bajo o sin stock.
- 🛡️ **Protección de Datos:** Lógica para prevenir la eliminación accidental de productos con inventario.

## 🚀 Instalación

### Requisitos
- Python 3.9 o superior

### Pasos de Configuración

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/devseniorlabpython/hardware-shop.git
    cd hardware-shop
    ```

2.  **Ejecutar la aplicación:**
    ```bash
    python main.py
    ```

## 📁 Estructura del Proyecto

La arquitectura del proyecto está diseñada para ser modular y escalable:

```
hardware-shop/
├── main.py                   # Capa de Presentación (Interfaz de Usuario)
├── producto_crud.py          # Capa de Acceso a Datos (Implementación del Repositorio)
├── repositorio.py            # Contrato del Repositorio (Interfaz Abstracta)
├── operaciones.log           # Archivo de logs (generado automáticamente)
├── .gitignore                # Archivos ignorados por Git
└── README.md                 # Documentación del proyecto
```

## 🛠️ Arquitectura: Patrón Repositorio

Este proyecto utiliza el Patrón Repositorio para desacoplar la lógica de la aplicación de los detalles de cómo se almacenan los datos.

1.  **`repositorio.py` (El Contrato):**
    Define la interfaz `ProductoRepository` con métodos abstractos como `get_all()`, `get_by_id()`, `create()`, etc. Cualquier clase que gestione datos *debe* implementar esta interfaz.

2.  **`producto_crud.py` (La Implementación):**
    Contiene la clase `InMemoryProductoRepository`, que implementa el contrato `ProductoRepository` usando una lista de diccionarios en memoria como si fuera una base de datos.

3.  **`main.py` (El Cliente):**
    Interactúa únicamente con una instancia del repositorio a través de los métodos definidos en el contrato. No sabe si los datos vienen de una lista, una base de datos SQL o una API.

Esta estructura permite que en el futuro podamos cambiar la fuente de datos (por ejemplo, a una base de datos SQLite) simplemente creando una nueva clase de repositorio, sin tener que modificar `main.py`.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si eres un estudiante nuevo, aquí tienes algunas ideas para empezar:

1.  **Mejorar la Interfaz:** Implementa una tabla mejor formateada para la lista de productos.
2.  **Añadir Funcionalidad:** Crea una opción en el menú para ver solo los productos con stock bajo.
3.  **Mejorar la Documentación:** Añade `docstrings` y `type hints` a las funciones en `main.py`.

Consulta los issues abiertos en el repositorio para más ideas.

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
