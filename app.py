import streamlit as st

# Configuración de la página
st.set_page_config(page_title='YAQUE - ¿Y ahora qué?', page_icon="🤖", layout="wide")
st.title('🤖 YAQUE (¿Y ahora qué) - La App Auto-Evolutiva')

import nucleo  # noqa: E402  (después de set_page_config)

# La parte que se va creando sola vive en zona.py; nucleo.py es fijo y Gemini nunca lo ve ni lo cambia
nucleo.cargar_secretos()
nucleo.mostrar_zona()
nucleo.seccion_evolucion()
