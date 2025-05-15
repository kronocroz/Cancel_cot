from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
import requests

DB_URL = 'https://cancel-cot.onrender.com'


def query_db(query, params={}):
    try:
        response = requests.get(DB_URL + query, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"HTTP Request Error: {e}")
        return []
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute(query, args)
        rv = cur.fetchall()
    except sqlite3.Error as e:
        print(f"SQL Error: {e}")
        rv = []
    finally:
        con.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/cancelaciones/contar', methods=['GET'])
def contar_cancelaciones_por_causal():
    causal = request.args.get('causal')
    if not causal or not causal.strip():
        return jsonify({'error': 'El parámetro causal no puede estar vacío'}), 400

    # Consulta para contar y listar clientes por causal
    query = '''
        SELECT COUNT(*) as total, razon_social
        FROM cancelaciones
        WHERE LOWER(causal) LIKE ?
        GROUP BY razon_social
    '''
    search_param = f"%{causal.lower()}%"

    try:
        results = query_db('/cancelaciones', params={'causal': search_param})
    except sqlite3.Error as e:
        return jsonify({'error': f'Error al acceder a la base de datos: {str(e)}'}), 500

    if not results:
        return jsonify({'message': 'No se encontraron registros para el causal especificado.'}), 404

    # Estructura del JSON de respuesta
    clientes = [
        {'razon_social': row[1], 'total_cancelaciones': row[0]} for row in results
    ]

    total_causales = sum(row[0] for row in results)

    return jsonify({'total_causales': total_causales, 'clientes': clientes})

@app.route('/status', methods=['GET'])
def check_status():
    return jsonify({'message': 'API de cancelaciones activa'}), 200

# Ejecutar localmente
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
