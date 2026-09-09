# Versionado y alcance comprobable

[Inicio](README.md)

Referencia: aplicación **0.5.0**, commit `320a4c2709c13dd56455768a2f8819a815ad3997`,
esquema **8**, ABI nativa **2**, edición **2026-09-09**.

| Capa | Contrato |
|---|---|
| Producto | Versión de paquete 0.5.0 |
| Base | Migraciones ordenadas; definiciones desconocidas o alteradas rechazadas |
| Extensión | ABI 2 y versión propia del manifiesto con tres números |
| HTTP | `/api` y `/health` separado; no hay `/api/v1` publicado |
| Documentación | Mismos capítulos y alcance en de/en/fr/es/ko |

R1.9 incorpora host nativo, R1.10 artes marciales, R1.11 plantillas/PDF/CSV y R1.12
operación piloto. Piloto no equivale a instaladores universales firmados ni aceptación
en todos los equipos. Las traducciones no cambian el idioma de la interfaz.

ABI 1 y `/api/v1` son propuestas históricas. Sus callbacks de menús, vistas y REST
no son capacidades garantizadas en 0.5.0. Agenda, pagos, modo sin conexión, aislamiento
multi-tenant, UI libre de plugins, actualización automática y localización completa
quedan fuera del alcance. Verificar conjuntamente producto, ABI y rutas.

Tras un cambio, sincronizar las cinco lenguas, actualizar el commit de referencia
y ejecutar validación. Nunca traducir identificadores, claves JSON, URLs ni opciones.
El contrato de seguridad es el mismo en cualquier idioma.
