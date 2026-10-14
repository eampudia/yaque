if 'dibujo_mouse_objetos' not in st.session_state:
    st.session_state.dibujo_mouse_objetos = []
if 'dibujo_mouse_modo' not in st.session_state:
    st.session_state.dibujo_mouse_modo = 'Línea'
if 'dibujo_calc_num1' not in st.session_state:
    st.session_state.dibujo_calc_num1 = 0.0
if 'dibujo_calc_num2' not in st.session_state:
    st.session_state.dibujo_calc_num2 = 0.0
if 'dibujo_calc_op' not in st.session_state:
    st.session_state.dibujo_calc_op = 'Suma'

st.write('### Calculadora Rápida')
calc_col1, calc_col2, calc_col3, calc_col4 = st.columns(4)
with calc_col1:
    st.session_state.dibujo_calc_num1 = st.number_input('Número 1', value=st.session_state.dibujo_calc_num1, key='dibujo_mouse_num1')
with calc_col2:
    st.session_state.dibujo_calc_num2 = st.number_input('Número 2', value=st.session_state.dibujo_calc_num2, key='dibujo_mouse_num2')
with calc_col3:
    st.session_state.dibujo_calc_op = st.selectbox('Operación', ['Suma', 'Resta', 'Multiplicación', 'División'], key='dibujo_mouse_calc_op')
with calc_col4:
    st.write('')
    st.write('')
    if st.button('Calcular', key='dibujo_mouse_btn_calc'):
        n1 = st.session_state.dibujo_calc_num1
        n2 = st.session_state.dibujo_calc_num2
        op = st.session_state.dibujo_calc_op
        if op == 'Suma':
            res = n1 + n2
        elif op == 'Resta':
            res = n1 - n2
        elif op == 'Multiplicación':
            res = n1 * n2
        elif op == 'División':
            res = n1 / n2 if n2 != 0 else 'Error (división por cero)'
        st.success(f'Resultado: {res}')

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
