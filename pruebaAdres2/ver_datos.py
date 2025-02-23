import sqlite3

DB_NAME = "facturas.db"

def show_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM facturas")
    rows = cursor.fetchall()
    
    print("\nID | Nombre Archivo | Páginas | CUFE | Peso (KB)")
    print("-" * 80)
    for row in rows:
        print(row)
    
    conn.close()

show_data()
