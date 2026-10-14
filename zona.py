import random
from PIL import Image, ImageDraw, ImageOps, ImageEnhance, ImageFilter
import io

# Inicializar estado de sesión para el Akinator y el Editor estilo Photoshop
if "akinator_iniciado" not in st.session_state:
    st.session_state.akinator_iniciado = False
if "personaje_actual" not in st.session_state:
    st.session_state.personaje_actual = None
if "preguntas_hechas" not in st.session_state:
    st.session_state.preguntas_hechas = 0
if "candidatos" not in st.session_state:
    st.session_state.candidatos = []
if "historial" not in st.session_state:
    st.session_state.historial = []
if "juego_terminado" not in st.session_state:
    st.session_state.juego_terminado = False
if "adivinado" not in st.session_state:
    st.session_state.adivinado = False

# Definición de 10 personajes con sus características y colores para generar avatares bonitos
PERSONAJES = [
    {
        "nombre": "Harry Potter",
        "real": True,
        "genero": "masculino",
        "magia": True,
        "humano": True,
        "villano": False,
        "color": (120, 20, 20),
        "icono": "⚡"
    },
    {
        "nombre": "Darth Vader",
        "real": False,
        "genero": "masculino",
        "magia": True,
        "humano": True,
        "villano": True,
        "color": (30, 30, 30),
        "icono": "🌌"
    },
    {
        "nombre": "Wonder Woman",
        "real": False,
        "genero": "femenino",
        "magia": True,
        "humano": False,
        "villano": False,
        "color": (200, 160, 20),
        "icono": "⭐"
    },
    {
        "nombre": "Sherlock Holmes",
        "real": False,
        "genero": "masculino",
        "magia": False,
        "humano": True,
        "villano": False,
        "color": (50, 70, 90),
        "icono": "🔍"
    },
    {
        "nombre": "Elsa (Frozen)",
        "real": False,
        "genero": "femenino",
        "magia": True,
        "humano": True,
        "villano": False,
        "color": (100, 180, 220),
        "icono": "❄️"
    },
    {
        "nombre": "Albert Einstein",
        "real": True,
        "genero": "masculino",
        "magia": False,
        "humano": True,
        "villano": False,
        "color": (90, 90, 90),
        "icono": "💡"
    },
    {
        "nombre": "Batman",
        "real": False,
        "genero": "masculino",
        "magia": False,
        "humano": True,
        "villano": False,
        "color": (20, 20, 40),
        "icono": "🦇"
    },
    {
        "nombre": "Hermione Granger",
        "real": False,
        "genero": "femenino",
        "magia": True,
        "humano": True,
        "villano": False,
        "color": (150, 40, 40),
        "icono": "📚"
    },
    {
        "nombre": "Iron Man",
        "real": False,
        "genero": "masculino",
        "magia": False,
        "humano": True,
        "villano": False,
        "color": (220, 40, 40),
        "icono": "🤖"
    },
    {
        "nombre": "Cleopatra",
        "real": True,
        "genero": "femenino",
        "magia": False,
        "humano": True,
        "villano": False,
        "color": (180, 140, 40),
        "icono": "👑"
    }
]

# Función para generar una imagen bonita del personaje usando PIL
def generar_imagen_personaje(personaje):
    img = Image.new("RGB", (300, 300), color=personaje["color"])
    draw = ImageDraw.Draw(img)
    
    # Dibujar formas geométricas decorativas
    draw.ellipse([50, 50, 250, 250], outline=(255, 255, 255), width=4)
    draw.rectangle([70, 70, 230, 230], outline=(255, 255, 255), width=2)
    draw.ellipse([110, 110, 190, 190], fill=(255, 255, 255))
    
    # Convertir a buffer para mostrar en streamlit
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# Pestañas principales para separar el Akinator y el nuevo Editor de Fotos estilo Photoshop
pestana = st.tabs(["✨ Akinator Mágico", "🎨 Editor de Fotos Pro"])

