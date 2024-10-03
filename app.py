import os
import streamlit as st
import base64
from openai import OpenAI
import openai
#from PIL import Image
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_drawable_canvas import st_canvas

Expert=" "
profile_imgenh=" "
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: No se encontró la imagen en la ruta especificada."

# Configuración de la página en Streamlit
st.set_page_config(page_title='Dibujo Inteligente 🎨')
st.title('Tablero de Dibujo con IA 🖼️')

# Sección de la barra lateral
with st.sidebar:
    st.subheader("Acerca de esta app:")
    st.subheader("Descubre cómo la inteligencia artificial puede interpretar un boceto que dibujes en este tablero interactivo.")
    
st.subheader("Dibuja algo en el panel y luego presiona el botón para que la IA lo analice.")

# Parámetros del canvas
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Selecciona el grosor de la línea', 1, 30, 5)
stroke_color = st.color_picker("Elige el color del trazo", "#000000")
bg_color = '#FFFFFF'

# Componente de canvas para dibujo
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Color de relleno con algo de opacidad
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    drawing_mode=drawing_mode,
    key="canvas",
)

# Ingreso de clave de API de OpenAI
ke = st.text_input('Introduce tu clave de la API de OpenAI', type="password")
os.environ['OPENAI_API_KEY'] = ke

# Recuperar la clave de API
api_key = os.environ['OPENAI_API_KEY']

# Inicializar cliente de OpenAI
client = openai

# Botón para analizar la imagen
analyze_button = st.button("Analizar el dibujo con IA", type="secondary")

# Comprobaciones para asegurarse de que la imagen está cargada, la clave API está presente, y se ha presionado el botón
if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Procesando tu dibujo, por favor espera..."):
        # Convertir la imagen del canvas a un formato adecuado
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
        input_image.save('img.png')
        
        # Codificar la imagen en base64
        base64_image = encode_image_to_base64("img.png")
        
        # Texto de solicitud
        prompt_text = (f"Describe en español brevemente la imagen")

        # Crear payload para la solicitud de OpenAI
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

        # Realizar la solicitud a la API de OpenAI
        try:
            full_response = ""
            message_placeholder = st.empty()
            response = openai.chat.completions.create(
                model="gpt-4o-mini",  # Puedes cambiar a otro modelo si lo prefieres
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                            },
                        },
                    ],
                }],
                max_tokens=500,
            )

            # Mostrar la respuesta de la IA
            if response.choices[0].message.content is not None:
                full_response += response.choices[0].message.content
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

            if Expert == profile_imgenh:
                st.session_state.mi_respuesta = response.choices[0].message.content
    
        except Exception as e:
            st.error(f"Se ha producido un error: {e}")

else:
    # Advertencias para la acción del usuario
    if not api_key:
        st.warning("Por favor, ingresa tu clave API de OpenAI.")


