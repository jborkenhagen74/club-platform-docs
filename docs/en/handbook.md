# User handbook

## Sign-in and records

Sign in with your user account. Settings separate interface language from formatting locale. Module availability requires licensing, activation and user permissions. The extension manager also displays discovered modules that are not yet usable.

Create persons and organizations. Person dossiers contain contacts, addresses, memberships, official positions and attachments. Organizations support hierarchy. A user account can be linked to one person; this link controls personal views. Use descriptive search, sorting and filter controls. Open rows to edit records or related assignments.

## Permissions and lifecycle

Administrators manage groups, roles and permission selections with explanatory hints. Changes may not remove the acting administrator's own effective administrative rights. Verify access with a separate test user.

Archive removes a record from active lists and can be reversed. Permanent deletion is blocked by references. Missing module files can prevent safe reference checks. Posted financial history is corrected using reversal entries rather than deletion.

## Finance, contributions and purchases

Set the organization's currency before creating financial data. It becomes locked afterwards; no automatic conversion occurs. Enter decimal values such as `12.50` EUR in the UI. API amounts remain integer minor-unit strings.

Create a person's or organization's account. Receivables increase the outstanding balance; payments reduce it. The payment amount is displayed positively alongside its signed balance effect. Allocate payments to receivables; partial payments are allowed and overpayments remain unallocated. Correct mistakes with reversals and replacement postings.

Contributions use plans and membership assignments; purchases use products and items. Licensed person dossiers expose accounts. Organization-scoped readers only see the relevant organizations.

## Banking

Enable Finance and Banking. Open Banking inside Finance, reload accounts and create an organization bank account with name and IBAN. Currency comes from the organization.

Select the account, CSV or CAMT.053 and a UTF-8 statement. Edit or load a JSON mapping for CSV; the portal can export it. Review date, sign, currency and description in the preview, then confirm import. Import alone creates no payment. Select the correct finance account and separately confirm posting.

Review possible duplicates without unique bank references. Debits remain for manual review and cannot become incoming payments. [Mapping specification and limits](../banking.md).

## Calendar and events

Click a day in the monthly calendar, enter the appointment and assign a person or organization. Check timezone and recurrence. Personal visibility depends on account/person linkage; organization officials need current positions and explicit organization permissions. Person dossiers include assigned appointments.

Events manage registration windows, capacity and waiting lists. Fees require Finance. Free events do not require Calendar. Reminders are currently in-app only; email and push delivery are not implemented.

## Athlete licenses and documents

On a martial-arts person's license tab, enter name, issue date, expiry, issuing organization or free text, and warning days. Attach multiple evidence files. When Calendar is enabled, expiry entries are projected from current license data; edit the license itself to change them.

Templates use registered placeholders. Explicitly choose an address, position or examination when several match. Preview and rendering recheck permissions. See the [complete placeholder catalogue](placeholders.md).