with pestana[0]:
    st.markdown("<h2 style='text-align: center; color: #4A90E2;'>✨ El Gran Akinator Mágico ✨</h2>", unsafe_allow_html=True)
    st.write("Piensa en uno de estos 10 personajes y responde a mis preguntas. ¡A ver si logro adivinarlo!")

    # Mostrar los personajes posibles en un desplegable bonito
    with st.expander("👀 Ver la lista de los 10 personajes posibles"):
        cols = st.columns(5)
        for i, p in enumerate(PERSONAJES):
            with cols[i % 5]:
                st.markdown(f"**{p['icono']} {p['nombre']}**")

    st.markdown("---")

    def reiniciar_juego():
        st.session_state.akinator_iniciado = True
        st.session_state.candidatos = list(PERSONAJES)
        st.session_state.preguntas_hechas = 0
        st.session_state.historial = []
        st.session_state.juego_terminado = False
        st.session_state.adivinado = False
        st.session_state.personaje_actual = None

    if not st.session_state.akinator_iniciado:
        if st.button("🚀 ¡Empezar a Jugar!", use_container_width=True):
            reiniciar_juego()
            st.rerun()
    else:
        if not st.session_state.juego_terminado:
            candidatos = st.session_state.candidatos
            
            if len(candidatos) <= 1 or st.session_state.preguntas_hechas >= 5:
                st.session_state.juego_terminado = True
                st.session_state.adivinado = True
                st.session_state.personaje_actual = candidatos[0] if candidatos else random.choice(PERSONAJES)
                st.rerun()
            
            atributos_disponibles = ["magia", "genero", "humano", "villano", "real"]
            atrib = random.choice(atributos_disponibles)
            
            preguntas_map = {
                "magia": "🔮 ¿Tu personaje utiliza magia o poderes sobrenaturales?",
                "genero": "👤 ¿Tu personaje es de género femenino?",
                "humano": "🧬 ¿Tu personaje es un ser humano normal (sin superpoderes naturales/extraterrestres)?",
                "villano": "🦹 ¿Tu personaje es considerado un villano o antagonista?",
                "real": "📜 ¿Tu personaje es una persona real de la historia?"
            }
            
            st.subheader(f"Pregunta #{st.session_state.preguntas_hechas + 1}")
            st.write(preguntas_map[atrib])
            
            col1, col2, col3 = st.columns(3)
            
            def responder(respuesta):
                st.session_state.preguntas_hechas += 1
                nuevos_candidatos = []
                for c in st.session_state.candidatos:
                    if atrib == "genero":
                        val = (c[atrib] == "femenino")
                    else:
                        val = c[atrib]
                    
                    if respuesta == "Sí" and val:
                        nuevos_candidatos.append(c)
                    elif respuesta == "No" and not val:
                        nuevos_candidatos.append(c)
                    elif respuesta == "No estoy seguro":
                        nuevos_candidatos.append(c)
                
                if nuevos_candidatos:
                    st.session_state.candidatos = nuevos_candidatos
                
                if len(st.session_state.candidatos) == 1 or st.session_state.preguntas_hechas >= 5:
                    st.session_state.juego_terminado = True
                    st.session_state.adivinado = True
                    st.session_state.personaje_actual = st.session_state.candidatos[0]
                st.rerun()

            with col1:
                if st.button("✅ Sí", use_container_width=True):
                    responder("Sí")
            with col2:
                if st.button("❌ No", use_container_width=True):
                    responder("No")
            with col3:
                if st.button("❓ No sé", use_container_width=True):
                    responder("No estoy seguro")
                    
        else:
            personaje = st.session_state.personaje_actual
            st.balloons()
            st.success("🎉 ¡Akinator ha pensado en un resultado!")
            
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                img_buffer = generar_imagen_personaje(personaje)
                st.image(img_buffer, caption=f"{personaje['icono']} {personaje['nombre']}", use_container_width=True)
                
            with col_txt:
                st.markdown(f"### ¡Tu personaje es **{personaje['nombre']}**! {personaje['icono']}")
                st.write(f"Preguntas realizadas: **{st.session_state.preguntas_hechas}**")
                st.markdown("¿He acertado tu personaje?")
                
                if st.button("🔄 ¡Jugar otra vez!", use_container_width=True):
                    reiniciar_juego()
                    st.rerun()

