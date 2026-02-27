import os
import sys
import subprocess
import re
import time
import asyncio
import logging
from telethon import TelegramClient, events
import yt_dlp
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# ================= CONFIGURACIÓN Y LOGS =================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

try:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    PHONE = os.getenv("PHONE")

    # Procesar usuarios autorizados
    usuarios_str = os.getenv("USUARIOS_AUTORIZADOS", "")
    USUARIOS_AUTORIZADOS = [
        int(u.strip()) for u in usuarios_str.split(",") if u.strip().isdigit()
    ]

    # Configuraciones de TikTok
    CARPETA_DESCARGAS = os.getenv("CARPETA_DESCARGAS_TIKTOK", "./tiktok_downloads")
    CLEANUP_HOURS = int(os.getenv("CLEANUP_HOURS", 168))
    GRUPO_DESTINO = int(os.getenv("GRUPO_DESTINO_TIKTOK"))

except TypeError as e:
    logger.error("❌ Faltan variables en el archivo .env o tienen un formato incorrecto.")
    exit(1)

# Crear carpeta de descargas si no existe
if not os.path.exists(CARPETA_DESCARGAS):
    os.makedirs(CARPETA_DESCARGAS)
    logger.info(f"📁 Carpeta de TikTok creada: {CARPETA_DESCARGAS}")

# Inicializar cliente de Telethon con nombre de sesión único
client = TelegramClient("sesion_tiktok", API_ID, API_HASH)

# Regex para detectar cualquier enlace de TikTok (web o móvil)
TIKTOK_REGEX = r"(https?://)?(www\.|vm\.|vt\.)?tiktok\.com/(@[\w.-]+/video/\d+|\w+)"

def descargar_tiktok(url, carpeta_salida):
    """
    Descarga el video usando yt-dlp. 
    Por defecto para TikTok, yt-dlp extrae el video SIN marca de agua y SIN el final animado.
    """
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": f"{carpeta_salida}/%(id)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        archivo = ydl.prepare_filename(info_dict)
        
        # Extraer el título y limitarlo a 90 caracteres para evitar errores en Telegram
        titulo_completo = info_dict.get("title", "TikTok Video").strip()
        titulo = titulo_completo[:90] + "..." if len(titulo_completo) > 90 else titulo_completo
        
        return archivo, titulo

async def limpiar_carpeta_periodicamente():
    """Elimina videos locales más antiguos que CLEANUP_HOURS para liberar espacio"""
    while True:
        ahora = time.time()
        for filename in os.listdir(CARPETA_DESCARGAS):
            file_path = os.path.join(CARPETA_DESCARGAS, filename)
            if os.path.isfile(file_path):
                fecha_modificacion = os.stat(file_path).st_mtime
                tiempo_limite = CLEANUP_HOURS * 3600

                if fecha_modificacion < ahora - tiempo_limite:
                    try:
                        os.remove(file_path)
                        logger.info(f"🗑️ Archivo eliminado por antigüedad (+{CLEANUP_HOURS}h): {filename}")
                    except Exception as e:
                        logger.error(f"No se pudo eliminar {filename}: {e}")

        await asyncio.sleep(3600)

async def auto_actualizar_ytdlp():
    """Actualiza yt-dlp en segundo plano cada 24h para no perder compatibilidad con TikTok"""
    while True:
        await asyncio.sleep(86400)
        logger.info("🔄 Buscando actualizaciones de yt-dlp...")
        try:
            resultado = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
                capture_output=True,
                text=True,
            )

            if "Requirement already satisfied" in resultado.stdout and "Successfully installed" not in resultado.stdout:
                logger.info("⚡ yt-dlp ya está en su última versión.")
            else:
                logger.info("✅ ¡Nueva versión de yt-dlp instalada! Reiniciando el bot...")
                os.execv(sys.executable, [sys.executable] + sys.argv)

        except Exception as e:
            logger.error(f"❌ Error actualizando yt-dlp: {e}")

@client.on(events.NewMessage(chats=GRUPO_DESTINO))
async def manejador_tiktok(event):
    if event.sender_id not in USUARIOS_AUTORIZADOS:
        return

    texto = event.raw_text
    match = re.search(TIKTOK_REGEX, texto)

    if match:
        url = match.group(0)
        logger.info(f"🔗 Enlace detectado de {event.sender_id}: {url}")
        mensaje_estado = await event.reply("⏳ Descargando TikTok (Sin marca de agua)...")

        try:
            # Manejo de bucle asíncrono moderno (Python 3.14 compatible)
            loop = asyncio.get_running_loop()
            ruta_archivo, titulo = await loop.run_in_executor(
                None, descargar_tiktok, url, CARPETA_DESCARGAS
            )

            await mensaje_estado.edit("📤 Video descargado. Subiendo a Telegram...")

            await client.send_file(
                event.chat_id,
                ruta_archivo,
                caption=f"🎵 {titulo}",
                reply_to=event.message.id,
                supports_streaming=True,
            )

            await mensaje_estado.delete()
            logger.info("✅ TikTok subido exitosamente.")

        except Exception as e:
            await mensaje_estado.edit(f"❌ Ocurrió un error al procesar el video:\n`{str(e)}`")
            logger.error(f"Error procesando enlace {url}: {e}")

async def main():
    await client.start(phone=PHONE)

    logger.info("🤖 Bot de TikTok iniciado correctamente.")
    logger.info(f"🎯 Escuchando en el grupo: {GRUPO_DESTINO}")
    
    asyncio.create_task(limpiar_carpeta_periodicamente())
    asyncio.create_task(auto_actualizar_ytdlp())

    await client.run_until_disconnected()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot detenido manualmente por el usuario.")
