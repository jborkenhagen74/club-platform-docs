# Club Platform — Documentation / Dokumentation

**0.5.0 · 2026-09-09 · database schema 8 · native extension ABI 2**

| Sprache / Language | Dokumentation / Documentation | Benutzerhandbuch / User manual |
|---|---|---|
| Deutsch | [Deutsch](docs/de/README.md) | [Benutzerhandbuch](docs/de/user-manual.md) |
| English | [English](docs/en/README.md) | [User manual](docs/en/user-manual.md) |
| Français | [Français](docs/fr/README.md) | [Manuel utilisateur](docs/fr/user-manual.md) |
| Español | [Español](docs/es/README.md) | [Manual de usuario](docs/es/user-manual.md) |
| 한국어 | [한국어](docs/ko/README.md) | [사용자 설명서](docs/ko/user-manual.md) |

This repository contains the public documentation, REST contract, extension SDK and
standalone integration examples. It follows the original `docs/`, `openapi/`, `sdk/`
and `examples/` structure. The proprietary application implementation is not included.

The edition documents implementation commit `320a4c2709c13dd56455768a2f8819a815ad3997`.
Windows builds and PostgreSQL restore require maintenance commit
`6ebb363ec28ab8631fb82a88051351f87659b523`; see the translated operations chapters.
It describes delivered functionality and explicitly identifies limitations; it does
not turn future architecture proposals into supported API promises. Interface captions
remain those of the current German application; translated manuals are not UI language packs.

- [Machine-readable OpenAPI 3.1 contract](openapi/club-platform.yaml)
- [Exact resource keys](reference/resources.md)
- [Native extension SDK and ABI policy](sdk/README.md)
- [Buildable extension example](examples/extensions/hello-extension/README.md)
- [Minimal browser integration](examples/frontends/web-basic/README.md)
- [Documentation maintenance and validation](CONTRIBUTING.md)

Commands for building the application, operating its server and backing up its database
refer to an authorised checkout of the implementation repository. The extension example
in this repository builds independently and requires no private Core sources.

The existing [MIT license](LICENSE) applies to this documentation/SDK repository;
it does not grant access or rights to the private application implementation.
