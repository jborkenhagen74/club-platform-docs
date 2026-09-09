# Instalación y puesta en marcha

> Versión objetivo 0.6.0, preparación G0: API HTTP `/api/v1` y contrato `Client` común con `LocalClient`/`RestClient`. Se mantienen el esquema 8 y la ABI 2. Las rutas antiguas `/api/...` devuelven 404. Actualiza servidor, escritorio, portal y proxy conjuntamente. Las descripciones funcionales proceden de la base 0.5.0 y siguen siendo aplicables salvo lo actualizado en esta nota. Core Foundation II con ABI V3 y siete idiomas de interfaz aún no está completo.


[Inicio](README.md) · [Operación y recuperación](operations.md)

Antes de modificar una instalación, crear una copia verificada. Separar datos,
configuración y programas. Adaptar las rutas de ejemplo y no ejecutar pruebas
contra producción. Un archivo comprimido no es un instalador universal: hacen
falta bibliotecas del sistema y, para escritorio, un entorno Qt compatible.
El paquete de escritorio puede incluir Qt mediante la opción de despliegue del
producto. Compilar la aplicación exige acceso al repositorio de implementación;
este repositorio público no contiene su código propietario.

## Entornos de desarrollo

| Sistema | Referencia del proyecto |
|---|---|
| Windows | Visual Studio 2026; MSVC v143/14.44 para Qt 6.11.2 `msvc2022_64`; IncrediBuild opcional |
| macOS | Xcode completo, Apple Clang, VS Code, Ninja, ccache, Qt 6.11.2 `macos` |
| Linux | Compilador C++23, CMake/Ninja, SQLite, libsodium, cpp-httplib, nlohmann-json; Qt para escritorio |
| Portal | Node 22 compatible, al menos 22.12, y npm |

Son referencias del proyecto, no afirmaciones sobre la última versión disponible.
PostgreSQL requiere libpq. `QT_ROOT` apunta al SDK correspondiente. No incluir
`CMakeUserPresets.json` local en los commits.

Si macOS solo reconoce Command Line Tools, seleccionar el Xcode completo instalado:

```sh
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch
xcodebuild -version
export QT_ROOT="$HOME/Qt/6.11.2/macos"
```

En el repositorio de implementación:

```sh
./scripts/init-dev-macos.sh
./scripts/verify-dev-macos.sh
cmake --preset user-macos-vscode-debug
cmake --build --preset user-macos-vscode-debug --parallel
ctest --preset user-macos-vscode-debug --output-on-failure
```

En Windows, configurar `QT_ROOT`, por ejemplo `C:\Qt\6.11.2\msvc2022_64`, abrir
otro terminal y ejecutar `scripts\init-dev-windows.ps1` y
`scripts\verify-dev-windows.ps1`. El wrapper IncrediBuild admite
`-Configuration Debug -Desktop`. No reutilizar salidas de compilación entre sistemas.
Quick 3D/Shader Tools se destinan a funciones gráficas relacionadas; WebEngine no
es necesario para el portal independiente.

## Monopuesto y servidor

```sh
clubplatform-desktop --database /ruta/club/data.sqlite \
  --extensions /ruta/club/extensions
```

Una base nueva ofrece crear el primer administrador. Usar una contraseña de al
menos doce caracteres, iniciar sesión y activar extensiones desde `Administration`.
La biblioteca debe estar previamente en el directorio; la activación no la descarga.

Inicializar el servidor localmente y después arrancarlo:

```sh
clubplatform-server --sqlite /ruta/club/data.sqlite --init admin
clubplatform-server --sqlite /ruta/club/data.sqlite \
  --extensions /ruta/club/extensions \
  --portal-origin https://gestion.example
```

`--password-stdin` sirve para automatización controlada. No poner secretos en
argumentos, Git o registros públicos. Para PostgreSQL utilizar `--postgres` y
`CLUBPLATFORM_POSTGRESQL` mediante configuración protegida. Elegir exactamente
un proveedor de base.

El escritorio conectado utiliza `--server https://gestion.example`. La ruta local
no representa una réplica sin conexión. Configurar cuentas, permisos y módulos en
el servidor. El acceso remoto se realiza mediante HTTPS y proxy correcto; HTTP
se reserva al bucle local.

## Publicar el portal

```sh
cd apps/portal
npm ci
npm run build
```

Copiar el contenido de `dist/` a la raíz documental HTTPS. No se necesita un proceso
Node para servirlo. Redirigir `/api/v1/` a `127.0.0.1:8080`, fijar el `Host` de upstream
a `127.0.0.1:8080` y conservar `Origin` y `Authorization`. `--portal-origin` debe
coincidir exactamente, sin barra final. El portal funciona en `/`; un subdirectorio
arbitrario no es una configuración terminada en 0.5.0.

En desarrollo, Vite normalmente usa `http://127.0.0.1:5173`; permitir ese mismo
origen. `CLUB_API` cambia el destino del proxy de desarrollo. `npm run dev` no es
la forma de servir producción.

## Aceptación

Con datos de prueba, comprobar acceso, creación/guardado/relectura, organización,
afiliación, foto, descarga binaria, graduación, CSV y PDF. Una cuenta limitada debe
rechazar escrituras no autorizadas. Restaurar realmente una copia en otra base y
verificar que las sesiones anteriores quedan invalidadas. Revisar diálogos nativos
y visor PDF en cada OS. Compilar correctamente no sustituye la aceptación funcional.

## Ejemplo de proxy inverso HTTPS

Añade esta configuración Nginx al servidor virtual TLS existente. Adapta la raíz de archivos y configura certificado y escucha HTTPS en el entorno del servidor. El límite permite la carga JSON máxima; la aplicación mantiene sus límites de archivo decodificado. Inicia el servicio con exactamente el mismo origen público.

```nginx
root /srv/club-platform/portal;
client_max_body_size 8m;

location / {
    try_files $uri $uri/ /index.html;
}

location /api/v1/ {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host 127.0.0.1:8080;
    proxy_set_header Origin $http_origin;
    proxy_set_header Authorization $http_authorization;
}
```
