# Extension quick start

For current modules use **ABI V3** and the public example at
[`sdk/examples/v3-extension`](../../sdk/examples/v3-extension/CMakeLists.txt).
It builds independently of the private Club Platform source and libraries.

Follow the detailed German guide:

- [Module development without Core source](../de/module-entwicklung-ohne-core.md)
- [Download the PDF guide](../pdf/Club-Platform-Modulentwicklung-DE.pdf)
- [ABI V3 reference](../extension-v3.md)

You need both public headers in `sdk/include/clubplatform`, a compiler, CMake and
nlohmann-json. Integration testing also requires a separately supplied host binary
and a publisher-signed license covering the module ID.

The historical `sdk/extension_api.h` and `examples/extensions/hello-extension`
are not the API for new V3 modules. V3 does not expose a general host pointer for
registering arbitrary menus, Qt views or REST routes. Use its published manifest
and capability contracts; additional host behavior requires an agreed SDK change.
