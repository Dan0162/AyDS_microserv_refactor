This is a refactor of a

# Flask Microservice Demo

This project is an example of using nothing but python3, flask, requests, and docker to make a complete microservice architecture implementation.  Yes, it passes JSON around in between the microservices, which is arguably not a great idea, but it's hard to argue with how easy these are to spin up.

## Architecture Diagram

Here's the architecture diagram:

_Edit: I added another GET to the backend to test the custSearch functionality and demo a JSON payload in client. Details below._

![Architecture Diagram](https://i.imgur.com/IUAfN8O.png)

For testing fun all of the microservices are exposed, but in a real application only the backend (or API) would be.

## Description of the containers

There are four different docker images that are build for this demo. Backend is the API layer and it has three GET methods as illustrated in the diagram. For order details you can specify an integer from 1 to 1000. If you specify the count parameter it will show the first # of orders up to the count you specify.

The aggregate which is exposed locally on port 5003 combines information from the orders data service and the items data service. It has a single method which will actually return exactly the same thing as the backend /detail/ method, but of course you haven't exposed the aggregate microservice in the real world, and you'd do other value-add things in the API layer like authentication.

The orders microservice is a data service, and typically you'd be going after a database of some kind. Here a faker is used to create 1000 orders and they're kept in memory for the life of the run. The /custSearch method (which isn't used by the backend currently, but demonstrates how to take a JSON payload, much like you would pass to a microservice via a gRPC request or your preferred equivalent) can be queried through postman or some other REST testing interface. You'd set the "content-type" to "application/json" and provide a JSON payload like:

```json
{
  "name": "Daniel"
}
```

Lastly the items microservice provides information about 100 randomly created items. This one is never used directly by the backend, but indirectly through the aggregate. Again, this would be a database of some sort in the real world.

## Running it

You need docker and docker-compose. Follow your OS instructions for doing that.  The docker images start with Alpine and install Python3. The only dependencies in Python are Flask, Faker, and requests.

## Testing it

With the docker-compose running and postman, try the following URLS:

### A bunch of raw orders:

http://localhost:5000/orders?count=10

```json
[
    {
        "cust": "Mr. James Edwards",
        "id": 1,
        "items": [
            88,
            2,
            38,
            59,
            52,
            95,
            32,
            68,
            17
        ]
    },
    {
        "cust": "Sarah Taylor",
        "id": 2,
        ...and so on...
    }
    ...and so on...
]
```

### An order detail

http://localhost:5000/detail/5

Notice how the "items" element has been replaced with a list of item details.

```json
{
    "cust": "John Martinez",
    "id": 6,
    "items": [
        {
            "desc": "synthesize plug-and-play interfaces",
            "id": 72
        },
        {
            "desc": "target open-source action-items",
            "id": 18
        },
        {
            "desc": "grow dynamic web services",
            "id": 86
        },
        {
            "desc": "synthesize plug-and-play interfaces",
            "id": 72
        },
        {
            "desc": "streamline synergistic e-commerce",
            "id": 37
        }
    ]
}
```

### Customer name search

http://localhost:5000/custSearch/Dan

You can now hit this URL directly with a GET to perform a search by partial customer name. A space is just '%20'. This calls the underlying custSearch endpoint for the orders microservice, but takes the name and forms a JSON payload which is possibly a more familiar way to send data to a microservice for it to operate on rather than doing it through parameters.  Again Flask makes this absurdly simple.


### Test the search in the data microservice

POST http://localhost:5001/custSearch

*Note the port of the orders microservice here! This isn't the backend!*

Make sure to use a POST and to set "Content-Type: application/json" in the "headers" and to put something like `{"name": "Daniel"}` in the "body".  You'll get a list of order where the "cust" field contains the search parameter. The customer names are randomly generated, so you might want to try something simple.

## Refactorización

Esta sección describe las modificaciones realizadas o propuestas para habilitar el acceso seguro (HTTPS) a los microservicios, utilizando un proxy inverso.

Anteriormente, los servicios se comunicaban y eran accesibles a través de HTTP. Para añadir una capa de seguridad y permitir el tráfico cifrado, se ha implementado el uso de un proxy inverso (ej. Nginx) para manejar las conexiones HTTPS externas.

Los principales cambios incluyen:

1.  **Configuración de Proxy Inverso (Nginx):** Se propone añadir un servicio de proxy inverso (como Nginx) para que actúe como punto de entrada para las conexiones externas. Este proxy escuchará en el puerto estándar HTTPS (443) y reenviará las solicitudes a los servicios Flask apropiados dentro de la red Docker a través de HTTP.
    * Se requiere un archivo de configuración para Nginx (`nginx.conf`) que defina cómo manejar las conexiones SSL y cómo dirigir el tráfico a los servicios backend.

2.  **Certificados SSL:** Para habilitar HTTPS, se necesitan certificados SSL (un certificado y una clave privada).
    * Para desarrollo, se pueden generar certificados autofirmados utilizando herramientas como OpenSSL con un comando similar a:
        ```bash
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout private.key -out certificate.crt
        ```
        Se recomienda usar `localhost` como el Common Name (CN) del certificado para pruebas locales.
    * Para entornos de producción, se deben obtener certificados de una Autoridad Certificadora (CA) de confianza.

3.  **Actualización de `docker-compose.yml`:** Se ha modificado el archivo `docker-compose.yml` para incluir el nuevo servicio del proxy inverso.
    * Se mapean los puertos 80 (opcional, para redirigir HTTP a HTTPS) y 443 del host al contenedor del proxy.
    * Se montan los archivos de configuración de Nginx y el directorio que contiene los certificados SSL en el contenedor del proxy.
    * Se establece una dependencia para asegurar que el servicio backend esté corriendo antes de que se inicie el proxy.

4.  **Estructura de Archivos:** Se añade una carpeta `certs` (al mismo nivel que `docker-compose.yml`) para almacenar los archivos `certificate.crt` y `private.key`. El archivo `nginx.conf` también se coloca en la raíz del proyecto.

### Acceso a Endpoints mediante GET

Una vez que los servicios están en funcionamiento (y el proxy inverso está configurado si se usa HTTPS), se puede acceder a la información utilizando solicitudes HTTP GET estándar a los siguientes endpoints. Se proporcionan ejemplos asumiendo el acceso a través de HTTPS en `https://localhost` (si se utiliza el proxy inverso):

* **Buscar clientes por nombre (ej. "Dan"):**
    `https://localhost/custSearch/Dan`

* **Obtener una lista de pedidos (ej. 5 pedidos):**
    `https://localhost/orders?count=5`
    (Nota: El parámetro para especificar el número de pedidos es `count`.)

* **Obtener detalles para un pedido específico (ej. ID de Pedido 4):**
    `https://localhost/detail/4`

* **Obtener detalles para otro pedido específico (ej. ID de Pedido 5):**
    `https://localhost/detail/5`