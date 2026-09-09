# Native extension SDK — ABI 2

[Deutsch](../docs/de/extensions/getting-started.md) · [English](../docs/en/extensions/getting-started.md) · [Français](../docs/fr/extensions/getting-started.md) · [Español](../docs/es/extensions/getting-started.md) · [한국어](../docs/ko/extensions/getting-started.md)

Use [extension_v2.h](extension_v2.h) with Club Platform 0.5.0. It declares the
C structure `ClubExtensionV2` and entry-function pointer `ClubExtensionEntryV2`.
Export `clubplatform_extension_v2`; return a static ABI-2 structure. No Core headers,
STL objects, database handles or cross-boundary allocation are required.

[extension_api.h](extension_api.h) is retained solely as a historical ABI-1 proposal.
Its lifecycle/menu/view/REST callbacks are **not implemented by the 0.5.0 host**.
Do not mix the two headers or derive new modules from ABI 1.

The [buildable example](../examples/extensions/hello-extension/README.md) includes
only this public SDK. Compile separately for each target operating system and CPU.
