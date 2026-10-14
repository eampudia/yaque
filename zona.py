import random
from PIL import Image, ImageOps
import io

# Inicializar estado para el juego de Akinator simplificado pero visual y divertido
if "akinator_state" not in st.session_state:
    st.session_state.akinator_state = "inicio"
if "akinator_preguntas" not in st.session_state:
    st.session_state.akinator_preguntas = 0
if "akinator_candidatos" not in st.session_state:
    st.session_state.akinator_candidatos = []
if "akinator_personaje_actual" not in st.session_state:
    st.session_state.akinator_personaje_actual = None

# Base de datos de personajes divertidos con pistas y descripciones
PERSONAJES = [
    {
        "nombre": "Mario Bros",
        "tipo": "Ficción",
        "genero": "Masculino",
        "videojuego": True,
        "humano": True,
        "bigote": True,
        "descripcion": "¡Es un fontanero saltarín que rescata a una princesa y come champiñones!",
        "emoji": "🍄"
    },
    {
        "nombre": "Iron Man",
        "tipo": "Ficción",
        "genero": "Masculino",
        "videojuego": False,
        "humano": True,
        "bigote": True,
        "descripcion": "Genio, millonario, playboy, filántropo con una armadura tecnológica.",
        "emoji": "🦾"
    },
    {
        "nombre": "Goku",
        "tipo": "Ficción",
        "genero": "Masculino",
        "videojuego": False,
        "humano": False,
        "bigote": False,
        "descripcion": "Saiyajin amante de las peleas que busca las esferas del dragón.",
        "emoji": "🐉"
    },
    {
        "nombre": "Hermione Granger",
        "tipo": "Ficción",
        "genero": "Femenino",
        "videojuego": False,
        "humano": True,
        "bigote": False,
        "descripcion": "La bruja más brillante de su generación, experta en hechizos y libros.",
        "emoji": "⚡"
    },
    {
        "nombre": "Pikachu",
        "tipo": "Ficción",
        "genero": "Masculino",
        "videojuego": True,
        "humano": False,
        "bigote": False,
        "descripcion": "Pequeña criatura amarilla eléctrica muy famosa.",
        "emoji": "⚡"
    },
    {
        "nombre": "Albert Einstein",
        "tipo": "Real",
        "genero": "Masculino",
        "videojuego": False,
        "humano": True,
        "bigote": True,
        "descripcion": "Científico genio creador de la teoría de la relatividad y pelo despeinado.",
        "emoji": "🧠"
    },
    {
        "nombre": "Wonder Woman",
        "tipo": "Ficción",
        "genero": "Femenino",
        "videojuego": False,
        "humano": False,
        "bigote": False,
        "descripcion": "Princesa amazona con súper fuerza, lazo de la verdad y brazaletes.",
        "emoji": "⭐"
    },
    {
        "nombre": "Batman",
        "tipo": "Ficción",
        "genero": "Masculino",
        "videojuego": False,
        "humano": True,
        "bigote": False,
        "descripcion": "Caballero oscuro que protege Gotham City con gadgets y capa.",
        "emoji": "🦇"
    }
]

st.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <h2>🧞‍♂️ ¡Akinator Mágico en Streamlit!</h2>
    <p style='color: gray;'>Piensa en un personaje (real o de ficción) y trataré de adivinarlo haciendo algunas preguntas.</p>
