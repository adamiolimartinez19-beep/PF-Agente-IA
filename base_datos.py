# base_datos.py
import sqlite3
import os
from datetime import datetime, timedelta

class BaseDatos:
    def __init__(self):
        self.archivo = "ventas.db"
        self._inicializar_base_datos()
    
    def _inicializar_base_datos(self):
        """Crea la base de datos y tablas si no existen"""
        self._crear_tablas()
        # Solo insertar datos si las tablas están vacías
        if self._tablas_vacias():
            self._insertar_datos_ejemplo()
    
    def _tablas_vacias(self):
        """Verifica si las tablas principales están vacías"""
        try:
            conexion = sqlite3.connect(self.archivo)
            cursor = conexion.cursor()
            
            tablas = ['clientes', 'productos', 'empleados']
            for tabla in tablas:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                if cursor.fetchone()[0] > 0:
                    conexion.close()
                    return False
            conexion.close()
            return True
        except:
            return True
    
    def _crear_tablas(self):
        """Crea todas las tablas con estructura profesional"""
        conexion = sqlite3.connect(self.archivo)
        cursor = conexion.cursor()
        
        # Activar FOREIGN KEYS
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Tabla de categorías
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Tabla de proveedores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proveedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                contacto TEXT,
                telefono TEXT
            )
        ''')
        
        # Tabla de productos (mejorada)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                categoria_id INTEGER,
                proveedor_id INTEGER,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id),
                FOREIGN KEY (proveedor_id) REFERENCES proveedores (id)
            )
        ''')
        
        # Tabla de clientes (mejorada)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE,
                telefono TEXT,
                ciudad TEXT,
                fecha_registro DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        # Tabla de empleados (mejorada)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empleados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE,
                rol TEXT,
                fecha_contratacion DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        # Tabla de ventas (mejorada)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                empleado_id INTEGER,
                fecha DATE NOT NULL,
                total REAL NOT NULL,
                estado TEXT DEFAULT 'completada',
                FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                FOREIGN KEY (empleado_id) REFERENCES empleados (id)
            )
        ''')
        
        # Tabla de detalles_venta (nueva)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalles_venta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES ventas (id) ON DELETE CASCADE,
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        conexion.commit()
        conexion.close()
    
    def _insertar_datos_ejemplo(self):
        """Inserta datos de ejemplo coherentes y realistas"""
        conexion = sqlite3.connect(self.archivo)
        cursor = conexion.cursor()
        
        print("Insertando datos de ejemplo profesionales...")
        
        # 1. Insertar categorías
        categorias = [
            ('Electrónicos',),
            ('Ropa',),
            ('Hogar',),
            ('Deportes',)
        ]
        cursor.executemany('INSERT INTO categorias (nombre) VALUES (?)', categorias)
        
        # 2. Insertar proveedores
        proveedores = [
            ('TechCorp', 'Carlos Méndez', '3001234567'),
            ('ModaTotal', 'Ana López', '3109876543'),
            ('HogarExpress', 'Pedro Sánchez', '3205558899'),
            ('DeportesMax', 'Laura García', '3157773322')
        ]
        cursor.executemany('INSERT INTO proveedores (nombre, contacto, telefono) VALUES (?, ?, ?)', proveedores)
        
        # 3. Insertar productos con categorías y proveedores
        productos = [
            ('iPhone 15 Pro', '256GB, Titanio, Cámara 48MP', 1299.99, 25, 1, 1),
            ('Samsung Galaxy S24', '512GB, Pantalla Dynamic AMOLED', 1099.99, 18, 1, 1),
            ('MacBook Air M3', '13.6", 8GB RAM, 256GB SSD', 1499.99, 12, 1, 1),
            ('Camisa Polo Classic', 'Algodón 100%, Tallas S-XXL', 45.99, 50, 2, 2),
            ('Jeans Slim Fit', 'Denim elastizado, Color azul', 79.99, 30, 2, 2),
            ('Sofá 3 Plazas', 'Tela resistente, Color gris', 899.99, 8, 3, 3),
            ('Lámpara LED', 'RGB, Control remoto, 15W', 89.99, 40, 3, 3),
            ('Balón Fútbol', 'Tamaño 5, Oficial FIFA', 29.99, 60, 4, 4),
            ('Raqueta Tenis', 'Graphite, Peso 300g', 199.99, 15, 4, 4)
        ]
        cursor.executemany('''
            INSERT INTO productos (nombre, descripcion, precio, stock, categoria_id, proveedor_id) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', productos)
        
        # 4. Insertar clientes
        clientes = [
            ('María González', 'maria@email.com', '3001112233', 'Bogotá'),
            ('Carlos Rodríguez', 'carlos@email.com', '3104445566', 'Medellín'),
            ('Ana Martínez', 'ana@email.com', '3207778899', 'Cali'),
            ('Juan Pérez', 'juan@email.com', '3159990011', 'Bogotá'),
            ('Laura Díaz', 'laura@email.com', '3002223344', 'Medellín')
        ]
        cursor.executemany('INSERT INTO clientes (nombre, email, telefono, ciudad) VALUES (?, ?, ?, ?)', clientes)
        
        # 5. Insertar empleados
        empleados = [
            ('Sofia Castro', 'sofia@tienda.com', 'Vendedor', '2023-01-15'),
            ('Miguel Torres', 'miguel@tienda.com', 'Gerente', '2022-03-10'),
            ('Catalina Rojas', 'catalina@tienda.com', 'Cajero', '2023-06-20'),
            ('Andrés López', 'andres@tienda.com', 'Vendedor', '2023-02-28')
        ]
        cursor.executemany('INSERT INTO empleados (nombre, email, rol, fecha_contratacion) VALUES (?, ?, ?, ?)', empleados)
        
        # 6. Insertar ventas realistas
        # Fechas de los últimos 30 días
        fecha_base = datetime.now()
        ventas = [
            (1, 1, (fecha_base - timedelta(days=5)).strftime('%Y-%m-%d'), 1349.98, 'completada'),
            (2, 4, (fecha_base - timedelta(days=3)).strftime('%Y-%m-%d'), 1099.99, 'completada'),
            (3, 1, (fecha_base - timedelta(days=10)).strftime('%Y-%m-%d'), 1549.98, 'completada'),
            (4, 4, (fecha_base - timedelta(days=1)).strftime('%Y-%m-%d'), 125.98, 'completada'),
            (5, 1, (fecha_base - timedelta(days=15)).strftime('%Y-%m-%d'), 229.97, 'completada')
        ]
        cursor.executemany('INSERT INTO ventas (cliente_id, empleado_id, fecha, total, estado) VALUES (?, ?, ?, ?, ?)', ventas)
        
        # 7. Insertar detalles de venta
        detalles_venta = [
            (1, 1, 1, 1299.99),  # Venta 1: 1 iPhone
            (1, 4, 1, 49.99),    # Venta 1: 1 Camisa Polo
            (2, 2, 1, 1099.99),  # Venta 2: 1 Samsung Galaxy
            (3, 3, 1, 1499.99),  # Venta 3: 1 MacBook Air
            (3, 9, 1, 49.99),    # Venta 3: 1 Raqueta Tenis
            (4, 4, 2, 45.99),    # Venta 4: 2 Camisas Polo
            (4, 5, 1, 79.99),    # Venta 4: 1 Jeans
            (5, 8, 2, 29.99),    # Venta 5: 2 Balones
            (5, 9, 1, 199.99)    # Venta 5: 1 Raqueta Tenis
        ]
        cursor.executemany('''
            INSERT INTO detalles_venta (venta_id, producto_id, cantidad, precio_unitario) 
            VALUES (?, ?, ?, ?)
        ''', detalles_venta)
        
        conexion.commit()
        conexion.close()
        print("Datos de ejemplo insertados correctamente!")
    
    def ejecutar_consulta(self, consulta, parametros=()):
        """Ejecuta una consulta SQL y retorna los resultados Y nombres de columnas"""
        conexion = sqlite3.connect(self.archivo)
        cursor = conexion.cursor()
        
        try:
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(consulta, parametros)
            resultados = cursor.fetchall()
            
            # OBTENER NOMBRES DE COLUMNAS
            nombres_columnas = [descripcion[0] for descripcion in cursor.description] if cursor.description else []
            
            conexion.commit()
            return {
                'datos': resultados,
                'columnas': nombres_columnas
            }
        except Exception as e:
            print(f"Error en consulta SQL: {e}")
            return None
        finally:
            conexion.close()