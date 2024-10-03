import os
import streamlit as st
import base64
import openai
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Función para codificar imagen en base64
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."

# Configuración inicial de la página
st.set_page_config(page_title='Tablero Inteligente')
st.title('Tablero Inteligente')

# Barra lateral con descripción
with st.sidebar:
    st.subheader("Acerca de:")
    st.subheader("En esta aplicación veremos la capacidad que ahora tiene una máquina de interpretar un boceto")

st.subheader("Dibuja el boceto en el panel y presiona el botón para analizarla")

# Parámetros del canvas
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)
stroke_color = st.color_picker("Color de Trazo", "#000000")
bg_color = '#FFFFFF'
drawing_mode = st.sidebar.selectbox(
    "Herramienta de dibujo:",
    ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
)

# Componente del canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Color de relleno fijo con opacidad
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    drawing_mode=drawing_mode,
    key="canvas",
)

# Ingreso de clave para la API
ke = st.text_input('Ingresa tu Clave', type="password")
os.environ['OPENAI_API_KEY'] = ke

# Recuperar la clave de la API
api_key = os.environ['OPENAI_API_KEY']

# Inicializar cliente de OpenAI
client = openai

# Botón para analizar la imagen
analyze_button = st.button("Analiza la imagen", type="secondary")

# Verificar si se ha cargado una imagen y si el botón ha sido presionado
if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Analizando ..."):
        # Convertir la imagen del canvas en array y guardarla como PNG
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
        input_image.save('img.png')
        
        # Codificar la imagen en base64
        base64_image = encode_image_to_base64("img.png")
        
        prompt_text = "Describe en español la imagen brevemente"
        
        # Crear payload para la solicitud
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/png;base64,{base64_image}",
                    },
                ],
            }
        ]
        
        # Solicitud a la API de OpenAI
        try:
            full_response = ""
            message_placeholder = st.empty()
            response = client.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=500,
            )
            
            # Mostrar la respuesta
            if response.choices[0].message['content'] is not None:
                full_response += response.choices[0].message['content']
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"Ha ocurrido un error: {e}")

else:
    # Advertencias si falta la clave o la imagen
    if not api_key:
        st.warning("Por favor ingresa tu API key.")


