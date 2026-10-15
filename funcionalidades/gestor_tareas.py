st.subheader('Gestor Rápido de Tareas y Notas')
st.write('Anota tus pendientes y organiza tu día de manera sencilla.')
if 'gestor_tareas_lista' not in st.session_state:
    st.session_state.gestor_tareas_lista = []
nueva_tarea = st.text_input('Nueva tarea o nota:', key='gestor_tareas_input')
if st.button('Añadir tarea', key='gestor_tareas_btn'):
    if nueva_tarea.strip():
        st.session_state.gestor_tareas_lista.append(nueva_tarea)
        st.success('Tarea añadida con éxito.')
    else:
        st.warning('Escribe algo antes de añadir.')
if st.session_state.gestor_tareas_lista:
    st.markdown('### Tus tareas pendientes')
    for i, tarea in enumerate(st.session_state.gestor_tareas_lista):
        col1, col2 = st.columns([0.8, 0.2])
        col1.write(f'- {tarea}')
        if col2.button('Completar', key=f'gestor_tareas_del_{i}'):
            st.session_state.gestor_tareas_lista.pop(i)
            st.experimental_rerun()
