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
