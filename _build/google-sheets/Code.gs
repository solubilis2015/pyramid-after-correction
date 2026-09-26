/**
 * Pyramid Engineering — website enquiry form → Google Sheet
 *
 * Paste this whole file into the Apps Script editor that is bound to your
 * Google Sheet (Extensions → Apps Script), replacing the default Code.gs.
 * Then run setupSheet() once, and deploy as a Web App (see README.md).
 */

var SHEET_NAME = 'Enquiries';

var HEADERS = [
  'Name', 'Company', 'Email', 'Telephone', 'Service Required', 'Sector',
  'Plant/Site Location', 'Scope of Work', 'Consent', 'Timestamp'
];

// Longest value accepted per field; anything longer is cut off.
var MAX_LEN = { name: 120, company: 160, email: 160, phone: 40, service: 80,
                sector: 80, location: 200, message: 5000 };

/** Run once from the editor to create the sheet tab and header row. */
function setupSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
  sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]).setFontWeight('bold');
  sheet.setFrozenRows(1);
}

/** Receives the website form (application/x-www-form-urlencoded POST). */
function doPost(e) {
  var p = (e && e.parameter) || {};

  // Honeypot: real visitors never fill this hidden field. Pretend success so bots learn nothing.
  if (p.website_url) return json_({ ok: true });

  var data = {};
  Object.keys(MAX_LEN).forEach(function (k) {
    data[k] = String(p[k] || '').trim().slice(0, MAX_LEN[k]);
  });

  var missing = ['name', 'company', 'email', 'message'].filter(function (k) { return !data[k]; });
  if (missing.length) return json_({ ok: false, error: 'Missing required fields: ' + missing.join(', ') });
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) return json_({ ok: false, error: 'Invalid email address' });
  if (p.consent !== 'yes') return json_({ ok: false, error: 'Consent is required' });

  var row = [
    data.name, data.company, data.email, data.phone, data.service, data.sector,
    data.location, data.message, 'Yes', new Date()
  ].map(safeCell_);

  // Lock so two submissions arriving together cannot overwrite the same row.
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    if (!sheet) { setupSheet(); sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME); }
    sheet.appendRow(row);
  } catch (err) {
    return json_({ ok: false, error: 'Could not save the enquiry. Please try again.' });
  } finally {
    lock.releaseLock();
  }
  return json_({ ok: true });
}

/** Lets you open the Web App URL in a browser to check it is live. */
function doGet() {
  return json_({ ok: true, message: 'Pyramid Engineering enquiry endpoint is running.' });
}

// Stop spreadsheet formula injection: text starting with = + - @ is stored as plain text.
function safeCell_(v) {
  return (typeof v === 'string' && /^[=+\-@]/.test(v)) ? "'" + v : v;
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
