import os
import re
import sqlite3
import PyPDF2

# Expresión regular para extraer el CUFE
CUFE_REGEX = r"\b([0-9a-fA-F]\n*){95,100}\b"

# Configuración de la base de datos
DB_NAME = "facturas.db"

def create_database():
    """Crea la base de datos y la tabla si no existe."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo TEXT,
            numero_paginas INTEGER,
            cufe TEXT,
            peso_archivo_kb REAL
        )
    ''')
    conn.commit()
    conn.close()

def extract_cufe_from_pdf(pdf_path):
    """Extrae el CUFE de un archivo PDF usando una expresión regular."""
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            
            # Buscar el CUFE en el texto
            match = re.search(CUFE_REGEX, text)
            cufe = match.group(0) if match else None

            return len(pdf_reader.pages), cufe
    except Exception as e:
        print(f"Error procesando {pdf_path}: {e}")
        return None, None

def save_to_database(file_name, num_pages, cufe, file_size_kb):
    """Guarda los datos en la base de datos SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO facturas (nombre_archivo, numero_paginas, cufe, peso_archivo_kb)
        VALUES (?, ?, ?, ?)
    ''', (file_name, num_pages, cufe, file_size_kb))
    conn.commit()
    conn.close()

def process_pdfs(directory):
    """Procesa todos los archivos PDF en la carpeta especificada."""
    create_database()

    for file_name in os.listdir(directory):
        if file_name.lower().endswith(".pdf"):
            file_path = os.path.join(directory, file_name)
            file_size_kb = os.path.getsize(file_path) / 1024  # Convertir a KB
            
            num_pages, cufe = extract_cufe_from_pdf(file_path)
            if num_pages is not None and cufe is not None:
                save_to_database(file_name, num_pages, cufe, file_size_kb)
                print(f"Procesado: {file_name} - CUFE: {cufe}")

# Ruta de la carpeta con los PDF
pdf_folder = "C:\\adres\\pruebaAdres2\\facturas"
process_pdfs(pdf_folder)
