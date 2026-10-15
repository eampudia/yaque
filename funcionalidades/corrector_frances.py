st.subheader('Corrector de Redacciones en Francés (Nivel B2.1)')
st.write('Escribe tu redacción en francés a continuación y obtén sugerencias de mejora y correcciones.')
if 'corrector_frances_texto' not in st.session_state:
    st.session_state.corrector_frances_texto = ''
if 'corrector_frances_resultado' not in st.session_state:
    st.session_state.corrector_frances_resultado = None
texto_usuario = st.text_area('Tu texto en francés:', value=st.session_state.corrector_frances_texto, key='corrector_frances_input_texto')
if st.button('Analizar y corregir', key='corrector_frances_btn_enviar'):
    if texto_usuario.strip() == '':
        st.warning('Por favor, escribe algo antes de enviar.')
    else:
        st.session_state.corrector_frances_texto = texto_usuario
        resultado = 'Análisis de nivel B2.1:\n\n' + f'Has escrito: {texto_usuario}\n\nSugerencias:\n- Asegúrate de usar correctamente los tiempos del subjuntivo.\n- Enriquece tu vocabulario utilizando conectores lógicos más variados (como "en outre", "par conséquent").'
        st.session_state.corrector_frances_resultado = resultado
if st.session_state.corrector_frances_resultado:
    st.markdown('### Resultados')
    st.info(st.session_state.corrector_frances_resultado)
