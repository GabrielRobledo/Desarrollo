import pyodbc
import streamlit as st
import plotly.express as px
import pandas as pd

# Parámetros de conexión
server = 'IPSDB-Replica' 
database = 'DoCo'
username = 'IPSCOR\36548944'
password = ''


    # Crear una cadena de conexión utilizando ODBC Driver 18
conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes; Encrypt=no'
conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=IPSDB-Replica;DATABASE=DoCo;Trusted_Connection=yes; Encrypt=no')
#conn = pyodbc.connect(conn_str)
    # Establecer la conexión
try:
        conn = pyodbc.connect(conn_str)
        print("Conexión exitosa")



except Exception as e:
        print(f"Error de conexión: {e}")
    
cursor = conn.cursor()

# Establecer configuración de la página y Titulo del Reporte
st.set_page_config(page_title="Mi Reporte", layout="wide")
st.title("Reporte Situacion Previsional IPS 15-11-2024 al 30-11-2024")

# Primer consulta SQL Cantidad de Expedientes por tipo
consulta1 = """select [Tipo Expedientes], COUNT(Extracto) as 'Cantidad' from expedientes where [Tipo Expedientes] = 'Jubilación Ordinaria' or  [Tipo Expedientes] = 'Retiro Policial Voluntario' or [Tipo Expedientes] = 'Jubilación por Invalidez' or  [Tipo Expedientes] = 'Retiro Policial por Incapacidad' or [Tipo Expedientes] = 'Retiro Policial Obligatorio' or [Tipo Expedientes] = 'Reconocimiento de Servicios'  and [Fecha inicio] between '15-11-2024' AND '30-11-2024' group by [Tipo Expedientes] """
cursor.execute(consulta1)
resultado1 = cursor.fetchall()

data1=[]

for fila in resultado1:
    data1.append({"Tipo Expedientes": fila[0], "Cantidad": fila[1]})

df = pd.DataFrame(data1)

tiposExptes= df['Tipo Expedientes'].unique()
# Calcular el total de la columna "Valor"
total_valor = df["Cantidad"].sum()

# Crear gráfico interactivo
fig = px.bar(df, x='Tipo Expedientes', y="Cantidad", text='Cantidad', text_auto=True)

# Usar st.columns para colocar los gráficos en columnas
col1, col2, col3 = st.columns(3)

# Mostrar los gráficos en las columnas
with col1:
    st.write("Cantidad de Expedientes por tipo")
    st.dataframe(df)

with col2:
    st.plotly_chart(fig)

data2=[]

# Segundo consulta SQL Listado Expedientes Por Sector Actual
consulta2 = """select [Sector Actual], COUNT(Extracto) AS 'Cant de Exptes' from expedientes where [Tipo Expedientes] = 'Jubilación Ordinaria' or  [Tipo Expedientes] = 'Retiro Policial Voluntario' or [Tipo Expedientes] = 'Jubilación por Invalidez' or  [Tipo Expedientes] = 'Retiro Policial por Incapacidad' or [Tipo Expedientes] = 'Retiro Policial Obligatorio' or [Tipo Expedientes] = 'Reconocimiento de Servicios'  and [Fecha inicio] between '15-11-2024' AND '30-11-2024' group by  [Sector Actual] """
cursor.execute(consulta2)
resultado2 = cursor.fetchall()

for fila in resultado2:
    data2.append({"Sector Actual": fila[0], "Cantidad": fila[1]})

df2 = pd.DataFrame(data2)

# Crear gráfico interactivo
fig2 = px.bar(df2, x='Sector Actual', y="Cantidad", text='Cantidad', text_auto=True, width= 900, height= 600)    

col4, col5, col6 = st.columns(3)
# Mostrar los gráficos en las columnas
with col4:
    st.write("Listado Expedientes Por Sector Actual")
    st.dataframe(df2)
    
with col5:
    st.plotly_chart(fig2)

# Segundo consulta SQL Listado Expedientes Solicitados
consulta3 = """select [Tipo Expedientes], COUNT(Extracto) as 'Cantidad Solicitados' from expedientes where [Tipo Expedientes] = 'Jubilación Ordinaria' or  [Tipo Expedientes] = 'Retiro Policial Voluntario' or [Tipo Expedientes] = 'Jubilación por Invalidez' or  [Tipo Expedientes] = 'Retiro Policial por Incapacidad' or [Tipo Expedientes] = 'Retiro Policial Obligatorio' or [Tipo Expedientes] = 'Reconocimiento de Servicios'  and [Fecha inicio] between '15-11-2024' AND '30-11-2024' group by [Tipo Expedientes]"""
cursor.execute(consulta3)
resultados3 = cursor.fetchall()

data3=[]

for fila in resultados3:
    data3.append({"Tipo Expedientes": fila[0], "Cantidad": fila[1]})

df3 = pd.DataFrame(data3)

fig3 = px.pie(df3, names='Tipo Expedientes', values="Cantidad", hole=.5)

col7, col8, col9 = st.columns(3)
# Mostrar los gráficos en las columnas
with col7:
    st.write("Listado Expedientes Solicitados")
    st.dataframe(df3)

with col8:
    st.plotly_chart(fig3)


