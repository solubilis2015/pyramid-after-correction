# Contact form → Google Sheet

The enquiry form on `contact.html` posts to a Google Apps Script Web App, which appends each
enquiry as a row in a Google Sheet. `Code.gs` in this folder is the script.

## 1. Create the sheet
1. Go to https://sheets.google.com and create a blank spreadsheet, e.g. **Pyramid – Website Enquiries**.
2. Leave it empty — the script creates an **Enquiries** tab with these headers:
   `Name | Company | Email | Telephone | Service Required | Sector | Plant/Site Location | Scope of Work | Consent | Timestamp`

## 2. Add the script
1. In the spreadsheet: **Extensions → Apps Script**.
2. Delete everything in `Code.gs` and paste the contents of `Code.gs` from this folder. Save (Ctrl+S).
3. In the function dropdown at the top, choose **setupSheet** and click **Run**.
4. Approve the permission prompt (Review permissions → your account → Advanced → Go to project → Allow).
   The **Enquiries** tab with bold headers now exists.

## 3. Deploy as a Web App
1. **Deploy → New deployment**. Click the gear icon → **Web app**.
2. Description: `Website enquiry form`. **Execute as: Me**. **Who has access: Anyone**.
3. Click **Deploy**, then copy the **Web app URL** (it ends in `/exec`).
4. Optional check: open the URL in a browser — it should show `{"ok":true,...}`.

## 4. Connect the website
In `contact.html`, replace `PASTE_YOUR_APPS_SCRIPT_WEB_APP_URL_HERE` in the form's
`data-sheet-endpoint` attribute with the URL. Upload the site. Until a URL is set, the form
falls back to opening the visitor's email app, as before.

## Updating the script later
Edit the code, then **Deploy → Manage deployments → (pencil) Edit → Version: New version → Deploy**.
This keeps the same URL. Creating a *New deployment* instead gives a new URL that you must
paste into `contact.html` again.

## Files (drawings/specifications)
Files are not sent to the sheet. After submitting, a visitor who selected files is shown an
"Email them to enquiry@pyramid-groups.com" link to send the attachments separately.
