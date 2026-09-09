# Aportaciones declarativas a la interfaz

> Versión objetivo 0.6.0, preparación G0: API HTTP `/api/v1` y contrato `Client` común con `LocalClient`/`RestClient`. Se mantienen el esquema 8 y la ABI 2. Las rutas antiguas `/api/...` devuelven 404. Actualiza servidor, escritorio, portal y proxy conjuntamente. Las descripciones funcionales proceden de la base 0.5.0 y siguen siendo aplicables salvo lo actualizado en esta nota. Core Foundation II con ABI V3 y siete idiomas de interfaz aún no está completo.


[Inicio](../README.md) · [Desarrollo](getting-started.md)

ABI 2 describe tipos y campos. Escritorio y portal generan pestañas y formularios
en **fichas personales**. El manifiesto no añade menús, widgets o scripts arbitrarios.
Estos tipos no se incorporan automáticamente a fichas de organizaciones.

El `label` del tipo es el título de pestaña; el del campo es su etiqueta.
`integer` representa un entero y `date` se transporta en ISO. La presentación usa
la configuración regional del sistema/navegador. Marcar opcionales y enviar cadena
vacía si no hay valor. Las claves técnicas no se traducen; los labels de 0.5.0
son cadenas simples, no diccionarios multilingües.

El host vuelve a comprobar permisos al leer y guardar. Puede denegar una operación
incluso tras abrir la ficha. Conservar revisiones y resolver `409` comparando datos,
no forzando sobrescritura. Una pestaña visible no demuestra permiso de escritura.

Prueba de aceptación: cargar/activar como administrador, abrir persona, completar
obligatorios, guardar y reabrir. Probar fecha inválida y valor rechazado por la
lógica del módulo. Permitir luego lectura a un rol limitado y comprobar que no
puede escribir. Revisar ambas interfaces y ventana estrecha. Artes marciales
muestra nombres libres y niveles 1–30, no una clasificación universal entre federaciones.
