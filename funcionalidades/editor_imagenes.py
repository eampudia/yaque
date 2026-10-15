from PIL import Image, ImageEnhance, ImageOps
import io

if 'editor_img_archivo' not in st.session_state:
    st.session_state.editor_img_archivo = None
if 'editor_img_brillo' not in st.session_state:
    st.session_state.editor_img_brillo = 1.0
if 'editor_img_contraste' not in st.session_state:
    st.session_state.editor_img_contraste = 1.0
if 'editor_img_rotacion' not in st.session_state:
    st.session_state.editor_img_rotacion = 0
if 'editor_img_filtro' not in st.session_state:
    st.session_state.editor_img_filtro = 'Normal'

st.markdown('### 🖼️ Editor de Imágenes Creativo')
st.markdown('Sube una imagen, ajusta sus propiedades y aplica filtros básicos de forma sencilla.')

archivo_subido = st.file_uploader('Sube tu imagen (PNG, JPG, JPEG)', type=['png', 'jpg', 'jpeg'], key='editor_img_uploader')

if archivo_subido is not None:
    try:
        imagen_original = Image.open(archivo_subido)
        st.session_state.editor_img_archivo = archivo_subido
    except Exception as e:
        st.error('No se pudo cargar la imagen. Comprueba el formato.')
        imagen_original = None
else:
    imagen_original = None

if imagen_original:
    col_cont1, col_cont2 = st.columns([1, 1])
    
    with col_cont1:
        st.markdown('#### Controles de Edición')
        st.session_state.editor_img_brillo = st.slider('Brillo', 0.1, 2.0, 1.0, 0.1, key='editor_img_slider_brillo')
        st.session_state.editor_img_contraste = st.slider('Contraste', 0.1, 2.0, 1.0, 0.1, key='editor_img_slider_contraste')
        st.session_state.editor_img_rotacion = st.selectbox('Rotación', [0, 90, 180, 270], key='editor_img_select_rotacion')
        st.session_state.editor_img_filtro = st.selectbox('Filtro', ['Normal', 'Escala de Grises', 'Invertir', 'Negativo'], key='editor_img_select_filtro')
        
        if st.button('Restablecer valores', key='editor_img_btn_reset'):
            st.session_state.editor_img_brillo = 1.0
            st.session_state.editor_img_contraste = 1.0
            st.session_state.editor_img_rotacion = 0
            st.session_state.editor_img_filtro = 'Normal'
            st.rerun()

    imagen_procesada = imagen_original.copy()
    
    if st.session_state.editor_img_rotacion != 0:
        imagen_procesada = imagen_procesada.rotate(st.session_state.editor_img_rotacion, expand=True)
    
    if st.session_state.editor_img_brillo != 1.0:
        enhancer = ImageEnhance.Brightness(imagen_procesada)
        imagen_procesada = enhancer.enhance(st.session_state.editor_img_brillo)
        
    if st.session_state.editor_img_contraste != 1.0:
        enhancer = ImageEnhance.Contrast(imagen_procesada)
        imagen_procesada = enhancer.enhance(st.session_state.editor_img_contraste)
        
    filtro = st.session_state.editor_img_filtro
    if filtro == 'Escala de Grises':
        imagen_procesada = ImageOps.grayscale(imagen_procesada)
    elif filtro == 'Invertir':
        if imagen_procesada.mode == 'RGBA':
            r, g, b, a = imagen_procesada.split()
            rgb_img = Image.merge('RGB', (r, g, b))
            inv_img = ImageOps.invert(rgb_img)
            r2, g2, b2 = inv_img.split()
            imagen_procesada = Image.merge('RGBA', (r2, g2, b2, a))
        else:
            if imagen_procesada.mode != 'RGB':
                imagen_procesada = imagen_procesada.convert('RGB')
            imagen_procesada = ImageOps.invert(imagen_procesada)
    elif filtro == 'Negativo':
        if imagen_procesada.mode == 'RGB':
            imagen_procesada = ImageOps.invert(imagen_procesada)

    with col_cont2:
        st.markdown('#### Vista Previa')
        st.image(imagen_procesada, use_container_width=True)
        
        buffer = io.BytesIO()
        formato_guardado = imagen_original.format if imagen_original.format in ['PNG', 'JPEG', 'JPG'] else 'PNG'
        if formato_guardado == 'JPG':
            formato_guardado = 'JPEG'
        imagen_procesada.save(buffer, format=formato_guardado)
        bytes_imagen = buffer.getvalue()
        
        st.download_button(
            label='📥 Descargar imagen editada',
            data=bytes_imagen,
            file_name=f'imagen_editada.{formato_guardado.lower()}',
            mime=f'image/{formato_guardado.lower()}',
            key='editor_img_btn_download'
        )
else:
    st.info('Por favor, sube una imagen mediante el selector superior para comenzar a editarla.')
