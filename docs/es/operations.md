# Operación e integración

## Prueba local

Ejecuta los comandos en el repositorio privado del programa, no en el de documentación. Requisitos: preset macOS con Qt, ICU, libxml2 y dependencias nativas; Node.js 22 desde 22.12. Ejecuta `--init admin` solo una vez sobre una base nueva; solicita contraseña. Mantén abierto el servidor y ejecuta el segundo bloque en otra terminal desde la raíz del proyecto. Ctrl+C detiene cada proceso. La base de prueba está separada de los datos del escritorio.

```bash
cmake --preset user-macos-vscode-debug
cmake --build --preset user-macos-vscode-debug --parallel
mkdir -p build/portal-test
./build/user-macos-vscode-debug/apps/server/clubplatform-server \
  --sqlite build/portal-test/data.sqlite --init admin
./build/user-macos-vscode-debug/apps/server/clubplatform-server \
  --sqlite build/portal-test/data.sqlite \
  --extensions "$PWD/build/user-macos-vscode-debug/runtime-extensions" \
  --port 8080 --portal-origin http://127.0.0.1:5173
```

```bash
cd apps/portal
npm ci
npm run dev -- --port 5173 --strictPort
```

http://127.0.0.1:5173

## Autenticación y despliegue

`POST /api/v1/auth/login` recibe `{"login":"…","password":"…"}` y devuelve `token`, `user_id`, `login`, `expires_at`. Envía `Authorization: Bearer <token>` y conserva el token en memoria. `GET /api/v1/auth/me` verifica la sesión; `POST /api/v1/auth/logout` la revoca. Valores predeterminados: ocho horas máximas, 30 minutos de inactividad y bloqueo de 30 segundos tras cinco fallos. El servidor comprueba permisos y módulos.

En producción un proxy HTTPS sirve el portal y reenvía `/api/v1` al servidor loopback. `--portal-origin` debe coincidir exactamente con el origen del navegador. Conserva Origin y usa Host localhost/127.0.0.1 hacia el servidor. CORS no autentica criptográficamente portales: otros clientes pueden omitir Origin. mTLS/BFF no está implementado. No incluyas secretos en JavaScript.

## Licencias y módulos

1. Genera y protege las claves privadas del editor y de activación fuera del repositorio.
2. Despliega la autoridad detrás de HTTPS: [guía de operación](../../tools/activation/README.md).
3. Define módulos, límites, vigencia y política de activación. Banking exige `finance` y `banking`.
4. Firma con la clave del editor y registra la licencia en la autoridad. Distribuye solo claves públicas y archivos firmados.
5. Configura `CLUBPLATFORM_PINNED_LICENSE_KEY` para paquetes de producción. Las licencias antiguas de desarrollo no protegen contra copias.
6. Importa y activa la licencia, instala y activa los módulos. En el portal se vincula la instalación del servidor, no cada navegador.
7. Libera la instalación anterior antes de trasladarla y activa el nuevo equipo. El modo sin conexión debe estar permitido. La revocación sin conexión puede tardar hasta que caduque el arrendamiento.

Esquemas: 18 banca, 17 activación, 16 monedas, 15 vínculo usuario/persona, 14 calendario/eventos. Antes de actualizar: detener servidor, verificar copia y desplegar versiones compatibles. Restaurar en otro equipo no sustituye la activación.

## API y SDK

El [índice API](../api/overview.md) reúne los contratos. Los importes API son cadenas de enteros en unidades menores. Revisiones e identificadores de origen protegen modificaciones y reintentos. La importación requiere vista previa y confirmación: [contrato](../banking.md).

ABI V3 usa una interfaz C y manifiestos. Las extensiones nativas son código de confianza dentro del proceso, sin aislamiento. Persistencia y autorización pertenecen al servidor. Véanse [V3](../extension-v3.md), [marcadores](placeholders.md) y [estado de aceptación](../status.md).

