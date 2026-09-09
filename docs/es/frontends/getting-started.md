# Frontends e integración con el servidor web

> Versión objetivo 0.6.0, preparación G0: API HTTP `/api/v1` y contrato `Client` común con `LocalClient`/`RestClient`. Se mantienen el esquema 8 y la ABI 2. Las rutas antiguas `/api/...` devuelven 404. Actualiza servidor, escritorio, portal y proxy conjuntamente. Las descripciones funcionales proceden de la base 0.5.0 y siguen siendo aplicables salvo lo actualizado en esta nota. Core Foundation II con ABI V3 y siete idiomas de interfaz aún no está completo.


[Inicio](../README.md) · [REST](../api/overview.md) · [Instalación](../installation.md)

El portal usa React/TypeScript y Tailwind 4. `npm ci` respeta el lockfile;
`npm run build` produce archivos estáticos en `dist/`. Código PDF y fuentes se
cargan desde el build cuando se necesitan, sin CDN obligatorio.
`examples/frontends/web-basic` demuestra solo acceso y lista de personas.

Servir portal y API bajo el mismo origen HTTPS. El proxy envía `/api/v1/` al host
local con `Host: 127.0.0.1:8080`, conservando `Authorization` y `Origin`.
Configurar ese origen exacta mediante `--portal-origin`. Sin configuración se
rechazan peticiones de navegador con Origin. No sustituirla por acceso comodín.

Configurar `/health` aparte si se necesita supervisión pública; el proxy `/api/v1/`
no lo incluye. No registrar cuerpos, contraseñas o tokens. DNS, certificados y
cuentas de servicio son responsabilidad operativa; el producto no automatiza certificados.

## Comportamiento del cliente

Mantener el token solo en memoria, nunca en URLs ni almacenamiento persistente.
Ante `401`, borrar sesión, listas personales y borradores y pedir acceso nuevo.
Explicar `403`. Después de fallo de red en escritura, releer antes de reintentar;
tras `409`, comparar la revisión actual.

Paginar listas. Mostrar nombres de referencias mediante `labels` o registros
relacionados mientras se envían IDs. Renderizar texto sin interpretarlo como HTML.
Descargar solo por acción explícita del usuario. Los archivos subidos no se
convierten en plugins ejecutables.

## Apariencia y alcance

Los temas claro, oscuro, bosque, ciruela y alto contraste complementan el modo
sistema. Las fechas visibles siguen la configuración regional y la API conserva ISO.
En pantallas pequeñas, `Aktenbereich` elige la sección. Las definiciones y permisos
de campos Core siguen administrándose en escritorio. La cuenta no queda vinculada
automáticamente a su propio socio.

Utilizar [OpenAPI](../../../openapi/club-platform.yaml) junto a la
[referencia de campos](../../../reference/resources.md). No copiar rutas inexistentes
como `/api/v1/appointments` del borrador anterior. Probar compatibilidad antes de actualizar.
