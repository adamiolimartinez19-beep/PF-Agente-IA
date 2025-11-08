# agente_ia.py
import os
from groq import Groq
from dotenv import load_dotenv
from base_datos import BaseDatos

# Cargar variables de entorno
load_dotenv()

class AgenteIA:
    def __init__(self):
        self.bd = BaseDatos()
        self.cliente_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.esquema_bd = self._obtener_esquema_bd()
    
    def _obtener_esquema_bd(self):
        """Retorna el esquema completo de la base de datos para el prompt"""
        return """
        ESQUEMA DE BASE DE DATOS:

        TABLA categorias:
        - id (INTEGER, PRIMARY KEY)
        - nombre (TEXT)

        TABLA proveedores:
        - id (INTEGER, PRIMARY KEY)
        - nombre (TEXT)
        - contacto (TEXT)
        - telefono (TEXT)

        TABLA productos:
        - id (INTEGER, PRIMARY KEY)
        - nombre (TEXT)
        - descripcion (TEXT)
        - precio (REAL)
        - stock (INTEGER)
        - categoria_id (INTEGER, FOREIGN KEY a categorias.id)
        - proveedor_id (INTEGER, FOREIGN KEY a proveedores.id)

        TABLA clientes:
        - id (INTEGER, PRIMARY KEY)
        - nombre (TEXT)
        - email (TEXT)
        - telefono (TEXT)
        - ciudad (TEXT)
        - fecha_registro (DATE)

        TABLA empleados:
        - id (INTEGER, PRIMARY KEY)
        - nombre (TEXT)
        - email (TEXT)
        - rol (TEXT)
        - fecha_contratacion (DATE)

        TABLA ventas:
        - id (INTEGER, PRIMARY KEY)
        - cliente_id (INTEGER, FOREIGN KEY a clientes.id)
        - empleado_id (INTEGER, FOREIGN KEY a empleados.id)
        - fecha (DATE)
        - total (REAL)
        - estado (TEXT)

        TABLA detalles_venta:
        - id (INTEGER, PRIMARY KEY)
        - venta_id (INTEGER, FOREIGN KEY a ventas.id)
        - producto_id (INTEGER, FOREIGN KEY a productos.id)
        - cantidad (INTEGER)
        - precio_unitario (REAL)

        RELACIONES PRINCIPALES:
        - productos.categoria_id → categorias.id
        - productos.proveedor_id → proveedores.id
        - ventas.cliente_id → clientes.id
        - ventas.empleado_id → empleados.id
        - detalles_venta.venta_id → ventas.id
        - detalles_venta.producto_id → productos.id
        """
    
    def _generar_prompt(self, pregunta):
        """Genera el prompt estricto para Groq"""
        return f"""
        Eres exclusivamente un generador de consultas SQL. Tu única función es convertir preguntas en español a código SQL.

        {self.esquema_bd}

        REGLAS ESTRICTAS:
        1. RESPUESTA ÚNICAMENTE CON EL CÓDIGO SQL
        2. NO incluyas explicaciones, texto adicional, comentarios o saludos
        3. NO uses markdown, backticks, o formato especial
        4. SIEMPRE comienza directamente con SELECT
        5. Si no entiendes la pregunta, genera una consulta por defecto: SELECT * FROM productos LIMIT 5

        EJEMPLOS DE ENTRADA/SALIDA:
        Entrada: "lista de empleados"
        Salida: SELECT * FROM empleados

        Entrada: "productos con stock bajo" 
        Salida: SELECT nombre, precio, stock FROM productos WHERE stock < 10

        Entrada: "ventas de María González"
        Salida: SELECT v.*, c.nombre as cliente, e.nombre as empleado FROM ventas v JOIN clientes c ON v.cliente_id = c.id JOIN empleados e ON v.empleado_id = e.id WHERE c.nombre LIKE '%María González%'

        Entrada: "qué ha comprado Carlos Rodríguez"
        Salida: SELECT p.nombre as producto, dv.cantidad, dv.precio_unitario, v.fecha FROM ventas v JOIN clientes c ON v.cliente_id = c.id JOIN detalles_venta dv ON v.id = dv.venta_id JOIN productos p ON dv.producto_id = p.id WHERE c.nombre LIKE '%Carlos Rodríguez%'

        Entrada: "productos de la categoría electrónicos"
        Salida: SELECT p.nombre, p.precio, p.stock FROM productos p JOIN categorias c ON p.categoria_id = c.id WHERE c.nombre LIKE '%Electrónicos%'

        Entrada: "ventas de este mes"
        Salida: SELECT v.id, c.nombre as cliente, e.nombre as empleado, v.total, v.fecha FROM ventas v JOIN clientes c ON v.cliente_id = c.id JOIN empleados e ON v.empleado_id = e.id WHERE v.fecha >= date('now', 'start of month')

        Entrada: "empleados que son vendedores"
        Salida: SELECT nombre, email, fecha_contratacion FROM empleados WHERE rol LIKE '%vendedor%'

        Entrada: "clientes de Bogotá"
        Salida: SELECT nombre, email, telefono FROM clientes WHERE ciudad LIKE '%Bogotá%'

        Entrada: "productos más vendidos"
        Salida: SELECT p.nombre, SUM(dv.cantidad) as total_vendido FROM detalles_venta dv JOIN productos p ON dv.producto_id = p.id GROUP BY p.id, p.nombre ORDER BY total_vendido DESC

        INSTRUCCIÓN FINAL: 
        Responde EXCLUSIVAMENTE con el código SQL, sin nada más.

        Entrada: "{pregunta}"
        Salida:
        """
    
    def _es_sql_seguro(self, sql):
        """Valida que el SQL sea seguro para ejecutar"""
        if not sql:
            return False
            
        sql_upper = sql.upper().strip()
        
        # Solo permitir SELECT
        if not sql_upper.startswith('SELECT'):
            return False
            
        # Bloquear palabras peligrosas
        palabras_peligrosas = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
        for palabra in palabras_peligrosas:
            if palabra in sql_upper:
                return False
                
        return True
    
    def _formatear_sql_para_html(self, sql):
        """Formatea el SQL para mostrarlo bonito en HTML"""
        # Limpiar y formatear el SQL
        sql_limpio = sql.strip()
        
        # Crear caja de código con estilo
        sql_html = f"""
        <div class='sql-container'>
            <div class='sql-header'>
                <span class='sql-icon'></span>
                <strong>SQL Generado</strong>
            </div>
            <div class='sql-code'>
                <pre><code>{sql_limpio}</code></pre>
            </div>
        </div>
        """
        return sql_html
    
    def _ejecutar_sql(self, sql):
        """Ejecuta SQL y retorna SQL formateado + resultados"""
        try:
            print(f"Ejecutando SQL: {sql}")
            resultado_completo = self.bd.ejecutar_consulta(sql)
            
            if not resultado_completo:
                return "<div class='mensaje-error'>Error al ejecutar la consulta</div>"
            
            resultados = resultado_completo['datos']
            nombres_columnas = resultado_completo['columnas']
            
            print(f"Resultados obtenidos: {resultados}")
            print(f"Nombres de columnas: {nombres_columnas}")
            
            # Formatear SQL para mostrar
            sql_html = self._formatear_sql_para_html(sql)
            
            # Formatear resultados de tabla
            tabla_html = self._formatear_resultados(resultados, nombres_columnas)
            
            # Combinar SQL + Tabla
            return sql_html + tabla_html
            
        except Exception as e:
            print(f"Error ejecutando SQL: {e}")
            return f"<div class='mensaje-error'>Error en la consulta: {str(e)}</div>"
    
    def procesar_pregunta(self, pregunta):
        """Procesa preguntas usando Groq IA"""
        pregunta = pregunta.strip()
        
        if not pregunta:
            return "<div class='mensaje-error'>Por favor escribe una pregunta</div>"
        
        try:
            # Generar SQL usando Groq
            prompt = self._generar_prompt(pregunta)
            
            respuesta = self.cliente_groq.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.1,
                max_tokens=200
            )
            
            sql_generado = respuesta.choices[0].message.content.strip()
            sql_generado = sql_generado.replace('```sql', '').replace('```', '').strip()

            print(f"SQL generado: {sql_generado}")
            print(f"¿Es seguro?: {self._es_sql_seguro(sql_generado)}")

            # Validar seguridad
            if not self._es_sql_seguro(sql_generado):
                print(f"SQL rechazado: {sql_generado}")
                return "<div class='mensaje-error'>Consulta no permitida por seguridad</div>"
            
            # Ejecutar el SQL y retornar resultados
            return self._ejecutar_sql(sql_generado)
            
        except Exception as e:
            return f"<div class='mensaje-error'>Error al procesar: {str(e)}</div>"
    
    def _formatear_resultados(self, resultados, nombres_columnas):
        """Formatea los resultados en una tabla HTML con nombres reales de columnas"""
        if not resultados:
            return "<p>No se encontraron resultados</p>"
        
        # Si no hay nombres de columnas, usar nombres genéricos
        if not nombres_columnas:
            nombres_columnas = [f"Columna {i+1}" for i in range(len(resultados[0]))]
        
        # Crear tabla HTML
        tabla_html = """
        <div class='resultados-container'>
            <div class='resultados-header'>
                <span class='tabla-icon'></span>
                <strong>Resultados</strong>
            </div>
            <table class='tabla-bonita'>
                <thead>
                    <tr>
        """
        
        # Agregar encabezados REALES
        for nombre_columna in nombres_columnas:
            # Formatear nombres de columnas (remplazar _ por espacios, capitalizar)
            nombre_bonito = nombre_columna.replace('_', ' ').title()
            tabla_html += f"<th>{nombre_bonito}</th>"
        
        tabla_html += """
                    </tr>
                </thead>
                <tbody>
        """
        
        # Agregar filas de datos
        for fila in resultados:
            tabla_html += "<tr>"
            for valor in fila:
                # Formatear números y valores None
                if valor is None:
                    valor_str = "-"
                elif isinstance(valor, float):
                    valor_str = f"${valor:.2f}"
                elif isinstance(valor, int):
                    # Si es un ID, mostrarlo normal, si es stock/precio, formatear
                    if any(palabra in str(valor).lower() for palabra in ['id', 'codigo']):
                        valor_str = str(valor)
                    else:
                        valor_str = f"{valor:,}"  # Formato con separadores de miles
                else:
                    valor_str = str(valor)
                tabla_html += f"<td>{valor_str}</td>"
            tabla_html += "</tr>"
        
        tabla_html += """
                </tbody>
            </table>
            <p class='contador-resultados'>Se encontraron {cantidad} resultados</p>
        </div>
        """.format(cantidad=len(resultados))
        
        return tabla_html