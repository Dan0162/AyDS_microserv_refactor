from faker import Faker  # Faker para generar datos ficticios
from flask import Flask, jsonify, request  # Flask para crear la aplicación web
import logging  # Para manejar los logs
import random  # Para generar números aleatorios

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

# Inicializamos una lista vacía para almacenar los datos
data = []

# Creamos una instancia de Faker para generar datos ficticios
fake = Faker()

# Definimos una ruta para obtener todos los pedidos
@app.route('/allOrders', methods=['GET'])
def all_orders():
    # Devolvemos todos los pedidos en formato JSON con un código HTTP 200
    return jsonify(data), 200

# Definimos una ruta para obtener un pedido específico por su número
@app.route('/order/<int:num>', methods=['GET'])
def get_order(num):
    # Devolvemos el pedido correspondiente en formato JSON con un código HTTP 200
    return jsonify(data[num]), 200

# Definimos una ruta para buscar pedidos por nombre de cliente
@app.route('/custSearch', methods=['POST'])
def cust_search():
    # Obtenemos el JSON enviado en la solicitud
    json = request.get_json()
    # Extraemos el nombre del cliente del JSON
    name = json.get('name', '')
    # Filtramos los pedidos que coincidan con el nombre del cliente
    result = [order for order in data if name in order['cust']]
    # Devolvemos los resultados de la búsqueda en formato JSON con un código HTTP 200
    return jsonify(result), 200

# Función para crear un pedido ficticio
def create_order(num):
    # Generamos un pedido con un ID, un nombre de cliente ficticio y una lista de ítems aleatorios
    return {
        'id': num,
        'cust': fake.name(),
        'items': [random.randint(1, 100) for _ in range(1, random.randint(1, 10))]
    }

# Función para crear una lista de pedidos ficticios
def create_data():
    # Generamos una lista de 999 pedidos ficticios
    return [create_order(num) for num in range(1, 1000)]

# Punto de entrada principal de la aplicación
if __name__ == '__main__':
    # Generamos los datos ficticios al iniciar la aplicación
    data = create_data()
    # Configuramos el nivel de los logs a INFO
    app.logger.setLevel(logging.INFO)
    # Ejecutamos la aplicación Flask en modo debug y escuchando en todas las interfaces de red
    app.run(debug=True, host='0.0.0.0')
