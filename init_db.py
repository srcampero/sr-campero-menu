import sqlite3

# Conectamos a tu base de datos real
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Borra la tabla vieja para meter la nueva información limpia
cursor.execute('DROP TABLE IF EXISTS productos')
cursor.execute('''
    CREATE TABLE productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL,
        imagen_url TEXT,
        likes INTEGER DEFAULT 0
    )
''')

# NOMBRES LIMPIOS: Tu archivo index.html ya se encarga de poner el /static/images/
productos = [
    (
        "Pollo Estilo Broaster (1 Entero)", 
        "10 piezas de delicioso pollo crujiente hecho al momento, Incluye: salsa, papas fritas, ensalada de col y tortillas calientes, ¡Listo para llevar a casa!", 
        270.00, 
        "pollo_entero.jpg"
    ),
    (
        "Pollo Estilo Broaster (1/2 Pollo)", 
        "5 piezas de delicioso pollo crujiente hecho al momento, Incluye: salsa, papas fritas, ensalada de col y tortillas calientes, ¡Listo para llevar a casa!", 
        150.00, 
        "medio_pollo.jpg"
    ),
    (
        "Crunchy Burguer", 
        "Hamburguesa con filete de pechuga de pollo empanizado súper cuziente, vegetales frescos y aderezo especial en pan suave.", 
        80.00, 
        "crunchy_burguer.jpg"
    ),
    (
        "Paquete Crunchy Burguer", 
        "Nuestra Crunchy Burguer acompañada de una buena porción de papas fritas doradas y refresco de 355 ml.", 
        110.00, 
        "paquete_crunchy.jpg"
    )
]

# Esto mete la lista a la base de datos
cursor.executemany('INSERT INTO productos (nombre, descripcion, precio, imagen_url) VALUES (?, ?, ?, ?)', productos)
conn.commit()
conn.close()
print("¡Base de datos limpia y corregida localmente!")