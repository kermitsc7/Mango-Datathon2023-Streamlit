import streamlit as st
import os
from PIL import Image
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import random
import ast
import io

#Cargamos el grafo
file = open("data/final_products.pickle",'rb')
graph = pickle.load(file)
file.close()

#Cargamos los datos
product_data = pd.read_csv('data/final_products.csv')
outfit_data = pd.read_csv('data/final_outfits.csv')

# Función para redimensionar una imagen manteniendo la proporción de aspecto
def redimensionar_imagen(imagen, ancho_maximo):
    # Mantener la proporción de aspecto
    proporción = ancho_maximo / float(imagen.size[0])
    alto = int((float(imagen.size[1]) * float(proporción)))
    imagen = imagen.resize((ancho_maximo, alto), Image.ANTIALIAS)
    return imagen

def mostrar_imagen(product_data, codigo_ropa):
    prenda = product_data[product_data["cod_modelo_color"] == codigo_ropa]
    prenda_filename = prenda["des_filename"].iloc[0]
    # Cargar la imagen
    img = Image.open(prenda_filename)

    return img

def mostrar_outfit(dataset_o, dataset_f, num_outfit):
    filas = 4
    columnas = 4
    
    items = dataset_o[dataset_o["cod_outfit"]==num_outfit]["cod_modelo_color"].iloc[0]
    items = ast.literal_eval(items)
    path_items_list = []
    for item in items:
        prenda = dataset_f[dataset_f["cod_modelo_color"] == item]
        prenda_filename = prenda["des_filename"].iloc[0]
        path_items_list.append(prenda_filename)
    
    fig, axes = plt.subplots(filas, columnas, figsize=(15, 15))  # Ajusta el tamaño según necesites
    axes = axes.flatten()

    for i, nombre_imagen in enumerate(path_items_list):
        img = Image.open(nombre_imagen)
        axes[i].imshow(img)
        axes[i].axis('off')  # Ocultar los ejes
        
    # Ocultar subplots vacíos si existen
    for j in range(i + 1, filas * columnas):
        axes[j].axis('off')

    plt.tight_layout()
    
    # Convertir la figura a un buffer de imagen PNG
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    
    # Retornar el buffer para que pueda ser mostrado en Streamlit
    return buf


header_html = """
    <div style='background-color: white; padding: 10px; border-radius: 5px;'>
        <h1 style='color: black; text-align: center; font-family: stencil, sans-serif;'>MANGO</h1>
    </div>
    """

slider = """
    <div>
        <h4 style='color: white; text-align: left; font-family: stencil, sans-serif;'>Que prenda quieres combinar?</h4>
    </div>
    """

img_slider = "./images_streamlit"
# Usar Markdown para inyectar el HTML
st.markdown(header_html, unsafe_allow_html=True)

st.image("./portada.png")


imagenes = [os.path.join(img_slider, img) for img in os.listdir(img_slider) if img.endswith((".png", ".jpg", ".jpeg"))]

# Slider
st.markdown(slider, unsafe_allow_html=True)
st.write("Desliza el slider para escojer una de las prendas disponibles")
indice_seleccionado = st.slider("",0, len(imagenes) - 1, 0)
col1, col2, col3 = st.columns([1,2,1])
if imagenes:
    imagen = Image.open(imagenes[indice_seleccionado])
    with col2:
        st.image(imagen)


# Crear un botón en Streamlit
if st.button('Clica para Generar!'):
    
    # Código que siempre se muestra, independientemente de si el botón se presiona o no
   
    name = imagenes[indice_seleccionado]
    partes = name.split('_')
    aux = partes[2]+ "-" + partes[3]
    aux2 = aux.split('.')
    resultado = aux2[0]
    cod_modelo_color_ejemplo = resultado # Reemplaza con un código real
    outfits = []

    tabla_recomendaciones_final = product_data[(product_data['cod_modelo_color'] == cod_modelo_color_ejemplo)]
    num = 7900
    generem = True
    while(generem != False):
        num = random.choice(list(tabla_recomendaciones_final['cod_outfit']))
        if num <= 7842:
            generem = True
        else:
            outfits.append(num)

        if len(outfits) > 5:
            generem = False

    st.write("OUTFITS DISPONIBLES")
    st.image(mostrar_outfit(outfit_data, product_data, outfits[0]))
    st.image(mostrar_outfit(outfit_data, product_data, outfits[1]))
    st.image(mostrar_outfit(outfit_data, product_data, outfits[2]))
    st.image(mostrar_outfit(outfit_data, product_data, outfits[3]))
    st.image(mostrar_outfit(outfit_data, product_data, outfits[4]))

