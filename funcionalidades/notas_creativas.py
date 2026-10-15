if 'notas_creativas_lista' not in st.session_state:
    st.session_state.notas_creativas_lista = []

st.markdown('### 📝 Bloc de Notas y Recordatorios Creativos')
st.markdown('Apunta tus ideas rápidas, tareas o inspiraciones diarias en un solo lugar.')

with st.form(key='notas_creativas_form'):
    nuevo_titulo = st.text_input('Título de la nota', key='notas_creativas_input_titulo')
    nuevo_contenido = st.text_area('Contenido', key='notas_creativas_input_contenido')
    submit_nota = st.form_submit_button('Añadir Nota')
    if submit_nota:
        if nuevo_titulo.strip() and nuevo_contenido.strip():
            st.session_state.notas_creativas_lista.insert(0, {'titulo': nuevo_titulo, 'contenido': nuevo_contenido})
            st.success('¡Nota añadida con éxito!')
        else:
            st.warning('Por favor, rellena tanto el título como el contenido.')

st.divider()
st.markdown('#### Tus Notas Guardadas')

if st.session_state.notas_creativas_lista:
    if st.button('Borrar todas las notas', key='notas_creativas_btn_borrar'):
        st.session_state.notas_creativas_lista = []
        st.rerun()
    
    for idx, nota in enumerate(st.session_state.notas_creativas_lista):
        with st.expander(f"{nota['titulo']}", expanded=(idx == 0)):
            st.write(nota['contenido'])
            if st.button('Eliminar nota', key=f'notas_creativas_del_{idx}'):
                st.session_state.notas_creativas_lista.pop(idx)
                st.rerun()
else:
    st.info('No hay notas guardadas todavía. ¡Crea la primera arriba!')
