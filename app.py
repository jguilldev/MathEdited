from flask import Flask, render_template, request, jsonify
import sympy as sp
import io
import base64
from matplotlib import pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.json
    expresion = data.get('expresion')
    try:
        simbolos = sp.symbols('x y z')
        resultado = sp.sympify(expresion, locals={**{str(s): s for s in simbolos}, **sp.__dict__})
        resultado = sp.simplify(resultado)

        # Generar LaTeX
        latex_code = sp.latex(resultado)

        # Generar Imagen de la ecuación
        buf = io.BytesIO()
        sp.preview(resultado, output='png', viewer='BytesIO', outputbuffer=buf)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return jsonify({
            'resultado': str(resultado),
            'latex': latex_code,
            'imagen': img_base64
        })
    except Exception as e:
        return jsonify({'error': 'Error al evaluar la expresión: ' + str(e)})

if __name__ == '__main__':
    app.run(debug=True)
