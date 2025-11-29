# Sistema de Gestión de Reservas - Hotel 23 de Mayo

Sistema automatizado para importar y distribuir reservas hoteleras en grilla de ocupación por pisos.

## 📋 Descripción

Este proyecto procesa archivos CSV exportados desde el sistema hotelero y:
1. **Importa** todas las reservas a la hoja "Ingresos 23 D MAYO"
2. **Distribuye** automáticamente los pasajeros a las grillas de cada piso
3. **Actualiza** estadísticas en tiempo real (pasajeros, reservas, MAP)

## 🏨 Estructura del Hotel

### PISO 1 (21 habitaciones)
**Rango:** 101 - 121

| Habitación | Tipo | Plazas |
|------------|------|--------|
| 101 | DOBLE INDIVIDUALES | 2 |
| 102 | DOBLE INDIVIDUALES | 2 |
| 103 | DOBLE INDIVIDUALES | 2 |
| 104 | DOBLE INDIVIDUALES | 2 |
| 105 | DOBLE INDIVIDUALES | 2 |
| 106 | DOBLE INDIVIDUALES | 2 |
| 107 | DOBLE INDIVIDUALES | 2 |
| 108 | DOBLE INDIVIDUALES | 2 |
| 109 | DOBLE INDIVIDUALES | 2 |
| 110 | DOBLE INDIVIDUALES | 2 |
| 111 | DOBLE INDIVIDUALES | 2 |
| 112 | DOBLE INDIVIDUALES | 2 |
| 113 | DOBLE INDIVIDUALES | 2 |
| 114 | DOBLE INDIVIDUALES | 2 |
| 115 | TRIPLE | 3 |
| 116 | TRIPLE | 3 |
| 117 | TRIPLE | 3 |
| 118 | TRIPLE | 3 |
| 119 | TRIPLE | 3 |
| 120 | DOBLE INDIVIDUALES | 2 |
| 121 | DOBLE INDIVIDUALES | 2 |

**Capacidad total PISO 1:** 45 plazas

### PISO 2 (21 habitaciones)
**Rango:** 222 - 242

| Habitación | Tipo | Plazas |
|------------|------|--------|
| 222 | DOBLE INDIVIDUALES | 2 |
| 223 | DOBLE INDIVIDUALES | 2 |
| 224 | DOBLE INDIVIDUALES | 2 |
| 225 | DOBLE INDIVIDUALES | 2 |
| 226 | DOBLE INDIVIDUALES | 2 |
| 227 | TRIPLE | 3 |
| 228 | TRIPLE | 3 |
| 229 | TRIPLE | 3 |
| 230 | TRIPLE | 3 |
| 231 | TRIPLE | 3 |
| 232 | TRIPLE | 3 |
| 233 | TRIPLE | 3 |
| 234 | TRIPLE | 3 |
| 235 | TRIPLE | 3 |
| 236 | TRIPLE | 3 |
| 237 | TRIPLE | 3 |
| 238 | DOBLE INDIVIDUALES | 2 |
| 239 | DOBLE INDIVIDUALES | 2 |
| 240 | CUADRUPLE | 4 |
| 241 | DOBLE INDIVIDUALES | 2 |
| 242 | DOBLE INDIVIDUALES | 2 |

**Capacidad total PISO 2:** 55 plazas

### PISO 3 (11 habitaciones)
**Rango:** 343 - 353

| Habitación | Tipo | Plazas |
|------------|------|--------|
| 343 | TRIPLE | 3 |
| 344 | TRIPLE | 3 |
| 345 | TRIPLE | 3 |
| 346 | TRIPLE | 3 |
| 347 | TRIPLE | 3 |
| 348 | TRIPLE | 3 |
| 349 | TRIPLE | 3 |
| 350 | TRIPLE | 3 |
| 351 | TRIPLE | 3 |
| 352 | TRIPLE | 3 |
| 353 | TRIPLE | 3 |

**Capacidad total PISO 3:** 33 plazas

---

**CAPACIDAD TOTAL HOTEL:** 53 habitaciones | 133 plazas

## 🚀 Uso

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/xpablodaniel/recepcion2026.git
cd recepcion2026

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install openpyxl  # Para Excel
pip install odfpy     # Para ODS (LibreOffice)
```

### Procesar Reservas

**Para Excel (.xlsx) - Casa:**
```bash
python procesar_reservas.py archivo.csv
```

**Para ODS (LibreOffice) - Trabajo:**
```bash
python procesar_reservas_ods.py archivo.csv
```

**Ejemplo:**
```bash
# En casa con Excel
python procesar_reservas.py consultaRegimenReport.csv

