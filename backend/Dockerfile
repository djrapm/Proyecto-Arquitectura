# Usamos la imagen oficial de Python slim
FROM python:3.11-slim

# Evitamos bytecode y habilitamos salida en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalamos dependencias básicas
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Creamos directorio de la app
WORKDIR /app

# Copiamos requirements
COPY requirements.txt .

# Instalamos dependencias Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Montaje del código host al contenedor 
VOLUME /app

# Comando para desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

