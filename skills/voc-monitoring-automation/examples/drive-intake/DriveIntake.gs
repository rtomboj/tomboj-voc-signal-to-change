/**
 * VOC Drive intake helper
 *
 * Converts .xlsx/.xls files in a configured VOC_Automation Drive folder into
 * Google Sheets copies. The originals remain untouched. It does not collect
 * reviews, add workbook tabs, create triggers, classify feedback, or send alerts.
 *
 * Setup:
 * 1. Set Script Property VOC_AUTOMATION_FOLDER_ID to the folder ID or URL.
 * 2. Enable the Advanced Drive service (Drive API v3).
 * 3. Run convertVocXlsxToSheets manually and review the execution log.
 *
 * The function requests Drive access because it lists existing files in the
 * configured folder, reads each workbook, and creates a converted copy.
 */
var VOC_INTAKE = {
  FOLDER_PROPERTY: 'VOC_AUTOMATION_FOLDER_ID',
  SHEET_MIME_TYPE: 'application/vnd.google-apps.spreadsheet',
  SOURCE_ID_PROPERTY: 'vocSourceFileId',
  VERSION: '1'
};

/**
 * Convert Excel workbooks in the configured folder to Google Sheets copies.
 * Safe to run again in the same Apps Script project: converted copies are
 * identified by a private Drive appProperty containing the original file ID.
 *
 * @return {Array<Object>} Conversion status and Sheet links for each workbook.
 */
function convertVocXlsxToSheets() {
  var folderId = getVocFolderId_();
  var folder = Drive.Files.get(folderId, {
    fields: 'id,name,mimeType,driveId',
    supportsAllDrives: true
  });

  if (folder.mimeType !== 'application/vnd.google-apps.folder') {
    throw new Error('VOC_AUTOMATION_FOLDER_ID must refer to a Drive folder.');
  }

  var files = listVocFolderFiles_(folderId, folder.driveId);
  var results = [];

  files.forEach(function (source) {
    if (!/\.xlsx?$/i.test(source.name || '')) {
      return;
    }

    try {
      var existing = findVocConversion_(folderId, folder.driveId, source.id);
      if (existing.length > 1) {
        results.push({
          status: 'review-duplicate-conversions',
          sourceName: source.name,
          sourceId: source.id,
          matchingSheetIds: existing.map(function (item) { return item.id; })
        });
        return;
      }

      if (existing.length === 1) {
        results.push({
          status: 'already-converted',
          sourceName: source.name,
          sourceId: source.id,
          sheetName: existing[0].name,
          sheetId: existing[0].id,
          sheetUrl: getSheetUrl_(existing[0])
        });
        return;
      }

      var sourceBlob = DriveApp.getFileById(source.id).getBlob();
      var targetName = source.name.replace(/\.xlsx?$/i, '') + ' (Google Sheets)';
      var converted = Drive.Files.create({
        name: targetName,
        mimeType: VOC_INTAKE.SHEET_MIME_TYPE,
        parents: [folderId],
        appProperties: {
          vocSourceFileId: source.id,
          vocIntakeVersion: VOC_INTAKE.VERSION
        }
      }, sourceBlob, {
        fields: 'id,name,mimeType,webViewLink,parents,appProperties',
        supportsAllDrives: true
      });

      results.push({
        status: 'converted',
        sourceName: source.name,
        sourceId: source.id,
        sheetName: converted.name,
        sheetId: converted.id,
        sheetUrl: getSheetUrl_(converted)
      });
    } catch (error) {
      results.push({
        status: 'failed',
        sourceName: source.name,
        sourceId: source.id,
        error: String(error && error.message ? error.message : error)
      });
    }
  });

  if (results.length === 0) {
    results.push({
      status: 'no-excel-files-found',
      folderName: folder.name,
      folderId: folder.id
    });
  }

  console.log(JSON.stringify({
    folderName: folder.name,
    folderId: folder.id,
    results: results
  }, null, 2));

  return results;
}

/**
 * Accept either a raw Drive folder ID or its /folders/ URL.
 *
 * @return {string} Drive folder ID.
 */
function getVocFolderId_() {
  var value = PropertiesService.getScriptProperties()
    .getProperty(VOC_INTAKE.FOLDER_PROPERTY);

  if (!value) {
    throw new Error(
      'Set the Script Property VOC_AUTOMATION_FOLDER_ID to the VOC_Automation folder ID or URL.'
    );
  }

  value = value.trim();
  var match = value.match(/\/folders\/([A-Za-z0-9_-]+)/) ||
    value.match(/[?&]id=([A-Za-z0-9_-]+)/);
  var folderId = match ? match[1] : value;

  if (!/^[A-Za-z0-9_-]{10,}$/.test(folderId)) {
    throw new Error('The configured folder value does not look like a Drive folder ID or URL.');
  }

  return folderId;
}

/**
 * List direct children of the configured folder, including Shared Drive items.
 *
 * @param {string} folderId Drive folder ID.
 * @param {?string} driveId Shared Drive ID, if the folder is in a Shared Drive.
 * @return {Array<Object>} Direct child files.
 */
function listVocFolderFiles_(folderId, driveId) {
  var files = [];
  var pageToken;

  do {
    var options = {
      q: "'" + folderId + "' in parents and trashed = false",
      pageSize: 100,
      fields: 'nextPageToken,files(id,name,mimeType,webViewLink,parents)',
      supportsAllDrives: true,
      includeItemsFromAllDrives: true
    };

    if (driveId) {
      options.corpora = 'drive';
      options.driveId = driveId;
    }
    if (pageToken) {
      options.pageToken = pageToken;
    }

    var response = Drive.Files.list(options);
    files = files.concat(response.files || []);
    pageToken = response.nextPageToken;
  } while (pageToken);

  return files;
}

/**
 * Find an existing converted copy by the original workbook's Drive file ID.
 *
 * @param {string} folderId Destination folder ID.
 * @param {?string} driveId Shared Drive ID, if applicable.
 * @param {string} sourceId Original workbook file ID.
 * @return {Array<Object>} Matching Google Sheets copies.
 */
function findVocConversion_(folderId, driveId, sourceId) {
  var options = {
    q: "'" + folderId + "' in parents and appProperties has { key='" +
      VOC_INTAKE.SOURCE_ID_PROPERTY + "' and value='" + sourceId +
      "' } and trashed = false",
    pageSize: 100,
    fields: 'files(id,name,mimeType,webViewLink,parents)',
    supportsAllDrives: true,
    includeItemsFromAllDrives: true
  };

  if (driveId) {
    options.corpora = 'drive';
    options.driveId = driveId;
  }

  var response = Drive.Files.list(options);
  return (response.files || []).filter(function (file) {
    return file.mimeType === VOC_INTAKE.SHEET_MIME_TYPE;
  });
}

/**
 * Return a browser URL for a Google Sheet.
 *
 * @param {Object} file Drive file resource.
 * @return {string} Google Sheets URL.
 */
function getSheetUrl_(file) {
  return file.webViewLink ||
    'https://docs.google.com/spreadsheets/d/' + file.id + '/edit';
}
