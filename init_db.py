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
    
    # Tus productos iniciales exactos
    productos = [
        ("Pollo Estilo Broaster (1 Entero)", "10 piezas de delicioso pollo crujiente. Incluye: salsa, papas fritas, ensalada de col y tortillas calientes. ¡Listo para llevar a casa!", 290.00, "pollo_entero.jpg"),
        ("Pollo Estilo Broaster (1/2 Pollo)", "5 piezas de pollo crujiente hechas al momento. Incluye: salsa, papas fritas, ensalada de col y tortillas.", 170.00, "medio_pollo.jpg"),
        ("Crunchy Burguer", "Hamburguesa con filete de pechuga de pollo empanizado súper crujiente, vegetales frescos y aderezo especial en pan brioche suave.", 95.00, "crunchy_burguer.jpg"),
        ("Paquete Crunchy Burguer", "Nuestra Crunchy Burguer acompañada de una buena porción de papas fritas doradas y refresco de lata de 355 ml.", 140.00, "paquete_crunchy.jpg")
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