# Manual de usuario

> Versión objetivo 0.6.0, preparación G0: API HTTP `/api/v1` y contrato `Client` común con `LocalClient`/`RestClient`. Se mantienen el esquema 8 y la ABI 2. Las rutas antiguas `/api/...` devuelven 404. Actualiza servidor, escritorio, portal y proxy conjuntamente. Las descripciones funcionales proceden de la base 0.5.0 y siguen siendo aplicables salvo lo actualizado en esta nota. Core Foundation II con ABI V3 y siete idiomas de interfaz aún no está completo.


[Inicio](README.md) · [Instalación](installation.md) · [Operación](operations.md)

**Edición:** 0.5.0 / 2026-09-09. Para administración, instructores y responsables
del sistema. Los ejemplos son ficticios. Las etiquetas alemanas citadas corresponden
a la interfaz real; la visibilidad depende de permisos y tamaño de pantalla.

## Contenido

1. [Conceptos básicos](#conceptos-básicos)
2. [Iniciar sesión](#iniciar-sesión)
3. [Organizaciones y jerarquía](#organizaciones-y-jerarquía)
4. [Ficha personal](#ficha-personal)
5. [Afiliaciones y cargos](#afiliaciones-y-cargos)
6. [Fotos y archivos](#fotos-y-archivos)
7. [Artes marciales](#artes-marciales)
8. [Campos personalizados](#campos-personalizados)
9. [Plantillas e informes](#plantillas-e-informes)
10. [Apariencia y ayuda](#apariencia-y-ayuda)
11. [Administración](#administración)
12. [Incidencias y control diario](#incidencias-y-control-diario)

## Conceptos básicos

Una **persona** representa a un socio, instructor, contacto o colaborador. Un
**usuario** es una cuenta de acceso. Son registros diferentes: una persona puede
administrarse sin cuenta y no se vincula automáticamente al usuario conectado.

Una **organización** puede ser escuela, club, federación o empresa. Una
**afiliación** vincula persona y organización con número, estado y fechas. Un
**cargo** describe una función y una **relación** otro vínculo de contacto o apoyo.
No duplicar personas para representar varias afiliaciones. Los derechos proceden
de la cuenta, no de la jerarquía organizativa.

## Iniciar sesión

1. Abrir el escritorio o la dirección HTTPS proporcionada por administración.
2. Verificar modo monopuesto/servidor. Nombres iguales en dos bases no significan sincronización.
3. Introducir usuario y contraseña y pulsar `Anmelden`.
4. Confirmar que aparecen las fichas esperadas.

`Administrator einrichten` crea el primer administrador de una base monopuesto
vacía; no es el procedimiento para añadir compañeros. Las cuentas de servidor
las prepara administración. La contraseña necesita al menos doce caracteres.
Tras varios fallos, esperar brevemente y revisar credenciales.

Recargar el portal exige entrar de nuevo. Por defecto, la sesión dura como máximo
ocho horas o 30 minutos de inactividad. Guardar antes de una pausa y salir de la
sesión; un navegador abierto no bloquea el puesto. Cambiar contraseña en escritorio:
`Administration → Passwort ändern`. El portal todavía no tiene un formulario específico.

## Organizaciones y jerarquía

Abrir `Organisationen` y buscar antes de crear. Elegir `Neu anlegen`, indicar nombre
completo y tipo: `Dachverband` (federación superior), `Landesverband` (regional),
`Verein` (club), `Sportschule` (escuela deportiva), `Unternehmen` (empresa),
`Sonstige` (otra). Completar nombre corto, registro, fundación, web, contactos,
dirección e identificadores federativos conocidos. Pulsar `Speichern`, reabrir
y revisar. No inventar números para rellenar campos opcionales.

Crear primero la federación nacional; después la regional seleccionando la nacional
como superior; finalmente club o escuela seleccionando la regional. Usar una
referencia a un registro existente: escribir el nombre no crea el enlace.
`Struktur` en escritorio muestra organizaciones subordinadas.
`Verbandszugehörigkeit` recoge vínculos adicionales con función y fechas.
Una entidad no puede ser su propio antepasado: corregir la cadena, no crear un duplicado.
Estas relaciones no conceden derechos de usuario.

`Abteilungen` contiene departamentos y deportes. `Beiträge` contiene grupos de
cuotas, moneda y periodicidad. Los importes son **céntimos**: 25,00 EUR se introduce
como `2500`. No se ejecuta ningún cobro. Miembros, cargos, relaciones, contactos,
direcciones y archivos se gestionan desde la ficha; algunas vistas difieren entre
escritorio y portal.

## Ficha personal

1. Abrir `Personen` y buscar nombre/apellidos para evitar duplicados.
2. Crear la persona, introducir nombre y apellidos y guardar.
3. Abrir el registro o seleccionar `Akte öffnen`.
4. Completar cada sección necesaria y guardarla.

La búsqueda es literal y distingue mayúsculas. Acortar el texto y revisar páginas
siguientes si no aparece el resultado. Cada página contiene como máximo 100 elementos,
no necesariamente todo el conjunto.

| Etiqueta | Contenido |
|---|---|
| Übersicht | Identidad, nombre y apellidos |
| Persönlich | Nacimiento, tratamiento, género, tutor y contacto de emergencia |
| Kontakt | Teléfono, correo y otros medios identificados |
| Anschriften | Direcciones con etiqueta clara |
| Mitgliedschaften | Organización, número, estado y fechas de afiliación |
| Funktionen | Cargos y periodos |
| Beziehungen | Otros vínculos organizativos |
| Dateien | Documentos; foto en la cabecera |
| Eigene Felder | Campos Core autorizados en escritorio |
| Graduierungen / Prüfungshistorie | Graduaciones/exámenes tras activar el módulo |
| Dokumente / Dokumentvorlagen | Documentos para esta persona |

Las fechas siguen el formato del sistema/navegador. La API y exportaciones técnicas
pueden mostrar `2026-09-08`; respetar el patrón que presenta el control.
En pantallas pequeñas seleccionar sección con `Aktenbereich`.
En escritorio, `Entwurf behalten und schließen` conserva un borrador marcado con
un punto: **no está guardado en la base**. En el portal guardar o descartar
conscientemente el formulario antes de navegar. Un borrador no es una copia de seguridad.

## Afiliaciones y cargos

Desde la ficha personal, `Mitgliedschaften → Neu anlegen`. La persona ya está
fijada; elegir organización explícitamente. Rellenar número de socio, estado,
inicio y, si corresponde, tipo, departamento, grupo de cuotas y datos de baja.
Desde una ficha organizativa, la organización queda fijada y se elige la persona.

La fecha final no puede preceder a la inicial. `Aktiv`, `Ruhend`, `Beendet` son
activo, suspendido temporalmente y finalizado; no equivalen al estado de la cuenta.
Para una baja, modificar la afiliación existente con fecha y motivo, sin recrear
la persona. No se automatizan facturas, recordatorios, domiciliaciones ni cómputos
legales de preaviso.

En `Funktionen`, introducir cargo y fechas, por ejemplo instructor o dirección.
Un cargo funcional no concede derechos del programa: no sustituye `martial.write`.
Una persona puede tener varias afiliaciones y cargos.

## Fotos y archivos

Situar la foto personal o logo organizativo en la cabecera fija. Usar
`Foto auswählen`, `Logo auswählen` o `Foto / Logo hochladen`. Se admiten PNG/JPEG;
se redimensionan y pueden rechazarse imágenes excesivas o dañadas. Una imagen nueva
sustituye a la anterior del mismo registro.

Para contratos, certificados y anexos, abrir `Dateien` o `Unterlagen und Dateien`,
pulsar `Datei hochladen`, escoger archivo y esperar confirmación. Revisar nombre
y ficha correcta. Máximo 5 MiB: 5 × 1.024 × 1.024 bytes. Usar nombres descriptivos;
no guardar credenciales ni intentar instalar módulos mediante esta función.

Elegir el archivo o `Herunterladen` y seleccionar destino. Abrir después
voluntariamente con un programa adecuado. Conservar el original hasta comprobar
una descarga de control. 0.5.0 no ofrece una interfaz general para borrar archivos;
consultar administración si se adjuntó al registro equivocado. No todas las listas
permiten búsqueda por nombre de archivo.

## Artes marciales

Administración debe colocar la biblioteca en el host y activarla. Entonces aparecen
`Graduierungen` y `Prüfungshistorie` en las fichas. Si faltan, comprobar conexión
y activación; si se deniega acceso, revisar también permisos del módulo.

Una graduación incluye disciplina/estilo, nivel 1–30, denominación libre, fecha de
concesión y examinador opcional. Ejemplo: `Taekwon-Do`, nivel `8`, `8. Kup`.
La cifra es neutral y no impone una escala universal entre federaciones; aplicar
la normativa propia de la organización.

Un examen incluye disciplina, nivel objetivo, fecha, resultado, examinador y notas
opcionales. Escribir exactamente `passed` (aprobado) o `failed` (no aprobado).
Guardar el examen no crea automáticamente graduación ni certificado: realizarlos
y comprobarlos por separado. No hay autorización automática de examen ni cálculo de tasas.

## Campos personalizados

En escritorio, administración define campos por tipo de registro: texto, entero,
decimal, sí/no o fecha. Después concede derechos por grupo. Los valores se editan
en `Eigene Felder` dentro de la ficha.

El permiso de solo escritura oculta el valor actual: un campo aparentemente vacío
no demuestra que no exista dato. Revisar y respaldar antes de cambiar tipo;
una sola conversión imposible cancela toda la migración. El portal todavía no
administra las definiciones y permisos de estos campos Core.

## Plantillas e informes

Administración crea título y texto plano en `Dokumentvorlagen`. Solo se aceptan
estos marcadores, cuyas claves no se traducen:

```text
Certificado de participación

Certificamos la participación de {{given_name}} {{family_name}}.
Fecha de expedición: {{date}}
```

No inventar `{{member_number}}` u otros: se rechazan los desconocidos. La plantilla
no ejecuta código. Elegir los datos abriendo la ficha de la persona correspondiente.

Escritorio: abrir plantilla guardada en `Dokumente`, elegir
`Gespeicherte Vorlage als PDF öffnen`, indicar destino y revisar con el visor del
sistema. Portal: `PDF-Vorschau`. Si el móvil no admite vista integrada, usar
`PDF öffnen` o `Herunterladen`. Comprobar nombre, fecha, saltos de línea y texto
antes de entregar. No se envía correo automático. La fecha de plantilla se inserta
actualmente en ISO.

Para listas, seleccionar recurso y filtro, después `CSV exportieren` o
`Gefilterte Liste exportieren`. Puede incluir hasta 5.000 filas de todas las páginas.
Evitar cambios concurrentes durante la exportación. En la hoja de cálculo,
seleccionar UTF-8 y separador coma. El apóstrofo inicial de valores parecidos a
fórmulas es una protección; no eliminarlo sin revisar. Si la lista queda vacía,
comprobar permisos y filtros.

## Apariencia y ayuda

Escritorio: `Einstellungen → Ansicht → Darstellung und Farben`. Modo sistema sigue
claro/oscuro y cinco temas incluyen alto contraste. El escritorio admite también
colores propios. Portal: `Einstellungen → Ansicht`, sistema o claro, oscuro,
bosque, ciruela, alto contraste. Los valores de color personalizados todavía no
son una opción independiente en el portal.

Administración fija logo y fondo en `Einstellungen → Startbildschirm` o ajustes
equivalentes del portal. Son visibles **antes de iniciar sesión**: no usar datos
confidenciales. No representan la foto personal de un miembro.

En escritorio, `Hilfe → Nach Updates suchen` consulta versiones estables. Un depósito
privado puede exigir acceso; una consulta fallida no prueba que esté actualizado.
No se instala nada automáticamente. Coordinar el cambio de versión con administración.

## Administración

Crear usuario, incorporarlo a un grupo, asignar rol al grupo y permisos al rol.
Comprobar la cadena completa. Lectura general: `records.read`; afiliaciones:
también `memberships.read`; artes marciales: también `martial.read`.
Añadir escritura solo cuando haga falta. No conceder `*` para ocultar fallos sin diagnóstico.

El último administrador activo no puede deshabilitarse ni perder su última
asignación administrativa. Ante pérdida de contraseña usar recuperación local
documentada; no existe API público de reinicio de administrador. Los cargos
funcionales no son roles de seguridad. Los campos necesitan sus permisos de grupo adicionales.

## Incidencias y control diario

| Situación | Paso siguiente |
|---|---|
| No avanza después del nombre | Revisar acción de crear/guardar, error visible, ventana y build |
| Cambios no visibles | Confirmar ficha/modo, actualizar y quitar filtros |
| Acceso denegado | Revisar con administración rol y permisos de campo/módulo |
| Registro cambiado por otra persona | Conservar cambios deseados, releer y comparar |
| Error de red tras guardar | Verificar si ya se guardó antes de repetir |
| Módulo ausente | Revisar ruta, activación y versión |
| PDF no abre | Comprobar archivo, visor o “PDF öffnen” |
| Archivo demasiado grande | Preparar copia menor conservando el original |

Al terminar, resolver borradores, releer cambios importantes y cerrar sesión.
Administración supervisa copias y ensayos de recuperación. Para soporte indicar
versión, modo, hora, acción y mensaje, sin contraseñas, tokens ni datos personales innecesarios.
