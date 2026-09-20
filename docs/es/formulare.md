# Referencia de formularios

Esta referencia enumera todos los campos de las acciones financieras y de calendario disponibles. Abre el área, elige la operación y completa los campos. Revisa antes de guardar/confirmar y después recarga. Crea primero los registros relacionados para rellenar los selectores vacíos. Las capturas muestran formularios reales con datos de prueba, no una validación contable.

[Volver al manual](handbook.md) · [Screenshots](../images/pilot/README.md)

## Finanzas

### Crear cuenta

`finance` · `account.create`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Titular (persona u organización) | Selección | Obligatorio |
| Organización | Selección | Obligatorio |

![Crear cuenta (DE)](../images/pilot/desktop/finance-operation-00.png)

### Registrar deuda

`finance` · `receivable.create`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Cuenta | Selección | Obligatorio |
| Importe | Importe en la moneda de la organización | Obligatorio |
| Fecha contable | Fecha | Obligatorio |
| Vencimiento | Fecha | Obligatorio |
| Descripción / concepto | Texto | Obligatorio |

![Registrar deuda (DE)](../images/pilot/desktop/finance-operation-01.png)

### Registrar pago

`finance` · `payment.create`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Cuenta | Selección | Obligatorio |
| Importe | Importe en la moneda de la organización | Obligatorio |
| Fecha contable | Fecha | Obligatorio |
| Descripción / concepto | Texto | Obligatorio |
| Referencia de pago | Texto | Obligatorio |

![Registrar pago (DE)](../images/pilot/desktop/finance-operation-02.png)

### Asignar pago

`finance` · `allocation.create`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Pago | Selección | Obligatorio |
| Deuda | Selección | Obligatorio |
| Importe | Importe en la moneda de la organización | Obligatorio |

![Asignar pago (DE)](../images/pilot/desktop/finance-operation-03.png)

### Anular asiento

`finance` · `entry.reverse`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Asiento | Selección | Obligatorio |
| Fecha contable | Fecha | Obligatorio |
| Descripción / concepto | Texto | Obligatorio |

![Anular asiento (DE)](../images/pilot/desktop/finance-operation-04.png)

### Crear plan de cuotas

`contributions` · `plan.create`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Organización | Selección | Obligatorio |
| Nombre | Texto | Obligatorio |
| Importe | Importe en la moneda de la organización | Obligatorio |
| Intervalo (1, 3, 6 o 12 meses) | Entero | Obligatorio |
| Válido desde | Fecha | Obligatorio |
| Válido hasta | Fecha | Obligatorio |
| Día de vencimiento (1–31) | Entero | Obligatorio |

![Crear plan de cuotas (DE)](../images/pilot/desktop/finance-operation-05.png)

### Asignar cuota

`contributions` · `assignment.create`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Afiliaciones | Selección | Obligatorio |
| Plan de cuotas | Selección | Obligatorio |
| Cuenta | Selección | Obligatorio |
| Válido desde | Fecha | Obligatorio |
| Válido hasta | Fecha | Obligatorio |
| Importe personalizado | Importe en la moneda de la organización | Opcional |
| Descuento (100 = 1 %, 10000 = 100 %) | Entero | Obligatorio |

![Asignar cuota (DE)](../images/pilot/desktop/finance-operation-06.png)

### Finalizar asignación de cuota

`contributions` · `assignment.end`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Asignación de cuota | Selección | Obligatorio |
| Válido hasta | Fecha | Obligatorio |

![Finalizar asignación de cuota (DE)](../images/pilot/desktop/finance-operation-07.png)

### Facturar cuotas

`contributions` · `contributions.bill`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Asignación de cuota | Selección | Obligatorio |
| Facturar hasta (inclusive) | Fecha | Obligatorio |

![Facturar cuotas (DE)](../images/pilot/desktop/finance-operation-08.png)

### Registrar reclamación

`contributions` · `reminder.create`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Deuda | Selección | Obligatorio |
| Fecha de reclamación | Fecha | Obligatorio |
| Plazo de pago | Fecha | Obligatorio |
| Cargo | Importe en la moneda de la organización | Obligatorio |
| Descripción / concepto | Texto | Obligatorio |

![Registrar reclamación (DE)](../images/pilot/desktop/finance-operation-09.png)

### Crear producto

`purchases` · `product.create`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Organización | Selección | Obligatorio |
| Nombre | Texto | Obligatorio |
| Descripción / concepto | Texto | Obligatorio |
| Precio | Importe en la moneda de la organización | Obligatorio |

