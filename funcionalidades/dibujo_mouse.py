if 'dibujo_mouse_objetos' not in st.session_state:
    st.session_state.dibujo_mouse_objetos = []
if 'dibujo_mouse_modo' not in st.session_state:
    st.session_state.dibujo_mouse_modo = 'Línea'
if 'dibujo_calc_pantalla' not in st.session_state:
    st.session_state.dibujo_calc_pantalla = '0'
if 'dibujo_calc_n1' not in st.session_state:
    st.session_state.dibujo_calc_n1 = None
if 'dibujo_calc_op' not in st.session_state:
    st.session_state.dibujo_calc_op = None
if 'dibujo_calc_nuevo' not in st.session_state:
    st.session_state.dibujo_calc_nuevo = True

st.markdown('### 🧮 Calculadora Estilo Windows')

with st.container():
    st.markdown('<style>div[data-testid="stHorizontalBlock"] > div {{padding: 2px;}}</style>', unsafe_allow_html=True)
    st.text_input('Pantalla', value=st.session_state.dibujo_calc_pantalla, key='dibujo_mouse_calc_screen', disabled=True, label_visibility='collapsed')
    
    def agregar_digito(digito):
        if st.session_state.dibujo_calc_nuevo or st.session_state.dibujo_calc_pantalla == '0' or st.session_state.dibujo_calc_pantalla == 'Error':
            st.session_state.dibujo_calc_pantalla = str(digito)
            st.session_state.dibujo_calc_nuevo = False
        else:
            st.session_state.dibujo_calc_pantalla += str(digito)

    def establecer_operacion(op):
        try:
            st.session_state.dibujo_calc_n1 = float(st.session_state.dibujo_calc_pantalla)
        except:
            st.session_state.dibujo_calc_n1 = 0.0
        st.session_state.dibujo_calc_op = op
        st.session_state.dibujo_calc_nuevo = True

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button('C', key='win_calc_c', use_container_width=True):
            st.session_state.dibujo_calc_pantalla = '0'
            st.session_state.dibujo_calc_n1 = None
            st.session_state.dibujo_calc_op = None
            st.session_state.dibujo_calc_nuevo = True
    with c2:
        if st.button('±', key='win_calc_sign', use_container_width=True):
            try:
                val = float(st.session_state.dibujo_calc_pantalla)
                st.session_state.dibujo_calc_pantalla = str(-val)
            except:
                pass
    with c3:
        if st.button('%', key='win_calc_perc', use_container_width=True):
            try:
                val = float(st.session_state.dibujo_calc_pantalla) / 100
                st.session_state.dibujo_calc_pantalla = str(val)
            except:
                pass
    with c4:
        if st.button('÷', key='win_calc_div', use_container_width=True):
            establecer_operacion('/')

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button('7', key='win_calc_7', use_container_width=True):
            agregar_digito('7')
    with c2:
        if st.button('8', key='win_calc_8', use_container_width=True):
            agregar_digito('8')
    with c3:
        if st.button('9', key='win_calc_9', use_container_width=True):
            agregar_digito('9')
    with c4:
        if st.button('×', key='win_calc_mul', use_container_width=True):
            establecer_operacion('*')

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button('4', key='win_calc_4', use_container_width=True):
            agregar_digito('4')
    with c2:
        if st.button('5', key='win_calc_5', use_container_width=True):
            agregar_digito('5')
    with c3:
        if st.button('6', key='win_calc_6', use_container_width=True):
            agregar_digito('6')
    with c4:
        if st.button('-', key='win_calc_sub', use_container_width=True):
            establecer_operacion('-')

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button('1', key='win_calc_1', use_container_width=True):
            agregar_digito('1')
    with c2:
        if st.button('2', key='win_calc_2', use_container_width=True):
            agregar_digito('2')
    with c3:
        if st.button('3', key='win_calc_3', use_container_width=True):
            agregar_digito('3')
    with c4:
        if st.button('+', key='win_calc_add', use_container_width=True):
            establecer_operacion('+')

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button('0', key='win_calc_0', use_container_width=True):
            agregar_digito('0')
    with c2:
        if st.button('.', key='win_calc_dot', use_container_width=True):
            if '.' not in st.session_state.dibujo_calc_pantalla:
                st.session_state.dibujo_calc_pantalla += '.'
    with c3:
        if st.button('⌫', key='win_calc_back', use_container_width=True):
            if len(st.session_state.dibujo_calc_pantalla) > 1:
                st.session_state.dibujo_calc_pantalla = st.session_state.dibujo_calc_pantalla[:-1]
            else:
                st.session_state.dibujo_calc_pantalla = '0'
    with c4:
        if st.button('=', key='win_calc_eq', use_container_width=True):
            if st.session_state.dibujo_calc_op and st.session_state.dibujo_calc_n1 is not None:
                try:
                    n2 = float(st.session_state.dibujo_calc_pantalla)
                    n1 = st.session_state.dibujo_calc_n1
                    op = st.session_state.dibujo_calc_op
                    if op == '+':
                        res = n1 + n2
                    elif op == '-':
                        res = n1 - n2
                    elif op == '*':
                        res = n1 * n2
                    elif op == '/':
                        res = n1 / n2 if n2 != 0 else 'Error'
                    st.session_state.dibujo_calc_pantalla = str(res)
                    st.session_state.dibujo_calc_n1 = None
                    st.session_state.dibujo_calc_op = None
                    st.session_state.dibujo_calc_nuevo = True
                except:
                    st.session_state.dibujo_calc_pantalla = 'Error'

