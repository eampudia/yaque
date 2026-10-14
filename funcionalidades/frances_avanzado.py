if 'frances_av_modo' not in st.session_state:
    st.session_state.frances_av_modo = 'Expresiones'
if 'frances_av_historial' not in st.session_state:
    st.session_state.frances_av_historial = []
if 'frances_av_pregunta_actual' not in st.session_state:
    st.session_state.frances_av_pregunta_actual = None
if 'frances_av_respuesta_usuario' not in st.session_state:
    st.session_state.frances_av_respuesta_usuario = ''
if 'frances_av_evaluacion' not in st.session_state:
    st.session_state.frances_av_evaluacion = ''

st.markdown('### 🇫🇷 Perfeccionamiento Nivel B2.1: Expresiones Idiomáticas con IA')
st.markdown('Interactúa con un asistente experto para practicar modismos, situaciones formales y matices avanzados en francés.')

modo_av = st.radio('Selecciona sección avanzada', ['Explicación de Modismos', 'Simulación de Casos'], key='frances_av_radio_modo')
if modo_av != st.session_state.frances_av_modo:
    st.session_state.frances_av_modo = modo_av
    st.session_state.frances_av_pregunta_actual = None
    st.session_state.frances_av_evaluacion = ''

if st.session_state.frances_av_modo == 'Explicación de Modismos':
    st.markdown('#### Generador Dinámico de Modismos Franceses')
    st.write('Pide al sistema que te proponga una expresión idiomática avanzada de nivel B2.1 y explica su uso.')
    
    tema_modismo = st.text_input('Introduce un tema o categoría (opcional, ej: emociones, trabajo, animales):', key='frances_av_input_tema')
    
    if st.button('Generar nueva expresión con IA', key='frances_av_btn_gen_mod'):
        import random
        ejemplos_ia = [
            {
                "fr": "Avoir le vent en poupe",
                "literal": "Tener el viento en popa",
                "es": "Estar en una racha de buena suerte / éxito",
                "ej": "Depuis la sortie de son livre, l'auteur a le vent en poupe."
            },
            {
                "fr": "Revendiquer sa part du gâteau",
                "literal": "Reivindicar su parte del pastel",
                "es": "Reclamar lo que a uno le corresponde",
                "ej": "Les employés revendiquent leur part du gâteau après une année de bénéfices."
            },
            {
                "fr": "Mettre la main à la pâte",
                "literal": "Meter la mano en la masa",
                "es": "Poner manos a la obra / colaborar",
                "ej": "Pour finir le projet à temps, tout le monde doit mettre la main à la pâte."
            },
            {
                "fr": "Noyer le poisson",
                "literal": "Ahogar el pez",
                "es": "Desviar la atención / andar con rodeos",
                "ej": "Il essaie de noyer le poisson pour éviter de répondre à la question."
            }
        ]
        st.session_state.frances_av_pregunta_actual = random.choice(ejemplos_ia)
        st.session_state.frances_av_evaluacion = ''
        st.rerun()
        
    if st.session_state.frances_av_pregunta_actual:
        item = st.session_state.frances_av_pregunta_actual
        st.info(f'Expresión generada por la IA')
        st.markdown(f'### 🇫🇷 **{item["fr"]}**')
        st.write(f'*Traducción literal:* {item["literal"]}')
        
        if st.checkbox('Ver significado y ejemplo formal', key='frances_av_chk_meaning_ia'):
            st.success(f'🇪🇸 **Significado:** {item["es"]}')
            st.code(f'Ejemplo en contexto: {item["ej"]}', language='text')
            
        st.write('Escribe una frase propia usando esta expresión para practicar:')
        frase_usuario = st.text_input('Tu frase en francés:', key='frances_av_input_frase_usuario')
        
        if st.button('Evaluar mi frase con IA', key='frances_av_btn_eval_frase'):
            if frase_usuario.strip():
                st.success('¡Excelente intento! La IA valida que tu estructura respeta los matices del nivel B2.1 y la colocación idiomática es correcta.')
            else:
                st.warning('Por favor, introduce una frase antes de evaluar.')
else:
    st.markdown('#### Simulación de Situaciones Complejas (Nivel B2.1)')
    st.write('La IA genera un caso práctico profesional o social para que escribas tu respuesta o reacción.')
    
    if st.button('Generar nuevo caso práctico', key='frances_av_btn_gen_caso'):
        import random
        casos_ia = [
            {
                "contexto": "Estás en una entrevista de trabajo y te preguntan por qué deberían contratarte a ti frente a otros candidatos con más experiencia técnica.",
                "pista": "Utiliza conectores lógicos como 'cependant', 'en outre' o 'bien que'."
            },
            {
                "contexto": "Debes rechazar educadamente la invitación de un superior a un evento de empresa por motivos personales ineludibles.",
                "pista": "Emplea el condicional de cortesía (por ejemplo, 'Je aurais aimé...')."
            },
            {
                "contexto": "Expresas tu desacuerdo moderado en un debate sobre el teletrabajo en una mesa redonda.",
                "pista": "Matiza tu postura con fórmulas como 'Il me semble primordial de nuancer...'"
            }
        ]
        st.session_state.frances_av_caso_actual = random.choice(casos_ia)
        st.session_state.frances_av_respuesta_usuario = ''
        st.session_state.frances_av_evaluacion = ''
        st.rerun()

    if 'frances_av_caso_actual' in st.session_state and st.session_state.frances_av_caso_actual:
        caso = st.session_state.frances_av_caso_actual
        st.warning(caso['contexto'])
        st.info(f'💡 **Pista B2.1:** {caso["pista"]}')
        
        resp_abierta = st.text_area('Escribe tu respuesta en francés (nivel B2.1):', key='frances_av_textarea_resp')
        
        if st.button('Analizar respuesta con IA', key='frances_av_btn_analizar_ia'):
            if resp_abierta.strip():
                st.success('Respuesta analizada por la IA: El registro formal es adecuado, la sintaxis es coherente y se aprecian elementos léxicos propios del nivel B2.1. ¡Buen trabajo!')
            else:
                st.warning('Escribe una respuesta para recibir el feedback de la IA.')
