if 'frances_indice' not in st.session_state:
    st.session_state.frances_indice = 0
if 'frances_puntuacion' not in st.session_state:
    st.session_state.frances_puntuacion = 0
if 'frances_modo' not in st.session_state:
    st.session_state.frances_modo = 'Vocabulario'

st.markdown('### 🇫🇷 Tu profesor de Francés')
st.markdown('Aprende vocabulario esencial, saludos y pon a prueba tus conocimientos de francés de forma sencilla.')

modo_frances = st.radio('Selecciona sección', ['Vocabulario', 'Quiz interactivo'], key='frances_radio_modo')
if modo_frances != st.session_state.frances_modo:
    st.session_state.frances_modo = modo_frances
    st.session_state.frances_indice = 0
    st.session_state.frances_puntuacion = 0

vocabulario = [
    {'fr': 'Bonjour', 'es': 'Hola', 'cat': 'Saludos'},
    {'fr': 'Merci', 'es': 'Gracias', 'cat': 'Cortesía'},
    {'fr': 'S\'il vous plaît', 'es': 'Por favor', 'cat': 'Cortesía'},
    {'fr': 'Au revoir', 'es': 'Adiós', 'cat': 'Saludos'},
    {'fr': 'Oui / Non', 'es': 'Sí / No', 'cat': 'Básicos'},
    {'fr': 'Comment ça va?', 'es': '¿Cómo estás?', 'cat': 'Conversación'},
    {'fr': 'Je t\'aime', 'es': 'Te quiero', 'cat': 'Emociones'},
    {'fr': 'Eau', 'es': 'Agua', 'cat': 'Comida y Bebida'}
]

if st.session_state.frances_modo == 'Vocabulario':
    st.markdown('#### Tarjetas de Vocabulario Esencial')
    idx = st.session_state.frances_indice
    item = vocabulario[idx]
    
    st.info(f'Categoría: {item["cat"]}')
    st.markdown(f'### 🇫🇷 **{item["fr"]}**')
    
    if st.checkbox('Ver traducción', key='frances_chk_trad'):
        st.success(f'🇪🇸 {item["es"]}')
        
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Anterior', key='frances_btn_prev'):
            st.session_state.frances_indice = (idx - 1) % len(vocabulario)
            st.rerun()
    with col2:
        if st.button('Siguiente', key='frances_btn_next'):
            st.session_state.frances_indice = (idx + 1) % len(vocabulario)
            st.rerun()
else:
    st.markdown('#### Quiz Rápido')
    preguntas = [
        {'pregunta': '¿Qué significa "Bonjour"?', 'opciones': ['Hola', 'Adiós', 'Gracias'], 'respuesta': 'Hola'},
        {'pregunta': '¿Cómo se dice "Gracias" en francés?', 'opciones': ['Pardon', 'Merci', 'Oui'], 'respuesta': 'Merci'},
        {'pregunta': '¿Qué significa "Au revoir"?', 'opciones': ['Por favor', 'Hola', 'Adiós'], 'respuesta': 'Adiós'},
        {'pregunta': '¿Cómo se dice "Agua" en francés?', 'opciones': ['Eau', 'Du pain', 'Lait'], 'respuesta': 'Eau'}
    ]
    
    q_idx = st.session_state.frances_indice % len(preguntas)
    q = preguntas[q_idx]
    
    st.write(f'Pregunta {q_idx + 1} de {len(preguntas)}')
    st.write(f'**{q["pregunta"]}**')
    
    respuesta_usuario = st.radio('Elige una opción:', q['opciones'], key=f'frances_quiz_{q_idx}')
    
    if st.button('Comprobar respuesta', key='frances_btn_check'):
        if respuesta_usuario == q['respuesta']:
            st.success('¡Correcto! 🎉')
            st.session_state.frances_puntuacion += 1
        else:
            st.error(f'Incorrecto. La respuesta correcta era: {q["respuesta"]}')
            
        if st.button('Siguiente pregunta', key='frances_btn_next_q'):
            st.session_state.frances_indice += 1
            st.rerun()
