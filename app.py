from flask import Flask, render_template, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DATABASE_URL = "postgresql://alfredo:7JqAwDij6nCpyFzJKT0CRWPKwcdXAS26@dpg-d8nf26nlk1mc739m157g-a.oregon-postgres.render.com/srcampero"

def actualizar_base_datos_fuerza_bruta():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # 1. Tumbamos la tabla vieja congelada
        cur.execute("DROP TABLE IF EXISTS productos;")
        
        # 2. La creamos idéntica y limpia
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
        
        # 3. Datos oficiales sin errores de acoplamiento
        menu_oficial = [
            ("Pollo Entero Broaster", "Delicioso pollo entero preparado al estilo Broaster, crujiente por fuera y jugoso por dentro. Incluye complementos.", 240.00, "pollo_entero.jpg"),
            ("Medio Pollo Broaster", "Medio pollo preparado al estilo Broaster, súper crujiente y lleno de sabor. Incluye complementos.", 130.00, "medio_pollo.jpg"),
            ("Crunchy Burguer", "Hamburguesa con filete de pechuga de pollo empanizado súper crujiente, vegetales frescos y aderezo especial en pan suave.", 80.00, "crunchy_burguer.jpg"),
            ("Paquete Crunchy Burguer", "Hamburguesa Crunchy Burguer acompañada de una orden de papas fritas doraditas y bebida fría.", 115.00, "paquete_crunchy.jpg"),
            ("Papas fritas", "1 orden de deliciosas papas fritas, doraditas con especias.", 40.00, "papas_fritas.jpg"),
            ("Tenders de pollo", "1 orden de 5 pzas. de tiras de pollo crujientes y llenos de sabor con su rico dip de la casa.", 80.00, "tenders_pollo.jpg"),
            ("Nuggets de pollo", "1 orden de Nuggets jugosos y llenos de sabor.", 40.00, "nuggets_pollo.jpg"),
            
            # SECCIÓN FIN DE SEMANA (Nombres exactos de tu captura)
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
        print("¡BASE DE DATOS RESETEADA EXITOSAMENTE!")
    except Exception as e:
        print("Error reseteando BD:", e)

# Ejecutamos el reseteo justo al arrancar la app
actualizar_base_datos_fuerza_bruta()

@app.route('/')
def index():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, descripcion, precio, imagen, likes FROM productos ORDER BY id ASC;")
        productos = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', productos=productos)
    except Exception as e:
        return f"Error al cargar el menú: {e}", 500

@app.route('/like/<int:producto_id>', methods=['POST'])
def like_producto(producto_id):
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        cur.execute("UPDATE productos SET likes = likes + 1 WHERE id = %s;", (producto_id,))
        conn.commit()
        cur.execute("SELECT likes FROM productos WHERE id = %s;", (producto_id,))
        producto = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify(success=True, likes=producto['likes'])
    except:
        return jsonify(success=False), 500

if __name__ == '__main__':
    app.run(debug=True)
