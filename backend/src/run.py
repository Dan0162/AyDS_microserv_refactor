# Importamos las librerías necesarias
from flask import Flask, json, jsonify, request  # Flask para crear la aplicación web
import logging  # Para manejar los logs
import requests  # Para realizar solicitudes HTTP

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

# Definimos una ruta para obtener todos los pedidos
@app.route('/orders', methods=['GET'])
def orders():
    # Obtenemos el parámetro opcional 'count' de la solicitud
    count = request.args.get('count')
    # Realizamos una solicitud al servicio de pedidos para obtener todos los pedidos
    data = requests.get('http://demo_orders:5000/allOrders').json()
    if count:
        # Si se especifica 'count', devolvemos solo esa cantidad de pedidos
        return jsonify(data[:int(count)]), 200
    else:
        # Si no se especifica 'count', devolvemos todos los pedidos
        return jsonify(data), 200

# Definimos una ruta para obtener los detalles de un pedido específico
@app.route('/detail/<int:order_id>', methods=['GET'])
def detail(order_id):
    # Realizamos una solicitud al servicio de agregación para obtener los detalles del pedido
    data = requests.get('http://demo_aggregate:5000/detail/{}'.format(order_id)).json()
    # Devolvemos los detalles del pedido en formato JSON
    return jsonify(data), 200

# Definimos una ruta para buscar clientes por nombre
@app.route('/custSearch/<string:name>', methods=['GET'])
def cust_search(name):
    # Creamos un payload con el nombre del cliente
    payload = {'name': name}
    # Realizamos una solicitud al servicio de pedidos para buscar clientes
    data = requests.post('http://demo_orders:5000/custSearch', json=payload).json()
    # Devolvemos los resultados de la búsqueda en formato JSON
    return jsonify(data), 200

# Punto de entrada principal de la aplicación
if __name__ == '__main__':
    # Configuramos el nivel de los logs a INFO
    app.logger.setLevel(logging.INFO)
    # Ejecutamos la aplicación Flask en modo debug y escuchando en todas las interfaces de red
    app.run(debug=True, host='0.0.0.0')
