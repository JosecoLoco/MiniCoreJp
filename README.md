# Minicore - Tienda de Impresión 3D

Este proyecto es una tienda en línea especializada en productos impresos en 3D, con categorías por festividades y funcionalidades de carrito de compras.

## Requisitos Previos

- Python 3.8 o superior
- Node.js 14 o superior
- MongoDB 4.4 o superior

## Instalación

### Backend

1. Navega a la carpeta del backend:
```bash
cd backend
```

2. Crea un entorno virtual:
```bash
python -m venv venv
```

3. Activa el entorno virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

5. Crea un archivo `.env` con las siguientes variables:
```
MONGO_URI=mongodb://localhost:27017
DB_NAME=minicore_db
DEBUG=True
SECRET_KEY=dev_key_change_in_production
CORS_ORIGINS=http://localhost:3000
```

### Frontend

1. Navega a la carpeta del frontend:
```bash
cd frontend
```

2. Instala las dependencias:
```bash
npm install
```

## Ejecución

### Backend

1. Asegúrate de que MongoDB esté corriendo
2. En la carpeta `backend`, ejecuta:
```bash
python app.py
```

### Frontend

1. En la carpeta `frontend`, ejecuta:
```bash
npm start
```

La aplicación estará disponible en:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

## Características

- Registro e inicio de sesión de usuarios
- Catálogo de productos por categorías festivas
- Carrito de compras persistente
- Selección de material y fecha de entrega
- Gestión de pedidos

## Estructura del Proyecto

```
.
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── requirements.txt
│   └── .env
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/
    │   ├── App.js
    │   └── index.js
    ├── package.json
    └── README.md
``` 