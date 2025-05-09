from datetime import datetime
from bson import ObjectId

class Producto:
    def __init__(self, db):
        self.collection = db.productos

    def crear_producto(self, producto):
        try:
            producto['fecha_creacion'] = datetime.utcnow()
            resultado = self.collection.insert_one(producto)
            producto['_id'] = str(resultado.inserted_id)
            print(f"Producto creado con ID: {producto['_id']}")
            return producto
        except Exception as e:
            print(f"Error al crear producto: {e}")
            return None

    def obtener_todos(self):
        try:
            productos = list(self.collection.find())
            print(f"Total de productos en la base de datos: {len(productos)}")
            for producto in productos:
                producto['_id'] = str(producto['_id'])
                # Asegurarse de que todos los campos necesarios estén presentes
                producto.setdefault('nombre', '')
                producto.setdefault('precio', 0)
                producto.setdefault('imagen', '')
                producto.setdefault('descripcion', '')
                producto.setdefault('categoria', '')
                producto.setdefault('material', 'PLA')
            return productos
        except Exception as e:
            print(f"Error al obtener todos los productos: {e}")
            return []

    def obtener_por_categoria(self, categoria):
        try:
            print(f"Buscando productos para categoría: {categoria}")
            productos = list(self.collection.find({'categoria': categoria}))
            print(f"Productos encontrados para categoría {categoria}: {len(productos)}")
            for producto in productos:
                producto['_id'] = str(producto['_id'])
                # Asegurarse de que todos los campos necesarios estén presentes
                producto.setdefault('nombre', '')
                producto.setdefault('precio', 0)
                producto.setdefault('imagen', '')
                producto.setdefault('descripcion', '')
                producto.setdefault('categoria', categoria)
                producto.setdefault('material', 'PLA')
            return productos
        except Exception as e:
            print(f"Error al obtener productos por categoría: {e}")
            return []

    def obtener_por_id(self, id):
        try:
            producto = self.collection.find_one({'_id': ObjectId(id)})
            if producto:
                producto['_id'] = str(producto['_id'])
                # Asegurarse de que todos los campos necesarios estén presentes
                producto.setdefault('nombre', '')
                producto.setdefault('precio', 0)
                producto.setdefault('imagen', '')
                producto.setdefault('descripcion', '')
                producto.setdefault('categoria', '')
                producto.setdefault('material', 'PLA')
            return producto
        except Exception as e:
            print(f"Error al obtener producto por ID: {e}")
            return None

    def actualizar_producto(self, id, datos):
        try:
            resultado = self.collection.update_one(
                {'_id': ObjectId(id)},
                {'$set': datos}
            )
            return resultado.modified_count > 0
        except Exception as e:
            print(f"Error al actualizar producto: {e}")
            return False

    def eliminar_producto(self, id):
        try:
            resultado = self.collection.delete_one({'_id': ObjectId(id)})
            return resultado.deleted_count > 0
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            return False

class Usuario:
    def __init__(self, db):
        self.collection = db.usuarios

    def crear_usuario(self, usuario):
        usuario['fecha_registro'] = datetime.utcnow()
        usuario['carrito'] = []
        usuario['password'] = str(usuario['password'])  # Asegura que la contraseña sea string
        return self.collection.insert_one(usuario)

    def obtener_por_email(self, email):
        usuario = self.collection.find_one({'email': email})
        if usuario:
            usuario['_id'] = str(usuario['_id'])
            if 'password' in usuario:
                usuario['password'] = str(usuario['password'])
        return usuario

    def actualizar_carrito(self, email, carrito):
        return self.collection.update_one(
            {'email': email},
            {'$set': {'carrito': carrito}}
        )

    def obtener_carrito(self, email):
        usuario = self.obtener_por_email(email)
        return usuario.get('carrito', []) if usuario else []

    def crear_pedido(self, email, pedido):
        pedido['fecha_pedido'] = datetime.utcnow()
        pedido['estado'] = 'pendiente'
        return self.collection.update_one(
            {'email': email},
            {'$push': {'pedidos': pedido}}
        ) 