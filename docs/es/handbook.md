# Manual de usuario

## Acceso y fichas

Inicia sesión con tu cuenta. Los ajustes separan idioma y formato regional. Los módulos requieren licencia, activación y permisos. El gestor también muestra módulos detectados que todavía no están disponibles.

Crea personas y organizaciones. Las fichas incluyen contactos, direcciones, membresías, cargos y archivos. Las organizaciones admiten jerarquías. Una cuenta de usuario puede vincularse a una persona para las vistas personales. Utiliza búsqueda, ordenación y filtros descriptivos; abre una fila para editar su ficha o asignaciones.

## Permisos y ciclo de vida

Los administradores asignan grupos, roles y permisos mediante listas con ayuda. No pueden eliminar sus propios permisos administrativos efectivos. Verifica los cambios con otra cuenta.

Archivar es reversible. Las referencias bloquean la eliminación definitiva; un módulo ausente puede impedir verificarlas. Las operaciones financieras se corrigen mediante contrapartidas, nunca borrando el historial.

## Finanzas, cuotas y compras

Define la moneda de la organización antes de crear datos financieros. Después queda bloqueada, sin conversión automática. Introduce decimales como `12,50` EUR; la API conserva unidades monetarias menores enteras.

Crea una cuenta para la persona u organización. Los cobros pendientes aumentan el saldo; los pagos lo reducen. El importe pagado aparece positivo y su efecto en el saldo por separado. Asigna pagos a deudas: se permiten pagos parciales y excedentes sin asignar. Corrige con anulación y nueva operación.

Las cuotas usan planes y membresías; las compras usan productos y líneas. Las cuentas personales aparecen según licencia y permisos. Los responsables solo consultan las organizaciones autorizadas.

## Banca

Activa Finance y Banking. Abre Banca en Finanzas, carga las cuentas y crea una cuenta con organización, nombre e IBAN. La moneda procede de la organización.

Selecciona cuenta, CSV o CAMT.053 y archivo UTF-8. Edita o carga el mapeo JSON de CSV; el portal permite exportarlo. Revisa fechas, signos, monedas y conceptos, y confirma la importación. Importar no crea pagos. Después selecciona la cuenta financiera y confirma el registro del ingreso.

Revisa posibles duplicados sin referencia única. Los débitos quedan para revisión manual y no se registran como ingresos. [Especificación y límites](../banking.md).

## Calendario y eventos

Haz clic en un día, introduce la cita y asigna persona u organización. Comprueba zona horaria y repetición. La visibilidad personal depende del vínculo cuenta/persona; los responsables requieren cargo vigente y permisos de organización. La ficha personal incluye citas asignadas.

Los eventos gestionan inscripción, plazos, plazas y lista de espera. Las tarifas requieren Finance; eventos gratuitos no requieren Calendar. Los recordatorios son internos, sin correo ni notificaciones push.

## Licencias deportivas y documentos

En la ficha deportiva introduce nombre, fechas de expedición y caducidad, entidad emisora y días de aviso. Adjunta varios justificantes. Calendar proyecta los vencimientos desde la licencia; modifica esta para corregirlos.

Las plantillas usan marcadores registrados. Selecciona dirección, cargo o examen explícitamente si hay varios. Vista previa y generación vuelven a verificar permisos. [Lista completa](placeholders.md).
