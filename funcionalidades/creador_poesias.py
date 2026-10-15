st.subheader('Creador de Poesías para Alumnos')
st.write('Genera o redacta poemas educativos y creativos adaptados para tus clases.')
if 'creador_poesias_texto' not in st.session_state:
    st.session_state.creador_poesias_texto = ''
if 'creador_poesias_tema' not in st.session_state:
    st.session_state.creador_poesias_tema = ''
tema = st.text_input('Tema o palabra clave para el poema:', value=st.session_state.creador_poesias_tema, key='creador_poesias_input_tema')
if st.button('Crear poesía', key='creador_poesias_btn'):
    if tema.strip() == '':
        st.warning('Por favor, introduce un tema.')
    else:
        st.session_state.creador_poesias_tema = tema
        st.session_state.creador_poesias_texto = f'Bajo el cielo de azul brillante, \nla clase escucha muy atenta y constante, \naprendiendo con alegría y valor, \nacerca de {tema} con gran fervor.'
if st.session_state.creador_poesias_texto:
    st.markdown('### Poesía Generada')
    st.success(st.session_state.creador_poesias_texto)