</div>
""", unsafe_allow_html=True)

estado = st.session_state.get("akinator_state", "inicio")

if estado == "inicio":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### ¿Estás listo?")
        st.info("Piensa en uno de estos personajes o en cualquier otro similar:\n- **Mario Bros, Iron Man, Goku, Hermione, Pikachu, Albert Einstein, Wonder Woman, Batman**")
        if st.button("🚀 ¡Empezar a Jugar!", use_container_width=True):
            st.session_state.akinator_state = "jugando"
            st.session_state.akinator_preguntas = 0
            st.session_state.akinator_candidatos = list(PERSONAJES)
            st.rerun()

elif estado == "jugando":
    candidatos = st.session_state.get("akinator_candidatos", PERSONAJES)
    preguntas_hechas = st.session_state.get("akinator_preguntas", 0)

    # Si nos quedan pocos candidatos o ya hicimos muchas preguntas, intentamos adivinar
    if len(candidatos) <= 1 or preguntas_hechas >= 4:
        if len(candidatos) > 0:
            st.session_state.akinator_personaje_actual = candidatos[0]
        else:
            st.session_state.akinator_personaje_actual = random.choice(PERSONAJES)
        st.session_state.akinator_state = "adivinanza"
        st.rerun()

    # Seleccionar una pregunta lógica basada en los candidatos restantes
    # Evaluamos qué atributo distingue mejor
    st.markdown(f"### Pregunta #{preguntas_hechas + 1}")
    
    # Determinamos la pregunta según el progreso
    if preguntas_hechas == 0:
        pregunta_texto = "¿Tu personaje pertenece al mundo de la **ficción** (películas, cómics, videojuegos)?"
        clave_filtro = "tipo"
        valor_si = "Ficción"
    elif preguntas_hechas == 1:
        # Ver género
        pregunta_texto = "¿Es de género **masculino**?"
        clave_filtro = "genero"
        valor_si = "Masculino"
    elif preguntas_hechas == 2:
        # Ver si es humano
        pregunta_texto = "¿Es un **ser humano** (sin superpoderes naturales de raza alienígena/mágica)?"
        clave_filtro = "humano"
        valor_si = True
    else:
        # Ver bigote o videojuego
        pregunta_texto = "¿Tiene **bigote** o vello facial destacado?"
        clave_filtro = "bigote"
        valor_si = True

    st.markdown(f"#### 🔮 {pregunta_texto}")

    col1, col2, col3, col4 = st.columns(4)

    def responder(respuesta):
        nonlocal candidatos, clave_filtro, valor_si
        if respuesta == "si":
            st.session_state.akinator_candidatos = [c for c in candidatos if c.get(clave_filtro) == valor_si]
        elif respuesta == "no":
            st.session_state.akinator_candidatos = [c for c in candidatos if c.get(clave_filtro) != valor_si]
        st.session_state.akinator_preguntas = st.session_state.get("akinator_preguntas", 0) + 1
        st.rerun()

    with col1:
        if st.button("✅ Sí", use_container_width=True):
            responder("si")
    with col2:
        if st.button("❌ No", use_container_width=True):
            responder("no")
    with col3:
        if st.button("🤷 No sé", use_container_width=True):
            responder("nose")
    with col4:
        if st.button("🤔 Probablemente sí", use_container_width=True):
            responder("si")

elif estado == "adivinanza":
    personaje = st.session_state.get("akinator_personaje_actual", PERSONAJES[0])
    
    st.markdown("### 🎯 ¡Creo que ya sé quién es!")
    
    col_img, col_info = st.columns([1, 2])
    
    with col_img:
        # Crear una bonita tarjeta visual con PIL simulando la foto/avatar del personaje
        img = Image.new('RGB', (300, 300), color=(40, 40, 60))
        # Añadir un marco bonito usando PIL
        img_con_marco = ImageOps.expand(img, border=10, fill=(255, 215, 0))
        
        buffer = io.BytesIO()
        img_con_marco.save(buffer, format='PNG')
        st.image(buffer.getvalue(), caption=f"{personaje['nombre']} {personaje['emoji']}", use_container_width=True)
        
    with col_info:
        st.markdown(f"## ¡Es **{personaje['nombre']}**! {personaje['emoji']}")
        st.markdown(f"*{personaje['descripcion']}*")
        st.info("¿He acertado tu personaje?")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🎉 ¡Sí, acertaste!", use_container_width=True):
                st.session_state.akinator_state = "victoria"
                st.rerun()
        with c2:
            if st.button("❌ Fallaste", use_container_width=True):
                st.session_state.akinator_state = "derrota"
                st.rerun()

elif estado == "victoria":
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1>🏆 ¡Genio de la lámpara otra vez! 🧞‍♂️</h1>
        <p style='font-size: 1.2rem;'>¡He vuelto a adivinar el personaje gracias a mi gran sabiduría virtual!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Jugar otra vez", use_container_width=True):
        st.session_state.akinator_state = "inicio"
        st.rerun()

elif estado == "derrota":
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1>🙇‍♂️ ¡Me has vencido!</h1>
        <p style='font-size: 1.2rem;'>¡Has logrado ganarle al Akinator de Streamlit! Felicidades.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Volver a intentar la revancha", use_container_width=True):
        st.session_state.akinator_state = "inicio"
        st.rerun()
