from flask import Flask, render_template, jsonify, redirect
import psycopg2
from psycopg2.extras import RealDictCursor
import urllib.parse


import psycopg2

def reconstruir_menu_completo():
    url_database = "postgresql://alfredo:7JqAwDij6nCpyFzJKT0CRWPKwcdXAS26@dpg-d8nf26nlk1mc739m157g-a.oregon-postgres.render.com/srcampero"
    try:
        conn = psycopg2.connect(url_database)
        cur = conn.cursor()
        
        cur.execute("DROP TABLE IF EXISTS productos;")
        
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
        
        menu_oficial = [
            # --- TUS CLÁSICOS DE SIEMPRE ---
            ("Pollo Entero Broaster", "Delicioso pollo entero preparado al estilo Broaster, crujiente por fuera y jugoso por dentro. Incluye complementos.", 270.00, "pollo_entero.jpg"),
            ("Medio Pollo Broaster", "Medio pollo preparado al estilo Broaster, súper crujiente y lleno de sabor. Incluye complementos.", 150.00, "medio_pollo.jpg"),
            ("Crunchy Burguer", "Hamburguesa con filete de pechuga de pollo empanizado súper crujiente, vegetales frescos y aderezo especial en pan suave.", 80.00, "crunchy_burguer.jpg"),
            ("Paquete Crunchy Burguer", "Hamburguesa Crunchy Burguer acompañada de una orden de papas fritas doraditas y bebida fría.", 110.00, "paquete_hamburguesa.jpg"),
            
            # --- COMPLEMENTOS ---
            ("Papas fritas", "1 orden de deliciosas papas fritas, doraditas con especias.", 40.00, "papas_fritas.jpg"),
            ("Tenders de pollo", "1 orden de 5 pzas. de tiras de pollo crujientes y llenos de sabor con su rico dip de la casa.", 80.00, "tenders_pollo.jpg"),
            ("Nuggets de pollo", "1 orden de Nuggets jugosos y llenos de sabor.", 40.00, "nuggets_pollo.jpg"),
            
            # --- SECCIÓN BIRRIA ---
            ("1 Litro de consomé de birria", "Delicioso consomé de la casa. Incluye: cebolla, cilantro, tortillas y limón.", 80.00, "litro_consome.jpg"),
            ("½ Litro de consomé de birria", "Delicioso consomé de la casa. Incluye: cebolla, cilantro, tortillas y limón.", 45.00, "medio_litro_consome.jpg"),
            ("1 Litro de consomé con carne", "180 grs. de carne de res suave y jugosa. Incluye: salsa, cebolla, cilantro, tortillas y limón.", 160.00, "litro_con_carne.jpg"),
            ("½ Litro de consomé con carne", "90 grs. de carne de res suave y jugosa. Incluye: salsa, cebolla, cilantro, tortillas y limón.", 85.00, "medio_litro_con_carne.jpg"),
            ("1 Kg. de carne de birria", "1 kg de deliciosa, suave y jugosa carne de birria. Incluye: salsa, cebolla, cilantro, tortillas y limón.", 460.00, "un_kg_birria.jpg"),
            ("¾ Kg. de carne de birria", "¾ kg de deliciosa, suave y jugosa carne de birria. Incluye: salsa, cebolla, cilantro, tortillas y limón.", 360.00, "tres_cuartos_birria.jpg"),
            ("½ Kg. de carne de birria", "½ kg de deliciosa, suave y jugosa carne de birria. Incluye: salsa, cebolla, cilantro, tortillas y limón.", 240.00, "medio_kg_birria.jpg"),
            ("¼ Kg. de carne de birria", "¼ kg de deliciosa, suave y jugosa carne de birria. Incluye: salsa, cebolla, cilantro, tortillas y limón.", 120.00, "cuarto_kg_birria.jpg")
        ]
        
        for p in menu_oficial:
            cur.execute("INSERT INTO productos (nombre, descripcion, precio, imagen, likes) VALUES (%s, %s, %s, %s, 0);", p)
            
        conn.commit()
        cur.close()
        conn.close()
        print("--- ¡BASE DE DATOS CONFIGURADA SÓLIDAMENTE! ---")
    except Exception as e:
        print("Error en reconstrucción:", e)

reconstruir_menu_completo()
app = Flask(__name__)

# Tu URL real de Render configurada fijamente
DATABASE_URL = "postgresql://alfredo:7JqAwDij6nCpyFzJKT0CRWPKwcdXAS26@dpg-d8nf26nlk1mc739m157g-a.oregon-postgres.render.com/srcampero"

def query_db(query, args=(), one=False):
    # Conexión a la base de datos de internet PostgreSQL
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    cur = conn.cursor()
    cur.execute(query, args)
    
    # Si la consulta cambia datos (como el UPDATE de los likes)
    if cur.description is None:
        conn.commit()
        conn.close()
        return None
        
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# Ruta principal: Muestra el menú interactivo
@app.route('/')
def index():
    productos = query_db('SELECT * FROM productos ORDER BY id ASC')
    return render_template('index.html', productos=productos)

# Ruta para dar "Me gusta" sin recargar la página (AJAX)
@app.route('/like/<int:producto_id>', methods=['POST'])
def dar_like(producto_id):
    # Cambiado el "?" de SQLite por "%s" que usa PostgreSQL
    query_db('UPDATE productos SET likes = likes + 1 WHERE id = %s', [producto_id])
    res = query_db('SELECT likes FROM productos WHERE id = %s', [producto_id], one=True)
    return jsonify({'exito': True, 'likes': res['likes']})

# Ruta para el botón de pedir: Genera el texto para WhatsApp
@app.route('/pedir/<int:producto_id>')
def pedir(producto_id):
    pag = query_db('SELECT * FROM productos WHERE id = %s', [producto_id], one=True)
    if pag:
        mensaje = f"¡Hola, Sr. Campero! 🍗 Quisiera ordenar para llevar:\n\n* *{pag['nombre']}* * (${pag['precio']:.2f})\n\nMe gustaría pasar a recogerlo."
        mensaje_encriptado = urllib.parse.quote(mensaje)
        return redirect(f"https://wa.me/529616768289?text={mensaje_encriptado}")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
