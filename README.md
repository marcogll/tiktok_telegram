# 🎵 Telegram TikTok Downloader Bot

Bot / userbot automatizado en Python que monitorea un grupo específico de Telegram y descarga videos de TikTok enviados por usuarios autorizados.

Gracias a la integración con `yt-dlp`, los videos se descargan sin marca de agua y sin la pantalla final animada del logo de TikTok, de forma nativa.

---

## ✨ Características Principales

* 🚫 **Sin Marca de Agua**: Extrae el archivo multimedia original desde los servidores de TikTok, evitando compresión adicional y marcas de agua.
* 🔒 **Control de Acceso Estricto**: Solo procesa enlaces enviados por usuarios autorizados (mediante su ID de Telegram).
* 🎯 **Monitoreo Aislado**: Opera silenciosamente en un grupo específico configurado por variables de entorno.
* 🧹 **Auto-Limpieza de Disco**: Recolector en segundo plano que elimina los videos locales tras X horas, evitando saturación de almacenamiento.
* 🔄 **Auto-Actualización Inteligente**: Ejecuta una tarea cada 24 horas para actualizar `yt-dlp` vía `pip` y reinicia automáticamente si hay una nueva versión.
* 👯 **Convive con otros Bots**: Utiliza un archivo de sesión independiente (`sesion_tiktok.session`) y variables de entorno únicas, permitiendo ejecutarlo junto a otros bots sin conflictos.

---

## 🛠️ Requisitos Previos

* Python 3.9 o superior (testeado compatible con Python 3.14).
* FFmpeg instalado en el sistema (recomendado por `yt-dlp`).

Instalación de FFmpeg según sistema:

* **Arch Linux**:

  ```bash
  sudo pacman -S ffmpeg
  ```

* **Ubuntu / Debian**:

  ```bash
  sudo apt install ffmpeg
  ```

* **macOS**:

  ```bash
  brew install ffmpeg
  ```

* Credenciales de la API de Telegram (`API_ID` y `API_HASH`) obtenidas en `my.telegram.org`.

---

## 📦 Instalación

1. Clona o descarga los archivos en tu máquina local.

2. Crea un entorno virtual (recomendado):

   ```bash
   python -m venv .venv
   ```

3. Activa el entorno virtual:

   * Linux / macOS:

     ```bash
     source .venv/bin/activate
     ```

   * Windows:

     ```bash
     .venv\Scripts\activate
     ```

4. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuración

Copia o renombra el archivo `.env.example` a `.env` en el mismo directorio que el script y añade tu configuración.

> [!IMPORTANT]
> Nunca compartas tu archivo `.env`, ya que contiene credenciales de acceso a Telegram.

```env
# ============================================
# Credenciales de Telegram
# ============================================
API_ID=tu_api_id
API_HASH=tu_api_hash
PHONE=+521234567890

# Usuarios permitidos (IDs separados por comas)
USUARIOS_AUTORIZADOS=123456789,987654321

# ============================================
# Configuración del bot de TikTok
# ============================================
LOG_LEVEL=INFO
CLEANUP_HOURS=168

# ID del grupo de Telegram donde escuchará enlaces (Suele llevar signo menos)
GRUPO_DESTINO_TIKTOK=-1009876543210
CARPETA_DESCARGAS_TIKTOK=./tiktok_downloads
```

---

## 🚀 Uso

Asegúrate de tener el entorno virtual activado y ejecuta:

```bash
python bot_tiktok.py
```

---

## 🔑 Primer Inicio de Sesión

En la primera ejecución, la terminal solicitará un código de autenticación de 5 dígitos enviado por Telegram a la app oficial.

Una vez introducido, se creará el archivo `sesion_tiktok.session`. A partir de ese momento, el bot iniciará automáticamente sin volver a pedir autenticación.

---

## 📝 Notas Adicionales

* **Enlaces Soportados**: Reconoce formatos cortos (`vm.tiktok.com`, `vt.tiktok.com`) y enlaces largos (`tiktok.com/@usuario/...`).
* **Límites de Telegram**: Los títulos pueden incluir descripciones y hashtags extensos. El bot recorta automáticamente a 90 caracteres para evitar errores en la API al enviar mensajes.

