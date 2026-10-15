import calendar
import datetime

if 'cal_anio' not in st.session_state:
    st.session_state.cal_anio = datetime.date.today().year
if 'cal_mes' not in st.session_state:
    st.session_state.cal_mes = datetime.date.today().month
if 'cal_notas' not in st.session_state:
    st.session_state.cal_notas = {}

st.markdown('### 📅 Calendario del Mes')
st.markdown('Consulta los días del mes actual, navega entre meses y añade notas personales para cada día.')

hoy = datetime.date.today()

col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
with col_nav1:
    if st.button('◀ Mes Anterior', key='cal_btn_ant'):
        if st.session_state.cal_mes == 1:
            st.session_state.cal_mes = 12
            st.session_state.cal_anio -= 1
        else:
            st.session_state.cal_mes -= 1
        st.rerun()
with col_nav2:
    nombre_mes = calendar.month_name[st.session_state.cal_mes]
    st.markdown(f'<h4 style="text-align: center;">{nombre_mes} {st.session_state.cal_anio}</h4>', unsafe_allow_html=True)
with col_nav3:
    if st.button('Mes Siguiente ▶', key='cal_btn_sig'):
        if st.session_state.cal_mes == 12:
            st.session_state.cal_mes = 1
            st.session_state.cal_anio += 1
        else:
            st.session_state.cal_mes += 1
        st.rerun()

matriz_mes = calendar.monthcalendar(st.session_state.cal_anio, st.session_state.cal_mes)
dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

cols_dias = st.columns(7)
for idx, dia in enumerate(dias_semana):
    with cols_dias[idx]:
        st.markdown(f'<div style="text-align: font-weight: bold; text-align: center;">{dia[:3]}</div>', unsafe_allow_html=True)

for semana in matriz_mes:
    cols_sem = st.columns(7)
    for idx, dia_num in enumerate(semana):
        with cols_sem[idx]:
            if dia_num == 0:
                st.write('')
            else:
                fecha_str = f"{st.session_state.cal_anio}-{st.session_state.cal_mes:02d}-{dia_num:02d}"
                tiene_nota = fecha_str in st.session_state.cal_notas and st.session_state.cal_notas[fecha_str]
                etiqueta = f'📌 {dia_num}' if tiene_nota else str(dia_num)
                
                es_hoy = (st.session_state.cal_anio == hoy.year and st.session_state.cal_mes == hoy.month and dia_num == hoy.day)
                
                if es_hoy:
                    btn_type = 'primary'
                else:
                    btn_type = 'secondary'
                
                if st.button(etiqueta, key=f'cal_dia_{fecha_str}', use_container_width=True):
                    st.session_state.cal_dia_seleccionado = fecha_str
                    st.rerun()

st.divider()
if 'cal_dia_seleccionado' not in st.session_state:
    st.session_state.cal_dia_seleccionado = hoy.strftime('%Y-%m-%d')

st.markdown(f'#### 📝 Notas para el día: {st.session_state.cal_dia_seleccionado}')
nota_actual = st.session_state.cal_notas.get(st.session_state.cal_dia_seleccionado, '')
nuevo_texto_nota = st.text_area('Añade o edita tu nota:', value=nota_actual, key='cal_input_nota')

col_b1, col_b2 = st.columns(2)
with col_b1:
    if st.button('Guardar nota', key='cal_btn_guardar'):
        st.session_state.cal_notas[st.session_state.cal_dia_seleccionado] = nuevo_texto_nota
        st.success('Nota guardada correctamente.')
with col_b2:
    if st.button('Eliminar nota', key='cal_btn_eliminar'):
        if st.session_state.cal_dia_seleccionado in st.session_state.cal_notas:
            del st.session_state.cal_notas[st.session_state.cal_dia_seleccionado]
            st.success('Nota eliminada.')
            st.rerun()
