# Importamos las librerías necesarias
from flask import Flask, jsonify, request  # Flask para crear la aplicación web
import logging  # Para manejar los logs
import requests  # Para realizar solicitudes HTTP

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

# Definimos una ruta para obtener los detalles de un pedido
@app.route('/detail/<int:order_id>', methods=['GET'])
def detail(order_id):
    # Realizamos una solicitud al servicio de pedidos para obtener los datos del pedido
    order = requests.get('http://demo_orders:5000/order/{}'.format(order_id)).json()
    
    # Obtenemos los detalles de los ítems asociados al pedido
    items = [_fetch_item(item_id) for item_id in order.get('items', [])]
    
    # Eliminamos la clave 'items' del pedido original y la reemplazamos con los detalles completos
    del order['items']
    order['items'] = items
    
    # Devolvemos el pedido con los detalles de los ítems en formato JSON y un código HTTP 200
    return jsonify(order), 200

# Función auxiliar para obtener los detalles de un ítem
def _fetch_item(item_id):
    # Realizamos una solicitud al servicio de ítems para obtener los datos del ítem
    return requests.get('http://demo_items:5000/item/{}'.format(item_id)).json()

# Punto de entrada principal de la aplicación
if __name__ == '__main__':
    # Configuramos el nivel de los logs a INFO
    app.logger.setLevel(logging.INFO)
    
    # Ejecutamos la aplicación Flask en modo debug y escuchando en todas las interfaces de red
    app.run(debug=True, host='0.0.0.0')
