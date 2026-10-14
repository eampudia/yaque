import streamlit as st
from google import genai
import os
import random
import re
import shutil
import subprocess
import threading
import unicodedata
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title='YAQUE - ¿Y ahora qué?', page_icon="🤖", layout="wide")
st.title('🤖 YAQUE (¿Y ahora qué) - La App Auto-Evolutiva')

# Leer un secreto de varias fuentes: secretos de Streamlit, Colab o variables de entorno
def leer_secreto(nombre):
    try:
        if nombre in st.secrets:
            return st.secrets[nombre]
    except Exception:
        pass
    try:
        from google.colab import userdata
        valor = userdata.get(nombre)
        if valor:
            return valor
    except Exception:
        pass
    return os.environ.get(nombre, "")

google_api_key = leer_secreto("GOOGLE_API_KEY")

# Credenciales de GitHub
github_token = leer_secreto("GITHUB_TOKEN")
github_repo = leer_secreto("GITHUB_REPO")  # Formato: usuario/repositorio
github_branch = leer_secreto("GITHUB_BRANCH") or "master"

# Versión base de YAQUE: la app nunca la modifica ni la borra, solo la copia sobre master al hacer reset
RAMA_ORIGINAL = "ORIGINAL"
# Comando oculto: escrito en el campo de texto, guarda una bitácora y restaura la versión ORIGINAL
COMANDO_RESET = "haz un reset"


def url_repo():
    return f"https://oauth2:{github_token}@github.com/{github_repo}.git"


def git(*args):
    """Ejecuta un comando git. Si falla, lanza un error sin el token de GitHub en el mensaje."""
    try:
        return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout
    except subprocess.CalledProcessError as error:
        detalle = f"git {args[0]} falló: {(error.stderr or error.stdout or '').strip()}"
        if github_token:
            detalle = detalle.replace(github_token, "***")
        raise RuntimeError(detalle) from None


def configurar_git():
    git("config", "user.email", "yaque-bot@colab.com")
    git("config", "user.name", "YAQUE Bot")


def elegir_modelo(client):
    """Devuelve el modelo Gemini 'flash lite' de texto más reciente, o None si no hay ninguno."""
    # Solo modelos que generan texto: fuera los de voz, imagen, audio, tiempo real o embeddings
    palabras_excluidas = ('tts', 'image', 'audio', 'live', 'embedding', 'native')
    modelos_filtrados = []
    for m in client.models.list():
        nombre = m.name.lower()
        acciones = getattr(m, 'supported_actions', None)
        if acciones is not None and 'generateContent' not in acciones:
            continue
        if 'gemini' in nombre and 'flash' in nombre and 'lite' in nombre \
                and not any(p in nombre for p in palabras_excluidas):
            modelos_filtrados.append(m.name)

    if not modelos_filtrados:
        return None

    # Extraer la versión numérica del nombre (los modelos sin número, p. ej. '-latest', van al principio)
    def extraer_numero_version(nombre):
        coincidencias = re.findall(r'\d+\.\d+|\d+', nombre)
        if coincidencias:
            return float(coincidencias[0])
        return float('-inf')

    # Ordenar de menor a mayor versión (a igual versión, las estables por delante
    # de las 'preview'/'exp') y quedarnos con la más reciente
    def clave_orden(nombre):
        es_estable = not any(p in nombre.lower() for p in ('preview', 'exp'))
        return (extraer_numero_version(nombre), es_estable)

    return sorted(modelos_filtrados, key=clave_orden)[-1]


def describir_app(codigo):
    """Resume en una frase corta qué hace la app ahora mismo, para la bitácora."""
    descripcion_por_defecto = "Estado antes del reset"
    if not google_api_key:
        return descripcion_por_defecto
    try:
        client = genai.Client(api_key=google_api_key)
        modelo = elegir_modelo(client)
        if not modelo:
            return descripcion_por_defecto
        respuesta = client.models.generate_content(
            model=modelo,
            contents=(
                "Resume en una sola frase en español, de 10 palabras como máximo, qué hace esta "
                "aplicación de Streamlit. Responde solo con la frase, sin comillas ni punto final.\n\n"
                f"```python\n{codigo}\n```"
            ),
        )
        return (respuesta.text or "").strip().splitlines()[0][:120] or descripcion_por_defecto
    except Exception:
        return descripcion_por_defecto


def nombre_rama_bitacora(descripcion):
    """Ej: 'bitacora/2026-10-14-153000-escritorio-con-ventanas-y-reloj'."""
    texto = unicodedata.normalize("NFKD", descripcion).encode("ascii", "ignore").decode()
    resumen = re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")[:50].rstrip("-")
    fecha = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    return f"bitacora/{fecha}-{resumen}" if resumen else f"bitacora/{fecha}"


