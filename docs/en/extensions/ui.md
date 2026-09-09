# Declarative UI contributions

[Language home](../README.md) · [Development](getting-started.md)

ABI 2 describes record types and fields. Desktop and portal turn these into tabs
and forms in **person dossiers**. A manifest does not supply arbitrary menus,
widgets or scripts. Native types are not automatically attached to organisation
dossiers by this contract.

A type's `label` becomes its tab caption; a field's `label` captions the input.
`integer` is a whole number, while `date` travels as ISO text. Display uses the
system/browser locale. Optional fields should be visibly optional and still sent
as empty strings when absent. Technical keys are language-independent. Manifest
labels in 0.5.0 are ordinary strings, not translation dictionaries.

The service checks permissions again on reading and saving. Access may therefore
be denied even after a dossier was opened. Preserve revisions; do not bypass
`409` with a forced overwrite. A visible tab does not establish write permission.

Acceptance for a module: load and activate as administrator, open a person, fill
required fields, save, close and reopen. Try an invalid date and a domain-invalid
value. Then permit a reader to read while verifying that writing fails. Exercise
both interfaces and a narrow window. The martial-arts module demonstrates free
rank designations and stages 1–30; its numeric field is not a universal federation
ranking system.
