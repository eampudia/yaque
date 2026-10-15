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

st.markdown('### 🧮 Calculadora Compacta')

with st.container():
    st.markdown('<style>div[data-testid="stHorizontalBlock"] > div {{padding: 1px;}} .stButton>button {{padding: 1px 0px; font-size: 11px; min-height: 20px;}}</style>', unsafe_allow_html=True)
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
st.write('### Editor Gráfico Interactivo')
st.markdown('Dibuja libremente o añade formas geométricas configurando los parámetros.')

col1, col2, col3 = st.columns(3)
with col1:
    st.session_state.dibujo_mouse_modo = st.selectbox('Herramienta', ['Línea', 'Rectángulo', 'Círculo'], key='dibujo_mouse_select_modo')
with col2:
    st.session_state.dibujo_mouse_color = st.color_picker('Color', '#1f77b4', key='dibujo_mouse_color_picker')
with col3:
    st.session_state.dibujo_mouse_grosor = st.slider('Grosor', 1, 10, 3, key='dibujo_mouse_grosor_slider')

col_x1, col_y1, col_x2, col_y2 = st.columns(4)
with col_x1:
    x1 = st.number_input('X inicio', value=0.0, key='dibujo_mouse_x1')
with col_y1:
    y1 = st.number_input('Y inicio', value=0.0, key='dibujo_mouse_y1')
with col_x2:
    x2 = st.number_input('X fin', value=10.0, key='dibujo_mouse_x2')
with col_y2:
    y2 = st.number_input('Y fin', value=10.0, key='dibujo_mouse_y2')

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button('Añadir figura', key='dibujo_mouse_btn_add'):
        nuevo_obj = {
            'tipo': st.session_state.dibujo_mouse_modo,
            'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
            'color': st.session_state.dibujo_mouse_color,
            'grosor': st.session_state.dibujo_mouse_grosor
        }
        st.session_state.dibujo_mouse_objetos.append(nuevo_obj)
        st.success('Figura añadida al lienzo.')
with col_btn2:
    if st.button('Limpiar lienzo', key='dibujo_mouse_btn_limpiar'):
        st.session_state.dibujo_mouse_objetos = []
        st.rerun()

if st.session_state.dibujo_mouse_objetos:
    import pandas as pd
    import altair as alt
    import numpy as np
    
    datos_grafica = []
    for idx, obj in enumerate(st.session_state.dibujo_mouse_objetos):
        t = obj['tipo']
        fig_id = f'{t} {idx+1}'
        color = obj.get('color', '#1f77b4')
        if t == 'Línea':
            datos_grafica.append({'id': idx, 'x': obj['x1'], 'y': obj['y1'], 'figura': fig_id, 'color': color})
            datos_grafica.append({'id': idx, 'x': obj['x2'], 'y': obj['y2'], 'figura': fig_id, 'color': color})
        elif t == 'Rectángulo':
            hx1, hy1, hx2, hy2 = obj['x1'], obj['y1'], obj['x2'], obj['y2']
            puntos_rect = [
                (hx1, hy1), (hx2, hy1), (hx2, hy2), (hx1, hy2), (hx1, hy1)
            ]
            for px, py in puntos_rect:
                datos_grafica.append({'id': idx, 'x': px, 'y': py, 'figura': fig_id, 'color': color})
        elif t == 'Círculo':
            cx, cy = obj['x1'], obj['y1']
            radio = max(1.0, ((obj['x2'] - cx) ** 2 + (obj['y2'] - cy) ** 2) ** 0.5)
            angulos = np.linspace(0, 2 * np.pi, 50)
            for ang in angulos:
                px = cx + radio * np.cos(ang)
                py = cy + radio * np.sin(ang)
                datos_grafica.append({'id': idx, 'x': px, 'y': py, 'figura': fig_id, 'color': color})
                
    df_plot = pd.DataFrame(datos_grafica)
    if not df_plot.empty:
        colores_unicos = df_plot.set_index('figura')['color'].to_dict()
        dominio = list(colores_unicos.keys())
        rango = list(colores_unicos.values())
        
        chart = alt.Chart(df_plot).mark_line(point=True, strokeWidth=3).encode(
            x=alt.X('x:Q', scale=alt.Scale(zero=False)),
            y=alt.Y('y:Q', scale=alt.Scale(zero=False)),
            color=alt.Color('figura:N', scale=alt.Scale(domain=dominio, range=rango))
        ).properties(width='container', height=450).interactive()
        
        st.altair_chart(chart, use_container_width=True)
else:
    st.info('Añade tu primera figura geométrica utilizando los controles de coordenadas superiores.')
