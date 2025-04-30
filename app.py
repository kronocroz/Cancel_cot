from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Endpoint raíz para verificar que la API está activa
@app.route('/')
def home():
    return "✅ API de cancelaciones está activa."

# Endpoint para consultar todas las cancelaciones
@app.route('/cancelaciones', methods=['GET'])
def obtener_cancelaciones():
    try:
        conn = sqlite3.connect("cancel.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cancelaciones LIMIT 100")
        filas = cursor.fetchall()
        conn.close()

        # Convertir resultado a lista de diccionarios
        resultados = [dict(fila) for fila in filas]

        return jsonify(resultados)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ejecutar localmente
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
