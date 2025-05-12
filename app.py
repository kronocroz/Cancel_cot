from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = 'cancel.db'

def query_db(query, args=(), one=False):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    con.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/cancelaciones/causal', methods=['GET'])
def get_cancelaciones_by_causal():
    causal = request.args.get('causal')
    if not causal or not causal.strip():
        return jsonify({'error': 'El parámetro causal no puede estar vacío'}), 400

    # Consulta para obtener todos los registros del causal sin duplicados
    query = '''
        SELECT DISTINCT causal, bodega, fecha_cancel, doc, razon_social, ref, descripcion, cant, valor
        FROM cancelaciones
        WHERE causal LIKE ?
    '''
    search_param = f"%{causal}%"
    try:
        results = query_db(query, (search_param,))
    except sqlite3.Error as e:
        return jsonify({'error': f'Error al acceder a la base de datos: {str(e)}'}), 500

    if not results:
        return jsonify({'message': 'No se encontraron registros para el causal especificado.'}), 404

    # Estructura del JSON de respuesta
    cancelaciones = []
    for row in results:
        cancelacion = {
            'causal': row[0],
            'bodega': row[1],
            'fecha_cancel': row[2],
            'doc': row[3],
            'razon_social': row[4],
            'ref': row[5],
            'descripcion': row[6],
            'cantidad': row[7],
            'valor': row[8]
        }
        if cancelacion not in cancelaciones:
            cancelaciones.append(cancelacion)

    # Generar lista de causales únicos para sugerencias
    causales_unicos = list(set([c['causal'] for c in cancelaciones]))

    return jsonify({'causales_sugeridos': causales_unicos, 'cancelaciones': cancelaciones})

# Ejecutar localmente
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
