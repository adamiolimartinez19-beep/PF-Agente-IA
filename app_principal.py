# app_principal.py
from flask import Flask, render_template_string, request, jsonify
from agente_ia import AgenteIA

app = Flask(__name__)
agente = AgenteIA()

# HTML mejorado con CSS profesional + estilos para SQL
HTML_BASE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agente de Ventas Inteligente</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .pregunta-section {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 4px solid #3498db;
        }
        
        .input-group {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        #preguntaInput {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        #preguntaInput:focus {
            outline: none;
            border-color: #3498db;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }
        
        button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }
        
        .ejemplos {
            margin-top: 20px;
            font-size: 14px;
            color: #6c757d;
        }
        
        .ejemplos strong {
            color: #2c3e50;
        }
        
        #resultado {
            margin-top: 20px;
            transition: all 0.3s ease;
        }
        
        /* Estilos para el contenedor de SQL */
        .sql-container {
            background: #1e1e1e;
            border-radius: 10px;
            margin: 20px 0;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .sql-header {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 16px;
            font-weight: 600;
        }
        
        .sql-icon {
            font-size: 18px;
        }
        
        .sql-code {
            padding: 20px;
            background: #1e1e1e;
            color: #d4d4d4;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.5;
            overflow-x: auto;
        }
        
        .sql-code pre {
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .sql-code code {
            color: #d4d4d4;
        }
        
        /* Estilos para el contenedor de resultados */
        .resultados-container {
            margin: 20px 0;
        }
        
        .resultados-header {
            background: linear-gradient(135deg, #27ae60, #2ecc71);
            color: white;
            padding: 12px 20px;
            border-radius: 10px 10px 0 0;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 16px;
            font-weight: 600;
        }
        
        .tabla-icon {
            font-size: 18px;
        }
        
        .tabla-bonita {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 0 0 10px 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .tabla-bonita th {
            background: linear-gradient(135deg, #34495e, #2c3e50);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 14px;
            letter-spacing: 0.5px;
        }
        
        .tabla-bonita td {
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
            color: #2c3e50;
        }
        
        .tabla-bonita tr:hover {
            background-color: #f8f9fa;
            transform: scale(1.01);
            transition: all 0.2s ease;
        }
        
        .tabla-bonita tr:last-child td {
            border-bottom: none;
        }
        
        .contador-resultados {
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
            margin-top: 10px;
            padding: 10px;
            background: #ecf0f1;
            border-radius: 5px;
        }
        
        .mensaje-error {
            background: #e74c3c;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        .mensaje-info {
            background: #3498db;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #7f8c8d;
        }
        
        @media (max-width: 768px) {
            .input-group {
                flex-direction: column;
            }
            
            #preguntaInput {
                width: 100%;
            }
            
            button {
                width: 100%;
            }
            
            .content {
                padding: 20px;
            }
            
            .sql-code {
                font-size: 12px;
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Agente de Ventas Inteligente</h1>
            <p>Consulta información de empleados, productos y clientes en lenguaje natural</p>
        </div>
        
        <div class="content">
            <div class="pregunta-section">
                <div class="input-group">
                    <input type="text" id="preguntaInput" 
                           placeholder="Ej: lista de empleados, stock de productos, ver clientes..." 
                           autocomplete="off" />
                    <button onclick="hacerPregunta()">Consultar</button>
                </div>
                
                <div class="ejemplos">
                    <strong>Ejemplos:</strong> 
                    "lista de empleados" • "stock de productos" • "productos con stock bajo" • "ver clientes"
                </div>
            </div>
            
            <div id="resultado"></div>
        </div>
    </div>

    <script>
        function hacerPregunta() {
            const pregunta = document.getElementById('preguntaInput').value.trim();
            const resultadoDiv = document.getElementById('resultado');
            
            if (!pregunta) {
                resultadoDiv.innerHTML = '<div class="mensaje-error">Por favor, escribe una pregunta</div>';
                return;
            }
            
            resultadoDiv.innerHTML = '<div class="loading">Procesando tu consulta...</div>';
            
            fetch('/preguntar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pregunta: pregunta })
            })
            .then(response => response.json())
            .then(data => {
                resultadoDiv.innerHTML = data.respuesta;
            })
            .catch(error => {
                resultadoDiv.innerHTML = '<div class="mensaje-error">Error al procesar la consulta: ' + error + '</div>';
            });
        }
        
        // Permitir Enter para enviar
        document.getElementById('preguntaInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                hacerPregunta();
            }
        });
        
        // Enfocar el input al cargar la página
        document.getElementById('preguntaInput').focus();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_BASE)

@app.route('/preguntar', methods=['POST'])
def preguntar():
    datos = request.get_json()
    pregunta = datos.get('pregunta', '')
    
    if not pregunta:
        return jsonify({'respuesta': '<div class="mensaje-error">Por favor escribe una pregunta</div>'})
    
    respuesta = agente.procesar_pregunta(pregunta)
    return jsonify({'respuesta': respuesta})

if __name__ == '__main__':
    print("Iniciando agente de ventas en http://localhost:5000")
    app.run(debug=True)