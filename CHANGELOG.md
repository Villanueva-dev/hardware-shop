# 📋 Registro de Cambios

Todos los cambios importantes de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

### Planeado
- Persistencia en base de datos SQLite
- Interfaz gráfica con tkinter
- Exportación a CSV y JSON
- Sistema de autenticación
- API REST con FastAPI

## [1.0.0] - 2025-08-06

### ✨ Agregado
- Sistema CRUD completo para gestión de productos
- Clase `Producto` con atributos: nombre, precio, stock
- Control inteligente de stock con alertas automáticas
- Sistema de logging completo para auditoría
- Función `agregar_producto()` con validación de stock
- Función `leer_productos()` con indicadores visuales de stock
- Función `leer_producto()` con análisis detallado de inventario
- Función `actualizar_producto()` con actualización parcial de campos
- Función `eliminar_producto()` con protección contra pérdida de inventario
- Función `exportar_productos_txt()` para generar reportes
- Datos de ejemplo precargados (6 productos de hardware)
- Documentación completa en README.md
- Archivo .gitignore configurado
- Estructura de carpetas organizada

### 🔧 Configuración
- Logging automático en `operaciones.log`
- Exportación automática a carpeta `exports-txt/`
- Encoding UTF-8 para caracteres especiales
- Umbral de stock bajo configurado en 5 unidades

### 🛡️ Seguridad
- Confirmación requerida para eliminar productos con stock > 0
- Logging de todas las operaciones para auditoría
- Validación de IDs de productos existentes

### 📊 Productos de Ejemplo Incluidos
- NVIDIA RTX 4070 ($599.99) - 12 unidades
- AMD Ryzen 7 7700X ($349.99) - 8 unidades  
- Corsair Vengeance DDR5 32GB ($199.99) - 15 unidades
- ASUS ROG Strix B650-E ($299.99) - 3 unidades (Stock bajo)
- Monitor Samsung Odyssey G7 27" ($449.99) - 0 unidades (Sin stock)
- Teclado Mecánico Logitech G Pro X ($129.99) - 25 unidades

### 📝 Documentación
- README.md completo con ejemplos de uso
- Docstrings en todas las funciones
- Comentarios explicativos en código crítico
- Guía de instalación y configuración

---

## Tipos de Cambios

- `✨ Agregado` para nuevas funcionalidades
- `🔧 Cambiado` para cambios en funcionalidades existentes
- `🚫 Deprecado` para funcionalidades que serán removidas
- `🗑️ Removido` para funcionalidades removidas
- `🐛 Corregido` para corrección de bugs
- `🛡️ Seguridad` para mejoras de seguridad