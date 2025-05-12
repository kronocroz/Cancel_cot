from flask import Flask, request, jsonify, send_file
import sqlite3
import pandas as pd
import os

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

@app.route("/analisis_causal", methods=["GET"])
def analisis_causal():
    try:
        conn = sqlite3.connect("cancel.db")
        cursor = conn.cursor()

        query = """
            SELECT causal, COUNT(*) AS total_cancelaciones, SUM(valor) AS valor_total
            FROM cancelaciones
            GROUP BY causal
            ORDER BY valor_total DESC
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        conn.close()

        # Formato de respuesta
        response = [
            {
                "causal": row[0],
                "total_cancelaciones": row[1],
                "valor_total": row[2]
            }
            for row in resultados
        ]

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ejecutar localmente
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
