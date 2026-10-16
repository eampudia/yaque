import time
st.subheader('Temporizador Pomodoro')
st.write('Gestiona tu tiempo de trabajo y descanso con esta técnica.')
if 'pomodoro_tiempo' not in st.session_state:
    st.session_state.pomodoro_tiempo = 25 * 60
if 'pomodoro_activo' not in st.session_state:
    st.session_state.pomodoro_activo = False
minutos = st.session_state.pomodoro_tiempo // 60
segundos = st.session_state.pomodoro_tiempo % 60
st.markdown(f'### {minutos:02d}:{segundos:02d}')
col1, col2, col3 = st.columns(3)
if col1.button('Iniciar', key='pomodoro_btn_iniciar'):
    st.session_state.pomodoro_activo = True
if col2.button('Pausar', key='pomodoro_btn_pausar'):
    st.session_state.pomodoro_activo = False
if col3.button('Reiniciar', key='pomodoro_btn_reiniciar'):
    st.session_state.pomodoro_activo = False
    st.session_state.pomodoro_tiempo = 25 * 60
if st.session_state.pomodoro_activo:
    if st.session_state.pomodoro_tiempo > 0:
        time.sleep(1)
        st.session_state.pomodoro_tiempo -= 1
        st.experimental_rerun()
    else:
        st.session_state.pomodoro_activo = False
        st.success('¡Tiempo completado! Tómate un descanso.')
