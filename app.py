from flask import Flask, render_template, request, jsonify
import sympy as sp
import re

app = Flask(__name__)

def preprocesar_expresion(expresion):
    # Reemplaza los operadores de potencia
    expresion = expresion.replace('^', '**')
    
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
        return jsonify({'success': True, 'latex': latex})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
