import sqlite3

def inicializar_base_de_datos():
    # Conectar a la base de datos (se creará el archivo si no existe)
    conexion = sqlite3.connect("srcampero.db")
    cursor = conexion.cursor()
    
    # Crear la tabla de productos si no existe (CORREGIDO AQUÍ)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL,
            imagen_url TEXT
        )
    """)
    
    # Limpiar datos previos para evitar duplicados en las pruebas
    cursor.execute("DELETE FROM productos")
    
    # Tus productos iniciales exactos con tus URLs reales de GitHub en formato RAW
    productos = [
        (
            "Pollo Estilo Broaster (1 Entero)", 
            "10 piezas de delicioso pollo crujiente hecho al momento, Incluye: salsa, papas fritas, ensalada de col y tortillas calientes, ¡Listo para llevar a casa!", 
            270.00, 
            "https://raw.githubusercontent.com/Alfe2801/srcamperobot/main/static/images/pollo_entero.jpg"
        ),
        (
            "Pollo Estilo Broaster (1/2 Pollo)", 
            "5 piezas de delicioso pollo crujiente hecho al momento, Incluye: salsa, papas fritas, ensalada de col y tortillas calientes, ¡Listo para llevar a casa!", 
            150.00, 
            "https://raw.githubusercontent.com/Alfe2801/srcamperobot/main/static/images/medio_pollo.jpg"
        ),
        (
            "Crunchy Burguer", 
            "Hamburguesa con filete de pechuga de pollo empanizado súper crujiente, vegetales frescos y aderezo especial en pan suave.", 
            80.00, 
            "https://raw.githubusercontent.com/Alfe2801/srcamperobot/main/static/images/crunchy_burguer.jpg"
        ),
        (
            "Paquete Crunchy Burguer", 
            "Nuestra Crunchy Burguer acompañada de una buena porción de papas fritas doradas y refresco de 355 ml.", 
            110.00, 
            "https://raw.githubusercontent.com/Alfe2801/srcamperobot/main/static/images/paquete_crunchy.jpg"
        )
    ]
    
    # Insertar los productos en la base de datos
    cursor.executemany(
        "INSERT INTO productos (nombre, descripcion, precio, imagen_url) VALUES (?, ?, ?, ?)", 
        productos
    )
    
    # GUARDAR CAMBIOS DEFINITIVOS
    conexion.commit()
    
    print("¡Base de datos del Sr. Campero actualizada con éxito con las nuevas imágenes 9:16!")
    
    # Cerrar la conexión
    conexion.close()

if __name__ == "__main__":
    inicializar_base_de_datos()