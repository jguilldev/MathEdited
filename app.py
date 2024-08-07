from flask import Flask, render_template, request, jsonify
import sympy as sp
import re
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

def preprocesar_expresion(expresion):
    # Reemplaza los operadores de potencia
    expresion = expresion.replace('^', '**')

    # Reemplaza símbolos comunes por su equivalente en sympy
    simbolos = {
        '×': '*',
        '÷': '/',
        '√': 'sqrt',
        'π': 'pi',
        'sin': 'sin',
        'cos': 'cos',
        'tan': 'tan',
        'csc': 'csc',
        'sec': 'sec',
        'cot': 'cot',
        'ln': 'log',
        'log': 'log',
        'e^': 'exp',
        'sinh': 'sinh',
        'cosh': 'cosh',
        'tanh': 'tanh',
        '∂/∂x': 'diff',
        '∫': 'integrate',
        'lim': 'limit',
        '∑': 'Sum',
        '∏': 'Product',
        '∨': 'or',
        '∧': 'and',
        '¬': 'not',
        '≠': '!=',
        '≤': '<=',
        '≥': '>='
    }
    for simbolo, reemplazo in simbolos.items():
        expresion = expresion.replace(simbolo, reemplazo)

    # Añadir multiplicación explícita
    expresion = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expresion)
    expresion = re.sub(r'([a-zA-Z)])(\d)', r'\1*\2', expresion)

    return expresion

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/renderizar', methods=['POST'])
def renderizar():
    expresion = request.json['expresion']
    try:
        expresion_procesada = preprocesar_expresion(expresion)
        expr = sp.sympify(expresion_procesada)
        latex = sp.latex(expr)
        # Generar una imagen a partir de la expresión LaTeX
        imagen = generarLayoutex(latex)
        return jsonify({'success': True, 'imagen': imagen})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def generarLayoutex(latex):
    # Configurar matplotlib para renderizar la imagen
    plt.rcParams['text.usetex'] = True
    plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

    # Crear una figura y un eje
    fig, ax = plt.subplots()

    # Renderizar la expresión LaTeX en el eje
    ax.text(0.5, 0.5, f'${latex}$', fontsize=20, ha='center')

    # Ocultar los ejes
    ax.axis('off')

    # Guardar la figura en un buffer
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    # Codificar la imagen en base64
    imagen = base64.b64encode(buf.read()).decode('utf-8')

    return imagen

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)