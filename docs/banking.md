# Banking Foundation — CSV and CAMT.053

Development implementation, schema 18. Native/platform acceptance is pending CI.
Requires installed, active and licensed `banking` and `finance` modules, and
`banking.write` plus `finance.write` for all banking workspace operations.
Module 1.0.0 exposes `finance.payment-provider` v1. Native dependency: libxml2.

## Workflow

In Finance, open Banking and reload bank accounts. Create a bank account with
organization, display name, IBAN and the organization's currency. IBAN checksum
is validated. Currency changes are blocked once bank accounts exist.

Choose a bank account, format and statement. CSV supports an editable/importable
JSON mapping; the portal also exports that mapping. Review the preview, including
duplicates, then explicitly confirm import. Import does not create ledger entries.
Load imported entries, select the correct person's finance account within the
same organization and currency, then explicitly confirm posting. Credit entries
become payments in the existing ledger. Select an open receivable if desired:
matching shows an exact reference (the receivable's source ID equals the bank
reference or the complete remittance), an equal amount, or manual review.
These are suggestions, never automatic bookings. The allocation shown is the
smaller of payment and open receivable; partial payments leave the remaining
debt open, overpayments stay unallocated. Payment and allocation commit together
and retries cannot duplicate either. Changes since the suggestion are validated
again when posting. Use the ledger allocation action to distribute remaining
credit across additional receivables. Choosing no receivable posts credit only.
Debit entries are retained for manual review and cannot become incoming payments.
Unattended matching, outgoing-payment accounting, direct bank connections and
SEPA export are not implemented.

Repeated bank references with unchanged content are skipped. A changed amount or
description under the same reference causes a conflict. Without a reference the
identity uses booking date, amount, currency, description and counterparty.
Identical legitimate payments cannot be distinguished by that fallback: provide
a stable reference column in the mapping before importing such statements.
Repeating the confirmed payment action returns the existing payment. Reversing
that payment does not make the source available for an accidental second posting.

## JSON mapping

See [complete example](../resources/banking/csv-mapping.json). Version is `1`.
Input encoding is UTF-8 (optional BOM); convert other encodings before import.
`delimiter`: one of semicolon, comma, tab or pipe. `header`: true by default.
`skip_rows`: 0–100 nonempty records before the header/data. `columns` maps canonical
names to exact, trimmed, unique header names or zero-based integer column indices.
Indices also work with `header: false`. Canonical fields:

| Field | Required | Meaning |
|---|---|---|
| booking_date | yes | Booking date |
| amount | yes | Signed decimal amount, or unsigned with direction |
| currency | no | Currency column; otherwise mapping `currency`, default EUR |
| reference | recommended | Stable, unique reference within the bank account |
| description | no | Remittance / purpose |
| counterparty | no | Sender or recipient |
| bank_account | no | Must match the selected account's IBAN if populated |
| direction | no | Requires `credit_value` and `debit_value` in the mapping |

`date_format`: `YYYY-MM-DD` or `DD.MM.YYYY`. `decimal_separator`: comma (default)
or dot. `group_separator`: empty (default), or one distinct separator with strict
groups of three digits. Values must fit the currency's exact fraction digits;
no floating-point rounding. Quote escaping uses doubled quotes; quoted delimiters
and line breaks are supported. Maximum file: 2 MiB, 10,000 rows, 128 columns,
4,096 bytes per field. Malformed records reject the entire preview/import.
With `direction`, amount must be unsigned; exact credit/debit strings control sign.

## CAMT.053 profile

Reads ISO 20022 `camt.053.001.xx` namespaces and `BkToCstmrStmt/Stmt/Ntry` entries.
Only `BOOK` status, valid positive `Amt` with `Ccy`, `CRDT`/`DBIT`, booking date,
account IBAN, bank reference and entry/remittance information are accepted.
Entry-level amounts are imported exactly once; aggregate entries are not expanded
into extra payments. Pending and reversal entries reject the import for manual
review. This is a bounded supported profile, not full XSD validation or support
for every bank-specific variant. Test representative real bank exports first.
DTD/entities, network resources, XInclude and recovery parsing are disabled.

## API

All commands use `POST /api/v1/finance/commands/banking.<operation>` with JSON and
Bearer authentication. They run inside the shared authorized transaction.

| Operation | Request fields | Response |
|---|---|---|
| accounts | `{}` | accounts |
| account.create | organization_id, name, iban, currency | id |
| preview | bank_account_id, format (`csv`/`camt053`), contents, mapping | rows, preview_hash |
| import | same as preview, preview_hash, confirmed: true | imported count |
| transactions | bank_account_id, optional after cursor | up to 100 rows, next_cursor (null at end) |
| matches | transaction_id, account_id | transaction_id, open receivable rows with reason and allocation_amount |
| post | transaction_id, account_id, confirmed: true; optional receivable_id and allocation_amount together | existing/new payment id |

Amounts in the API are exact minor-unit strings. Matching is limited to the
selected account in the same organization and currency. Repeat posting with a
different account or allocation is a conflict, even after a reversal. Pagination
uses the last row ID as `after`; use `next_cursor` until null. Reload from the
first page after importing additional statements.

Preview hash binds the reviewed normalized rows and their current duplicate state.
If another import changes that state, generate a new preview. Banking operations
serialize against finance writes; failures roll back data and audit together.
Imports use a 3 MiB JSON envelope limit; normal commands retain the 16 KiB limit.

## Local macOS

Install libxml2 through your normal development setup (`brew install libxml2`).
Reconfigure and build with `cmake --preset user-macos-vscode-debug` and
`cmake --build --preset user-macos-vscode-debug --parallel`.
Use `build/user-macos-vscode-debug/runtime-extensions` as the server's extensions
directory to include all modules. Add `banking` to the signed license; rebuild
and re-sign the module package/catalog if using managed provisioning.
