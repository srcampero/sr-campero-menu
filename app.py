from flask import Flask, render_template, jsonify, redirect
import psycopg2
from psycopg2.extras import RealDictCursor
import urllib.parse

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
    cur.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    try:
        # Forzamos la consulta con las columnas limpias y ordenadas por ID
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, descripcion, precio, imagen, likes FROM productos ORDER BY id ASC;")
        productos = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', productos=productos)
    except Exception as e:
        print("Error al cargar el menú:", e)
        return "Error al cargar el menú", 500

@app.route('/like/<int:producto_id>', methods=['POST'])
def like_producto(producto_id):
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        # Sumamos el like al producto
        cur.execute("UPDATE productos SET likes = likes + 1 WHERE id = %s;", (producto_id,))
        conn.commit()
        
        # Obtenemos el nuevo total de likes para responderle a la página
        cur.execute("SELECT likes FROM productos WHERE id = %s;", (producto_id,))
        producto = cur.fetchone()
        cur.close()
        conn.close()
        
        if producto:
            return jsonify(success=True, likes=producto['likes'])
        return jsonify(success=False), 404
    except Exception as e:
        print("Error en el like:", e)
        return jsonify(success=False), 500

if __name__ == '__main__':
    app.run(debug=True)
