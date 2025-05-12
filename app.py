from flask import Flask, request, jsonify, send_file
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
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

app = Flask(__name__)

# Ruta para almacenar las gráficas generadas
GRAPH_PATH = "static/graphs/"
os.makedirs(GRAPH_PATH, exist_ok=True)

@app.route("/")
def home():
    return "✅ API de análisis de cancelaciones está activa."

@app.route("/analisis_causal", methods=["GET"])
def analisis_causal():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("cancel.db")
        query = """
            SELECT causal, COUNT(*) AS total_cancelaciones, SUM(valor) AS valor_total
            FROM cancelaciones
            GROUP BY causal
            ORDER BY valor_total DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()

        # Si no hay datos
        if df.empty:
            return jsonify({"mensaje": "No se encontraron datos de cancelaciones"}), 404

        # Crear el JSON de respuesta
        response_data = df.to_dict(orient="records")

        # Crear la gráfica
        plt.figure(figsize=(10, 6))
        plt.barh(df["causal"], df["valor_total"], color="skyblue", edgecolor="black")
        plt.xlabel("Valor Total Cancelado")
        plt.ylabel("Causal de Cancelación")
        plt.title("Distribución de Cancelaciones por Causal")
        plt.grid(axis="x", linestyle="--", alpha=0.7)
        plt.tight_layout()

        # Guardar la gráfica
        graph_file = os.path.join(GRAPH_PATH, "analisis_causal.png")
        plt.savefig(graph_file)
        plt.close()

        # Respuesta final con datos y URL de la gráfica
        response = {
            "data": response_data,
            "graph_url": request.url_root + graph_file
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/static/graphs/<filename>")
def get_graph(filename):
    """ Endpoint para servir las gráficas generadas """
    try:
        return send_file(os.path.join(GRAPH_PATH, filename), mimetype='image/png')
    except FileNotFoundError:
        return jsonify({"error": "Gráfico no encontrado"}), 404

# Ejecutar localmente
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
