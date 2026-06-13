import sqlite3

def crear_base_datos():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Crear tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            imagen_url TEXT NOT NULL,
            likes INTEGER DEFAULT 0
        )
    ''')
    
# Limpiar datos previos para pruebas
    cursor.execute("DELETE FROM productos")
    
    # Tus productos iniciales exactos con la URL corregida a medio_pollo
    productos = [
        ("Pollo Estilo Broaster (1 Entero)", "10 piezas de delicioso pollo crujiente hecho al momento, Incluye: salsa, papas fritas, ensalada de col y tortillas calientes, ¡Listo para llevar a casa!", 270.00, "https://raw.githubusercontent.com/Alfe2801/srcamperobot/main/static/images/pollo_entero.jpg"),
        ("Pollo Estilo Broaster (1/2 Pollo)", "5 piezas de delicioso pollo crujiente hecho al momento, Incluye: salsa, papas fritas, ensalada de col y tortillas calientes, ¡Listo para llevar a casa!", 150.00, "https://raw.githubusercontent.com/Alfe2801/srcamperobot/main/static/images/medio_pollo.jpg"),
        ("Crunchy Burguer", "Hamburguesa con filete de pechuga de pollo empanizado súper crujiente, vegetales frescos y aderezo especial en pan suave.", 80.00, "https://raw.githubusercontent.com/Alfe2801/srcamperobot/main/static/images/crunchy_burguer.jpg"),
        ("Paquete Crunchy Burguer", "Nuestra Crunchy Burguer acompañada de una buena porción de papas fritas doradas y refresco de 355 ml.", 110.00, "https://raw.githubusercontent.com/Alfe2801/srcamperobot/main/static/images/paquete_crunchy.jpg")
    ]
    cursor.executemany('''
        INSERT INTO productos (nombre, descripcion, precio, imagen_url)
        VALUES (?, ?, ?, ?)
    ''', productos)
    
    conn.commit()
    conn.close()
    print("¡Base de datos de Sr. Campero creada y cargada con éxito!")

if __name__ == '__main__':
    crear_base_datos()