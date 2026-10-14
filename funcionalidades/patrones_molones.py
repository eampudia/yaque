if 'patrones_forma' not in st.session_state:
    st.session_state.patrones_forma = 'Espiral'
if 'patrones_puntos' not in st.session_state:
    st.session_state.patrones_puntos = 300
if 'patrones_frecuencia' not in st.session_state:
    st.session_state.patrones_frecuencia = 5
if 'patrones_escala' not in st.session_state:
    st.session_state.patrones_escala = 1.0

st.markdown('### ✨ Generador de Patrones Molones')
st.markdown('Experimenta con fórmulas matemáticas para crear patrones geométricos y mandalas hipnóticos.')

col1, col2 = st.columns(2)
with col1:
    st.session_state.patrones_forma = st.selectbox('Tipo de patrón', ['Espiral', 'Rosa de Grandi', 'Lissajous', 'Caleidoscopio'], key='patrones_select_forma')
    st.session_state.patrones_puntos = st.slider('Número de puntos', 50, 1000, 400, key='patrones_slider_puntos')
with col2:
    st.session_state.patrones_frecuencia = st.slider('Frecuencia / Pétalos', 1, 20, 6, key='patrones_slider_freq')
    st.session_state.patrones_escala = st.slider('Escala o zoom', 0.5, 3.0, 1.0, key='patrones_slider_escala')

import numpy as np
import pandas as pd
import altair as alt

n = st.session_state.patrones_puntos
forma = st.session_state.patrones_forma
freq = st.session_state.patrones_frecuencia
escala = st.session_state.patrones_escala

if forma == 'Espiral':
    t = np.linspace(0, freq * 2 * np.pi, n)
    r = t * escala
    x = r * np.cos(t)
    y = r * np.sin(t)
elif forma == 'Rosa de Grandi':
    t = np.linspace(0, 2 * np.pi, n)
    r = np.sin(freq * t) * escala * 5
    x = r * np.cos(t)
    y = r * np.sin(t)
elif forma == 'Lissajous':
    t = np.linspace(0, 2 * np.pi, n)
    x = np.sin(freq * t) * escala * 5
    y = np.cos((freq + 1) * t) * escala * 5
else:
    t = np.linspace(0, freq * 2 * np.pi, n)
    r = (1 + np.sin(freq * t)) * escala * 3
    x = r * np.cos(t)
    y = r * np.sin(t)

df_patron = pd.DataFrame({'x': x, 'y': y, 'indice': np.arange(n)})

chart = alt.Chart(df_patron).mark_line(point=True, strokeWidth=2).encode(
    x=alt.X('x:Q', axis=alt.Axis(labels=False, title='')) ,
    y=alt.Y('y:Q', axis=alt.Axis(labels=False, title='')) ,
    color=alt.Color('indice:Q', scale=alt.Scale(scheme='turbo'), legend=None)
).properties(width='container', height=500).interactive()

st.altair_chart(chart, use_container_width=True)
st.success('¡Patrón generado con éxito! Usa el zoom y arrastra el gráfico para explorarlo.')
