# Extension quick start

Extensions use a versioned C ABI. This keeps the binary boundary stable across C++ compiler implementations while allowing each extension to use modern C++ internally.

An extension can register permissions, menu entries, views and REST routes through the host API. Future revisions will add typed registries for member-profile tabs, dashboard widgets, settings pages, scheduled jobs, persistence migrations and domain events.

See `examples/extensions/hello-extension`.
