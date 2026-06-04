from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import textwrap
import os

# =====================================
# CONFIGURACIÓN
# =====================================

ANCHO_CAJA = 850
ALTO_CAJA = 500

X_CAJA = 195
Y_CAJA = 410

# Posición del número de confesión
NUMERO_X = 330
NUMERO_Y = 390

FUENTE_RUTA = os.path.join(
    os.path.dirname(__file__),
    "fuentes",
    "Anton-Regular.ttf"
)


def obtener_fuente(tamano):

    return ImageFont.truetype(
        FUENTE_RUTA,
        tamano
    )


def crear_imagen(numero, texto):

    imagen = Image.open("fondo.png").convert("RGB")

    draw = ImageDraw.Draw(imagen)

    texto = texto.upper().strip()

    if not texto:
        texto = "SIN TEXTO"

    # =====================================
    # NÚMERO DE CONFESIÓN
    # =====================================

    fuente_numero = obtener_fuente(36)

    draw.text(
        (NUMERO_X, NUMERO_Y),
        str(numero),
        fill="white",
        font=fuente_numero
    )

    # =====================================
    # AJUSTE AUTOMÁTICO
    # =====================================

    tamano_fuente = 90
    interlineado = 18

    while tamano_fuente >= 24:

        fuente_texto = obtener_fuente(
            tamano_fuente
        )

        max_chars = 24

        lineas = textwrap.wrap(
            texto,
            width=max_chars
        )

        texto_envuelto = "\n".join(
            lineas
        )

        bbox = draw.multiline_textbbox(
            (0, 0),
            texto_envuelto,
            font=fuente_texto,
            spacing=interlineado,
            align="center"
        )

        cantidad_lineas = len(lineas)

        if cantidad_lineas > 12:
            tamano_fuente -= 2
            continue

        ancho_texto = bbox[2] - bbox[0]
        alto_texto = bbox[3] - bbox[1]

        if (
            ancho_texto <= ANCHO_CAJA
            and
            alto_texto <= ALTO_CAJA
        ):
            break

        tamano_fuente -= 2

    # =====================================
    # CENTRADO
    # =====================================

    x = X_CAJA + (
        (ANCHO_CAJA - ancho_texto) / 2
    )

    y = Y_CAJA + (
        (ALTO_CAJA - alto_texto) / 2
    )

    # baja un poco el texto visualmente
    y += 60

    # =====================================
    # SOMBRA
    # =====================================

    for dx, dy in [
        (-2, 0),
        (2, 0),
        (0, -2),
        (0, 2),
        (-1, -1),
        (1, 1),
        (-1, 1),
        (1, -1)
    ]:

        draw.multiline_text(
            (x + dx, y + dy),
            texto_envuelto,
            font=fuente_texto,
            fill="black",
            align="center",
            spacing=interlineado
        )

    # =====================================
    # TEXTO PRINCIPAL
    # =====================================

    draw.multiline_text(
        (x, y),
        texto_envuelto,
        font=fuente_texto,
        fill="white",
        align="center",
        spacing=interlineado
    )

    # =====================================
    # GUARDAR
    # =====================================

    os.makedirs(
        "generadas",
        exist_ok=True
    )

    ruta = f"generadas/confesion_{numero}.png"

    imagen.save(
        ruta,
        quality=95
    )

    return ruta