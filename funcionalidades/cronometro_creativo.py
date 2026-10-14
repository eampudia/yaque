if 'crono_tiempo' not in st.session_state:
    st.session_state.crono_tiempo = 0
if 'crono_activo' not in st.session_state:
    st.session_state.crono_activo = False
if 'crono_modo' not in st.session_state:
    st.session_state.crono_modo = 'Cronómetro'

st.markdown('### ⏱️ Control de Tiempo Creativo')
st.markdown('Gestiona tu tiempo de trabajo o mide intervalos de forma visual y sencilla.')

modo = st.radio('Selecciona modo', ['Cronómetro', 'Pomodoro (25 min)'], key='crono_radio_modo')
if modo != st.session_state.crono_modo:
    st.session_state.crono_modo = modo
    if modo == 'Pomodoro (25 min)':
        st.session_state.crono_tiempo = 1500
    else:
        st.session_state.crono_tiempo = 0
    st.session_state.crono_activo = False

col_t1, col_t2 = st.columns(2)
with col_t1:
    minutos = int(st.session_state.crono_tiempo // 60)
    segundos = int(st.session_state.crono_tiempo % 60)
    st.metric(label='Tiempo Actual', value=f'{minutos:02d}:{segundos:02d}')

with col_t2:
    st.write('')
    st.write('')
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        if st.button('Iniciar', key='crono_btn_start'):
            st.session_state.crono_activo = True
    with col_b2:
        if st.button('Pausar', key='crono_btn_pause'):
            st.session_state.crono_activo = False
    with col_b3:
        if st.button('Reiniciar', key='crono_btn_reset'):
            st.session_state.crono_activo = False
            st.session_state.crono_tiempo = 1500 if st.session_state.crono_modo == 'Pomodoro (25 min)' else 0

if st.session_state.crono_activo:
    import time
    time.sleep(1)
    if st.session_state.crono_modo == 'Pomodoro (25 min)':
        if st.session_state.crono_tiempo > 0:
            st.session_state.crono_tiempo -= 1
        else:
            st.session_state.crono_activo = False
            st.success('¡Tiempo de Pomodoro finalizado!')
    else:
        st.session_state.crono_tiempo += 1
    st.rerun()
