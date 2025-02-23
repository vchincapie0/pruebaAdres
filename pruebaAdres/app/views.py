import csv
import re
import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages


def validar_archivo(file):
    errors = []
    file_content = file.read().decode("utf-8").splitlines()
    reader = csv.reader(file_content, delimiter=",")

    for index, row in enumerate(reader, start=1):
        if len(row) != 5:
            errors.append(f"❌ Fila {index}: Número incorrecto de columnas ({len(row)} en lugar de 5).")
            continue

        # Validaciones individuales por columna
        if not re.match(r"^\d{3,10}$", row[0]):
            errors.append(f"⚠️ Fila {index}, Columna 1: Debe ser un número entre 3 y 10 caracteres.")

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", row[1]):
            errors.append(f"⚠️ Fila {index}, Columna 2: Correo electrónico inválido.")

        if row[2] not in ["CC", "TI"]:
            errors.append(f"⚠️ Fila {index}, Columna 3: Solo se permiten los valores 'CC' o 'TI'.")

        try:
            salario = int(row[3])
            if salario < 500000 or salario > 1500000:
                errors.append(f"⚠️ Fila {index}, Columna 4: El valor debe estar entre 500000 y 1500000.")
        except ValueError:
            errors.append(f"⚠️ Fila {index}, Columna 4: Debe ser un número.")

    return errors


def cargar_archivo(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            messages.error(request, "❌ No se ha seleccionado ningún archivo.")
            return redirect("cargar_archivo")

        if not file.name.endswith(".txt"):
            messages.error(request, "❌ Solo se permiten archivos .txt")
            return redirect("cargar_archivo")

        errors = validar_archivo(file)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            messages.success(request, "✅ Archivo validado con éxito. No se encontraron errores.")

        return redirect("cargar_archivo")

    return render(request, "cargar_archivo.html")
