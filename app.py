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

@app.route("/cancelaciones/test", methods=["GET"])
def obtener_cancelaciones_test():
    """ Obtener los primeros 5 registros de cancelaciones """
    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
            SELECT 
                bodega, 
                fecha_can AS fecha_cancel, 
                causal, 
                doc, 
                razon_social, 
                dpto, 
                ref, 
                descripcion, 
                cant, 
                valor 
            FROM cancelaciones 
            LIMIT 5
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        # Si no hay resultados
        if not rows:
            return jsonify({"mensaje": "No se encontraron cancelaciones"}), 404

        # Convertir a lista de diccionarios
        resultado = [dict(row) for row in rows]
        return jsonify(resultado)

    except Exception as e:
        # Captura y muestra el error completo
        error_message = f"Error en /cancelaciones/test: {str(e)}"
        print(error_message)
        return jsonify({"error": error_message}), 500        
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
