# Reducir el tamaño de GRILLA DE PAX.ods manteniendo solo datos de 2025
# Requires: pip install odfpy
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
import sys
import shutil
from datetime import datetime
import re

SRC = "GRILLA DE PAX.ods"
BACKUP = "GRILLA_DE_PAX_RESPALDO_HISTORICO.ods"
DEST = "GRILLA_DE_PAX_2025.ods"
SHEET_NAME = "Ingresos 23 D MAYO"

def extract_year_from_row(row):
    """Intenta extraer el año de una fila buscando fechas en las celdas"""
    cells = row.getElementsByType(TableCell)
    years_found = []
    
    for cell in cells:
        # Primero intentar obtener el atributo datevalue
        date_value = cell.getAttribute('datevalue')
        if date_value:
            match = re.search(r'20\d{2}', str(date_value))
            if match:
                years_found.append(int(match.group(0)))
        
        # Obtener el valor de texto de la celda
        paragraphs = cell.getElementsByType(P)
        for p in paragraphs:
            text = str(p)
            if text:
                # Buscar patrones de fecha comunes
                # Formato: dd/mm/yyyy, dd-mm-yyyy, yyyy-mm-dd, etc.
                date_patterns = [
                    r'\b(\d{1,2})[/-](\d{1,2})[/-](20\d{2})\b',  # dd/mm/yyyy o dd-mm-yyyy
                    r'\b(20\d{2})[/-](\d{1,2})[/-](\d{1,2})\b',  # yyyy-mm-dd o yyyy/mm/dd
                    r'\b(20\d{2})\b',  # solo año
                ]
                
                for pattern in date_patterns:
                    matches = re.finditer(pattern, text)
                    for match in matches:
                        groups = match.groups()
                        # Buscar el año (4 dígitos que empiecen con 20)
                        for g in groups:
                            if g and len(g) == 4 and g.startswith('20'):
                                try:
                                    years_found.append(int(g))
                                except:
                                    pass
    
    # Retornar el año más reciente encontrado en la fila
    if years_found:
        return max(years_found)
    return None

def filter_sheet_by_year(doc, sheet_name, min_year=2024):
    """Filtra una pestaña para mantener solo las filas desde el año especificado"""
    tables = doc.spreadsheet.getElementsByType(Table)
    target_table = None
    
    for table in tables:
        if table.getAttribute("name") == sheet_name:
            target_table = table
            break
    
    if not target_table:
        print(f"⚠️  No se encontró la pestaña '{sheet_name}'")
        return 0, 0
    
    rows = target_table.getElementsByType(TableRow)
    total_rows = len(rows)
    
    # Mantener la primera fila (encabezados) y las filas de años recientes
    rows_to_keep = []
    rows_to_remove = []
    year_stats = {}
    
    print(f"\n📊 Analizando {total_rows:,} filas en '{sheet_name}'...")
    print(f"   Manteniendo años >= {min_year}")
    
    for idx, row in enumerate(rows):
        # Mantener siempre las primeras 2 filas (encabezados)
        if idx < 2:
            rows_to_keep.append(row)
            continue
        
        year = extract_year_from_row(row)
        
        # Mantener si el año es >= min_year o si no se encontró año (para evitar borrar datos sin fecha)
        if year is None or year >= min_year:
            rows_to_keep.append(row)
            if year:
                year_stats[year] = year_stats.get(year, 0) + 1
        else:
            rows_to_remove.append(row)
            year_stats[year] = year_stats.get(year, 0) + 1
        
        # Mostrar progreso cada 1000 filas
        if (idx + 1) % 1000 == 0:
            print(f"   Procesadas {idx + 1:,} filas...")
    
    # Mostrar estadísticas por año
    print(f"\n   Estadísticas por año:")
    for year in sorted(year_stats.keys()):
        status = "✅ MANTENER" if year >= min_year else "❌ ELIMINAR"
        print(f"      {year}: {year_stats[year]:,} filas - {status}")
    
    # Eliminar las filas antiguas
    removed_count = 0
    for row in rows_to_remove:
        target_table.removeChild(row)
        removed_count += 1
    
    kept_count = len(rows_to_keep)
    
    return removed_count, kept_count

def main():
    print("="*70)
    print("🔧 REDUCCIÓN DE TAMAÑO DE ARCHIVO ODS")
    print("="*70)
    
    # Crear respaldo del archivo original
    print(f"\n📦 Creando respaldo del archivo original...")
    print(f"   {SRC} → {BACKUP}")
    shutil.copy2(SRC, BACKUP)
    print(f"   ✅ Respaldo creado")
    
    # Crear copia de trabajo
    print(f"\n📄 Creando archivo de trabajo...")
    shutil.copy2(SRC, DEST)
    
    try:
        # Cargar el documento
        print(f"\n📂 Cargando {DEST}...")
        doc = load(DEST)
        
        # Filtrar la pestaña principal
        print(f"\n🔍 Filtrando pestaña '{SHEET_NAME}'...")
        print(f"   Manteniendo registros de 2024 y 2025")
        
        removed, kept = filter_sheet_by_year(doc, SHEET_NAME, min_year=2024)
        
        # Guardar el archivo modificado
        print(f"\n💾 Guardando archivo reducido...")
        doc.save(DEST)
        
        # Mostrar resultados
        print("\n" + "="*70)
        print("✅ PROCESO COMPLETADO")
        print("="*70)
        print(f"\n📊 Resultados:")
        print(f"   • Filas eliminadas: {removed:,}")
        print(f"   • Filas conservadas: {kept:,}")
        print(f"   • Porcentaje eliminado: {(removed/(removed+kept)*100):.1f}%")
        
        print(f"\n📁 Archivos generados:")
        print(f"   • Respaldo histórico completo (2021-2023): {BACKUP}")
        print(f"   • Archivo reducido (2024-2025): {DEST}")
        
        # Comparar tamaños de archivo
        import os
        original_size = os.path.getsize(SRC) / (1024 * 1024)
        new_size = os.path.getsize(DEST) / (1024 * 1024)
        reduction = ((original_size - new_size) / original_size * 100)
        
        print(f"\n💾 Tamaño de archivos:")
        print(f"   • Original: {original_size:.2f} MB")
        print(f"   • Reducido: {new_size:.2f} MB")
        print(f"   • Reducción: {reduction:.1f}%")
        
        print("\n" + "="*70)
        print("🎉 ¡Listo! El archivo ha sido reducido exitosamente.")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error durante el proceso: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
