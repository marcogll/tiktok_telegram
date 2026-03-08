# 🎵 Telegram Social Media Downloader Bot

Bot / userbot automatizado en Python que monitorea un grupo específico de Telegram y descarga videos de TikTok e Instagram enviados por usuarios autorizados.

Gracias a la integración con `yt-dlp`, los videos se descargan sin marca de agua.

---

## ✨ Características Principales

* 🎯 **Multi-Plataforma**: Soporta TikTok (sin marca de agua), Instagram (reels, posts, stories), Facebook y X (Twitter).
* 🔒 **Control de Acceso Estricto**: Solo procesa enlaces enviados por usuarios autorizados (mediante su ID de Telegram).
* 🧹 **Auto-Limpieza de Disco**: Recolector en segundo plano que elimina los videos locales tras X horas.
* 🔄 **Auto-Actualización Inteligente**: Actualiza `yt-dlp` cada 24h y reinicia automáticamente si hay nueva versión.
* ⚙️ **Inicio con Sistema**: Script de arranque y servicio systemd incluidos.

---

## 🛠️ Requisitos Previos

* Python 3.9 o superior
* FFmpeg instalado en el sistema

Instalación de FFmpeg según sistema:

* **Arch Linux**: `sudo pacman -S ffmpeg`
* **Ubuntu / Debian**: `sudo apt install ffmpeg`
* **macOS**: `brew install ffmpeg`

---

## 📦 Instalación

1. Clona o descarga los archivos.

2. Crea un entorno virtual:
   ```bash
   python -m venv .venv
   ```

3. Activa el entorno virtual:
   ```bash
   source .venv/bin/activate
   ```

4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuración

### Obtener credenciales de Telegram

Para usar el bot necesitas crear una aplicación en Telegram:

1. Ve a [my.telegram.org](https://my.telegram.org) e inicia sesión con tu número de teléfono.
2. Click en **"API Development Tools"**.
3. Completa los datos:
   - **App title**: Nombre de tu aplicación (ej: TikTok Downloader Bot)
   - **Short name**: Nombre corto (ej: tiktokdl)
   - **URL**: Tu repositorio o sitio web (puede ser vacío)
   - **Platform**: Mobile
   - **Description**: Descripción breve (puedes poner "Bot para descargar videos")
4. Click en **"Create application"**.
5. Copia los valores:
   - **api_id**: Es un número (ej: `1234567`)
   - **api_hash**: Es una cadena larga de letras y números (ej: `a1b2c3d4e5f6...`)

**⚠️ IMPORTANTE**: Nunca compartas tu `API_HASH`. Es equivalente a una contraseña.

### Configurar variables de entorno

Copia `.env.example` a `.env` y configura:

```env
# Credenciales de Telegram
API_ID=tu_api_id
API_HASH=tu_api_hash
PHONE=+521234567890

# Usuarios permitidos (IDs separados por comas)
USUARIOS_AUTORIZADOS=123456789,987654321

# Configuración
LOG_LEVEL=INFO
CLEANUP_HOURS=168

# Grupo donde escuchará enlaces
GRUPO_DESTINO_TIKTOK=-1009876543210
CARPETA_DESCARGAS_TIKTOK=./tiktok_downloads
```

---

## 🚀 Uso

### Manual:
```bash
./start_bot.sh
```

### Con systemd (inicio automático):
```bash
sudo cp tiktok-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tiktok-bot
sudo systemctl start tiktok-bot
```

---

## 📝 Comandos útiles

* `sudo systemctl status tiktok-bot` - Ver estado
* `sudo systemctl restart tiktok-bot` - Reiniciar
* `tail -f bot.log` - Ver logs en tiempo real

---

## 📋 Enlaces soportados

* **TikTok**: `tiktok.com/@usuario/video/xxx`, `vm.tiktok.com/xxx`, `vt.tiktok.com/xxx`
* **Instagram**: `instagram.com/reel/xxx`, `instagram.com/p/xxx`, `instagram.com/stories/xxx`
* **Facebook**: `facebook.com/watch/?v=xxx`, `facebook.com/share/v/xxx`, `fb.watch/xxx`
* **X (Twitter)**: `x.com/usuario/status/xxx`, `twitter.com/usuario/status/xxx`
