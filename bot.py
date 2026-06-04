import sqlite3

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters
)

from imagen import crear_imagen


# ==================================================
# CONFIGURACIÓN
# ==================================================

TOKEN = "8823463067:AAGSQ4u_vOmcrcZSqEbu3rCXXSck2N1la30"

GROUP_ID = -1003216244272

BOT_ACTIVO = True


# ==================================================
# VERIFICAR ADMIN
# ==================================================

async def es_admin(context, user_id):

    try:

        miembro = await context.bot.get_chat_member(
            chat_id=GROUP_ID,
            user_id=user_id
        )

        return miembro.status in [
            "administrator",
            "creator"
        ]

    except:
        return False


# ==================================================
# START
# ==================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🤫 CONFESIONES ANÓNIMAS\n\n"
        "Envíame tu confesión y será publicada "
        "de forma completamente anónima."
    )


# ==================================================
# ACTIVAR
# ==================================================

async def on(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    global BOT_ACTIVO

    if not await es_admin(
        context,
        update.effective_user.id
    ):
        await update.message.reply_text(
            "⛔ Solo administradores."
        )
        return

    BOT_ACTIVO = True

    await update.message.reply_text(
        "🟢 Confesiones activadas."
    )


# ==================================================
# DESACTIVAR
# ==================================================

async def off(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    global BOT_ACTIVO

    if not await es_admin(
        context,
        update.effective_user.id
    ):
        await update.message.reply_text(
            "⛔ Solo administradores."
        )
        return

    BOT_ACTIVO = False

    await update.message.reply_text(
        "🔴 Confesiones desactivadas."
    )


# ==================================================
# ESTADO
# ==================================================

async def estado(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if BOT_ACTIVO:
        mensaje = "🟢 ACTIVADO"
    else:
        mensaje = "🔴 DESACTIVADO"

    await update.message.reply_text(
        f"Estado actual:\n\n{mensaje}"
    )


# ==================================================
# CONFESIONES
# ==================================================

async def recibir_confesion(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    global BOT_ACTIVO

    if not BOT_ACTIVO:

        await update.message.reply_text(
            "⚠️ Las confesiones están temporalmente cerradas."
        )

        return

    texto = update.message.text.strip()

    if not texto:
        return

    user_id = update.effective_user.id

    conn = sqlite3.connect(
        "confesiones.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO confesiones
        (user_id, texto)
        VALUES (?, ?)
        """,
        (
            user_id,
            texto
        )
    )

    conn.commit()

    numero_confesion = cursor.lastrowid

    conn.close()

    ruta_imagen = crear_imagen(
        numero_confesion,
        texto
    )

    with open(
        ruta_imagen,
        "rb"
    ) as foto:

        await context.bot.send_photo(
            chat_id=GROUP_ID,
            photo=foto,
            caption=f"TRAIGO CHISME 💅"
        )

    await update.message.reply_text(
        "Tu confesión fue publicada de forma anónima."
    )


# ==================================================
# APP
# ==================================================

app = (
    ApplicationBuilder()
    .token(TOKEN)
    .build()
)

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.add_handler(
    CommandHandler(
        "on",
        on
    )
)

app.add_handler(
    CommandHandler(
        "off",
        off
    )
)

app.add_handler(
    CommandHandler(
        "estado",
        estado
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT
        & ~filters.COMMAND
        & filters.ChatType.PRIVATE,
        recibir_confesion
    )
)

print("🤖 Bot iniciado correctamente...")

app.run_polling()