def hacer_reset():
    with st.status("Preparando el reset...", expanded=True) as estado:
        if not (github_token and github_repo):
            estado.update(label="No se puede hacer el reset", state="error")
            st.error("La aplicación no está conectada a GitHub.")
            return
        if github_branch == RAMA_ORIGINAL:
            estado.update(label="No se puede hacer el reset", state="error")
            st.error(f"La rama de trabajo no puede ser {RAMA_ORIGINAL}.")
            return
        try:
            # 1. Guardar la versión actual en una rama de bitácora
            estado.update(label="Escribiendo la bitácora...")
            estado.write("📝 Describiendo la versión actual para la bitácora...")
            descripcion = describir_app(codigo_actual)
            rama = nombre_rama_bitacora(descripcion)

            estado.write(f"📚 Guardando la versión actual en la rama {rama}...")
            configurar_git()
            git("add", "app.py")
            git("commit", "--allow-empty", "-m", f"Bitácora: {descripcion}")
            git("push", url_repo(), f"HEAD:refs/heads/{rama}")

            # 2. Sobrescribir la rama de trabajo con ORIGINAL (ORIGINAL solo se lee)
            estado.update(label="Volviendo a la versión ORIGINAL...")
            estado.write(f"⏪ Sobrescribiendo {github_branch} con {RAMA_ORIGINAL}...")
            git("fetch", url_repo(), RAMA_ORIGINAL)
            git("push", "--force", url_repo(), f"FETCH_HEAD:refs/heads/{github_branch}")
            git("reset", "--hard", "FETCH_HEAD")

            st.session_state.clear()
            estado.update(label="¡Reset completado!", state="complete")
            st.success(f"YAQUE ha vuelto a su versión ORIGINAL. La versión anterior está guardada en la rama '{rama}'. Recarga la página.")
        except Exception as e:
            estado.update(label="Algo ha salido mal en el reset", state="error")
            st.error(f"Ocurrió un error al hacer el reset: {e}")

# 1. Leer el código actual de app.py
try:
    with open("app.py", "r", encoding="utf-8") as f:
        codigo_actual = f.read()
except Exception as e:
    codigo_actual = "# Error leyendo el archivo app.py"

# Mostrar el área principal de la app auto-generada
st.markdown("--- (Inicio de la zona auto-generada) ---")

# --- NUEVA FUNCIONALIDAD: Calculador de Constelación Astral ---
st.subheader("✨ Calculador de Constelación Astral")
st.write("Descubre cuál es tu constelación astral y lee tu predicción cósmica basada en tu fecha de nacimiento.")

col1, col2 = st.columns(2)
with col1:
    nombre_usuario = st.text_input("Introduce tu nombre:", "Viajero Estelar")
    fecha_nacimiento = st.date_input("Selecciona tu fecha de nacimiento:", datetime(1995, 6, 15))

