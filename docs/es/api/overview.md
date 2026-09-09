# Contrato REST e integración

> Versión objetivo 0.6.0, preparación G0: API HTTP `/api/v1` y contrato `Client` común con `LocalClient`/`RestClient`. Se mantienen el esquema 8 y la ABI 2. Las rutas antiguas `/api/...` devuelven 404. Actualiza servidor, escritorio, portal y proxy conjuntamente. Las descripciones funcionales proceden de la base 0.5.0 y siguen siendo aplicables salvo lo actualizado en esta nota. Core Foundation II con ABI V3 y siete idiomas de interfaz aún no está completo.


[Inicio](../README.md) · [OpenAPI](../../../openapi/club-platform.yaml)

## Rutas reales

El desarrollo actual utiliza `/api/v1`. `/health` queda fuera de ese prefijo. OpenAPI describe las operaciones HTTP implementadas; los métodos internos no son automáticamente rutas HTTP.

| Área | Rutas |
|---|---|
| Sesión | `POST /api/v1/auth/login`, `GET /api/v1/auth/me`, `POST /api/v1/auth/logout`, `POST /api/v1/auth/password` |
| Personas | `GET/POST /api/v1/persons`, `GET/PUT /api/v1/persons/{id}` |
| Gestión | `GET/POST /api/v1/management/{resource}` |
| Archivos | `GET/POST /api/v1/assets`, `GET /api/v1/assets/{id}`, `GET /api/v1/branding` público |
| Extensiones | `GET /api/v1/extensions`, `POST /api/v1/extensions/install` |
| Documentos | `POST /api/v1/documents/render`, `GET /api/v1/reports` |
| Seguridad/campos | Operaciones de usuarios, grupos, roles y campos en OpenAPI |

## Sesiones y tipos

El acceso envía `{"login":"…","password":"…"}`. La respuesta incluye
`user_id`, `login`, `expires_at` en segundos Unix y token. Después enviar
`Authorization: Bearer TOKEN`. Ante `401`, descartar la sesión e iniciar otra.
No persistir contraseña ni token en el almacenamiento del navegador.

Las peticiones JSON necesitan `Content-Type: application/json`. Los valores de
gestión genérica son cadenas: `"8"`, `"true"`, `"2026-09-08"`. Las rutas específicas
de seguridad usan booleanos JSON reales para `enabled`, `active`, `read`, `write`.
Las revisiones son cadenas. Los identificadores suelen ser UUID; las asociaciones
pueden tener identificadores compuestos.

Crear persona:

```json
{"given_name":"Erika","family_name":"Mustermann"}
```

Modificar mediante `PUT /api/v1/persons/{id}`:

```json
{"revision":"1","given_name":"Erika","family_name":"Muster"}
```

La creación genérica utiliza `{"id":"","revision":"0","values":{…}}`;
la actualización mantiene ID y revisión leídas. No todo recurso permite editar:
`persons` y `organization_children` son vistas de lectura. Modificar personas por
su ruta específica o `person_identity`. Las asociaciones tienen semántica propia
de activación.

## Recursos y paginación

Las fichas usan `organizations`, `person_profiles`, `contacts`, `addresses`,
`relationships`, `memberships`, `positions`, `departments`, `fee_groups`,
`organization_affiliations`. Contactos/direcciones usan `entity_id`, datos personales
`person_id`, secciones organizativas `organization_id`. `owner` filtra la ficha
según el recurso; nunca concede permisos.

Administración: `users`, `groups`, `roles`, `group_members`, `group_roles`,
`role_permissions`, `field_definitions`, `field_permissions`, `field_values`.
Plantillas: `document_templates`. Registros nativos: `ext:martial.graduation` y
`ext:martial.exam`. La [referencia compartida](../../../reference/resources.md)
recoge las claves exactas. `labels` sirve para mostrar nombres; enviar los IDs.
No añadir campos desconocidos: ciertos recursos exigen el conjunto exacto.

Máximo 100 elementos por página. `after` es el último cursor; `q` es búsqueda
literal sensible a mayúsculas. Seguir `next_cursor` hasta `null` donde se devuelva.
Los archivos no incluyen `next_cursor`: tras 100 resultados utilizar la última
ID como `after` y detenerse en página corta o vacía. Las plantillas actualmente
ignoran búsqueda y owner. No todos los recursos admiten todos los filtros.

## Archivos, documentos y errores

Subir con `owner`, `purpose`, `filename`, `media_type`, `content` Base64 sin prefijo
Data URI. `file`/`photo` pertenecen a persona u organización; `logo`/`background`
usan owner vacío y requieren `security.manage`. Las listas dan metadatos; la
lectura individual incluye contenido. La imagen institucional se muestra antes
del acceso: no debe contener información confidencial.

`/api/v1/documents/render` recibe `template_id`, `person_id`, `date` y devuelve
`title`, `body`, **no PDF**. El PDF lo genera el cliente y la fecha de transporte
sigue siendo ISO. `/api/v1/reports` devuelve CSV UTF-8 con BOM para personas,
organizaciones, afiliaciones, cargos y datos nativos. Límite 5.000 filas; restringir
el filtro si se supera. El informe paginado no es una instantánea transaccional.

| Estado | Respuesta del cliente |
|---|---|
| 400 | Revisar JSON, campos, tipos y obligatorios |
| 401 | Descartar sesión y volver a entrar |
| 403 | Revisar permisos y Host/Origin |
| 404 | Comprobar ID y recurso existente |
| 409 | Releer, comparar y editar deliberadamente la revisión nueva |
| 500 | Investigar sin repetir escrituras a ciegas |

Una escritura con timeout puede haberse confirmado: leer antes de repetir.
No hay claves generales de idempotencia ni transacciones HTTP por lotes.
JSON estándar: 16 KiB; archivos: límite HTTP 8 MiB más límites del contenido
decodificado. Se autoriza un único origen exacta. Preflight con `OPTIONS /api/v1/…`;
`Host` upstream `localhost` o `127.0.0.1`, con puerto opcional. Acceso remoto por proxy HTTPS.
