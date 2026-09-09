# Operación, copias y actualizaciones

[Inicio](README.md) · [Instalación](installation.md)

Separar cuenta de servicio, programas, módulos y datos. Los usuarios del portal
no deben escribir en el directorio de módulos. Las copias contienen datos personales,
archivos y hashes de contraseñas: restringir acceso y proteger su destino.
`scripts/pilot-*.py` pertenece al paquete de implementación, no a este repositorio
público, y requiere Python 3.11 o posterior.

> La compilación en Windows y la restauración PostgreSQL requieren además el commit correctivo `cd765ba08bd2cd8c21969eb8fc20a52a9659e214`. Corrige el símbolo del SDK de Windows `LOAD_LIBRARY_SEARCH_DEFAULT_DIRS` y añade `--file=-` al exportar SQL con `pg_restore`. No cambia el esquema ni la API.

## SQLite

```sh
python3 scripts/pilot-data.py backup data.sqlite copia-2026-09-09
python3 scripts/pilot-data.py diagnose copia-2026-09-09/database.sqlite
python3 scripts/pilot-data.py restore copia-2026-09-09 restaurada.sqlite
```

La copia en línea incluye escrituras WAL confirmadas. El directorio destino no
debe existir. Se comprueban integridad, claves foráneas, secuencia de migraciones
y SHA-256. Un fallo puede dejar un directorio incompleto: sin manifiesto válido
no es una copia recuperable.

La restauración exige una base **nueva**, verifica datos e invalida sesiones.
Detener el host antes de cambiar su ruta a la base comprobada. Conservar la anterior
hasta la aceptación funcional. Los archivos adjuntos están incluidos; programas,
módulos, certificados y configuración necesitan recuperación separada.

## PostgreSQL

Usar `pg_dump`, `pg_restore`, `psql` compatibles con el servidor. Configurar acceso
mediante `pg_service.conf`, `.pgpass` o parámetros libpq protegidos. Crear base nueva
y vacía con servicio independiente; no ejecutar otro host sobre ella durante la restauración.

```sh
python3 scripts/pilot-postgres.py backup --service club-production --directory pg-backup
python3 scripts/pilot-postgres.py restore --service club-restore --directory pg-backup
```

Se crea archivo custom y manifiesto de checksum. Las tablas de usuario existentes
impiden restaurar. Restauración y revocación de sesiones comparten transacción.
No se importan propietarios/ACL antiguos; preparar roles de explotación aparte.
Nunca restaurar sobre tablas productivas activas.

## Procedimiento de actualización

1. Avisar, terminar trabajos y crear copia.
2. Situar nuevos binarios y módulos compatibles en un directorio de versión separado.
3. Restaurar en base de prueba nueva y arrancar el host nuevo para comprobar/aplicar migraciones.
4. Verificar acceso, cambios, afiliación, graduación, archivo, CSV y PDF, también con cuenta limitada.
5. Detener producción y, tras aceptación, cambiar programas/configuración y el portal correspondiente.
6. Recargar navegadores, iniciar sesión y comprobar datos.
7. Para volver atrás, usar aplicación antigua **y copia previa a sus migraciones correspondiente**.

No abrir una base migrada con binarios antiguos. Los cambios posteriores a la copia
pueden perderse al retroceder; tratarlos antes. Buscar actualizaciones no las instala.
Firma, notarización y despliegue general son pasos de entrega separados.

## Diagnóstico e incidencias

`clubplatform-server --sqlite BASE_PRUEBA --diagnose` informa de conexión y esquema
sin personas. Abrir el host comprueba **y aplica** migraciones. Para inspección
SQLite sin migrar, usar `pilot-data.py diagnose`. Registrar versión, modo, hora y
error sin contraseñas ni tokens.

Si Git indica falta de seguimiento, seleccionar la rama correcta y ejecutar una vez
`git branch --set-upstream-to=origin/feature/core-foundation feature/core-foundation`,
después `git pull --ff-only`. No eliminar cambios locales con reset forzado.
Un `403` obliga a revisar roles y proxy/origin. Para un módulo ausente comprobar
ruta, CPU, ABI, manifiesto instalado y activación. No alterar tablas de migración
ni manifiestos para eludir controles.
