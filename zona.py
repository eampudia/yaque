import random
from PIL import Image, ImageDraw, ImageOps, ImageEnhance, ImageFilter
import io

# Inicializar estado de sesión para el Akinator, Editor, la Calculadora y la nueva característica (Generador de Memes / Plantillas)
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

# Estado para el Generador de Memes
if "meme_texto_superior" not in st.session_state:
    st.session_state.meme_texto_superior = "CUANDO PROGRAMAS EN PYTHON"
if "meme_texto_inferior" not in st.session_state:
    st.session_state.meme_texto_inferior = "Y TODO FUNCIONA A LA PRIMERA"
if "meme_tamano_fuente" not in st.session_state:
    st.session_state.meme_tamano_fuente = 36
if "meme_color_texto" not in st.session_state:
    st.session_state.meme_color_texto = "Blanco"

# Definición extendida y rica de personajes para un Akinator de alta calidad
PERSONAJES = [
    {
        "nombre": "Harry Potter",
        "real": False,
        "genero": "masculino",
        "magia": True,
        "humano": True,
        "villano": False,
        "animacion": False,
        "franquicia": "Harry Potter",
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
        "animacion": False,
        "franquicia": "Star Wars",
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
        "animacion": False,
        "franquicia": "DC Comics",
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
        "animacion": False,
        "franquicia": "Literatura Clásica",
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
        "animacion": True,
        "franquicia": "Disney",
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
        "animacion": False,
        "franquicia": "Historia Real",
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
        "animacion": False,
        "franquicia": "DC Comics",
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
        "animacion": False,
        "franquicia": "Harry Potter",
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
        "animacion": False,
        "franquicia": "Marvel",
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
        "animacion": False,
        "franquicia": "Historia Real",
        "color": (180, 140, 40),
        "icono": "👑"
    },
    {
        "nombre": "Goku",
        "real": False,
        "genero": "masculino",
        "magia": True,
        "humano": False,
        "villano": False,
        "animacion": True,
        "franquicia": "Dragon Ball",
        "color": (230, 120, 20),
        "icono": "🐉"
    },
    {
        "nombre": "Spider-Man",
        "real": False,
        "genero": "masculino",
        "magia": False,
        "humano": True,
        "villano": False,
        "animacion": False,
        "franquicia": "Marvel",
        "color": (200, 30, 30),
        "icono": "🕷️"
    },
    {
        "nombre": "Joker",
        "real": False,
        "genero": "masculino",
        "magia": False,
        "humano": True,
        "villano": True,
        "animacion": False,
        "franquicia": "DC Comics",
        "color": (80, 20, 120),
        "icono": "🃏"
    },
    {
        "nombre": "Homer Simpson",
        "real": False,
        "genero": "masculino",
        "magia": False,
        "humano": True,
        "villano": False,
        "animacion": True,
        "franquicia": "Los Simpson",
        "color": (240, 200, 40),
        "icono": "🍩"
    },
    {
        "nombre": "Leonardo da Vinci",
        "real": True,
        "genero": "masculino",
        "magia": False,
        "humano": True,
        "villano": False,
        "animacion": False,
        "franquicia": "Historia Real",
        "color": (140, 100, 60),
        "icono": "🎨"
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

# Pestañas principales incluyendo la nueva característica (Generador de Memes)
pestana = st.tabs([
    "✨ Akinator Mágico", 
    "🎨 Editor de Fotos Pro", 
    "🧮 Calculadora Estilo Windows",
    "🃏 Creador de Memes Express"
])

with pestana[0]:
    st.markdown("<h2 style='text-align: center; color: #4A90E2;'>✨ El Gran Akinator Mágico ✨</h2>", unsafe_allow_html=True)
    st.write("Piensa en uno de los personajes de la lista y responde a mis preguntas. ¡Usaré lógica inteligente para adivinarlo!")

    with st.expander("👀 Ver la lista completa de personajes posibles"):
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

    if not st.session_state.get("akinator_iniciado", False):
        if st.button("🚀 ¡Empezar a Jugar!", use_container_width=True):
            reiniciar_juego()
            st.rerun()
    else:
        if not st.session_state.get("juego_terminado", False):
            candidatos = st.session_state.get("candidatos", list(PERSONAJES))
            preguntas_hechas = st.session_state.get("preguntas_hechas", 0)
            
            if len(candidatos) <= 1 or preguntas_hechas >= 7:
                st.session_state.juego_terminado = True
                st.session_state.adivinado = True
                st.session_state.personaje_actual = candidatos[0] if candidatos else random.choice(PERSONAJES)
                st.rerun()
            
            atributos_disponibles = ["magia", "genero", "humano", "villano", "real", "animacion"]
            mejor_atributo = None
            min_diferencia = float('inf')
            
            for atrib in atributos_disponibles:
                if any(atrib in c for c in candidatos):
                    conteo_si = sum(1 for c in candidatos if (c.get("genero") == "femenino" if atrib == "genero" else c.get(atrib, False)))
                    diferencia = abs(len(candidatos) / 2 - conteo_si)
                    if diferencia < min_diferencia:
                        min_diferencia = diferencia
                        mejor_atributo = atrib

            if not mejor_atributo:
                mejor_atributo = random.choice(atributos_disponibles)
            
            preguntas_map = {
                "magia": "🔮 ¿Tu personaje utiliza magia, superpoderes o habilidades sobrenaturales?",
                "genero": "👤 ¿Tu personaje es de género femenino?",
                "humano": "🧬 ¿Tu personaje es un ser humano (sin origen alienígena, dios, etc.)?",
                "villano": "🦹 ¿Tu personaje es considerado un villano, antagonista o criminal?",
                "real": "📜 ¿Tu personaje es una persona real de la historia o la vida real?",
                "animacion": "🎨 ¿Tu personaje pertenece a una obra de animación, dibujo animado o anime?"
            }
            
            st.subheader(f"Pregunta #{preguntas_hechas + 1}")
            st.write(preguntas_map.get(mejor_atributo, "¿Tu personaje cumple con esta característica?"))
            
            col1, col2, col3 = st.columns(3)
            
            def responder(respuesta):
                st.session_state.preguntas_hechas = st.session_state.get("preguntas_hechas", 0) + 1
                nuevos_candidatos = []
                for c in st.session_state.get("candidatos", list(PERSONAJES)):
                    if mejor_atributo == "genero":
                        val = (c.get(mejor_atributo) == "femenino")
                    else:
                        val = c.get(mejor_atributo, False)
                    
                    if respuesta == "Sí" and val:
                        nuevos_candidatos.append(c)
                    elif respuesta == "No" and not val:
                        nuevos_candidatos.append(c)
                    elif respuesta == "No estoy seguro":
                        nuevos_candidatos.append(c)
                
                if nuevos_candidatos:
                    st.session_state.candidatos = nuevos_candidatos
                
                if len(st.session_state.candidatos) == 1 or st.session_state.preguntas_hechas >= 7:
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
            personaje = st.session_state.get("personaje_actual", PERSONAJES[0])
            st.balloons()
            st.success("🎉 ¡Akinator ha deducido el resultado!")
            
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                img_buffer = generar_imagen_personaje(personaje)
                st.image(img_buffer, caption=f"{personaje['icono']} {personaje['nombre']}", use_container_width=True)
                
            with col_txt:
                st.markdown(f"### ¡Tu personaje es **{personaje['nombre']}**! {personaje['icono']}")
                st.write(f"Franquicia / Origen: **{personaje.get('franquicia', 'Desconocido')}**")
                st.write(f"Preguntas realizadas: **{st.session_state.get('preguntas_hechas', 0)}**")
                st.markdown("¿He acertado tu personaje?")
                
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    if st.button("🎯 ¡Sí, acertaste!", use_container_width=True):
                        st.success("¡Genial! Gracias por jugar.")
                with col_res2:
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

    calc_container = st.container()
    with calc_container:
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
            disp = st.session_state.get("calc_display", "0")
            if st.session_state.get("calc_nuevo", True) or disp == "0":
                st.session_state.calc_display = digito
                st.session_state.calc_nuevo = False
            else:
                st.session_state.calc_display = disp + digito

        def agregar_punto():
            disp = st.session_state.get("calc_display", "0")
            if st.session_state.get("calc_nuevo", True):
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
                st.session_state.calc_val_ant = float(st.session_state.get("calc_display", "0"))
            except ValueError:
                st.session_state.calc_val_ant = 0.0
            st.session_state.calc_op_pend = op
            st.session_state.calc_nuevo = True

        def calcular_resultado():
            try:
                val_actual = float(st.session_state.get("calc_display", "0"))
                op = st.session_state.get("calc_op_pend", None)
                ant = st.session_state.get("calc_val_ant", 0.0)
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
                    if isinstance(res, float) and res.is_integer():
                        res = int(res)
                    st.session_state.calc_display = str(res)
                else:
                    st.session_state.calc_display = "Error"

                st.session_state.calc_op_pend = None
                st.session_state.calc_nuevo = True
            except Exception:
                st.session_state.calc_display = "Error"
                st.session_state.calc_nuevo = True

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
                    val = float(st.session_state.get("calc_display", "0"))
                    res = -val
                    if isinstance(res, float) and res.is_integer():
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
                    val = float(st.session_state.get("calc_display", "0")) / 100.0
                    if isinstance(val, float) and val.is_integer():
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
                disp = st.session_state.get("calc_display", "0")
                if len(disp) > 1:
                    st.session_state.calc_display = disp[:-1]
                else:
                    st.session_state.calc_display = "0"
                st.rerun()

with pestana[3]:
    st.markdown("<h2 style='text-align: center; color: #FF8C00;'>🃏 Creador de Memes Express 🃏</h2>", unsafe_allow_html=True)
    st.write("Sube una imagen o usa una plantilla prediseñada para crear tus propios memes al instante.")

    archivo_meme = st.file_uploader("📂 Sube tu imagen para meme (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"], key="uploader_meme")

    if archivo_meme is not None:
        img_meme_base = Image.open(archivo_meme).convert("RGB")
    else:
        # Crear una imagen por defecto llamativa si no se sube ninguna
        img_meme_base = Image.new("RGB", (500, 400), color=(50, 50, 70))
        draw_def = ImageDraw.Draw(img_meme_base)
        draw_def.rectangle([40, 40, 460, 360], outline=(255, 255, 255), width=3)
        draw_def.text((120, 180), "¡Sube tu imagen aquí!", fill=(255, 255, 255))

    st.markdown("### ✍️ Textos del Meme")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        texto_superior = st.text_input("Texto Superior", value=st.session_state.get("meme_texto_superior", "CUANDO PROGRAMAS EN PYTHON"))
        st.session_state.meme_texto_superior = texto_superior
    with col_t2:
        texto_inferior = st.text_input("Texto Inferior", value=st.session_state.get("meme_texto_inferior", "Y TODO FUNCIONA A LA PRIMERA"))
        st.session_state.meme_texto_inferior = texto_inferior

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        tamano_fuente = st.slider("Tamaño de Fuente", 16, 72, st.session_state.get("meme_tamano_fuente", 36))
        st.session_state.meme_tamano_fuente = tamano_fuente
    with col_m2:
        color_texto_opc = st.selectbox("Color del Texto", ["Blanco", "Amarillo", "Verde Neón", "Cian"], index=0)
        st.session_state.meme_color_texto = color_texto_opc

    color_map = {
        "Blanco": (255, 255, 255),
        "Amarillo": (255, 255, 0),
        "Verde Neón": (0, 255, 128),
        "Cian": (0, 255, 255)
    }
    color_rgb = color_map.get(color_texto_opc, (255, 255, 255))

    # Generar imagen con texto de meme
    img_meme_final = img_meme_base.copy()
    draw_meme = ImageDraw.Draw(img_meme_final)

    # Dibujar texto superior centrado
    if texto_superior:
        # Usar trazo simulado para contorno negro y texto de color
        bbox = draw_meme.textbbox((0, 0), texto_superior)
        w_t = bbox[2] - bbox[0]
        x_t = (img_meme_final.width - w_t) / 2
        y_t = 15
        
        # Contorno negro para legibilidad
        for adj_x in [-2, -1, 0, 1, 2]:
            for adj_y in [-2, -1, 0, 1, 2]:
                draw_meme.text((x_t + adj_x, y_t + adj_y), texto_superior.upper(), fill=(0, 0, 0))
        draw_meme.text((x_t, y_t), texto_superior.upper(), fill=color_rgb)

    # Dibujar texto inferior centrado
    if texto_inferior:
        bbox_inf = draw_meme.textbbox((0, 0), texto_inferior)
        w_inf = bbox_inf[2] - bbox_inf[0]
        h_inf = bbox_inf[3] - bbox_inf[1]
        x_inf = (img_meme_final.width - w_inf) / 2
        y_inf = img_meme_final.height - h_inf - 25
        
        for adj_x in [-2, -1, 0, 1, 2]:
            for adj_y in [-2, -1, 0, 1, 2]:
                draw_meme.text((x_inf + adj_x, y_inf + adj_y), texto_inferior.upper(), fill=(0, 0, 0))
        draw_meme.text((x_inf, y_inf), texto_inferior.upper(), fill=color_rgb)

    st.markdown("---")
    st.markdown("#### 🖼️ Vista Previa del Meme")
    st.image(img_meme_final, use_container_width=True)

    buffer_meme = io.BytesIO()
    img_meme_final.save(buffer_meme, format="PNG")
    buffer_meme.seek(0)

    st.download_button(
        label="💾 Descargar Meme Creado (PNG)",
        data=buffer_meme,
        file_name="meme_generado.png",
        mime="image/png",
        use_container_width=True
    )
