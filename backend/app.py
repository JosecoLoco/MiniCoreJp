from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from models import Producto, Usuario
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de MongoDB
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    db = client.impresiones3d
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    exit(1)

# Inicializar modelos
producto_model = Producto(db)
usuario_model = Usuario(db)

@app.route('/')
def index():
    return jsonify({"mensaje": "API de Impresiones 3D funcionando correctamente"})

@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    try:
        print("Obteniendo productos...")
        categoria = request.args.get('categoria')
        print(f"Categoría solicitada: {categoria}")
        
        if categoria and categoria != 'todos':
            productos = producto_model.obtener_por_categoria(categoria)
            print(f"Productos encontrados para categoría {categoria}: {len(productos)}")
        else:
            productos = producto_model.obtener_todos()
            print(f"Total de productos encontrados: {len(productos)}")
        
        if not productos:
            print("No se encontraron productos")
            return jsonify([])
            
        print("Productos encontrados:", productos)
        return jsonify(productos)
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/productos/<id>', methods=['GET'])
def obtener_producto(id):
    try:
        producto = producto_model.obtener_por_id(id)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        return jsonify(producto)
    except Exception as e:
        print(f"Error al obtener producto: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/usuarios/registro', methods=['POST'])
def registro():
    try:
        datos = request.get_json()
        if not datos or not datos.get('email') or not datos.get('password'):
            return jsonify({"error": "Datos incompletos"}), 400
        
        if usuario_model.obtener_por_email(datos['email']):
            return jsonify({"error": "El email ya está registrado"}), 400
        
        usuario_model.crear_usuario(datos)
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    except Exception as e:
        print(f"Error en registro: {e}")
        return jsonify({"error": "Error al registrar usuario"}), 500

@app.route('/api/usuarios/login', methods=['POST'])
def login():
    try:
        datos = request.get_json()
        print('Datos recibidos en login:', datos)
        if not datos or not datos.get('email') or not datos.get('password'):
            return jsonify({"error": "Datos incompletos"}), 400
        
        usuario = usuario_model.obtener_por_email(datos['email'])
        print('Usuario encontrado:', usuario)
        if not usuario or usuario['password'] != datos['password']:
            print('Contraseña recibida:', datos['password'])
            print('Contraseña almacenada:', usuario['password'] if usuario else None)
            return jsonify({"error": "Credenciales inválidas"}), 401
        
        return jsonify({"mensaje": "Login exitoso", "usuario": usuario}), 200
    except Exception as e:
        print(f"Error en login: {e}")
        return jsonify({"error": "Error al iniciar sesión"}), 500

@app.route('/api/usuarios/carrito', methods=['GET'])
def obtener_carrito():
    try:
        email = request.args.get('email')
        if not email:
            return jsonify({"error": "Email no proporcionado"}), 400
        
        carrito = usuario_model.obtener_carrito(email)
        return jsonify(carrito)
    except Exception as e:
        print(f"Error al obtener carrito: {e}")
        return jsonify({"error": "Error al obtener carrito"}), 500

@app.route('/api/usuarios/carrito', methods=['PUT'])
def actualizar_carrito():
    try:
        datos = request.get_json()
        if not datos or not datos.get('email') or not datos.get('carrito'):
            return jsonify({"error": "Datos incompletos"}), 400
        
        usuario_model.actualizar_carrito(datos['email'], datos['carrito'])
        return jsonify({"mensaje": "Carrito actualizado exitosamente"})
    except Exception as e:
        print(f"Error al actualizar carrito: {e}")
        return jsonify({"error": "Error al actualizar carrito"}), 500

@app.route('/api/usuarios/pedidos', methods=['POST'])
def crear_pedido():
    try:
        datos = request.get_json()
        if not datos or not datos.get('email') or not datos.get('productos'):
            return jsonify({"error": "Datos incompletos"}), 400
        
        usuario_model.crear_pedido(datos['email'], datos)
        return jsonify({"mensaje": "Pedido creado exitosamente"}), 201
    except Exception as e:
        print(f"Error al crear pedido: {e}")
        return jsonify({"error": "Error al crear pedido"}), 500

@app.route('/api/usuarios/pedidos/estado', methods=['PUT'])
def actualizar_estado_pedido():
    try:
        datos = request.get_json()
        email = datos.get('email')
        fecha_pedido = datos.get('fecha_pedido')
        nuevo_estado = datos.get('estado')
        if not email or not fecha_pedido or not nuevo_estado:
            return jsonify({'error': 'Datos incompletos'}), 400
        usuario = db.usuarios.find_one({'email': email})
        if not usuario or 'pedidos' not in usuario:
            return jsonify({'error': 'Usuario o pedido no encontrado'}), 404
        actualizado = False
        for pedido in usuario['pedidos']:
            if str(pedido.get('fecha_pedido')) == str(fecha_pedido):
                pedido['estado'] = nuevo_estado
                actualizado = True
        if actualizado:
            db.usuarios.update_one({'email': email}, {'$set': {'pedidos': usuario['pedidos']}})
            return jsonify({'mensaje': 'Estado actualizado'}), 200
        else:
            return jsonify({'error': 'Pedido no encontrado'}), 404
    except Exception as e:
        print(f"Error al actualizar estado de pedido: {e}")
        return jsonify({'error': 'Error al actualizar estado de pedido'}), 500

@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        usuarios = list(db.usuarios.find())
        for u in usuarios:
            u['_id'] = str(u['_id'])
            if 'password' in u:
                del u['password']
        return jsonify(usuarios)
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return jsonify([]), 500

def inicializar_productos():
    try:
        # Forzar la inicialización eliminando productos existentes
        db.productos.delete_many({})
        print("Colección de productos limpiada")

        HOST_URL = "http://192.168.1.95:5000"
        productos_iniciales = [
            # Navidad
            {
                "nombre": "Árbol de Navidad",
                "precio": 29.99,
                "imagen": f"{HOST_URL}/static/navidad1.jpg",
                "descripcion": "Árbol de Navidad decorativo impreso en 3D",
                "categoria": "navidad",
                "material": "PLA"
            },
            {
                "nombre": "Adornos Navideños",
                "precio": 39.99,
                "imagen": f"{HOST_URL}/static/navidad2.jpg",
                "descripcion": "Set de adornos navideños impresos en 3D (Santa, renos, duende)",
                "categoria": "navidad",
                "material": "PLA"
            },
            # San Valentín
            {
                "nombre": "Corazón Decorativo",
                "precio": 24.99,
                "imagen": "/static/corazon_valentin.png",
                "descripcion": "Corazón decorativo para San Valentín",
                "categoria": "san_valentin",
                "material": "PLA"
            },
            {
                "nombre": "Marco de Fotos Corazón",
                "precio": 34.99,
                "imagen": "https://i.imgur.com/9JZqXKt.jpg",
                "descripcion": "Marco de fotos con forma de corazón",
                "categoria": "san_valentin",
                "material": "PLA"
            },
            {
                "nombre": "Like San Valentín",
                "precio": 14.99,
                "imagen": f"{HOST_URL}/static/Like.png",
                "descripcion": "Corazón tipo like para regalar en San Valentín",
                "categoria": "san_valentin",
                "material": "PLA"
            },
            # Halloween
            {
                "nombre": "Calabaza Decorativa",
                "precio": 27.99,
                "imagen": "https://i.imgur.com/7JZqXKt.jpg",
                "descripcion": "Calabaza decorativa para Halloween",
                "categoria": "halloween",
                "material": "PLA"
            },
            {
                "nombre": "Fantasma LED",
                "precio": 39.99,
                "imagen": "https://i.imgur.com/6JZqXKt.jpg",
                "descripcion": "Fantasma decorativo con iluminación LED",
                "categoria": "halloween",
                "material": "PLA"
            },
            # Pascua
            {
                "nombre": "Conejo de Pascua",
                "precio": 22.99,
                "imagen": "https://i.imgur.com/5JZqXKt.jpg",
                "descripcion": "Conejo decorativo para Pascua",
                "categoria": "pascua",
                "material": "PLA"
            },
            {
                "nombre": "Huevo Decorativo",
                "precio": 19.99,
                "imagen": "https://i.imgur.com/4JZqXKt.jpg",
                "descripcion": "Huevo decorativo para Pascua",
                "categoria": "pascua",
                "material": "PLA"
            }
        ]

        for producto in productos_iniciales:
            resultado = producto_model.crear_producto(producto)
            print(f"Producto creado: {resultado}")
        print("Productos inicializados correctamente")
    except Exception as e:
        print(f"Error al inicializar productos: {e}")

# Inicializar productos al arrancar la aplicación
inicializar_productos()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 