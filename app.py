import streamlit as st
from google import genai
import os
import subprocess

# Configuración de la página
st.set_page_config(page_title='YAQUE - ¿Y ahora qué?', page_icon="🤖", layout="wide")
st.title('🤖 YAQUE (¿Y ahora qué) - La App Auto-Evolutiva')

# Intentar obtener la API Key de varias fuentes seguras
google_api_key = ""
try:
    from google.colab import userdata
    google_api_key = userdata.get("GOOGLE_API_KEY")
except Exception:
    pass

if not google_api_key:
    google_api_key = os.environ.get("GOOGLE_API_KEY", "")

# Intentar obtener credenciales de GitHub desde secretos
github_token = ""
github_repo = ""  # Formato: usuario/repositorio
try:
    from google.colab import userdata
    github_token = userdata.get("GITHUB_TOKEN")
    github_repo = userdata.get("GITHUB_REPO")
except Exception:
    pass

# 1. Leer el código actual de app.py
try:
    with open("app.py", "r", encoding="utf-8") as f:
        codigo_actual = f.read()
except Exception as e:
    codigo_actual = "# Error leyendo el archivo app.py"

with st.sidebar:
    st.header("⚙️ Estado de la Aplicación")
    if google_api_key:
        st.success("Gemini API Key: Conectada")
    else:
        st.error("Falta GOOGLE_API_KEY")
    
    if github_token and github_repo:
        st.success(f"GitHub Repo: {github_repo} conectado")
    else:
        st.warning("Para subir cambios a GitHub, configura GITHUB_TOKEN y GITHUB_REPO en los secretos.")

    st.subheader("Código Fuente Actual")
    st.code(codigo_actual, language="python")

# Mostrar el área principal de la app auto-generada
st.markdown("--- (Inicio de la zona auto-generada) ---")
# Aquí puedes poner la lógica interactiva o componentes que la app se vaya creando a sí misma.
st.info("Esta es la versión inicial de YAQUE. ¡Pídeme añadirle cualquier funcionalidad usando el campo de abajo!")
st.markdown("--- (Fin de la zona auto-generada) ---")

# Sección fija al final de la página para la auto-evolución
st.write("### 🛠️ ¿Y ahora qué hacemos?")
requerimiento = st.text_area("Describe la nueva funcionalidad o cambio que quieres añadir a esta aplicación:", "", placeholder="Ej: Añade un gráfico de barras, un convertidor de unidades, o un juego de tres en raya en la zona intermedia...")

if st.button("Evolucionar Aplicación"):
    if not google_api_key:
        st.error("Necesitas configurar tu GOOGLE_API_KEY en los secretos para poder auto-evolucionar.")
    elif not requerimiento:
        st.warning("Por favor, escribe un requerimiento para modificar la app.")
    else:
        with st.spinner("YAQUE está reescribiendo su propio código fuente..."):
            try:
                client = genai.Client(api_key=google_api_key)
                
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
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=prompt,
                )
                
                nuevo_codigo = response.text.strip()
                
                # Limpiar posibles bloques markdown accidentales del LLM
                if nuevo_codigo.startswith("```python"):
                    nuevo_codigo = nuevo_codigo[9:]
                if nuevo_codigo.endswith("```"):
                    nuevo_codigo = nuevo_codigo[:-3]
                nuevo_codigo = nuevo_codigo.strip()
                
                # Guardar el nuevo código en app.py
                with open("app.py", "w", encoding="utf-8") as f:
                    f.write(nuevo_codigo)
                
                st.success("¡Código actualizado con éxito! Recarga la página de Streamlit para ver los cambios aplicados en caliente.")
                st.code(nuevo_codigo[:1000] + "\n... (código guardado con éxito)", language="python")

                # Sincronizar automáticamente con GitHub si están las credenciales
                if github_token and github_repo:
                    try:
                        st.info("Subiendo los cambios a GitHub...")
                        # Configurar git en silencio
                        subprocess.run(["git", "config", "--global", "user.email", "yaque-bot@colab.com"], check=True)
                        subprocess.run(["git", "config", "--global", "user.name", "YAQUE Bot"], check=True)
                        
                        # Intentar clonar/actualizar repo local si no está inicializado
                        # Para simplicidad en este script, hacemos un push directo si es un repo clonado
                        subprocess.run(["git", "add", "app.py"], check=True)
                        subprocess.run(["git", "commit", "-m", f"YAQUE Auto-update: {requerimiento[:50]}"], check=True)
                        
                        url_con_token = f"https://oauth2:{github_token}@github.com/{github_repo}.git"
                        subprocess.run(["git", "push", url_con_token, "HEAD:main"], check=True)
                        st.success("¡Sincronizado correctamente con tu repositorio de GitHub!")
                    except Exception as git_error:
                        st.warning(f"El código se actualizó localmente pero falló la subida a GitHub: {git_error}")

            except Exception as e:
                st.error(f"Ocurrió un error al procesar la actualización: {e}")
