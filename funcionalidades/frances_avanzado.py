if 'frances_av_indice' not in st.session_state:
    st.session_state.frances_av_indice = 0
if 'frances_av_puntuacion' not in st.session_state:
    st.session_state.frances_av_puntuacion = 0
if 'frances_av_modo' not in st.session_state:
    st.session_state.frances_av_modo = 'Expresiones'

st.markdown('### 🇫🇷 Perfeccionamiento Nivel B2.1: Expresiones Idiomáticas')
st.markdown('Domina los modismos, la estructura culta y las locuciones avanzadas en francés para alcanzar un nivel fluido.')

modo_av = st.radio('Selecciona sección avanzada', ['Expresiones', 'Situaciones complejas'], key='frances_av_radio_modo')
if modo_av != st.session_state.frances_av_modo:
    st.session_state.frances_av_modo = modo_av
    st.session_state.frances_av_indice = 0
    st.session_state.frances_av_puntuacion = 0

expresiones = [
    {'fr': 'Avoir le cafard', 'literal': 'Tener la cucaracha', 'es': 'Estar depre / melancólico', 'ej': 'Il a le cafard depuis qu\'il pleut.'},
    {'fr': 'Poser un lapin', 'literal': 'Poner un conejo', 'es': 'Dejar plantado a alguien', 'ej': 'Il m\'a posé un lapin au rendez-vous.'},
    {'fr': 'Coouter les yeux de la tête', 'literal': 'Costar los ojos de la cabeza', 'es': 'Costar un ojo de la cara', 'ej': 'Cette voiture coûte les yeux de la tête.'},
    {'fr': 'Faire la grasse matinée', 'literal': 'Hacer la grasa mañana', 'es': 'Dormir hasta tarde / quedarse en la cama', 'ej': 'Dimanche, j\'aime faire la grasse matinée.'},
    {'fr': 'Appeler un chat un chat', 'literal': 'Llamar a un gato un gato', 'es': 'Llamar a las cosas por su nombre', 'ej': 'Il faut appeler un chat un chat dans cette affaire.'}
]

if st.session_state.frances_av_modo == 'Expresiones':
    st.markdown('#### Locuciones y Modismos Franceses')
    idx = st.session_state.frances_av_indice % len(expresiones)
    item = expresiones[idx]
    
    st.info(f'Modismo {idx + 1} de {len(expresiones)}')
    st.markdown(f'### 🇫🇷 **{item["fr"]}**')
    st.write(f'*Traducción literal:* {item["literal"]}')
    
    if st.checkbox('Ver significado y ejemplo', key='frances_av_chk_meaning'):
        st.success(f'🇪🇸 **Significado:** {item["es"]}')
        st.code(f'Ejemplo: {item["ej"]}', language='text')
        
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Anterior expresión', key='frances_av_btn_prev'):
            st.session_state.frances_av_indice = (idx - 1) % len(expresiones)
            st.rerun()
    with col2:
        if st.button('Siguiente expresión', key='frances_av_btn_next'):
            st.session_state.frances_av_indice = (idx + 1) % len(expresiones)
            st.rerun()
else:
    st.markdown('#### Simulación de Situaciones Complejas (Nivel B2)')
    situaciones = [
        {
            'contexto': 'Estás en una reunión de trabajo y no estás de acuerdo con la propuesta de un colega de manera educada.',
            'opciones': [
                'Je ne suis pas du tout de votre avis, c\'est absurde.',
                'Je comprends votre point de vue, cependant permettez-moi de nuancer cette approche.',
                'Faites ce que vous voulez, ça m\'est égal.'
            ],
            'correcta': 'Je comprends votre point de vue, cependant permettez-moi de nuancer cette approche.'
        },
        {
            'contexto': 'Quieres expresar una hipótesis sobre el futuro económico en un debate formal.',
            'opciones': [
                'Il est probable que l\'inflation augmente si les mesures échouent.',
                'Je crois que l\'argent va grandir.',
                'Demain il fera beau.'
            ],
            'correcta': 'Il est probable que l\'inflation augmente si les mesures échouent.'
        }
    ]
    
    s_idx = st.session_state.frances_av_indice % len(situaciones)
    s = situaciones[s_idx]
    
    st.write(f'Caso práctico {s_idx + 1} de {len(situaciones)}')
    st.warning(s['contexto'])
    
    eleccion = st.radio('Selecciona la respuesta más adecuada y formal:', s['opciones'], key=f'frances_av_caso_{s_idx}')
    
    if st.button('Validar respuesta B2', key='frances_av_btn_val'):
        if eleccion == s['correcta']:
            st.success('¡Excelente elección léxica y de registro formal! 🎉')
            st.session_state.frances_av_puntuacion += 1
        else:
            st.error(f'Incorrecto. La opción más adecuada en nivel B2 es:\n\n"{s["correcta"]}"')
            
        if st.button('Siguiente caso', key='frances_av_btn_next_c'):
            st.session_state.frances_av_indice += 1
            st.rerun()
