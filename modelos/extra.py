"""
Patrón de diseño DECORATOR (GoF) — patrón estructural.
Implementado con CLASES. No confundir con los decoradores de función (@)
de decoradores/validaciones.py.

Hay dos tipos de decoradores que modelan cómo se pide un café:
1. VARIANTES DE PREPARACIÓN: corto, largo, cortado, lágrima.
2. AGREGADOS: leche, crema, dulce de leche, tamaño grande.
Ejemplo: Café -> Cortado -> ConCrema (el precio y la descripción se acumulan).
"""
from modelos.producto import Producto


class Extra(Producto):
    """Decorador base. Envuelve un Producto y le agrega precio y descripción."""

    def __init__(self, producto_envuelto, nombre_extra, precio_extra):
        self._producto = producto_envuelto
        self._nombre_extra = nombre_extra
        self._precio_extra = precio_extra
        super().__init__(
            nombre=producto_envuelto.nombre,
            precio=producto_envuelto.precio,
            categoria=producto_envuelto.categoria,
            stock=producto_envuelto.stock,
            sin_tacc=producto_envuelto.sin_tacc,
            vegetariano=producto_envuelto.vegetariano,
        )

    @property
    def precio(self):
        return self._producto.precio + self._precio_extra

    def descripcion(self):
        return f"{self._producto.descripcion()} + {self._nombre_extra}"

    def admite_extras(self):
        return self._producto.admite_extras()


# --- VARIANTES DE PREPARACIÓN ---

class Corto(Extra):
    def __init__(self, producto):
        super().__init__(producto, "corto", 0)


class Largo(Extra):
    def __init__(self, producto):
        super().__init__(producto, "largo", 100)


class Cortado(Extra):
    def __init__(self, producto):
        super().__init__(producto, "cortado", 150)


class Lagrima(Extra):
    def __init__(self, producto):
        super().__init__(producto, "lágrima", 200)


# --- AGREGADOS ---

class ConLeche(Extra):
    def __init__(self, producto):
        super().__init__(producto, "leche", 200)


class ConCrema(Extra):
    def __init__(self, producto):
        super().__init__(producto, "crema", 350)


class ConDulceDeLeche(Extra):
    def __init__(self, producto):
        super().__init__(producto, "dulce de leche", 300)


class Grande(Extra):
    def __init__(self, producto):
        super().__init__(producto, "tamaño grande", 400)


VARIANTES_DISPONIBLES = {
    "1": ("Corto", Corto),
    "2": ("Largo", Largo),
    "3": ("Cortado", Cortado),
    "4": ("Lágrima", Lagrima),
}

AGREGADOS_DISPONIBLES = {
    "1": ("Leche", ConLeche),
    "2": ("Crema", ConCrema),
    "3": ("Dulce de leche", ConDulceDeLeche),
    "4": ("Tamaño grande", Grande),
}