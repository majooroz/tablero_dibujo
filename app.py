import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# Título principal con estilo
st.markdown("<h1 style='text-align: center; color: #FFA500;'>🎨 Tablero de Dibujo Interactivo 🖌️</h1>", unsafe_allow_html=True)

# Barra lateral personalizada
with st.sidebar:
    st.markdown("<h2 style='color: #00FF00;'>🔧 Propiedades del Tablero</h2>", unsafe_allow_html=True)
    drawing_mode = st.selectbox(
        "Selecciona la herramienta de dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )
    
    # Slider con estilos adicionales
    stroke_width = st.slider('Ancho del trazo', 1, 30, 15)
    stroke_color = st.color_picker("Elige el color del trazo", "#FFFFFF")
    bg_color = '#000000'  # Fondo negro por defecto

# Componente del canvas con estilo y opacidad para el color de relleno
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Color de relleno con transparencia
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,  # Altura aumentada para mejor visualización
    width=500,   # Ancho ajustado para un tablero más amplio
    drawing_mode=drawing_mode,
    key="canvas",
)

# Agregar un pie de página estético
st.markdown("<footer style='text-align: center; color: #888;'>Crea algo increíble con este tablero interactivo 💡</footer>", unsafe_allow_html=True)
image = Image.open("flores.jpg")
st.image(image,caption = "flores")
texto = st.text_input("Tienes 20 años y no has conseguido mejorar tu arte, pues que lastima yo tampoco, qui te dejo una guia para dibujar mejor :)")
st.write("El texto escrito es", texto)
