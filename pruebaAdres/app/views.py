import csv
import re
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

def validate_csv(file_path):
    errors = []
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)  # Sigue leyéndolo como CSV
        rows = list(reader)

        # Validar número de columnas
        if len(rows[0]) != 5:
            return {'error': 'El archivo debe contener exactamente 5 columnas'}

        for i, row in enumerate(rows, start=1):
            if len(row) != 5:
                errors.append(f'Fila {i}: Número incorrecto de columnas')
                continue

            # Validaciones específicas de cada columna
            if not re.fullmatch(r'\d{3,10}', row[0]):
                errors.append(f'Fila {i}, Columna 1: Debe ser un número entre 3 y 10 caracteres')

            if not re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.\w+$', row[1]):
                errors.append(f'Fila {i}, Columna 2: Formato de correo inválido')

            if row[2] not in ['CC', 'TI']:
                errors.append(f'Fila {i}, Columna 3: Solo se permite "CC" o "TI"')

            try:
                value = int(row[3])
                if not (500000 <= value <= 1500000):
                    errors.append(f'Fila {i}, Columna 4: Debe estar entre 500000 y 1500000')
            except ValueError:
                errors.append(f'Fila {i}, Columna 4: No es un número válido')

    return {'errors': errors} if errors else {'success': 'Archivo validado correctamente'}

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        if not file.name.endswith('.csv') and not file.name.endswith('.txt'):
            return JsonResponse({'error': 'Solo se permiten archivos CSV o TXT'})

        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        validation_result = validate_csv(file_path)
        return JsonResponse(validation_result)

    return render(request, 'cargar_archivo.html')
