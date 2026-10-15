import io
from PIL import Image, ImageOps, ImageEnhance
st.subheader('Editor Básico de Imágenes')
st.write('Sube una imagen y aplica filtros o transformaciones básicas.')
if 'editor_fotos_imagen' not in st.session_state:
    st.session_state.editor_fotos_imagen = None
archivo = st.file_uploader('Sube tu imagen:', type=['jpg', 'jpeg', 'png'], key='editor_fotos_uploader')
if archivo is not None:
    st.session_state.editor_fotos_imagen = Image.open(archivo)
if st.session_state.editor_fotos_imagen is not None:
    img = st.session_state.editor_fotos_imagen
    st.image(img, caption='Imagen actual', use_column_width=True)
    opcion = st.selectbox('¿Qué quieres hacer?', ['Ninguna', 'Escala de grises', 'Rotar 90°', 'Invertir colores', 'Aumentar brillo'], key='editor_fotos_opcion')
    if opcion == 'Escala de grises':
        img = ImageOps.grayscale(img)
    elif opcion == 'Rotar 90°':
        img = img.rotate(90, expand=True)
    elif opcion == 'Invertir colores':
        img = ImageOps.invert(img.convert('RGB'))
    elif opcion == 'Aumentar brillo':
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.3)
    st.image(img, caption='Imagen editada', use_column_width=True)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    st.download_button('Descargar imagen editada', data=buf.getvalue(), file_name='imagen_editada.png', mime='image/png', key='editor_fotos_download')
