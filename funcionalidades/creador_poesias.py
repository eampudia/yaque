st.subheader('Créateur de Poésies pour Élèves')
st.write('Générez ou rédigez des poèmes éducatifs et créatifs adaptés pour vos cours en français.')
if 'creador_poesias_texto' not in st.session_state:
    st.session_state.creador_poesias_texto = ''
if 'creador_poesias_tema' not in st.session_state:
    st.session_state.creador_poesias_tema = ''
tema = st.text_input('Thème ou mot-clé pour le poème:', value=st.session_state.creador_poesias_tema, key='creador_poesias_input_tema')
if st.button('Créer la poésie', key='creador_poesias_btn'):
    if tema.strip() == '':
        st.warning('Veuillez introduire un thème.')
    else:
        st.session_state.creador_poesias_tema = tema
        st.session_state.creador_poesias_texto = f'Sous le ciel d’un bleu éclatant, \nla classe écoute attentivement et constant, \napprenant avec joie et valeur, \nautour de {tema} avec grand ardeur.'
if st.session_state.creador_poesias_texto:
    st.markdown('### Poésie Générée')
    st.success(st.session_state.creador_poesias_texto)
