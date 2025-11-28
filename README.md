# SISTEMA DE GESTIÓN HOTELERA - HOTEL 23 DE MAYO
## Manual de Usuario - Automatización Completa

---

## 📋 ARCHIVOS DEL SISTEMA

### Archivos de Datos:
- `GRILLA_DE_PAX_2026.ods` - Planilla principal de trabajo
- `GRILLA_DE_PAX_RESPALDO_HISTORICO.ods` - Respaldo con histórico completo
- `test-data-map.csv` - Archivo de ejemplo para pruebas

### Scripts Python:
- ⭐ `importar_y_distribuir.py` - **SCRIPT PRINCIPAL** - Proceso completo automatizado
- `importar_ingresos.py` - Paso 1: Importa CSV a "Ingresos 23 D MAYO"
- `distribuir_a_pisos.py` - Paso 2: Distribuye datos a PISO 1, PISO 2, PISO 3
- `reducir_archivo.py` - Utilidad: Limpia datos de años anteriores

### Scripts de Verificación:
- `debug_ingresos.py` - Ver últimas filas importadas
- `verificar_distribucion.py` - Verificar datos en los pisos
- `ver_pestanas.py` - Listar todas las pestañas del ODS

---

## 🚀 USO DIARIO - IMPORTACIÓN AUTOMÁTICA

### ⭐ OPCIÓN RECOMENDADA: Proceso Completo

**Un solo comando hace todo el trabajo:**

```bash
python importar_y_distribuir.py reservas.csv
```

**Esto ejecuta automáticamente:**
1. ✅ Importa el CSV a "Ingresos 23 D MAYO"
2. ✅ Distribuye automáticamente a PISO 1, PISO 2, PISO 3
3. ✅ Crea respaldos de seguridad con timestamp

**Ejemplo real:**
```bash
# Exportaste reservas_diciembre_2025.csv de tu sistema hotelero
python importar_y_distribuir.py reservas_diciembre_2025.csv

# Resultado:
# ✅ 150 registros importados a Ingresos
# ✅ 150 registros distribuidos a los pisos
# ✅ Archivo actualizado: GRILLA_DE_PAX_2026.ods
```

### OPCIÓN ALTERNATIVA: Paso a Paso

Si necesitas más control:

**Paso 1 - Importar CSV:**
```bash
python importar_ingresos.py reservas.csv
```

**Paso 2 - Distribuir a pisos:**
```bash
python distribuir_a_pisos.py
```

---

## 📊 CÓMO FUNCIONA

### Mapeo Automático de Campos

Tu CSV exportado (28 columnas) → ODS (14 columnas esenciales)

| Campo Final | CSV Origen | Descripción |
|-------------|------------|-------------|
| **HAB** | Columna 2 | Nro. habitación (101, 225, 344...) |
| **IN** | Columna 8 | Fecha de ingreso (dd/mm/yyyy) |
| **OUT** | Columna 9 | Fecha de egreso (dd/mm/yyyy) |
| **PAX** | Columna 5 | Cantidad de plazas/personas |
| **ID** | Columna 11 | Tipo de documento (DNI, Pasaporte...) |
| **N.º** | Columna 12 | Número de documento |
| **NOMBRE** | Columna 13 | Apellido y Nombre completo |
| **EDAD** | Columna 14 | Edad del huésped |
| **VOUCHER** | Columna 6 | Número de voucher/reserva |
| **MAP** | Columna 16 | Régimen alimentario (MP, PC, AI...) |
| **ESTADO** | Columna 23 | Estado de la reserva (T, C, P...) |
| **BENEFICIO** | Columna 17 | Paquete/Promoción aplicada |
| **SEDE** | Columna 7 | Sede/Sucursal origen |
| **OBSERVACIONES** | Columna 4 | Observaciones especiales |

### Distribución Inteligente por Piso

El sistema detecta automáticamente el piso según el número de habitación:

| Piso | Rango de Habitaciones | Pestaña ODS |
|------|----------------------|-------------|
| **PISO 1** | 101 - 118 | "PISO 1" |
| **PISO 2** | 201 - 232 | "PISO 2" |
| **PISO 3** | 301 - 344 | "PISO 3" |

**Ejemplo:**
- Habitación 105 → Se actualiza en PISO 1
- Habitación 225 → Se actualiza en PISO 2  
- Habitación 344 → Se actualiza en PISO 3

---

## 🔐 SISTEMA DE RESPALDOS

### Respaldos Automáticos

Cada vez que ejecutas un script, se crea un respaldo automático:

```
BACKUP_20251127_143055_GRILLA_DE_PAX_2026.ods
       └─ Fecha y hora exacta del respaldo
```

### Restaurar desde Respaldo

Si algo sale mal:

```bash
# Ver backups disponibles
ls -lh BACKUP_*.ods

# Restaurar el más reciente
cp BACKUP_20251127_143055_GRILLA_DE_PAX_2026.ods GRILLA_DE_PAX_2026.ods
```

### Limpiar Respaldos Antiguos

```bash
# Eliminar todos los backups
rm BACKUP_*.ods

# O mantener solo los más recientes manualmente
```

---

## 🔧 MANTENIMIENTO

### Reducir Tamaño del Archivo

Cuando el archivo ODS crece mucho (más de 5 MB):

```bash
python reducir_archivo.py
```

**Qué hace:**
- Elimina registros anteriores a 2024
- Mantiene solo datos recientes
- Reduce significativamente el tamaño

