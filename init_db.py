import psycopg2

# Tu URL real de Render ya acomodada
url_database = "postgresql://alfredo:7JqAwDij6nCpyFzJKT0CRWPKwcdXAS26@dpg-d8nf26nlk1mc739m157g-a.oregon-postgres.render.com/srcampero"

# Conectamos a la base de datos real en internet
conn = psycopg2.connect(url_database)
cursor = conn.cursor()

# Borra la tabla vieja en internet para meter la nueva información limpia
cursor.execute('DROP TABLE IF EXISTS productos')
cursor.execute('''
    CREATE TABLE productos (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        descripcion TEXT,
        precio NUMERIC(10, 2) NOT NULL,
        imagen_url VARCHAR(255),
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
        "Hamburguesa con filete de pechuga de pollo empanizado súper crujiente, vegetales frescos y aderezo especial en pan suave.", 
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

# Esto mete la lista a la base de datos de internet
cursor.executemany('INSERT INTO productos (nombre, descripcion, precio, imagen_url) VALUES (%s, %s, %s, %s)', productos)
conn.commit()
conn.close()
print("¡Base de datos de internet PostgreSQL cargada con éxito!")