with pestana[1]:
    st.markdown("<h2 style='text-align: center; color: #E24A90;'>🎨 Editor de Fotos Estilo Photoshop Pro 🎨</h2>", unsafe_allow_html=True)
    st.write("Sube una imagen y aplica herramientas profesionales de edición fotográfica en tiempo real.")

    archivo_foto = st.file_uploader("📂 Carga tu imagen (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

    if archivo_foto is not None:
        imagen_original = Image.open(archivo_foto).convert("RGB")
        
        # Barra lateral o controles de edición estilo Photoshop
        st.markdown("### 🎛️ Panel de Control y Ajustes")
        
        col_op1, col_op2 = st.columns(2)
        
        with col_op1:
            modo_color = st.selectbox("Modo de Color / Filtro", ["Normal", "Escala de Grises", "Sepia", "Invertir", "Alto Contraste"])
            efecto_blur = st.slider("Desenfocar (Blur)", 0, 10, 0)
            rotar = st.selectbox("Rotar / Espejo", ["Sin cambios", "Rotar 90°", "Rotar 180°", "Rotar 270°", "Reflejar Horizontal", "Reflejar Vertical"])

        with col_op2:
            brillo = st.slider("Brillo", 0.0, 2.0, 1.0, 0.1)
            contraste = st.slider("Contraste", 0.0, 2.0, 1.0, 0.1)
            saturacion = st.slider("Saturación", 0.0, 2.0, 1.0, 0.1)
            nitidez = st.slider("Nitidez", 0.0, 3.0, 1.0, 0.1)

        # Procesamiento de imagen paso a paso
        img_editada = imagen_original.copy()

        # 1. Rotaciones y Espejos
        if rotar == "Rotar 90°":
            img_editada = img_editada.rotate(90, expand=True)
        elif rotar == "Rotar 180°":
            img_editada = img_editada.rotate(180, expand=True)
        elif rotar == "Rotar 270°":
            img_editada = img_editada.rotate(270, expand=True)
        elif rotar == "Reflejar Horizontal":
            img_editada = ImageOps.mirror(img_editada)
        elif rotar == "Reflejar Vertical":
            img_editada = ImageOps.flip(img_editada)

        # 2. Modos de color y filtros
        if modo_color == "Escala de Grises":
            img_editada = ImageOps.grayscale(img_editada).convert("RGB")
        elif modo_color == "Invertir":
            img_editada = ImageOps.invert(img_editada)
        elif modo_color == "Sepia":
            gray = ImageOps.grayscale(img_editada)
            img_editada = ImageOps.colorize(gray, "#704214", "#FFC0CB").convert("RGB")
        elif modo_color == "Alto Contraste":
            enhancer = ImageEnhance.Contrast(img_editada)
            img_editada = enhancer.enhance(1.8)

        # 3. Desenfoque
        if efecto_blur > 0:
            img_editada = img_editada.filter(ImageFilter.GaussianBlur(efecto_blur))

        # 4. Ajustes de Enhancer (Brillo, Contraste, Saturación, Nitidez)
        if brillo != 1.0:
            img_editada = ImageEnhance.Brightness(img_editada).enhance(brillo)
        if contraste != 1.0:
            img_editada = ImageEnhance.Contrast(img_editada).enhance(contraste)
        if saturacion != 1.0:
            img_editada = ImageEnhance.Color(img_editada).enhance(saturacion)
        if nitidez != 1.0:
            img_editada = ImageEnhance.Sharpness(img_editada).enhance(nitidez)

        st.markdown("---")
        
        # Vista previa comparativa o directa
        col_prev1, col_prev2 = st.columns(2)
        with col_prev1:
            st.markdown("#### 📷 Imagen Original")
            st.image(imagen_original, use_container_width=True)
        with col_prev2:
            st.markdown("#### ✨ Imagen Editada (Pro)")
            st.image(img_editada, use_container_width=True)

        # Botón de descarga profesional
        buffer_salida = io.BytesIO()
        img_editada.save(buffer_salida, format="PNG")
        buffer_salida.seek(0)

        st.markdown("---")
        st.download_button(
            label="💾 Descargar Imagen Editada (PNG)",
            data=buffer_salida,
            file_name="foto_editada_pro.png",
            mime="image/png",
            use_container_width=True
        )
    else:
        st.info("💡 Sube una imagen arriba para activar las herramientas de edición estilo Photoshop.")
