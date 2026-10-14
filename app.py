import streamlit as st

import nucleo

# Configuración de la página, con el nombre que Gemini le ha puesto a la app según lo que contiene
# y el aspecto (icono, ancho, subtítulo y estilos) que se ha pedido por el chat
nombre = nucleo.leer_nombre()
apariencia = nucleo.leer_apariencia()
st.set_page_config(page_title=f'{nombre} - ¿Y ahora qué?', page_icon=apariencia["icono"], layout=apariencia["ancho"])
nucleo.aplicar_estilo()
if nombre == nucleo.NOMBRE_POR_DEFECTO:
    st.title(f'{apariencia["icono"]} YAQUE (¿Y ahora qué) - La App Auto-Evolutiva')
else:
    st.title(f'{apariencia["icono"]} {nombre}')
subtitulo = apariencia["subtitulo"] or (
    '' if nombre == nucleo.NOMBRE_POR_DEFECTO else 'Una app auto-evolutiva de YAQUE (¿Y ahora qué?)')
if subtitulo:
    st.caption(subtitulo)

# Lo que se va creando solo vive en funcionalidades/ (una pestaña cada una); nucleo.py es fijo y Gemini nunca lo ve ni lo cambia
nucleo.cargar_secretos()
nucleo.pedir_nombre()
nucleo.mostrar_funcionalidades()
nucleo.seccion_evolucion()
nucleo.mostrar_conectados()
