import streamlit as st

import nucleo

# Configuración de la página, con el nombre que Gemini le ha puesto a la app según lo que contiene
nombre = nucleo.leer_nombre()
st.set_page_config(page_title=f'{nombre} - ¿Y ahora qué?', page_icon="🤖", layout="wide")
if nombre == nucleo.NOMBRE_POR_DEFECTO:
    st.title('🤖 YAQUE (¿Y ahora qué) - La App Auto-Evolutiva')
else:
    st.title(f'🤖 {nombre}')
    st.caption('Una app auto-evolutiva de YAQUE (¿Y ahora qué?)')

# La parte que se va creando sola vive en zona.py; nucleo.py es fijo y Gemini nunca lo ve ni lo cambia
nucleo.cargar_secretos()
nucleo.pedir_nombre()
nucleo.mostrar_conectados()
nucleo.mostrar_zona()
nucleo.seccion_evolucion()
