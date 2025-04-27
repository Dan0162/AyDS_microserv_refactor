# Usamos una imagen base de Python 3.9 basada en Alpine Linux
FROM python:3.9-alpine

# Configuramos variables de entorno para evitar que Python genere archivos .pyc y para deshabilitar el buffer de salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalamos Python y pip
RUN apk update && apk add --no-cache python3 py3-pip

# Copiamos el archivo de dependencias (requirements.pip) al contenedor e instalamos las dependencias
COPY requirements.pip /app/requirements.pip
RUN pip3 install --no-cache-dir -r /app/requirements.pip

# Copiamos el código fuente de la aplicación al contenedor
COPY src /app/src

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app/src

# Exponemos el puerto 5000 para que la aplicación sea accesible
EXPOSE 5000

# Comando por defecto para ejecutar la aplicación
CMD ["python3", "run.py"]