if st.button("Consultar los Astros"):
    mes = fecha_nacimiento.month
    dia = fecha_nacimiento.day
    
    # Lógica sencilla para determinar constelación/signo astral
    if (mes == 3 and dia >= 21) or (mes == 4 and dia <= 19):
        constelacion, elemento = "Aries (El Carnero Estelar)", "Fuego"
    elif (mes == 4 and dia >= 20) or (mes == 5 and dia <= 20):
        constelacion, elemento = "Tauro (El Toro Celestial)", "Tierra"
    elif (mes == 5 and dia >= 21) or (mes == 6 and dia <= 20):
        constelacion, elemento = "Géminis (Los Gemelos Cósmicos)", "Aire"
    elif (mes == 6 and dia >= 21) or (mes == 7 and dia <= 22):
        constelacion, elemento = "Cáncer (El Cangrejo Lunar)", "Agua"
    elif (mes == 7 and dia >= 23) or (mes == 8 and dia <= 22):
        constelacion, elemento = "Leo (El León de Nebulosa)", "Fuego"
    elif (mes == 8 and dia >= 23) or (mes == 9 and dia <= 22):
        constelacion, elemento = "Virgo (La Doncella de las Estrellas)", "Tierra"
    elif (mes == 9 and dia >= 23) or (mes == 10 and dia <= 22):
        constelacion, elemento = "Libra (La Balanza Galáctica)", "Aire"
    elif (mes == 10 and dia >= 23) or (mes == 11 and dia <= 21):
        constelacion, elemento = "Escorpio (El Aguijón Cósmico)", "Agua"
    elif (mes == 11 and dia >= 22) or (mes == 12 and dia <= 21):
        constelacion, elemento = "Sagitario (El Arquero Astral)", "Fuego"
    elif (mes == 12 and dia >= 22) or (mes == 1 and dia <= 19):
        constelacion, elemento = "Capricornio (La Cabra de Cúmulo)", "Tierra"
    elif (mes == 1 and dia >= 20) or (mes == 2 and dia <= 18):
        constelacion, elemento = "Acuario (El Portador de Iones)", "Aire"
    else:
        constelacion, elemento = "Piscis (Los Peces de la Vía Láctea)", "Agua"

    st.success(f"¡Saludos, **{nombre_usuario}**!")
    st.markdown(f"🌌 Tu constelación astral es **{constelacion}** bajo el elemento **{elemento}**.")
    
    # Generar predicción aleatoria pero temática
    predicciones = [
        "Las alineaciones estelares indican que hoy es un día excelente para iniciar nuevos proyectos tecnológicos y evolucionar tu código mental.",
        "Un cúmulo cercano de energía te otorgará una claridad inusitada para resolver problemas complejos antes de que termine el ciclo lunar.",
        "La gravedad de tus pensamientos atraerá buenas vibraciones y sincronicidades inesperadas en tu entorno digital y personal.",
        "Los destellos de una supernova lejana iluminan tu creatividad; aprovecha para diseñar, construir o pedir un cambio radical a YAQUE."
    ]
    st.info(f"🔮 **Oráculo Cósmico:** {random.choice(predicciones)}")

st.markdown("--- (Fin de la zona auto-generada) ---")

# Frases para entretener mientras Gemini piensa
FRASES_MIENTRAS_PIENSA = [
    "Simplificando las reglas...",
    "Chirriando los caminos...",
    "Desenredando los bucles...",
    "Puliendo las llaves...",
    "Afinando los píxeles...",
    "Despertando a las variables...",
    "Barnizando las funciones...",
    "Negociando con los corchetes...",
    "Alineando los astros del código...",
    "Encerando los botones...",
    "Calibrando la imaginación...",
    "Ordenando los paréntesis por tamaño...",
    "Regando el árbol de dependencias...",
    "Peinando las indentaciones...",
    "Consultando al oráculo de Python...",
    "Atornillando los widgets...",
]

# Sección fija al final de la página para la auto-evolución
st.write("### 🛠️ ¿Y ahora qué hacemos?")
requerimiento = st.text_area("Describe la nueva funcionalidad o cambio que quieres añadir a esta aplicación:", "", placeholder="Ej: Añade un gráfico de barras, un convertidor de unidades, o un juego de tres en raya en la zona intermedia...")

