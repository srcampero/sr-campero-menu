from flask import Flask, render_template, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DATABASE_URL = "postgresql://alfredo:7JqAwDij6nCpyFzJKT0CRWPKwcdXAS26@dpg-d8nf26nlk1mc739m157g-a.oregon-postgres.render.com/srcampero"

@app.route('/')
def index():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        # Jalamos 'imagen_url' pero se la entregamos al HTML nombrada como 'imagen'
        cur.execute("SELECT id, nombre, descripcion, precio, imagen_url AS imagen, likes FROM productos ORDER BY id ASC;")
        productos = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', productos=productos)
    except Exception as e:
        print("Error al cargar el menú:", e)
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
