import streamlit as st
from google import genai
import os
import random
import re
import shutil
import subprocess
import threading

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

# 1. Leer el código actual de app.py
try:
    with open("app.py", "r", encoding="utf-8") as f:
        codigo_actual = f.read()
except Exception as e:
    codigo_actual = "# Error leyendo el archivo app.py"

# Mostrar el área principal de la app auto-generada
st.markdown("--- (Inicio de la zona auto-generada) ---")
# Aquí puedes poner la lógica interactiva o componentes que la app se vaya creando a sí misma.
st.info("Esta es la versión inicial de YAQUE. ¡Pídeme añadirle cualquier funcionalidad usando el campo de abajo!")
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
    if not google_api_key:
        st.error("La aplicación no está configurada para auto-evolucionar.")
    elif not requerimiento:
        st.warning("Por favor, escribe un requerimiento para modificar la app.")
    else:
        with st.status("YAQUE se pone manos a la obra...", expanded=True) as estado:
            try:
                client = genai.Client(api_key=google_api_key)

                # 1. Descargar todos los modelos disponibles desde la API
                estado.write("🔭 Buscando modelos de Gemini disponibles...")
                modelos_disponibles = []
                for m in client.models.list():
                    if 'gemini' in m.name.lower():
                        modelos_disponibles.append(m.name)

                if not modelos_disponibles:
                    estado.update(label="No hay modelos disponibles", state="error")
                    st.error("No se encontraron modelos de Gemini disponibles en esta cuenta.")
                    st.stop()

                # 2. Filtrar únicamente por la coincidencia estricta de 'flash' y 'lite'
                modelos_filtrados = [
                    m for m in modelos_disponibles
                    if 'flash' in m.lower() and 'lite' in m.lower()
                ]

                if not modelos_filtrados:
                    estado.update(label="No hay modelos disponibles", state="error")
                    st.error("No se encontraron modelos que coincidan con 'flash' y 'lite' en tu cuenta.")
                    st.stop()

                # 3. Función dinámica para extraer la versión numérica del string
                #    (los modelos sin número, p. ej. '-latest', van al principio)
                def extraer_numero_version(nombre):
                    coincidencias = re.findall(r'\d+\.\d+|\d+', nombre)
                    if coincidencias:
                        return float(coincidencias[0])
                    return float('-inf')

                # 4. Ordenar de menor a mayor versión y quedarnos con la más reciente
                modelos_ordenados = sorted(modelos_filtrados, key=extraer_numero_version)
                modelo_elegido = modelos_ordenados[-1]
                estado.write(f"🧠 Elegido el modelo {modelo_elegido}")

                prompt = (
                    f"Eres un programador experto en Python.\n"
                    f"Tu tarea es modificar el código de la aplicación de Python actual para añadir una nueva funcionalidad.\n\n"
                    f"CÓDIGO ACTUAL DE LA APLICACIÓN:\n"
                    f"```python\n{codigo_actual}\n```\n\n"
                    f"REQUERIMIENTO DEL USUARIO:\n"
                    f"{requerimiento}\n\n"
                    f"INSTRUCCIONES CRÍTICAS:\n"
                    f"1. Debes conservar SIEMPRE intacto el mecanismo de lectura de 'app.py', los secretos de API, y la sección final de '¿Y ahora qué hacemos?' para que la aplicación pueda seguir modificándose recursivamente.\n"
                    f"2. Integra la nueva funcionalidad de forma limpia e interactiva dentro de la sección intermedia de la app.\n"
                    f"3. Devuelve ÚNICAMENTE el código de Python completo y válido de la nueva versión de 'app.py'. No incluyas explicaciones en lenguaje natural, solo el bloque de código de Python puro sin marcas markdown extras de bloques de código en los extremos de la respuesta (no agregues ```python al inicio ni ``` al final). Devuelve solo el código ejecutable directo.\n"
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

                # Sincronizar automáticamente con GitHub si están las credenciales
                if github_token and github_repo:
                    try:
                        estado.update(label="Subiendo los cambios a GitHub...")
                        estado.write("🚀 Subiendo los cambios a GitHub...")
                        # Configurar git en silencio
                        subprocess.run(["git", "config", "--global", "user.email", "yaque-bot@colab.com"], check=True)
                        subprocess.run(["git", "config", "--global", "user.name", "YAQUE Bot"], check=True)
                        
                        # Intentar clonar/actualizar repo local si no está inicializado
                        # Para simplicidad en este script, hacemos un push directo si es un repo clonado
                        subprocess.run(["git", "add", "app.py"], check=True)
                        subprocess.run(["git", "commit", "-m", f"YAQUE Auto-update: {requerimiento[:50]}"], check=True)
                        
                        url_con_token = f"https://oauth2:{github_token}@github.com/{github_repo}.git"
                        subprocess.run(["git", "push", url_con_token, f"HEAD:{github_branch}"], check=True, capture_output=True, text=True)
                        estado.write("✅ Sincronizado con GitHub")
                    except Exception as git_error:
                        # Ocultar el token: el mensaje de error incluye el comando con la URL
                        detalle = str(git_error)
                        if isinstance(git_error, subprocess.CalledProcessError) and git_error.stderr:
                            detalle += f"\n{git_error.stderr}"
                        detalle = detalle.replace(github_token, "***")
                        st.warning(f"El código se actualizó localmente pero falló la subida a GitHub: {detalle}")

                estado.update(label="¡YAQUE ha evolucionado!", state="complete")
                st.success("¡Código actualizado con éxito! Recarga la página de Streamlit para ver los cambios aplicados en caliente.")

            except Exception as e:
                estado.update(label="Algo ha salido mal", state="error")
                st.error(f"Ocurrió un error al procesar la actualización: {e}")
