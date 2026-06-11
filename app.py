from flask import Flask, render_template, jsonify, redirect
import sqlite3
import urllib.parse

app = Flask(__name__)
DB_FILE = "database.db"

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# Ruta principal: Muestra el menú interactivo
@app.route('/')
def index():
    productos = query_db('SELECT * FROM productos')
    return render_template('index.html', productos=productos)

# Ruta para dar "Like" sin recargar la página (AJAX)
@app.route('/like/<int:producto_id>', methods=['POST'])
def dar_like(producto_id):
    query_db('UPDATE productos SET likes = likes + 1 WHERE id = ?', [producto_id])
    res = query_db('SELECT likes FROM productos WHERE id = ?', [producto_id], one=True)
    return jsonify({'success': True, 'likes': res['likes']})

# Ruta para el botón de pedir: Genera el texto para WhatsApp
@app.route('/pedir/<int:producto_id>')
def pedir(producto_id):
    p = query_db('SELECT * FROM productos WHERE id = ?', [producto_id], one=True)
    if p:
        mensaje = f"¡Hola, Sr. Campero! 🍗 Quisiera ordenar para llevar:\n\n• *{p['nombre']}* (${p['precio']:.2f})\n\nMe gustaría pasar a recogerlo en unos minutos. ¿Me confirman el tiempo de espera?"
        mensaje_enconded = urllib.parse.quote(mensaje)
        # Cambia el número si usas otro para recibir pedidos
        return redirect(f"https://wa.me/529616768289?text={mensaje_enconded}")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)