st.divider()
st.write('### Editor Gráfico con Ratón')
st.markdown('Dibuja líneas, rectángulos y círculos definiendo puntos iniciales y finales de forma interactiva.')
col1, col2 = st.columns(2)
with col1:
    st.session_state.dibujo_mouse_modo = st.selectbox('Selecciona herramienta', ['Línea', 'Rectángulo', 'Círculo'], key='dibujo_mouse_select_modo')
with col2:
    if st.button('Limpiar lienzo', key='dibujo_mouse_btn_limpiar'):
        st.session_state.dibujo_mouse_objetos = []
        st.rerun()
col_x1, col_y1, col_x2, col_y2 = st.columns(4)
with col_x1:
    x1 = st.number_input('X inicial', value=0.0, key='dibujo_mouse_x1')
with col_y1:
    y1 = st.number_input('Y inicial', value=0.0, key='dibujo_mouse_y1')
with col_x2:
    x2 = st.number_input('X final', value=10.0, key='dibujo_mouse_x2')
with col_y2:
    y2 = st.number_input('Y final', value=10.0, key='dibujo_mouse_y2')
if st.button('Añadir objeto', key='dibujo_mouse_btn_add'):
    nuevo_obj = {'tipo': st.session_state.dibujo_mouse_modo, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
    st.session_state.dibujo_mouse_objetos.append(nuevo_obj)
    st.success('Objeto añadido correctamente.')
if st.session_state.dibujo_mouse_objetos:
    import pandas as pd
    import altair as alt
    datos_grafica = []
    for idx, obj in enumerate(st.session_state.dibujo_mouse_objetos):
        t = obj['tipo']
        if t == 'Línea':
            datos_grafica.append({'id': idx, 'x': obj['x1'], 'y': obj['y1'], 'figura': f'Línea {idx}'})
            datos_grafica.append({'id': idx, 'x': obj['x2'], 'y': obj['y2'], 'figura': f'Línea {idx}'})
        elif t == 'Rectángulo':
            hx1, hy1, hx2, hy2 = obj['x1'], obj['y1'], obj['x2'], obj['y2']
            datos_grafica.append({'id': idx, 'x': hx1, 'y': hy1, 'figura': f'Rect {idx}'})
            datos_grafica.append({'id': idx, 'x': hx2, 'y': hy1, 'figura': f'Rect {idx}'})
            datos_grafica.append({'id': idx, 'x': hx2, 'y': hy2, 'figura': f'Rect {idx}'})
            datos_grafica.append({'id': idx, 'x': hx1, 'y': hy2, 'figura': f'Rect {idx}'})
            datos_grafica.append({'id': idx, 'x': hx1, 'y': hy1, 'figura': f'Rect {idx}'})
        elif t == 'Círculo':
            cx, cy = obj['x1'], obj['y1']
            radio = ((obj['x2'] - cx) ** 2 + (obj['y2'] - cy) ** 2) ** 0.5
            if radio < 0.5:
                radio = 5.0
            import numpy as np
            angulos = np.linspace(0, 2 * np.pi, 60)
            for ang in angulos:
                px = cx + radio * np.cos(ang)
                py = cy + radio * np.sin(ang)
                datos_grafica.append({'id': idx, 'x': px, 'y': py, 'figura': f'Círculo {idx}'})
    df_plot = pd.DataFrame(datos_grafica)
    if not df_plot.empty:
        chart = alt.Chart(df_plot).mark_line(point=True).encode(x='x', y='y', color='figura').properties(width=700, height=400)
        st.altair_chart(chart, use_container_width=True)
else:
    st.info('Añade objetos usando las coordenadas superior e inferior para empezar a dibujar.')
