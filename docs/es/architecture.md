# Arquitectura y modelo de seguridad

El controlador de escritorio utiliza exclusivamente la interfaz común `Client`. `LocalClient` accede a los servicios autenticados del núcleo dentro del proceso; `RestClient` realiza las mismas operaciones mediante `/api/v1`. La aplicación selecciona la implementación al iniciarse. El controlador UI no depende de los destinos de compilación host, application ni persistence.

> Versión objetivo 0.6.0, preparación G0: API HTTP `/api/v1` y contrato `Client` común con `LocalClient`/`RestClient`. Se mantienen el esquema 8 y la ABI 2. Las rutas antiguas `/api/...` devuelven 404. Actualiza servidor, escritorio, portal y proxy conjuntamente. Las descripciones funcionales proceden de la base 0.5.0 y siguen siendo aplicables salvo lo actualizado en esta nota. Core Foundation II con ABI V3 y siete idiomas de interfaz aún no está completo.


[Inicio](README.md) · [Manual de usuario](user-manual.md)

## Alcance

Esta edición describe **Club Platform 0.5.0**, commit
`320a4c2709c13dd56455768a2f8819a815ad3997`, esquema de base de datos 8 y ABI de
extensiones 2. La versión del producto, las migraciones y la ABI son contratos
distintos. Disponer de documentación traducida no implica que la interfaz,
actualmente mayoritariamente alemana, esté completamente traducida.

El producto administra personas, organizaciones, afiliaciones, cargos, contactos,
archivos y datos deportivos. Una persona puede estar vinculada a varias
organizaciones. Un usuario es una identidad de acceso: crear una persona no crea
una cuenta ni la vincula automáticamente al usuario conectado. Las organizaciones
pueden ser federaciones nacionales o regionales, clubes, escuelas deportivas,
empresas u otras entidades.

## Modos de ejecución

| Modo | Interfaz | Procesamiento y almacenamiento |
|---|---|---|
| Monopuesto | Qt Quick/QML | Host local, SQLite y servicios comunes |
| Escritorio conectado | Qt Quick/QML | REST por HTTPS; el servidor mantiene la conexión a la base |
| Portal web | React/TypeScript, Tailwind 4 | Archivos estáticos y proxy HTTPS hacia el servidor C++ |

La aplicación resuelve la sesión y comprueba permisos en cada operación. El cliente
no elige la identidad que actúa: se rechazan objetos REST con `actor` o `actor_id`.
El servidor escucha en `127.0.0.1`; un proxy inverso aporta TLS y acceso público.
Los clientes no deben acceder directamente a la base del servidor. SQLite y
PostgreSQL son alternativas, no almacenes sincronizados automáticamente.

El escritorio remoto no dispone de caché de escritura sin conexión. El portal
mantiene el token solo en memoria; recargar exige iniciar sesión de nuevo.
Únicamente la preferencia de apariencia se guarda localmente en el navegador.

## Datos y relaciones

Los UUID identifican registros independientemente del nombre o número de socio.
Las actualizaciones incluyen la revisión leída previamente; un conflicto evita
sobrescribir cambios concurrentes. Las revisiones REST son cadenas decimales,
para evitar redondeos de enteros grandes en JavaScript.

La ficha personal reúne identidad, datos personales, contactos, direcciones,
relaciones, afiliaciones, cargos, campos personalizados y archivos. La afiliación
vincula persona y organización, con departamento y grupo de cuotas opcionales.
Un grupo de cuotas es un dato de referencia, no un proceso automático de cobro,
facturación o domiciliación SEPA.

La organización superior define una jerarquía: federación nacional → federación
regional → escuela deportiva. Otras afiliaciones organizativas son relaciones
separadas. La jerarquía no concede permisos ni delimita tenants o seguridad por
fila. Se rechazan ciclos de organizaciones superiores.

Los campos personalizados tienen definición, tipo, permisos de grupo y valores.
Lectura y escritura son independientes. El permiso de solo escritura no revela
el valor actual. Cambiar de tipo exige convertir todos los valores; si uno falla,
se revierte toda la operación.

## Autenticación y autorización

Las contraseñas utilizan hashes Argon2id; los tokens también se almacenan como
hashes en el servidor. Valores predeterminados: ocho horas de duración absoluta,
30 minutos de inactividad y bloqueo de 30 segundos tras cinco fallos de acceso.
Evitar bucles de reintentos rápidos.

La cadena es usuario → grupos → roles → permisos; sin concesión se deniega el
acceso. `records.read/write` cubre registros generales; `memberships.read/write`,
afiliaciones y cargos. `security.manage` administra cuentas e imagen institucional;
`schema.manage`, definiciones, plantillas e instalación de módulos. `audit.read`
pertenece a la API interna; 0.5.0 no publica una ruta HTTP de auditoría dedicada.
`*` es acceso administrador amplio. Debe quedar al menos un administrador activo.

Los permisos de campo se añaden a los generales. Los datos de artes marciales
requieren también `martial.read` o `martial.write`. Esta versión no restringe
automáticamente cada cuenta a «su» persona u organización. El portal es una
interfaz administrativa con permisos, no un autoservicio de socios terminado.

## Archivos, transacciones y límites

El contenido de los archivos está en la base e incluido en su copia de seguridad.
Límite ordinario: 5 MiB; fotos e imagen institucional: 2 MiB en el servicio.
Las interfaces redimensionan PNG/JPEG y limitan el área a 16 megapíxeles.
Una imagen de perfil nueva sustituye a la anterior. Subir documentos nunca instala
módulos nativos.

Cambios y entradas de auditoría son transaccionales. SQLite serializa escrituras;
PostgreSQL utiliza sus mecanismos de transacción y bloqueo. Un CSV paginado no es
por ello una instantánea transaccional.

No asumir disponibles instaladores universales firmados, actualización automática,
pagos, agenda, sincronización sin conexión, aislamiento multi-tenant, envío automático
de documentos o menús/rutas libres de plugins. Consultar [versionado](versioning.md).
