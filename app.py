from flask import Flask, request, jsonify
import sqlite3
import os 

app = Flask(__name__)

# Conexión a la base de datos
DB_PATH = "cancel.db"

def connect_db():
    """ Conectar a la base de datos """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return "✅ API de Cancelaciones está activa."

@app.route("/cancelaciones", methods=["GET"])
def obtener_cancelaciones():
    """ Obtener todas las cancelaciones """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cancelaciones")
        cancelaciones = cursor.fetchall()
        conn.close()

        # Convertir a lista de diccionarios
        resultado = [dict(row) for row in cancelaciones]

        if not resultado:
            return jsonify({"mensaje": "No se encontraron cancelaciones"}), 404

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
