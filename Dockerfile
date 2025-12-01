# Imagen base oficial de Python
FROM python:3.10-slim

# Variables de entorno para evitar archivos .pyc y buffer de salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias
COPY requirements.txt /app/

# Instala las dependencias del proyecto
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo el código del proyecto al contenedor
COPY . /app/

# Expone el puerto 8000 (Django por defecto)
EXPOSE 8000

# Ejecuta las migraciones y arranca el servidor Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]