#CUARTA CONSULTA SQL LISTADO DE EXPEDIENTES NO RESUELTOS
consulta4 = """select exp.[Tipo Expedientes], COUNT(Extracto) as 'Cantidades'
from expedientes exp
where not exists (select pases.[Nro. Expedientes] from pases where Sector = 'Div. Despacho' and pases.[Nro. Expedientes]=exp.[Nro. Expedientes])
and ([Tipo Expedientes] = 'Jubilación Ordinaria' or  [Tipo Expedientes] = 'Retiro Policial Voluntario' or [Tipo Expedientes] = 'Jubilación por Invalidez' or  [Tipo Expedientes] = 'Retiro Policial por Incapacidad' or [Tipo Expedientes] = 'Retiro Policial Obligatorio' or [Tipo Expedientes] = 'Reconocimiento de Servicios') and ([Fecha inicio] between '15-11-2024' AND '30-11-2024') group by exp.[Tipo Expedientes]"""
cursor.execute(consulta4)
resultados4 = cursor.fetchall()

data4=[]

for fila in resultados4:
    data4.append({"Tipo Expedientes": fila[0], "Cantidades": fila[1]})

df4 = pd.DataFrame(data4)

fig4 = px.bar(df4, x='Tipo Expedientes', y='Cantidades', text='Cantidades', text_auto=True)
fig4.update_xaxes(tickangle=35)

col10, col11, col12 = st.columns(3)

# Mostrar los gráficos en las columnas
with col10:
    st.write("Listado Expedientes No Resueltos")
    st.dataframe(df4)

with col11:
    st.plotly_chart(fig4)


#QUINTA CONSULTA SQL LISTADO DE EXPEDIENTES NO RESUELTOS
consulta5 = """select CONVERT(DATE,[Fecha inicio]) 'Fecha incio', [Tipo Expedientes], Extracto from expedientes
where ([Tipo Expedientes] = 'Jubilación Ordinaria' or  [Tipo Expedientes] = 'Retiro Policial Voluntario' or [Tipo Expedientes] = 'Jubilación por Invalidez' or  [Tipo Expedientes] = 'Retiro Policial por Incapacidad' or [Tipo Expedientes] = 'Retiro Policial Obligatorio' or [Tipo Expedientes] = 'Reconocimiento de Servicios') and ([Fecha inicio] between '15-11-2024' AND '30-11-2024')"""
cursor.execute(consulta5)
resultados5 = cursor.fetchall()

data5 = []

if resultados5:
    for fila in resultados5:
        # Agregar el registro a la lista 'data'
        data5.append({"Fecha Inicio": fila[0], "Tipo Expediente": fila[1]})


df5 = pd.DataFrame(data5)

# Usamos la función pivot_table para crear la tabla dinámica
df_pivot = df5.pivot_table(
    index="Fecha Inicio",                   # Filas: fechas
    columns="Tipo Expediente",              # Columnas: tipos de expediente
    aggfunc="size",                         # Función de agregación: contar las filas
    fill_value=0,                           # Rellenar con 0 donde no haya datos
)


# Graficar la tabla dinámica

# Crear gráfico apilado
fig5 = px.bar(df_pivot, 
             x=df_pivot.index,  # Eje X: las fechas
             y=df_pivot.columns,  # Eje Y: los tipos de expediente
             title="Solicitudes por Día",
             labels={'Fecha Inicio': 'Fecha', 'value': 'Cantidad'},
             height=600,
             barmode='stack')  # 'stack' para apilar las barras
fig5.update_xaxes(tickangle=45)   

col13, col14, col15 = st.columns(3)

# Mostrar los gráficos en las columnas
with col13:
    st.write("Listado Expedientes Solicitados por dia")
    st.dataframe(df_pivot)

with col14:
    st.plotly_chart(fig5)


consulta6 = """select [Tipo Expedientes], DATEDIFF(DAY, [Fecha inicio], MIN([Fecha ingreso])) as 'Dias' from pases as p inner join expedientes as e on p.[Nro. Expedientes] = e.[Nro. Expedientes] where Sector='Div. Despacho' and 
([Tipo Expedientes] = 'Jubilación Ordinaria' or  [Tipo Expedientes] = 'Retiro Policial Voluntario' or [Tipo Expedientes] = 'Jubilación por Invalidez' or  [Tipo Expedientes] = 'Retiro Policial por Incapacidad' or [Tipo Expedientes] = 'Retiro Policial Obligatorio' or [Tipo Expedientes] = 'Reconocimiento de Servicios') and ([Fecha inicio] between '01-09-2024' AND '30-11-2024') group by [Tipo Expedientes], [Fecha inicio]"""
cursor.execute(consulta6)
resultados6 = cursor.fetchall()

data6 = []

if resultados6:
    for fila in resultados6:
        # Agregar el registro a la lista 'data'
        data6.append({"Tipo Expedientes": fila[0], "Promedio en Dias": fila[1]})


df6 = pd.DataFrame(data6).groupby(by='Tipo Expedientes').mean()

col16, col17, col18 = st.columns(3)

# Mostrar los gráficos en las columnas
with col16:
    st.write("Promedio de Resolucion de expedientes previsionales")
    st.dataframe(df6)

   

