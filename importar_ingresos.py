#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Importador CSV → Pestaña "Ingresos 23 D MAYO"
Replica la lógica del archivo Reserva.html
"""

from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
import csv
import sys
import shutil
from datetime import datetime

ODS_FILE = "GRILLA_DE_PAX_2026.ods"
SHEET_NAME = "Ingresos 23 D MAYO"

# Encabezados según Reserva.html
HEADERS = [
    'HAB',           # Nro. habitación
    'IN',            # Fecha de ingreso
    'OUT',           # Fecha de egreso
    'PAX',           # Cantidad plazas
    'ID',            # Tipo documento
    'N.º',           # Nro. doc.
    'NOMBRE',        # Apellido y nombre
    'EDAD',          # Edad
    'VOUCHER',       # Voucher
    'MAP',           # Servicio
    'ESTADO',        # Estado
    'BENEFICIO',     # Paquete
    'SEDE',          # Sede
    'OBSERVACIONES'  # Observación habitación
]

def create_backup():
    """Crea respaldo con timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"BACKUP_{timestamp}_{ODS_FILE}"
    shutil.copy2(ODS_FILE, backup_file)
    print(f"✅ Respaldo: {backup_file}")
    return backup_file

def read_csv_with_js_logic(csv_file):
    """
    Lee CSV usando la misma lógica que Reserva.html
    Extrae los campos en las posiciones exactas del JavaScript
    """
    print(f"\n📄 Procesando CSV: {csv_file}")
    
    records = []
    room_count = {}
    people_count = 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        # Saltar encabezado (línea 0)
        for i in range(1, len(lines)):
            line = lines[i].strip()
            
            if line:  # Omitir líneas vacías
                fields = line.split(',')
                
                # Extraer campos según posiciones del JS
                try:
                    room_number = fields[2]   # Nro. habitación
                    din = fields[8]           # Fecha ingreso
                    dout = fields[9]          # Fecha egreso
                    plazas = fields[5]        # Cantidad plazas
                    tipo_doc = fields[11]     # Tipo documento
                    nro_doc = fields[12]      # Nro. doc.
                    nombre = fields[13]       # Apellido y nombre
                    edad = fields[14]         # Edad
                    voucher = fields[6]       # Voucher
                    servicio = fields[16]     # Servicio
                    estado = fields[23]       # Estado
                    paquete = fields[17]      # Paquete
                    sede = fields[7]          # Sede
                    observacion = fields[4]   # Observación habitación
                    
                    record = {
                        'HAB': room_number,
                        'IN': din,
                        'OUT': dout,
                        'PAX': plazas,
                        'ID': tipo_doc,
                        'N.º': nro_doc,
                        'NOMBRE': nombre,
                        'EDAD': edad,
                        'VOUCHER': voucher,
                        'MAP': servicio,
                        'ESTADO': estado,
                        'BENEFICIO': paquete,
                        'SEDE': sede,
                        'OBSERVACIONES': observacion
                    }
                    
                    records.append(record)
                    
                    # Contar habitaciones y personas
                    if room_number in room_count:
                        room_count[room_number] += 1
                    else:
                        room_count[room_number] = 1
                    
                    people_count += 1
                    
                except IndexError:
                    print(f"⚠️  Fila {i} incompleta, omitida")
                    continue
    
    print(f"   Habitaciones que se ocupan: {len(room_count)}")
    print(f"   Cantidad de pax: {people_count}")
    print(f"   Registros procesados: {len(records)}")
    
    return records

def add_text_to_cell(cell, text):
    """Agrega texto a una celda"""
    p = P()
    p.addText(str(text))
    cell.appendChild(p)

def import_to_ods(records):
    """Importa los registros a la pestaña Ingresos"""
    print(f"\n📂 Abriendo {ODS_FILE}...")
    doc = load(ODS_FILE)
    
    # Buscar pestaña "Ingresos 23 D MAYO"
    tables = doc.spreadsheet.getElementsByType(Table)
    target_table = None
    
    for table in tables:
        if table.getAttribute("name") == SHEET_NAME:
            target_table = table
            break
    
    if not target_table:
        print(f"❌ No se encontró la pestaña '{SHEET_NAME}'")
        sys.exit(1)
    
    print(f"✅ Pestaña '{SHEET_NAME}' encontrada")
    
    # Verificar si tiene encabezados
    rows = target_table.getElementsByType(TableRow)
    has_headers = len(rows) > 0
    
    if not has_headers:
        print("   Agregando encabezados...")
        # Crear fila de encabezados
        header_row = TableRow()
        for header in HEADERS:
            cell = TableCell()
            add_text_to_cell(cell, header)
            header_row.appendChild(cell)
        target_table.appendChild(header_row)
    
    # Agregar datos
    print(f"   Importando {len(records)} registros...")
    for record in records:
        new_row = TableRow()
        
        for header in HEADERS:
            cell = TableCell()
            value = record.get(header, '')
            if value:
                add_text_to_cell(cell, value)
            new_row.appendChild(cell)
        
        target_table.appendChild(new_row)
    
    # Guardar (usar archivo temporal si el original está abierto)
    print(f"\n💾 Guardando {ODS_FILE}...")
    try:
        doc.save(ODS_FILE)
        print("✅ Datos importados exitosamente")
    except PermissionError:
        temp_file = f"TEMP_{ODS_FILE}"
        print(f"⚠️  Archivo bloqueado. Guardando como: {temp_file}")
        print("   CIERRA el archivo Excel/Calc y renombra el archivo TEMP a GRILLA_DE_PAX_2025.ods")
        doc.save(temp_file)
        print(f"✅ Datos guardados en {temp_file}")

def main():
    print("="*70)
    print("🏨 IMPORTACIÓN CSV → PESTAÑA 'Ingresos 23 D MAYO'")
    print("   Lógica basada en Reserva.html")
    print("="*70)
    
    if len(sys.argv) < 2:
        print(f"\n❌ Uso: python {sys.argv[0]} archivo.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    try:
        # 1. Crear respaldo
        create_backup()
        
        # 2. Leer CSV con lógica JS
        records = read_csv_with_js_logic(csv_file)
        
        # 3. Importar a ODS
        import_to_ods(records)
        
        print("\n" + "="*70)
        print("✅ IMPORTACIÓN COMPLETADA")
        print("="*70)
        
    except FileNotFoundError:
        print(f"\n❌ Archivo no encontrado: {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
