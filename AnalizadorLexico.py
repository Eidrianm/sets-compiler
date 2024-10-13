import re

class AnalizadorLexico:
    def __init__(self):
        # Diccionario para almacenar los patrones
        self.tokens_re = {
            'CONJ': r'CONJ\s*:\s*(\w+)\s*->\s*([\w,~]+);',
            'OPERA': r'OPERA\s*:\s*(\w+)\s*->\s*([\^\&U\s]+)\s*\{([\w]+)\}\s*\{([\w]+)\};',  
            'EVALUAR': r'EVALUAR\(\s*\{([\w,]+)\}\s*,\s*(\w+)\);',  
            'ID': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'NUM': r'[0-9]+',
            'OPERADOR': r'U|&|-|\^',
            'COMENTARIO': r'#.*|<!.*!>',
            'ESPACIOS': r'[ \t\r\n\f]+',
            'ERROR': r'.'
        }
        self.conjuntos = {}  # Almacenar los conjuntos creados
        self.operaciones = []  # Almacenar las operaciones encontradas

    def reportar_error(self, mensaje, linea, columna):
        print(f"{mensaje} en línea: {linea}, columna: {columna}")

    import re

    def analizar_lexico(self, texto):
        tokens = []
        resultados = []
        linea = 1
        columna = 1
        pos = 0
        
        while pos < len(texto):
            match = None
            for token_nombre, token_patron in self.tokens_re.items():
                regex = re.compile(token_patron)
                match = regex.match(texto, pos)
                if match:
                    token_valor = match.group(0)
                    if token_nombre == 'ESPACIOS':
                        # Ignorar espacios
                        pass
                    elif token_nombre == 'COMENTARIO':
                        # Ignorar comentarios
                        pass
                    elif token_nombre == 'CONJ':
                        nombre_conjunto = match.group(1)
                        elementos_conjunto = match.group(2)
                        conjunto_creado = self.guardar_conjunto(nombre_conjunto, elementos_conjunto)
                        resultados.append(conjunto_creado)  # Acumular el nombre y conjunto
                    elif token_nombre == 'OPERA':
                        nombre_operacion = match.group(1)
                        operador = match.group(2)
                        conjunto1 = match.group(3)
                        conjunto2 = match.group(4)
                        operacion_creada = self.guardar_operacion(nombre_operacion, operador, conjunto1, conjunto2)
                        resultados.append(operacion_creada)  # Acumular el nombre y operación
                    elif token_nombre == 'EVALUAR':
                        elementos = match.group(1)
                        elementos=elementos.strip(',')
                        conjuntos = [elem for elem in elementos]
                        conjunto1 = str(conjuntos[0])
                        
                        conjunto2 = str(conjuntos[2])
                        nombre_operacion = match.group(2)   
                        resultado_evaluacion = self.evaluar_operacion(conjunto1,conjunto2, nombre_operacion)
                        resultados.append(resultado_evaluacion)  # Agrega el token creado
                        
                    elif token_nombre == 'ERROR':
                        self.reportar_error(f"Carácter no reconocido: {token_valor}", linea, columna)
                    else:
                        tokens.append({
                            'tipo': token_nombre,
                            'valor': token_valor,
                            'linea': linea,
                            'columna': columna
                        })
                    pos += len(token_valor)  # Mover la posición por la longitud del token
                    columnas_avanzadas = len(token_valor)
                    columna += columnas_avanzadas
                    saltos_de_linea = token_valor.count('\n')
                    if saltos_de_linea > 0:
                        linea += saltos_de_linea
                        columna = 1
                    break
            
            if not match:
                self.reportar_error(f"Carácter no reconocido: {texto[pos]}", linea, columna)
                pos += 1
                columna += 1
            
        return resultados  # Devolver todos los resultados acumulados

    
    def guardar_conjunto(self, nombre, elementos_str):
        elementos = self.parsear_conjunto(elementos_str)
        self.conjuntos[nombre] = elementos
        return {"nombre": nombre, "conjunto": elementos}
    
    def guardar_operacion(self, nombre_operacion, operador, conjunto1, conjunto2):
        if conjunto1 not in self.conjuntos or conjunto2 not in self.conjuntos:
            return {"error": f"Conjuntos no definidos: {conjunto1}, {conjunto2}"}
        else:
            self.operaciones.append({
                'operacion': nombre_operacion,
                'operador': operador,
                'conjunto1': conjunto1,
                'conjunto2': conjunto2
            })
            return {"nombre_operacion": nombre_operacion, "operacion": f"{conjunto1} {operador} {conjunto2}"}
    
    def evaluar_operacion(self, conjunto1, conjunto2, nombre_operacion):
    
        if self.conjuntos[conjunto1]:
            conjunto1_set = self.conjuntos[conjunto1]
        else:
            return {"error": f"Conjunto no definido: {conjunto1}"}
    
        if self.conjuntos[conjunto2]:
            conjunto2_set = self.conjuntos[conjunto2]
        else:
            return {"error": f"Conjunto no definido: {conjunto2}"}
    
    # Buscar la operación por nombre
        operacion = next((op for op in self.operaciones if op['operacion'] == nombre_operacion), None)
        if not operacion:
            return {"error": f"Operación no definida: {nombre_operacion}"}

        operador = operacion['operador']
        print(operador)
    # Realizar la operación sobre los conjuntos
        if operador.strip()  == 'U':
            resultado = conjunto1_set.union(conjunto2_set)
        elif operador.strip() == '&':
            resultado = conjunto1_set.intersection(conjunto2_set)
        elif operador.strip()  == '-':
            resultado = conjunto1_set.difference(conjunto2_set)
        elif operador.strip()  == '^':
            resultado = conjunto1_set.symmetric_difference(conjunto2_set)
        else:
            return {"error": "Operador no válido"}

        return {"resultado": resultado}

    def parsear_conjunto(self, conjunto_str):
        elementos = []
        for elem in conjunto_str.split(','):
            if '~' in elem:
                inicio, fin = elem.split('~')
                elementos.extend(chr(i) for i in range(ord(inicio), ord(fin) + 1))
            else:
                elementos.append(elem)
        return set(elementos)

# Ejemplo de uso
codigo = """CONJ A = {1,2,3};
CONJ : B -> {4,5,6};
OPERA : union -> U {A},{B};
EVALUAR({A},{B},union);
"""

analizador = AnalizadorLexico()

# Ejecutar análisis


