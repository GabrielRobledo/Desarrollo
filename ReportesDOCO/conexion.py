import pyodbc

def conexion():
    # Parámetros de conexión
    server = 'IPSDB-Replica' 
    database = 'DoCo'
    username = 'IPSCOR\36548944'
    password = ''

    # Crear una cadena de conexión utilizando ODBC Driver 18
    conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes; Encrypt=no'

    # Establecer la conexión
    try:
        conn = pyodbc.connect(conn_str)
        print("Conexión exitosa")
        return conn
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None    
   
def consulta(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)

    #CAPTURAMOS LOS RESULTADOS EN UNA VARIABLE PARA LUEGO MOSTRAR
    resultados = cursor.fetchall()
    cursor.close()
    #CERRAMOS LA CONEXION A LA BASE DE DATOS
    #conn.close()

    return resultados