![Crear producto (DE)](../images/pilot/desktop/finance-operation-10.png)

### Modificar producto

`purchases` · `product.update`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Producto | Selección | Obligatorio |
| Revisión del producto | Entero | Obligatorio |
| Nombre | Texto | Obligatorio |
| Descripción / concepto | Texto | Obligatorio |
| Precio | Importe en la moneda de la organización | Obligatorio |
| Activo | Sí/No | Obligatorio |

![Modificar producto (DE)](../images/pilot/desktop/finance-operation-11.png)

### Registrar compra

`purchases` · `purchase.post`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Cuenta | Selección | Obligatorio |
| Fecha contable | Fecha | Obligatorio |
| Vencimiento | Fecha | Obligatorio |
| Descripción / concepto | Texto | Obligatorio |

Líneas de compra: Producto · Cantidad · Añadir línea / Eliminar línea.

![Registrar compra (DE)](../images/pilot/desktop/finance-operation-12.png)

### Registrar devolución

`purchases` · `purchase.return`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Línea de compra | Selección | Obligatorio |
| Cantidad | Entero | Obligatorio |
| Fecha contable | Fecha | Obligatorio |
| Descripción / concepto | Texto | Obligatorio |

![Registrar devolución (DE)](../images/pilot/desktop/finance-operation-13.png)

## Calendario y eventos

### Crear entrada de calendario

`calendar` · `create`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Título | Texto | Obligatorio |
| Descripción / concepto | Texto | Obligatorio |
| Lugar | Texto | Obligatorio |
| Persona u organización asignada | Selección | Obligatorio |
| Inicio | Fecha y hora | Obligatorio |
| Fin | Fecha y hora | Obligatorio |
| Zona horaria | Texto | Obligatorio |
| Todo el día | Sí/No | Obligatorio |
| Hora repetida en el cambio horario | earlier, later | Obligatorio |
| Repetición | none, DAILY, WEEKLY, MONTHLY | Obligatorio |
| Intervalo de repetición | Entero | Obligatorio |
| Número de fechas (máximo 366) | Entero | Obligatorio |

### Cancelar fecha de calendario

`calendar` · `cancel`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Fecha | Selección | Obligatorio |

### Crear recordatorio

`calendar` · `remind`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Fecha | Selección | Obligatorio |
| Recordatorio: minutos antes | Entero | Obligatorio |

### Completar recordatorio

`calendar` · `acknowledge`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Recordatorio | Selección | Obligatorio |

### Crear evento

`events` · `create`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Título | Texto | Obligatorio |
| Descripción / concepto | Texto | Obligatorio |
| Categoría | Texto | Obligatorio |
| Lugar | Texto | Obligatorio |
| Organización | Selección | Obligatorio |
| Persona responsable | Selección | Obligatorio |
| Inicio | Fecha y hora | Obligatorio |
| Fin | Fecha y hora | Obligatorio |
| Zona horaria | Texto | Obligatorio |
| Todo el día | Sí/No | Obligatorio |
| Hora repetida en el cambio horario | earlier, later | Obligatorio |
| Repetición | none, DAILY, WEEKLY, MONTHLY | Obligatorio |
| Intervalo de repetición | Entero | Obligatorio |
| Número de fechas (máximo 366) | Entero | Obligatorio |
| Inicio de inscripción | Fecha y hora | Obligatorio |
| Cierre de inscripción | Fecha y hora | Obligatorio |
| Plazas por fecha | Entero | Obligatorio |
| Cuota de participación | Importe en la moneda de la organización | Obligatorio |
| Moneda | Texto | Obligatorio |

### Inscribir / invitar participante

`events` · `register`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Fecha | Selección | Obligatorio |
| Persona | Selección | Obligatorio |
| Cuenta | Selección | Opcional |
| Estado | registered, invited | Obligatorio |

### Cambiar estado del participante

`events` · `participant`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Participante | Selección | Obligatorio |
| Versión del registro | Entero | Obligatorio |
| Estado | registered, confirmed, cancelled, attended, no_show | Obligatorio |

### Cambiar capacidad

`events` · `capacity`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Fecha | Selección | Obligatorio |
| Capacidad anterior | Entero | Obligatorio |
| Plazas por fecha | Entero | Obligatorio |

### Cancelar fecha de evento

`events` · `cancel`

| Campo | Entrada | Obligatorio |
|---|---|---|
| Fecha | Selección | Obligatorio |
