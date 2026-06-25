"""
Datos iniciales: menú realista y mozos de ejemplo.
El café es UN producto base; variantes y agregados se aplican con Decorator.
Stock alto en bebidas (no se "agotan"); stock contable en comidas.
"""
from modelos.producto import Bebida, Comida
from modelos.mozo import Mozo
from utils.categorias import Categoria


def cargar_menu_inicial(cafeteria):
    productos = [
        # --- BEBIDAS (productos base; admiten variantes y agregados) ---
        Bebida("Café", 1200, stock=50, vegetariano=True),
        Bebida("Té", 1100, stock=40, sin_tacc=True, vegetariano=True),
        Bebida("Mate cocido", 1000, stock=30, sin_tacc=True, vegetariano=True),
        Bebida("Submarino", 2000, stock=20, vegetariano=True),
        Bebida("Capuchino", 1800, stock=25, vegetariano=True),
        Bebida("Jugo de naranja", 1600, stock=15, sin_tacc=True, vegetariano=True),

        # --- SALADO (productos contables) ---
        Comida("Tostado de jamón y queso", 2800, Categoria.SALADO, stock=15),
        Comida("Medialuna de grasa", 700, Categoria.SALADO, stock=40),
        Comida("Fosforitos", 900, Categoria.SALADO, stock=30),
        Comida("Sándwich de miga", 2200, Categoria.SALADO, stock=10,
               vegetariano=True),

        # --- DULCE (productos contables) ---
        Comida("Medialuna de manteca", 800, Categoria.DULCE, stock=40,
               vegetariano=True),
        Comida("Factura rellena", 1000, Categoria.DULCE, stock=25,
               vegetariano=True),
        Comida("Alfajor de maicena", 1200, Categoria.DULCE, stock=20,
               sin_tacc=True, vegetariano=True),
        Comida("Budín de limón", 1400, Categoria.DULCE, stock=12,
               vegetariano=True),
    ]
    for p in productos:
        cafeteria.cargar_producto(p)


def cargar_mozos_iniciales(cafeteria):
    clave_comun = "1234"
    for nombre in ("Carlos", "María", "José"):
        cafeteria.registrar_mozo(Mozo(nombre, clave_comun))