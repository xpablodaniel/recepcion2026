#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FLUJO COMPLETO DE AUTOMATIZACIÓN
================================
1. Importa CSV → Ingresos_23_D_MAYO
2. Distribuye automáticamente → PISO_1, PISO_2, PISO_3

Uso: python importar_y_distribuir.py archivo.csv
"""

import sys
import subprocess
from pathlib import Path

def run_script(script_name, args=[]):
    """Ejecuta un script Python y retorna si fue exitoso"""
    cmd = [sys.executable, script_name] + args
    print(f"\n{'='*60}")
    print(f"Ejecutando: {' '.join(cmd)}")
    print('='*60)
    
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def main():
    if len(sys.argv) < 2:
        print("❌ ERROR: Falta el archivo CSV")
        print("\nUso:")
        print("  python importar_y_distribuir.py archivo.csv")
        print("\nEjemplo:")
        print("  python importar_y_distribuir.py test-data-map.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    if not Path(csv_file).exists():
        print(f"❌ ERROR: No se encuentra el archivo {csv_file}")
        sys.exit(1)
    
    print("\n" + "🚀 " * 30)
    print("  PROCESO AUTOMÁTICO COMPLETO - HOTEL 23 DE MAYO")
    print("🚀 " * 30)
    print(f"\nArchivo CSV: {csv_file}")
    print("\nPASOS:")
    print("  1️⃣  Importar CSV → Ingresos_23_D_MAYO")
    print("  2️⃣  Distribuir datos → PISO_1, PISO_2, PISO_3")
    print()
    
    # Paso 1: Importar CSV
    print("\n" + "🔵 PASO 1: IMPORTACIÓN ".ljust(60, '='))
    if not run_script("importar_ingresos.py", [csv_file]):
        print("\n❌ FALLO en la importación. Proceso detenido.")
        sys.exit(1)
    
    print("\n✅ Importación completada")
    
    # Paso 2: Distribuir a pisos
    print("\n" + "🔵 PASO 2: DISTRIBUCIÓN ".ljust(60, '='))
    if not run_script("distribuir_a_pisos.py"):
        print("\n⚠️  ADVERTENCIA: La distribución falló")
        print("   Los datos fueron importados correctamente a Ingresos_23_D_MAYO")
        print("   Pero NO se distribuyeron a los pisos automáticamente")
        print("\n💡 Puedes distribuirlos manualmente o revisar el error")
        sys.exit(1)
    
    print("\n✅ Distribución completada")
    
    # Resumen final
    print("\n" + "🎉 " * 30)
    print("  PROCESO COMPLETADO EXITOSAMENTE")
    print("🎉 " * 30)
    print("\n✅ Datos importados a: Ingresos_23_D_MAYO")
    print("✅ Datos distribuidos a: PISO_1, PISO_2, PISO_3")
    print(f"\n📊 Archivo actualizado: GRILLA_DE_PAX_2026.ods")
    print("💾 Respaldos automáticos creados con timestamp")
    print()

if __name__ == "__main__":
    main()
