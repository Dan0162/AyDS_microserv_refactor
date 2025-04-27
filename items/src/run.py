# Importamos las librerías necesarias
from faker import Faker  # Faker para generar datos ficticios
from flask import Flask, jsonify  # Flask para crear la aplicación web
import logging  # Para manejar los logs

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

# Inicializamos una lista vacía para almacenar los datos
data = []

# Creamos una instancia de Faker para generar datos ficticios
fake = Faker()

# Definimos una ruta para obtener todos los ítems
@app.route('/allItems', methods=['GET'])
def all_orders():
    # Devolvemos todos los ítems en formato JSON con un código HTTP 200
    return jsonify(data), 200

# Definimos una ruta para obtener un ítem específico por su número
@app.route('/item/<int:num>', methods=['GET'])
def get_order(num):
    # Devolvemos el ítem correspondiente en formato JSON con un código HTTP 200
    return jsonify(data[num]), 200

# Función para crear un ítem ficticio
def create_items(num):
    # Generamos un ítem con un ID y una descripción ficticia
    return {
        'id': num,
        'desc': fake.bs()
    }

# Función para crear una lista de ítems ficticios
def create_data():
    # Generamos una lista de 99 ítems ficticios
    return [create_items(num) for num in range(1, 100)]

# Punto de entrada principal de la aplicación
if __name__ == '__main__':
    # Generamos los datos ficticios al iniciar la aplicación
    data = create_data()
    # Configuramos el nivel de los logs a INFO
    app.logger.setLevel(logging.INFO)
    # Ejecutamos la aplicación Flask en modo debug y escuchando en todas las interfaces de red
    app.run(debug=True, host='0.0.0.0')