if st.button("Evolucionar Aplicación"):
    if requerimiento.strip().lower().rstrip(".!") == COMANDO_RESET:
        hacer_reset()
    elif not google_api_key:
        st.error("La aplicación no está configurada para auto-evolucionar.")
    elif not requerimiento:
        st.warning("Por favor, escribe un requerimiento para modificar la app.")
    else:
        with st.status("YAQUE se pone manos a la obra...", expanded=True) as estado:
            try:
                client = genai.Client(api_key=google_api_key)

                # 1. Descargar todos los modelos disponibles desde la API
                estado.write("🔭 Buscando modelos de Gemini disponibles...")
                modelo_elegido = elegir_modelo(client)
                if not modelo_elegido:
                    estado.update(label="No hay modelos disponibles", state="error")
                    st.error("No se encontraron modelos Gemini 'flash lite' de texto en tu cuenta.")
                    st.stop()
                estado.write(f"🧠 Elegido el modelo {modelo_elegido}")

                prompt = (
                    f"Eres un programador experto en Python.\n"
                    f"Tu tarea es modificar el código de la aplicación de Python actual para añadir una nueva funcionalidad.\n\n"
                    f"CÓDIGO ACTUAL DE LA APLICACIÓN:\n"
                    f"```python\n{codigo_actual}\n```\n\n"
                    f"REQUERIMIENTO DEL USUARIO:\n"
                    f"{requerimiento}\n\n"
                    f"INSTRUCCIONES CRÍTICAS:\n"
                    f"1. Debes conservar SIEMPRE intacto el mecanismo de lectura de 'app.py', los secretos de API, las funciones auxiliares (git, elegir_modelo, hacer_reset, etc.), el comando oculto de reset y la sección final de '¿Y ahora qué hacemos?' para que la aplicación pueda seguir modificándose recursivamente.\n"
                    f"2. Integra la nueva funcionalidad de forma limpia e interactiva dentro de la sección intermedia de la app.\n"
                    f"3. Devuelve ÚNICAMENTE el código de Python completo y válido de la nueva versión de 'app.py'. No incluyas explicaciones en lenguaje natural, solo el bloque de código de Python puro sin marcas markdown extras de bloques de código en los extremos de la respuesta (no agregues ```python al inicio ni ``` al final). Devuelve solo el código ejecutable directo.\n"
                    f"4. Si usas st.session_state, inicializa CADA clave por separado (con 'if clave not in st.session_state' o setdefault) y lee los diccionarios con .get(), porque el estado de sesiones anteriores puede no tener las claves nuevas.\n"
                )
                
                # Llamar a Gemini en un hilo aparte para ir mostrando frases mientras responde
                estado.write("✍️ Pidiendo a Gemini que reescriba la aplicación...")
                resultado = {}

                def llamar_a_gemini():
                    try:
                        resultado["respuesta"] = client.models.generate_content(
                            model=modelo_elegido,
                            contents=prompt,
                        )
                    except Exception as error_gemini:
                        resultado["error"] = error_gemini

                hilo = threading.Thread(target=llamar_a_gemini)
                hilo.start()
                frases = random.sample(FRASES_MIENTRAS_PIENSA, len(FRASES_MIENTRAS_PIENSA))
                indice = 0
                while hilo.is_alive():
                    estado.update(label=frases[indice % len(frases)])
                    indice += 1
                    hilo.join(timeout=2)

                if "error" in resultado:
                    raise resultado["error"]
                response = resultado["respuesta"]

                estado.update(label="Revisando el código nuevo...")
                estado.write("🔍 Comprobando que el código generado es válido...")

                # Gemini puede responder sin texto (bloqueo de seguridad, límite de tokens...)
                if not response.text:
                    motivo = "desconocido"
                    if response.candidates:
                        motivo = response.candidates[0].finish_reason
                    elif response.prompt_feedback:
                        motivo = response.prompt_feedback.block_reason
                    estado.update(label="Gemini no ha devuelto código", state="error")
                    st.error(f"Gemini ({modelo_elegido}) respondió sin código. Motivo: {motivo}. No se ha modificado app.py.")
                    st.stop()

                nuevo_codigo = response.text.strip()

                # Limpiar posibles bloques markdown accidentales del LLM
                if nuevo_codigo.startswith("```python"):
                    nuevo_codigo = nuevo_codigo[9:]
                if nuevo_codigo.endswith("```"):
                    nuevo_codigo = nuevo_codigo[:-3]
                nuevo_codigo = nuevo_codigo.strip()

                # Validar que el código generado es Python válido antes de sobrescribir nada
                try:
                    compile(nuevo_codigo, "app.py", "exec")
                except SyntaxError as syntax_error:
                    estado.update(label="El código generado no era válido", state="error")
                    st.error(f"El código generado no es válido, no se ha modificado app.py: {syntax_error}")
                    st.stop()

                # Guardar una copia de seguridad de la versión anterior
                estado.write("💾 Guardando copia de seguridad y escribiendo el código nuevo...")
                shutil.copyfile("app.py", "app.py.bak")

                # Guardar el nuevo código en app.py
                with open("app.py", "w", encoding="utf-8") as f:
                    f.write(nuevo_codigo)

                # Empezar con un estado limpio: el de la versión anterior puede no encajar con el código nuevo
                st.session_state.clear()

                # Sincronizar automáticamente con GitHub si están las credenciales
                if github_token and github_repo and github_branch != RAMA_ORIGINAL:
                    try:
                        estado.update(label="Subiendo los cambios a GitHub...")
                        estado.write("🚀 Subiendo los cambios a GitHub...")
                        configurar_git()
                        git("add", "app.py")
                        git("commit", "-m", f"YAQUE Auto-update: {requerimiento[:50]}")
                        git("push", url_repo(), f"HEAD:refs/heads/{github_branch}")
                        estado.write("✅ Sincronizado con GitHub")
                    except Exception as git_error:
                        st.warning(f"El código se actualizó localmente pero falló la subida a GitHub: {git_error}")

                estado.update(label="¡YAQUE ha evolucionado!", state="complete")
                st.success("¡Código actualizado con éxito! Recarga la página de Streamlit para ver los cambios aplicados en caliente.")

            except Exception as e:
                estado.update(label="Algo ha salido mal", state="error")
                st.error(f"Ocurrió un error al procesar la actualización: {e}")