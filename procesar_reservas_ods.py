#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador unificado de reservas para ODS (LibreOffice)
Importa datos del CSV a la hoja Ingresos Y los distribuye a los pisos en un solo paso
"""

from odf import opendocument, table, text, style
from odf.opendocument import load
import csv
import sys
import shutil
from datetime import datetime
from pathlib import Path
from collections import defaultdict

ODS_FILE = "Grilla de Pax 2030.ods"

# Mapeo de habitaciones a pisos
PISO_RANGES = {
    'PISO_1': (101, 121),
    'PISO_2': (222, 242),
    'PISO_3': (343, 353)
}

PISO_SHEET_NAMES = {
    'PISO_1': 'PISO 1',
    'PISO_2': 'PISO 2',
    'PISO_3': 'PISO 3'
}

def create_backup():
    """Crea respaldo con timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"BACKUP_{timestamp}_{ODS_FILE}"
    shutil.copy2(ODS_FILE, backup_file)
    print(f"✅ Respaldo: {backup_file}")
    return backup_file

def get_piso_for_room(room_number):
    """Determina a qué piso pertenece una habitación"""
    try:
        room_num = int(str(room_number).strip())
        for piso, (min_room, max_room) in PISO_RANGES.items():
            if min_room <= room_num <= max_room:
                return piso
    except (ValueError, TypeError):
        pass
    return None

def get_cell_value(cell):
    """Obtiene el valor de una celda ODS"""
    try:
        # Intentar obtener el valor directamente
        value = cell.getAttribute('value')
        if value:
            return value
        
        # Si no tiene atributo value, buscar en el texto
        paragraphs = cell.getElementsByType(text.P)
        if paragraphs:
            content = []
            for p in paragraphs:
                content.append(str(p))
            return ''.join(content) if content else None
        return None
    except:
        return None

def set_cell_value(cell, value):
    """Establece el valor de una celda ODS"""
    if cell is None:
        return
    
    # Limpiar contenido anterior
    for element in cell.childNodes[:]:
        cell.removeChild(element)
    
    # Agregar nuevo valor
    if value is not None:
        p = text.P()
        p.addText(str(value))
        cell.addElement(p)

def get_sheet_by_name(doc, sheet_name):
    """Obtiene una hoja por nombre"""
    sheets = doc.spreadsheet.getElementsByType(table.Table)
    for sheet in sheets:
        if sheet.getAttribute('name') == sheet_name:
            return sheet
    return None

def get_row_count(sheet):
    """Cuenta las filas de una hoja"""
    rows = sheet.getElementsByType(table.TableRow)
    return len(rows)

def get_cell(sheet, row_idx, col_idx):
    """Obtiene una celda específica (índices basados en 0)"""
    rows = sheet.getElementsByType(table.TableRow)
    if row_idx < len(rows):
        row = rows[row_idx]
        cells = row.getElementsByType(table.TableCell)
        if col_idx < len(cells):
            return cells[col_idx]
    return None

def read_csv_data(csv_file):
    """Lee datos del CSV y los organiza por habitación"""
    print(f"\n📄 Procesando CSV: {csv_file}")
    
    registros = []
    habitaciones = set()
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            hab = row.get('Nro. habitación', '').strip()
            
            if not hab:
                continue
            
            habitaciones.add(hab)
            
            # Estructura según columnas de Ingresos
            registro = {
                'HAB': hab,
                'IN': row.get('Fecha de ingreso', ''),
                'OUT': row.get('Fecha de egreso', ''),
                'PAX': row.get('Cantidad plazas', ''),
                'ID': row.get('Tipo documento', ''),
                'N.º': row.get('Nro. doc.', ''),
                'NOMBRE': row.get('Apellido y nombre', ''),
                'EDAD': row.get('Edad', ''),
                'VOUCHER': row.get('Voucher', ''),
                'MAP': row.get('Servicios', ''),
                'ESTADO': row.get('Estado', ''),
                'BENEFICIO': row.get('Paquete', ''),
                'SEDE': row.get('Sede', ''),
                'OBSERVACIONES': ''
            }
            
            registros.append(registro)
    
    print(f"   Habitaciones que se ocupan: {len(habitaciones)}")
    print(f"   Cantidad de pax: {len(registros)}")
    print(f"   Registros procesados: {len(registros)}")
    
    return registros

def agrupar_por_habitacion(registros):
    """Agrupa registros por habitación para distribuir a pisos"""
    habitaciones_map = defaultdict(list)
    
    for registro in registros:
        hab = registro['HAB']
        habitaciones_map[hab].append(registro)
    
    # Organizar por piso
    distribuidos = {}
    for hab, regs in habitaciones_map.items():
        piso = get_piso_for_room(hab)
        if piso:
            if piso not in distribuidos:
                distribuidos[piso] = []
            distribuidos[piso].append({
                'room': hab,
                'pax_list': regs
            })
    
    return distribuidos

