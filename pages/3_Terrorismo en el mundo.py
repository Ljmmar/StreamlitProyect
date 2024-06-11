import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Terrorismo en el mundo")

# Función para intentar leer el archivo con diferentes codificaciones
def read_csv_with_fallback(file_path, encodings=['utf-8', 'latin1']):
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("No se pudo leer el archivo con las codificaciones probadas.")

try:
    df = read_csv_with_fallback('static/datasets/terrorismo.csv')
    st.write("Archivo cargado correctamente")
    
    # Filtros
    years = df['iyear'].unique()
    countries = df['country_txt'].unique()
    attack_types = df['attacktype1_txt'].unique()

    selected_year = st.selectbox("Seleccione el año", years)
    selected_country = st.selectbox("Seleccione el país", countries)
    selected_attack_type = st.selectbox("Seleccione el tipo de ataque", attack_types)

    # Filtrar datos según selección
    filtered_df = df[(df['iyear'] == selected_year) &
                     (df['country_txt'] == selected_country) &
                     (df['attacktype1_txt'] == selected_attack_type)]
    
    st.dataframe(filtered_df)  # Muestra los datos filtrados
    
    # Crear gráfico de barras
    if not filtered_df.empty:
        fig = px.bar(filtered_df, 
                     x='iyear', 
                     y='nkill', 
                     color='attacktype1_txt', 
                     title='Cantidad de ataques por año',
                     labels={'iyear': 'Año', 'nkill': 'Número de Muertes', 'attacktype1_txt': 'Tipo de Ataque'})
        st.plotly_chart(fig)
    else:
        st.write("No se encontraron datos para los filtros seleccionados.")
    
except FileNotFoundError:
    st.error("Error: El archivo 'terrorismo.csv' no se encontró en la ruta especificada.")
except pd.errors.EmptyDataError:
    st.error("Error: El archivo 'terrorismo.csv' está vacío.")
except pd.errors.ParserError:
    st.error("Error: Hubo un problema al parsear el archivo 'terrorismo.csv'.")
except ValueError as e:
    st.error(f"Error de codificación: {e}")
except Exception as e:
    st.error(f"Error inesperado: {e}")
