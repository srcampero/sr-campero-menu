import psycopg2 

url_database = "postgresql://alfredo:7JqAwDij6nCpyFzJKT0CRWPKwcdXAS26@dpg-d8nf26nlk1mc739m157g-a.oregon-postgres.render.com/srcampero" 

def init_db():
    conn = psycopg2.connect(url_database)
    cur = conn.cursor()

    # 1. Borramos la tabla vieja para meter el menú nuevo limpio y sin repeticiones
    cur.execute('DROP TABLE IF EXISTS productos;')

    # 2. Creamos la tabla con la estructura correcta
    cur.execute('''
        CREATE TABLE productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            descripcion TEXT NOT NULL,
            precio NUMERIC(10,2) NOT NULL,
            imagen VARCHAR(100) NOT NULL,
            likes INTEGER DEFAULT 0
        );
    ''')

    # 3. Lista oficial y completa de Sr. Campero (Clásicos, Nuevos y Fin de Semana)
    productos = [
        # --- SECCIÓN: CLÁSICOS DE POLLO Y HAMBURGUESAS ---
        ("Pollo Entero Broaster", "Delicioso pollo entero preparado al estilo Broaster, crujiente por fuera y jugoso por dentro. Incluye complementos.", 240.00, "pollo_entero.jpg"),
        ("Medio Pollo Broaster", "Medio pollo preparado al estilo Broaster, súper crujiente y lleno de sabor. Incluye complementos.", 130.00, "medio_pollo.jpg"),
        ("Crunchy Burguer", "Hamburguesa con filete de pechuga de pollo empanizado súper crujiente, vegetales frescos y aderezo especial en pan suave.", 80.00, "crunchy_burguer.jpg"),
        ("Paquete Crunchy Burguer", "Hamburguesa Crunchy Burguer acompañada de una orden de papas fritas doraditas y bebida fría.", 115.00, "paquete_hamburguesa.jpg"),
        
        # --- SECCIÓN: COMPLEMENTOS NUEVOS ---
        ("Papas fritas", "1 orden de deliciosas papas fritas, doraditas con especias.", 40.00, "papas_fritas.jpg"),
        ("Tenders de pollo", "1 orden de 5 pzas. de tiras de pollo crujientes y llenos de sabor con su rico dip de la casa.", 80.00, "tenders_pollo.jpg"),
        ("Nuggets de pollo", "1 orden de Nuggets jugosos y llenos de sabor.", 40.00, "nuggets_pollo.jpg"),

        # --- SECCIÓN: BIRRIA PARA EL FIN DE SEMANA ---
        ("1 Litro de consomé de birria", "Delicioso consomé incluye: Cebolla/cilantro, tortilla y limón.", 80.00, "litro_consome.jpg"),
        ("½ Litro de consomé de birria", "Delicioso consomé incluye: Cebolla/cilantro, tortilla y limón.", 45.00, "medio_litro_consome.jpg"),
        ("1 Litro de consomé con carne", "180 grs. de carne, salsa, cebolla/cilantro y tortilla y limón.", 160.00, "litro_con_carne.jpg"),
        ("½ Litro de consomé con carne", "90 grs. de carne, salsa, cebolla/cilantro y tortilla y limón.", 85.00, "medio_litro_con_carne.jpg"),
        ("1 Kg. de carne de birria", "1 kg de deliciosa, suave y jugosa carne de birria, incluye: salsa, cebolla/cilantro, tortilla y limón.", 460.00, "un_kg_birria.jpg"),
        ("¾ Kg. de carne de birria", "¾ kg de deliciosa, suave y jugosa carne de birria, incluye: salsa, cebolla/cilantro, tortilla y limón.", 360.00, "tres_cuartos_birria.jpg"),
        ("½ Kg. de carne de birria", "½ kg de deliciosa, suave y jugosa carne de birria, incluye: salsa, cebolla/cilantro, tortilla y limón.", 240.00, "medio_kg_birria.jpg"),
        ("¼ Kg. de carne de birria", "¼ kg de deliciosa, suave y jugosa carne de birria, incluye: salsa, cebolla/cilantro, tortilla y limón.", 120.00, "cuarto_kg_birria.jpg")
    ]

    # 4. Insertar los productos en la base de datos
    for p in productos:
        cur.execute('''
            INSERT INTO productos (nombre, descripcion, precio, imagen, likes)
            VALUES (%s, %s, %s, %s, 0);
        ''', p)

    conn.commit()
    cur.close()
    conn.close()
    print("¡Base de datos de Sr. Campero actualizada con éxito al 100%!")

if __name__ == '__main__':
    init_db()