**Resultado típico:**
```
Antes: 1.4 MB → Después: 0.7 MB (50% reducción)
```

---

## ✅ VERIFICACIÓN Y DIAGNÓSTICO

### Ver Últimas Importaciones

```bash
python debug_ingresos.py
```

Muestra las últimas 10 filas importadas con:
- HAB, IN, OUT, NOMBRE

### Verificar Distribución a Pisos

```bash
python verificar_distribucion.py
```

Verifica que las habitaciones de prueba (101, 225, 344) tengan datos correctos en sus pisos.

### Listar Todas las Pestañas

```bash
python ver_pestanas.py
```

---

## ⚠️ CASOS ESPECIALES

### Habitaciones con Múltiples Huéspedes

Si una habitación tiene 3 personas:
- El CSV tendrá 3 filas con el mismo número de habitación
- Se importan las 3 filas a "Ingresos 23 D MAYO"
- En los pisos se actualiza con el **PRIMER** registro encontrado

### Habitaciones Fuera de Rango

Si importas una habitación 150 (fuera del rango 101-118):
- Se importa correctamente a "Ingresos"
- NO se distribuye a ningún piso (queda solo en Ingresos)

### CSV con Formato Diferente

Si tu CSV no tiene exactamente 28 columnas:
- Edita `importar_ingresos.py`
- Ajusta los índices en la sección de mapeo
- Consulta con el desarrollador si necesitas ayuda

---

## 📝 EJEMPLO COMPLETO PASO A PASO

### Escenario: Recibiste 50 reservas nuevas

**1. Exportar desde tu sistema hotelero**
```
Archivo generado: reservas_semana_12.csv
```

**2. Ejecutar importación automática**
```bash
cd /ruta/a/recepcion2026
python importar_y_distribuir.py reservas_semana_12.csv
```

**3. Ver resultado en pantalla**
```
🚀 PROCESO AUTOMÁTICO COMPLETO - HOTEL 23 DE MAYO 🚀

Archivo CSV: reservas_semana_12.csv

PASOS:
  1️⃣  Importar CSV → Ingresos_23_D_MAYO
  2️⃣  Distribuir datos → PISO_1, PISO_2, PISO_3

✅ Datos importados: 50 registros
✅ Datos distribuidos: 50 registros
   PISO_1: 15 registros
   PISO_2: 28 registros
   PISO_3: 7 registros

📊 Archivo actualizado: GRILLA_DE_PAX_2026.ods
💾 Respaldos automáticos creados
```

**4. Abrir LibreOffice Calc**
```
Abrir: GRILLA_DE_PAX_2026.ods

Verificar:
- Pestaña "Ingresos 23 D MAYO": últimas 50 filas
- Pestaña "PISO 1": habitaciones 101-118 actualizadas
- Pestaña "PISO 2": habitaciones 201-232 actualizadas
- Pestaña "PISO 3": habitaciones 301-344 actualizadas
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### ERROR: "No se encontró la pestaña"

**Causa:** Nombres incorrectos de pestañas o archivo

**Solución:**
```bash
# Verificar nombres de pestañas
python ver_pestanas.py

# Deben ser exactamente:
# - "Ingresos 23 D MAYO" (con espacios)
# - "PISO 1" (con espacio)
# - "PISO 2" (con espacio)
# - "PISO 3" (con espacio)
```

### ERROR: "FileNotFoundError"

**Causa:** El archivo ODS no está en la carpeta correcta

**Solución:**
```bash
# Verificar que estás en la carpeta correcta
pwd
# Debe mostrar: .../recepcion2026

# Verificar que existe el archivo
ls GRILLA_DE_PAX_2026.ods
```

### Los datos no aparecen en los pisos

**Causa:** Números de habitación fuera de rango

**Solución:**
```bash
# Verificar qué habitaciones se importaron
python debug_ingresos.py

# Las habitaciones deben estar en:
# 101-118, 201-232, 301-344
```

### El proceso es muy lento

**Causa:** Archivo ODS muy grande (muchos datos históricos)

**Solución:**
```bash
# Reducir tamaño eliminando datos antiguos
python reducir_archivo.py
```

---

## 💻 REQUISITOS TÉCNICOS

### Software Necesario:
- Python 3.10 o superior
- Librerías instaladas: `odfpy`, `pandas`, `openpyxl`

### Instalación de Librerías (si es necesario):
```bash
pip install odfpy pandas openpyxl
```

### Sistema Operativo:
- ✅ Linux/Ubuntu (probado)
- ✅ Windows con WSL
- ✅ macOS (compatible)

---

## 📞 CONTACTO Y SOPORTE

Para problemas técnicos o mejoras:
- Revisar los scripts en la carpeta `recepcion2026`
- Consultar este manual
- Verificar que las pestañas tengan los nombres correctos

---

## 🎯 RESUMEN RÁPIDO

| Tarea | Comando |
|-------|---------|
| **Importar y distribuir (completo)** | `python importar_y_distribuir.py archivo.csv` |
| Solo importar | `python importar_ingresos.py archivo.csv` |
| Solo distribuir | `python distribuir_a_pisos.py` |
| Verificar importación | `python debug_ingresos.py` |
| Verificar distribución | `python verificar_distribucion.py` |
| Reducir tamaño archivo | `python reducir_archivo.py` |
| Ver pestañas | `python ver_pestanas.py` |
| Eliminar backups | `rm BACKUP_*.ods` |

---

**Última actualización:** 27 de Noviembre de 2025  
**Versión del sistema:** 2.0 - Automatización Completa
