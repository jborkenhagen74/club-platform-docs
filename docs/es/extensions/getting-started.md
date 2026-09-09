# Desarrollo de extensiones nativas

> Versión objetivo 0.6.0, preparación G0: API HTTP `/api/v1` y contrato `Client` común con `LocalClient`/`RestClient`. Se mantienen el esquema 8 y la ABI 2. Las rutas antiguas `/api/...` devuelven 404. Actualiza servidor, escritorio, portal y proxy conjuntamente. Las descripciones funcionales proceden de la base 0.5.0 y siguen siendo aplicables salvo lo actualizado en esta nota. Core Foundation II con ABI V3 y siete idiomas de interfaz aún no está completo.


[Inicio](../README.md) · [Interfaz](ui.md) · [Ejemplo](../../../examples/extensions/hello-extension/README.md)

El host 0.5.0 requiere **ABI 2**. `sdk/extension_api.h` conserva el borrador ABI 1;
sus callbacks de ciclo de vida, menús y REST no son utilizables en este host.
Usar `sdk/extension_v2.h`. La frontera C evita objetos STL y liberaciones entre
módulos, pero la biblioteca debe corresponder al sistema y arquitectura CPU.

Los módulos ejecutan código de confianza con permisos del proceso host. No existe
sandbox. Proteger el directorio administrativamente, revisar bibliotecas y nunca
cargarlas desde las carpetas normales de archivos subidos. Se cargan al inicio,
sin sustitución en caliente.

## Entrada y manifiesto

Exportar `clubplatform_extension_v2`. Devuelve una estructura de vida permanente
con número ABI, manifiesto UTF-8 y validador. Las cadenas siguen siendo propiedad
del módulo. El validador recibe tipo y JSON como cadenas y devuelve exactamente
`1` si acepta; ninguna excepción puede cruzar la ABI. No se entrega conexión de base.

El manifiesto contiene `id`, `name`, `version`, `types`. La versión tiene tres
componentes numéricos. La ID de módulo no contiene puntos; los tipos comienzan por
`modulo.`. Cada tipo tiene `key`, `label`, `fields`; cada campo `key`, `label`, `type`
y opcionalmente `required:false`. Tipos: `text`, `integer`, `decimal`, `boolean`,
`date`. Las claves empiezan por minúscula y usan minúsculas, cifras, guiones bajos
y puntos de espacio de nombres. Se rechazan duplicados y espacios ajenos.

Enviar todos los campos declarados, incluidos opcionales vacíos como cadena vacía.
Los desconocidos se rechazan. El host valida tipos y obligatorios antes del
validador del módulo; máximo actual 512 bytes UTF-8 por valor. El ejemplo añade
asistencia a entrenamiento usando únicamente la cabecera pública:

```sh
cmake -S examples/extensions/hello-extension -B build/hello-extension -DCMAKE_BUILD_TYPE=Release
cmake --build build/hello-extension --config Release
```

Copiar la biblioteca resultante al directorio dedicado; comprobar la subcarpeta
`Release`/`Debug` con Visual Studio. Iniciar con `--extensions /ruta/absoluta` o
`CLUBPLATFORM_EXTENSIONS`. El escritorio remoto no vuelve a cargar los módulos
del servidor en el equipo cliente.

## Activación y datos

Un administrador conectado selecciona `Erweiterungen aktivieren` o envía `{}` a
`POST /api/v1/extensions/install`. Requiere `schema.manage`. Registro de tipos y
manifiesto son transaccionales y auditados. `GET /api/v1/extensions` presenta módulos
cargados e `installed`; reinstalar el mismo manifiesto es válido.

Los registros nativos actualmente pertenecen a personas. Ejemplo:
`/api/v1/management/ext:attendance.session`. `values` incluye `person_id`, que el host
retira antes de llamar al validador. Asignar a roles `attendance.read/write` además
de `records.read/write`. La visibilidad de un botón no sustituye los permisos.

Se rechaza al cargar un manifiesto distinto del instalado. Subir su versión no
migra datos: hace falta migración explícita y copia verificada. Rutas REST libres,
tareas de fondo, QML/JavaScript ejecutable empaquetado y hot reload quedan fuera de ABI 2.
