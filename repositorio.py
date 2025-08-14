from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ProductoRepository(ABC):
    """
    Define el contrato para las operaciones de persistencia de productos.
    Cualquier clase que gestione el almacenamiento de productos debe implementar estos métodos.
    """

    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        """Devuelve todos los productos."""
        pass

    @abstractmethod
    def get_by_id(self, id_producto: int) -> Dict[str, Any] | None:
        """Devuelve un producto por su ID."""
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo producto."""
        pass

    @abstractmethod
    def update(self, id_producto: int, data: Dict[str, Any]) -> Dict[str, Any] | None:
        """Actualiza un producto existente."""
        pass

    @abstractmethod
    def delete(self, id_producto: int) -> bool:
        """Elimina un producto y devuelve True si tuvo éxito."""
        pass

    @abstractmethod
    def get_by_low_stock(self) -> List[Dict[str, Any]]:
        """Muestra los productos con Stock bajo (< 5 unds)."""
        pass