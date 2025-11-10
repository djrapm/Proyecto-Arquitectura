# Dragon Ball Memory Game

¡Bienvenido al **Dragon Ball Memory Game**! 🐉  

Un juego de memoria temático de Dragon Ball, desarrollado con **Django** y **JavaScript**. Incluye login/registro, selección de nivel, tablero de juego interactivo, estadísticas y efectos de sonido.

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

    git clone URL_DEL_REPOSITORIO
    cd cd Proyecto_Arquitectura/backend

2. crear un entorno virtual 

    python -m venv .venv
    # Windows
    .venv\Scripts\activate

3. instalar dependencias 

    pip install -r requirements.txt

4. aplicar migraciones

    python manage.py migrate

5. ejecutar 

    python manage.py runserver

6. abrir 

    http://localhost:8000/login/

## con docker 

0. Clonar el repositorio:

    git clone URL_DEL_REPOSITORIO
    cd Proyecto_Arquitectura/backend


1. construir imagen 

    docker build -t dragonball-memory .

levantar contenedor 

    docker-compose up -d

migraciones

docker-compose exec web python manage.py migrate

3. Acceder 
    http://localhost:8000/login/

