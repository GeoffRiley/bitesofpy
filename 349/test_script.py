import pytest

from script import get_accentuated_sentence

PHRASES = [
    (
        "Cuando era pequeno me gustaba jugar en la via",
        "Cuando era pequeño me gustaba jugar en la vía",
    ),
    ("un dos tres ... accion", "un dos tres ... acción"),
    ("anadir otra aficion", "añadir otra afición"),
    (
        "bajo el arbol descansando vi un avion",
        "bajo el árbol descansando vi un avión",
    ),
    (
        "no tomes mucho azucar o hay que evitar la bascula",
        "no tomes mucho azúcar o hay que evitar la báscula",
    ),
    (
        "vehiculo volando, utopia o realidad pronto ...?",
        "vehículo volando, utopía o realidad pronto ...?",
    ),
    (
        "telefono publico ... apenas ya no se ve en esta epoca",
        "teléfono público ... apenas ya no se ve en esta época",
    ),
    ("me falta jamon y jabon", "me falta jamón y jabón"),
    (
        "leyendo un libro en el jardin ... tarde de exito",
        "leyendo un libro en el jardín ... tarde de éxito",
    ),
    (
        "sesion de escribir, primera pagina de mi poesia hecha",
        "sesión de escribir, primera página de mi poesía hecha",
    ),
]


@pytest.mark.parametrize("text, accentuated_text", PHRASES)
def test_get_accentuated_sentence(text, accentuated_text):
    assert get_accentuated_sentence(text) == accentuated_text
