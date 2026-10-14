import random
from PIL import Image, ImageDraw, ImageOps, ImageEnhance, ImageFilter
import io

# Inicializar estado de sesión para el Akinator, Editor y la Calculadora
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

# Estado para la calculadora
if "calc_display" not in st.session_state:
    st.session_state.calc_display = "0"
if "calc_op_pend" not in st.session_state:
    st.session_state.calc_op_pend = None
if "calc_val_ant" not in st.session_state:
    st.session_state.calc_val_ant = 0.0
if "calc_nuevo" not in st.session_state:
    st.session_state.calc_nuevo = True

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
    
    draw.ellipse([50, 50, 250, 250], outline=(255, 255, 255), width=4)
    draw.rectangle([70, 70, 230, 230], outline=(255, 255, 255), width=2)
    draw.ellipse([110, 110, 190, 190], fill=(255, 255, 255))
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# Pestañas principales para separar el Akinator, el Editor de Fotos y la nueva Calculadora
pestana = st.tabs(["✨ Akinator Mágico", "🎨 Editor de Fotos Pro", "🧮 Calculadora Estilo Windows"])

with pestana[0]:
    st.markdown("<h2 style='text-align: center; color: #4A90E2;'>✨ El Gran Akinator Mágico ✨</h2>", unsafe_allow_html=True)
    st.write("Piensa en uno de estos 10 personajes y responde a mis preguntas. ¡A ver si logro adivinarlo!")

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

        img_editada = imagen_original.copy()

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

        if efecto_blur > 0:
            img_editada = img_editada.filter(ImageFilter.GaussianBlur(efecto_blur))

        if brillo != 1.0:
            img_editada = ImageEnhance.Brightness(img_editada).enhance(brillo)
        if contraste != 1.0:
            img_editada = ImageEnhance.Contrast(img_editada).enhance(contraste)
        if saturacion != 1.0:
            img_editada = ImageEnhance.Color(img_editada).enhance(saturacion)
        if nitidez != 1.0:
            img_editada = ImageEnhance.Sharpness(img_editada).enhance(nitidez)

        st.markdown("---")
        
        col_prev1, col_prev2 = st.columns(2)
        with col_prev1:
            st.markdown("#### 📷 Imagen Original")
            st.image(imagen_original, use_container_width=True)
        with col_prev2:
            st.markdown("#### ✨ Imagen Editada (Pro)")
            st.image(img_editada, use_container_width=True)

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

with pestana[2]:
    st.markdown("<h2 style='text-align: center; color: #2E8B57;'>🧮 Calculadora Estilo Windows 🧮</h2>", unsafe_allow_html=True)
    st.write("Una calculadora limpia y funcional con interfaz clásica.")

    # Contenedor visual tipo calculadora
    calc_container = st.container()
    with calc_container:
        # Pantalla de la calculadora
        display_val = st.session_state.get("calc_display", "0")
        st.markdown(
            f"""
            <div style="background-color: #222; color: #00FFCC; padding: 15px; border-radius: 8px; font-size: 28px; text-align: right; font-family: monospace; margin-bottom: 15px; border: 2px solid #444;">
                {display_val}
            </div>
            """,
            unsafe_allow_html=True
        )

        def agregar_digito(digito):
            disp = st.session_state.calc_display
            if st.session_state.calc_nuevo or disp == "0":
                st.session_state.calc_display = digito
                st.session_state.calc_nuevo = False
            else:
                st.session_state.calc_display = disp + digito

        def agregar_punto():
            disp = st.session_state.calc_display
            if st.session_state.calc_nuevo:
                st.session_state.calc_display = "0."
                st.session_state.calc_nuevo = False
            elif "." not in disp:
                st.session_state.calc_display = disp + "."

        def limpiar_todo():
            st.session_state.calc_display = "0"
            st.session_state.calc_op_pend = None
            st.session_state.calc_val_ant = 0.0
            st.session_state.calc_nuevo = True

        def establecer_operacion(op):
            try:
                st.session_state.calc_val_ant = float(st.session_state.calc_display)
            except ValueError:
                st.session_state.calc_val_ant = 0.0
            st.session_state.calc_op_pend = op
            st.session_state.calc_nuevo = True

        def calcular_resultado():
            try:
                val_actual = float(st.session_state.calc_display)
                op = st.session_state.calc_op_pend
                ant = st.session_state.calc_val_ant
                res = val_actual

                if op == "+":
                    res = ant + val_actual
                elif op == "-":
                    res = ant - val_actual
                elif op == "*":
                    res = ant * val_actual
                elif op == "/":
                    if val_actual == 0:
                        res = "Error"
                    else:
                        res = ant / val_actual

                if res != "Error":
                    if res.is_integer():
                        res = int(res)
                    st.session_state.calc_display = str(res)
                else:
                    st.session_state.calc_display = "Error"

                st.session_state.calc_op_pend = None
                st.session_state.calc_nuevo = True
            except Exception:
                st.session_state.calc_display = "Error"
                st.session_state.calc_nuevo = True

        # Botonera de la calculadora en rejilla (4 columnas)
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            if st.button("C", use_container_width=True):
                limpiar_todo()
                st.rerun()
            if st.button("7", use_container_width=True):
                agregar_digito("7")
                st.rerun()
            if st.button("4", use_container_width=True):
                agregar_digito("4")
                st.rerun()
            if st.button("1", use_container_width=True):
                agregar_digito("1")
                st.rerun()
            if st.button("0", use_container_width=True):
                agregar_digito("0")
                st.rerun()

        with c2:
            if st.button("±", use_container_width=True):
                try:
                    val = float(st.session_state.calc_display)
                    res = -val
                    if res.is_integer():
                        res = int(res)
                    st.session_state.calc_display = str(res)
                except:
                    pass
                st.rerun()
            if st.button("8", use_container_width=True):
                agregar_digito("8")
                st.rerun()
            if st.button("5", use_container_width=True):
                agregar_digito("5")
                st.rerun()
            if st.button("2", use_container_width=True):
                agregar_digito("2")
                st.rerun()
            if st.button(".", use_container_width=True):
                agregar_punto()
                st.rerun()

        with c3:
            if st.button("%", use_container_width=True):
                try:
                    val = float(st.session_state.calc_display) / 100.0
                    if val.is_integer():
                        val = int(val)
                    st.session_state.calc_display = str(val)
                except:
                    pass
                st.rerun()
            if st.button("9", use_container_width=True):
                agregar_digito("9")
                st.rerun()
            if st.button("6", use_container_width=True):
                agregar_digito("6")
                st.rerun()
            if st.button("3", use_container_width=True):
                agregar_digito("3")
                st.rerun()
            if st.button("=", use_container_width=True):
                calcular_resultado()
                st.rerun()

        with c4:
            if st.button("÷", use_container_width=True):
                establecer_operacion("/")
                st.rerun()
            if st.button("×", use_container_width=True):
                establecer_operacion("*")
                st.rerun()
            if st.button("-", use_container_width=True):
                establecer_operacion("-")
                st.rerun()
            if st.button("+", use_container_width=True):
                establecer_operacion("+")
                st.rerun()
            if st.button("⌫", use_container_width=True):
                disp = st.session_state.calc_display
                if len(disp) > 1:
                    st.session_state.calc_display = disp[:-1]
                else:
                    st.session_state.calc_display = "0"
                st.rerun()