def procesar_reservas(csv_file):
    """Proceso unificado: importa a Ingresos y distribuye a pisos"""
    
    if not Path(csv_file).exists():
        print(f"❌ ERROR: No se encuentra el archivo {csv_file}")
        return False
    
    if not Path(ODS_FILE).exists():
        print(f"❌ ERROR: No se encuentra el archivo {ODS_FILE}")
        return False
    
    print("="*70)
    print("  PROCESADOR UNIFICADO DE RESERVAS (ODS)")
    print("  1. Importar reservas a hoja Ingresos")
    print("  2. Distribuir reservas a grilla (PISO 1/2/3)")
    print("="*70)
    
    # Crear respaldo
    create_backup()
    
    # Leer datos del CSV
    registros = read_csv_data(csv_file)
    
    if not registros:
        print("❌ No hay registros para procesar")
        return False
    
    # Abrir ODS
    print(f"\n📂 Abriendo {ODS_FILE}...")
    doc = load(ODS_FILE)
    
    # ========== PASO 1: IMPORTAR A INGRESOS ==========
    print("\n📥 PASO 1: Importando a hoja Ingresos...")
    
    # Buscar hoja Ingresos (con espacios o guiones bajos)
    sheet_ingresos = get_sheet_by_name(doc, 'Ingresos 23 D MAYO')
    if not sheet_ingresos:
        sheet_ingresos = get_sheet_by_name(doc, 'Ingresos_23_D_MAYO')
    
    if not sheet_ingresos:
        print("❌ ERROR: Hoja 'Ingresos 23 D MAYO' no encontrada")
        print("   Hojas disponibles:")
        sheets = doc.spreadsheet.getElementsByType(table.Table)
        for s in sheets:
            print(f"      - {s.getAttribute('name')}")
        return False
    
    # Encontrar primera fila vacía (empezando desde fila 1, índice 1)
    rows = sheet_ingresos.getElementsByType(table.TableRow)
    start_row = 1  # Fila 2 en términos de usuario (índice 1)
    
    # Buscar primera fila vacía
    for idx in range(1, len(rows)):
        cell = get_cell(sheet_ingresos, idx, 0)  # Columna A
        if cell and not get_cell_value(cell):
            start_row = idx
            break
    
    print(f"   Importando {len(registros)} registros a partir de la fila {start_row + 1}...")
    
    # Importar registros
    for idx, registro in enumerate(registros):
        row_idx = start_row + idx
        
        # Asegurarse de que la fila existe
        while row_idx >= len(rows):
            new_row = table.TableRow()
            for _ in range(14):  # 14 columnas
                new_row.addElement(table.TableCell())
            sheet_ingresos.addElement(new_row)
            rows = sheet_ingresos.getElementsByType(table.TableRow)
        
        # Columnas: HAB, IN, OUT, PAX, ID, N.º, NOMBRE, EDAD, VOUCHER, MAP, ESTADO, BENEFICIO, SEDE, OBSERVACIONES
        set_cell_value(get_cell(sheet_ingresos, row_idx, 0), registro['HAB'])
        set_cell_value(get_cell(sheet_ingresos, row_idx, 1), registro['IN'])
        set_cell_value(get_cell(sheet_ingresos, row_idx, 2), registro['OUT'])
        set_cell_value(get_cell(sheet_ingresos, row_idx, 3), registro['PAX'])
        set_cell_value(get_cell(sheet_ingresos, row_idx, 4), registro['ID'])
        set_cell_value(get_cell(sheet_ingresos, row_idx, 5), registro['N.º'])
        set_cell_value(get_cell(sheet_ingresos, row_idx, 6), registro['NOMBRE'])
        set_cell_value(get_cell(sheet_ingresos, row_idx, 7), registro['EDAD'])
        set_cell_value(get_cell(sheet_ingresos, row_idx, 8), registro['VOUCHER'])
        set_cell_value(get_cell(sheet_ingresos, row_idx, 9), registro['MAP'])
        set_cell_value(get_cell(sheet_ingresos, row_idx, 10), registro['ESTADO'])
        set_cell_value(get_cell(sheet_ingresos, row_idx, 11), registro['BENEFICIO'])
        set_cell_value(get_cell(sheet_ingresos, row_idx, 12), registro['SEDE'])
        set_cell_value(get_cell(sheet_ingresos, row_idx, 13), registro['OBSERVACIONES'])
    
    print(f"   ✓ {len(registros)} registros importados (filas {start_row + 1}-{start_row + len(registros)})")
    
    # ========== ACTUALIZAR RESUMEN EN H277:H279 ==========
    print("\n📋 Actualizando resumen estadístico...")
    
    habitaciones_unicas = set()
    total_pax = 0
    total_map = 0
    
    for registro in registros:
        habitaciones_unicas.add(registro['HAB'])
        total_pax += 1
        if 'comida' in str(registro['MAP']).lower() or 'pensión' in str(registro['MAP']).lower():
            total_map += 1
    
    cant_habitaciones = len(habitaciones_unicas)
    
    # Actualizar celdas H277:H279 (índices 276-278, columna 7)
    set_cell_value(get_cell(sheet_ingresos, 276, 7), str(total_pax))
    set_cell_value(get_cell(sheet_ingresos, 277, 7), str(cant_habitaciones))
    set_cell_value(get_cell(sheet_ingresos, 278, 7), str(total_map))
    
    print(f"   ✓ Resumen actualizado en H277:H279")
    print(f"      • Pasajeros: {total_pax}")
    print(f"      • Reservas: {cant_habitaciones}")
    print(f"      • MAP: {total_map}")
    
    # ========== PASO 2: DISTRIBUIR A PISOS ==========
    print("\n📊 PASO 2: Distribuyendo a grilla de pisos...")
    
    distribuidos = agrupar_por_habitacion(registros)
    
    print("\n   Distribución por piso:")
    for piso, records in distribuidos.items():
        print(f"      {piso}: {len(records)} habitaciones")
    
    actualizaciones_exitosas = 0
    
    for piso_interno, records in distribuidos.items():
        sheet_name = PISO_SHEET_NAMES[piso_interno]
        
        # Buscar hoja con espacios o guiones bajos
        sheet_piso = get_sheet_by_name(doc, sheet_name)
        if not sheet_piso:
            sheet_name_alt = sheet_name.replace(' ', '_')
            sheet_piso = get_sheet_by_name(doc, sheet_name_alt)
        
        if not sheet_piso:
            print(f"   ⚠️  Hoja {sheet_name} no encontrada")
            continue
        
        print(f"\n   Procesando {sheet_name}...")
        piso_rows = sheet_piso.getElementsByType(table.TableRow)
        
        for record in records:
            room_number = record['room']
            pax_list = record['pax_list']
            
            # Buscar habitación en columna B (índice 1)
            encontrado = False
            for row_idx in range(1, len(piso_rows)):
                cell = get_cell(sheet_piso, row_idx, 1)  # Columna B
                if cell:
                    hab_value = get_cell_value(cell)
                    if str(hab_value).strip() == str(room_number).strip():
                        encontrado = True
                        
                        print(f"      HAB {room_number} encontrada (fila {row_idx + 1}) - {len(pax_list)} pax")
                        
                        current_row = row_idx
                        for idx, data in enumerate(pax_list):
                            # Actualizar desde columna C (índice 2)
                            set_cell_value(get_cell(sheet_piso, current_row, 2), data['IN'])
                            set_cell_value(get_cell(sheet_piso, current_row, 3), data['OUT'])
                            set_cell_value(get_cell(sheet_piso, current_row, 4), data['PAX'])
                            set_cell_value(get_cell(sheet_piso, current_row, 5), data['ID'])
                            set_cell_value(get_cell(sheet_piso, current_row, 6), data['N.º'])
                            set_cell_value(get_cell(sheet_piso, current_row, 7), data['NOMBRE'])
                            set_cell_value(get_cell(sheet_piso, current_row, 8), data['EDAD'])
                            set_cell_value(get_cell(sheet_piso, current_row, 9), data['VOUCHER'])
                            set_cell_value(get_cell(sheet_piso, current_row, 10), data['MAP'])
                            set_cell_value(get_cell(sheet_piso, current_row, 11), data['ESTADO'])
                            
                            print(f"         ✓ Pax {idx+1}/{len(pax_list)}: {data['NOMBRE']} (fila {current_row + 1})")
                            actualizaciones_exitosas += 1
                            current_row += 1
                        
                        break
            
            if not encontrado:
                print(f"      ⚠️  HAB {room_number} NO encontrada en {sheet_name}")
    
    # Guardar
    print(f"\n📊 Resumen:")
    print(f"   • Registros en Ingresos: {len(registros)}")
    print(f"   • Pax distribuidos en pisos: {actualizaciones_exitosas}")
    
    print("\n💾 Guardando cambios...")
    
    try:
        doc.save(ODS_FILE)
        print(f"✅ Archivo guardado: {ODS_FILE}")
        
        print("\n" + "="*70)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("="*70)
        print(f"   ✓ Importación a Ingresos: {len(registros)} registros")
        print(f"   ✓ Distribución a pisos: {actualizaciones_exitosas} pax en grilla")
        print(f"   ✓ Archivo: {ODS_FILE}")
        print("="*70)
        
        return True
    except Exception as e:
        print(f"❌ ERROR al guardar: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("❌ ERROR: Falta el archivo CSV")
        print("\nUso:")
        print("  python procesar_reservas_ods.py archivo.csv")
        print("\nEjemplo:")
        print("  python procesar_reservas_ods.py consultaRegimenReport.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    success = procesar_reservas(csv_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
