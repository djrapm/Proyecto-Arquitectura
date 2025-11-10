# Dragon Ball Memory Game

¡Bienvenido al **Dragon Ball Memory Game**! 🐉  

Un juego de memoria temático de Dragon Ball, desarrollado con **Django** y **JavaScript**. Incluye login , registro, selección de nivel, tablero de juego interactivo, estadísticas y efectos de sonido.

---

## 🎯 Requisitos

- Python 3.11+
- Django 5.x
- Docker (opcional, pero recomendado)
- Navegador moderno (Chrome, Firefox, Edge)

---

## 📦 Instalación

### Opción 1: Localmente sin Docker

1. Clonar el repositorio:

    git clone https://github.com/djrapm/Proyecto-Arquitectura.git
    cd Proyecto_Arquitectura/backend

2. crear un entorno virtual (recomendable) 

    python -m venv .venv
    .venv\Scripts\activate

3. instalar dependencias 

    pip install -r requirements.txt

4. aplicar migraciones

    python manage.py migrate

5. ejecutar 

    python manage.py runserver

6. abrir navegador

    http://localhost:8000/login/

## Opcion 2: con docker 

1. Clonar el repositorio:

    git clone https://github.com/djrapm/Proyecto-Arquitectura.git
    cd Proyecto_Arquitectura/backend

2. construir imagen 

    docker build -t dragonball-memory .

3. levantar contenedor 

    docker-compose up -d

4. Aplicar migraciones

docker-compose exec web python manage.py migrate

5. Acceder al navegador
   
    http://localhost:8000/login/