# En el trabajo con LibreOffice
python procesar_reservas_ods.py consultaRegimenReport.csv
```

### Formato del CSV

El archivo CSV debe contener las siguientes columnas del sistema hotelero:

- `Nro. habitación`
- `Fecha de ingreso`
- `Fecha de egreso`
- `Cantidad plazas`
- `Tipo documento`
- `Nro. doc.`
- `Apellido y nombre`
- `Edad`
- `Voucher`
- `Servicios` (MAP/Comida)
- `Estado`
- `Paquete`
- `Sede`

## 📊 Características

✅ **Importación automática** a hoja "Ingresos 23 D MAYO"
✅ **Distribución inteligente** por piso según número de habitación
✅ **Grupos familiares completos** en filas consecutivas
✅ **Histórico acumulativo** (no sobreescribe datos existentes)
✅ **Estadísticas automáticas** en celdas H277:H279:
   - H277: Total pasajeros
   - H278: Total reservas (habitaciones)
   - H279: Total MAP (Media Pensión)
✅ **Respaldo automático** antes de cada proceso
✅ **Resumen detallado** en consola

## 📁 Archivos

**Scripts:**
- `procesar_reservas.py` - Script para Excel (.xlsx) - **Usar en casa**
- `procesar_reservas_ods.py` - Script para LibreOffice (.ods) - **Usar en trabajo**

**Archivos de datos:**
- `Grilla de Pax 2030.xlsx` - Archivo Excel de trabajo (casa)
- `Grilla de Pax 2030.ods` - Archivo ODS de trabajo (trabajo)
- `GRILLA_DE_PAX_RESPALDO_HISTORICO.ods` - Respaldo histórico completo
- `test-data-map.csv` - Datos de prueba (15 registros, 7 habitaciones)

**Documentación:**
- `README.md` - Esta documentación

## 🔄 Flujo de Trabajo Diario

**En casa (Windows + Excel):**
1. Exportar CSV desde sistema hotelero
2. Ejecutar: `python procesar_reservas.py nombre_archivo.csv`
3. Verificar salida en consola
4. Abrir `Grilla de Pax 2030.xlsx` para revisar
5. Las nuevas reservas se agregan debajo de las existentes

**En el trabajo (Linux + LibreOffice):**
1. Exportar CSV desde sistema hotelero
2. Ejecutar: `python procesar_reservas_ods.py nombre_archivo.csv`
3. Verificar salida en consola
4. Abrir `Grilla de Pax 2030.ods` para revisar
5. Las nuevas reservas se agregan debajo de las existentes

## ⚙️ Requisitos Técnicos

**Para Excel (casa):**
- Python 3.10+
- openpyxl 3.1.5+
- Microsoft Excel

**Para ODS (trabajo):**
- Python 3.10+
- odfpy 1.4.1+
- LibreOffice Calc

## 📝 Notas Importantes

- **Formato Excel (.xlsx)**: Se utiliza Excel en lugar de ODS por problemas de compatibilidad
- **Columna C**: Los datos en las grillas de PISO empiezan en columna C (IN/fecha ingreso)
- **Columna B**: Contiene el número de habitación (no se modifica)
- **Filas consecutivas**: Cada pax de una habitación ocupa una fila diferente
- **Respaldos**: Se crean automáticamente con formato `BACKUP_YYYYMMDD_HHMMSS_*.xlsx`

## 🏗️ Historial del Proyecto

### Problemas Resueltos

1. **Archivo ODS corrupto**: El archivo original GRILLA_DE_PAX_2026.ods no podía abrirse en Excel
   - **Solución**: Migración completa a formato .xlsx con openpyxl

2. **Importación y distribución separadas**: Proceso en dos pasos era ineficiente
   - **Solución**: Script unificado `procesar_reservas.py`

3. **Solo primer pax por habitación**: No se distribuían familias completas
   - **Solución**: Distribución de todos los pax en filas consecutivas

4. **Sin estadísticas**: No había resumen automático
   - **Solución**: Actualización automática de celdas H277:H279

### Versión Actual: 2.0

- ✅ Proceso unificado (importar + distribuir)
- ✅ Soporte completo para grupos familiares
- ✅ Estadísticas automáticas
- ✅ Histórico acumulativo
- ✅ Formato Excel nativo (.xlsx)

## 👨‍💻 Autor

**Pablo Daniel**
- GitHub: [@xpablodaniel](https://github.com/xpablodaniel)
- Proyecto: Hotel 23 de Mayo - Sistema de Recepción 2026

## 📄 Licencia

Este proyecto es de uso interno para el Hotel 23 de Mayo.
