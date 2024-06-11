import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar el archivo CSV con encoding especificado
df = pd.read_csv('static/datasets/restaurante.csv', encoding='latin1')

st.title("Proyecto Restaurante")
# Convertir la columna 'Fecha' a tipo de dato de fecha
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Filtros
filtro_fecha = st.date_input("Selecciona un rango de fechas:", value=(df['Fecha'].min().date(), df['Fecha'].max().date()))
filtro_estado = st.selectbox("Selecciona un estado:", df['Estado'].unique())

# Convertir el rango de fechas a tipo de dato de fecha
fecha_inicio = pd.to_datetime(filtro_fecha[0])
fecha_fin = pd.to_datetime(filtro_fecha[1])

# Aplicar filtros
df_filtrado = df[(df['Fecha'] >= fecha_inicio) & (df['Fecha'] <= fecha_fin) & (df['Estado'] == filtro_estado)]

# Mostrar los datos filtrados en una tabla
st.write("Datos filtrados del restaurante:")
st.write(df_filtrado)

# Crear un gráfico de barras para visualizar los ingresos por mes
fig = px.bar(df_filtrado, x='Fecha', y='Total', title=f'Ingresos del restaurante para el estado "{filtro_estado}"')
st.plotly_chart(fig)
