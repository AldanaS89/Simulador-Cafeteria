"""
Cafetería: clase central que coordina el sistema (rol del Gerente).
- AGREGACIÓN: agrupa Mozos y administra el Menú (Productos).
- Valida duplicados y usa excepciones personalizadas.
"""
from utils.categorias import Categoria
from modelos.pedido import Pedido
from modelos.excepciones import (
    ProductoDuplicadoError,
    ProductoNoEncontradoError,
    PrecioInvalidoError,
)
from decoradores.validaciones import verificar_stock, requiere_login


class Cafeteria:
    def __init__(self, nombre):
        self.nombre = nombre
        self._menu = []
        self._mozos = {}
        self.mozo_actual = None
        self._contador_pedidos = 0

    # ---------- Administración del menú (Gerente) ----------

    def cargar_producto(self, producto):
        """Agrega un producto. No permite duplicados (nombre + categoría)."""
        duplicado = any(
            p.nombre.lower() == producto.nombre.lower()
            and p.categoria == producto.categoria
            for p in self._menu
        )
        if duplicado:
            raise ProductoDuplicadoError(
                f"Ya existe '{producto.nombre}' en la categoría "
                f"{producto.categoria}."
            )
        self._menu.append(producto)

    def modificar_precio(self, nombre_producto, nuevo_precio):
        if nuevo_precio <= 0:
            raise PrecioInvalidoError("El precio debe ser mayor que cero.")
        producto = self.buscar_producto(nombre_producto)
        producto._precio = nuevo_precio
        print(f"  Precio de '{producto.nombre}' actualizado a ${nuevo_precio:.0f}.")

    def reponer_stock(self, nombre_producto, cantidad):
        if cantidad <= 0:
            raise PrecioInvalidoError("La cantidad a reponer debe ser positiva.")
        producto = self.buscar_producto(nombre_producto)
        producto.reponer_stock(cantidad)
        print(f"  Stock de '{producto.nombre}' repuesto. Ahora: {producto.stock}.")

    def buscar_producto(self, nombre):
        for p in self._menu:
            if p.nombre.lower() == nombre.lower():
                return p
        raise ProductoNoEncontradoError(f"Producto '{nombre}' no encontrado.")

    def menu_por_categoria(self):
        agrupado = {cat: [] for cat in Categoria}
        for p in self._menu:
            agrupado[p.categoria].append(p)
        return agrupado

    @property
    def menu(self):
        return list(self._menu)

    def valor_inventario(self):
        return round(sum(p.precio * p.stock for p in self._menu), 2)

    def productos_agotados(self):
        return [p for p in self._menu if p.stock <= 0]

    # ---------- Login de mozos ----------

    def registrar_mozo(self, mozo):
        self._mozos[mozo.nombre.lower()] = mozo

    def login(self, nombre, clave):
        mozo = self._mozos.get(nombre.lower())
        if mozo and mozo.verificar_clave(clave):
            self.mozo_actual = mozo
            return True
        return False

    def logout(self):
        self.mozo_actual = None

    # ---------- Operación de pedidos (Mozo) ----------

    @requiere_login
    def nuevo_pedido(self):
        self._contador_pedidos += 1
        pedido = Pedido(self._contador_pedidos, self.mozo_actual.nombre)
        self.mozo_actual.registrar_pedido(pedido)
        return pedido

    @verificar_stock
    def agregar_al_pedido(self, producto, pedido):
        """Verifica stock (vía @verificar_stock) y descuenta una unidad."""
        producto.descontar_stock(1)
        return True

    # ---------- Cierre del día (Gerente) ----------

    def cierre_del_dia(self):
        total = 0
        detalle = []
        for mozo in self._mozos.values():
            vendido = mozo.total_vendido()
            cantidad = len(mozo.pedidos_finalizados())
            total += vendido
            detalle.append((mozo.nombre, cantidad, vendido))
        return total, detalle