# Drive intake helper

This small Apps Script project converts Excel workbooks placed in a Google Drive folder into Google Sheets copies and logs the resulting Sheet URLs and IDs. It is the intake step for VOC Part 2.

It leaves each original `.xlsx` or `.xls` file unchanged. It does not collect public reviews, alter workbook tabs, create monitoring triggers, classify feedback, send alerts, or call an LLM. The later monitoring project still needs a source-specific adapter and user-approved cadence.

## Setup

1. Create a Drive folder named `VOC_Automation` and place the Part 1 Markdown report and Excel workbook in it. Keep both files as the untouched benchmark originals.
2. Create a standalone Apps Script project at [script.google.com](https://script.google.com/).
3. Add `DriveIntake.gs` to the project. Enable the Drive API v3 Advanced Google service. The included `appsscript.json` shows the service and OAuth scope used by this example.
4. In **Project Settings → Script Properties**, add:
   - Property: `VOC_AUTOMATION_FOLDER_ID`
   - Value: the folder ID or the folder URL
5. Run `convertVocXlsxToSheets` manually and authorize the requested Google Drive access.
6. Open **Executions** and review the log. For each converted workbook, copy the `sheetUrl` or `sheetId` into the Part 2 setup conversation. The Markdown report remains a Drive file; the workbook gets a Google Sheets copy. Before editing the converted Sheet, make a dated backup. Excel conversion can change formulas, charts, formatting, or validation, so check the important tabs and formulas against the original before adding the monitor.

The script lists the configured folder's direct children. It does not recursively search subfolders. It handles `.xlsx` and `.xls` filenames and skips other files.

## Permissions and behavior

The example asks for the Drive OAuth scope `https://www.googleapis.com/auth/drive`, which is broad: Apps Script uses it to list, read, and create files. The function operates on the configured folder, but the OAuth grant is not technically restricted to that folder. Review the code, use an account permitted to access the VOC folder, and limit who can edit the Apps Script project. Converted copies are created in the same folder and inherit its sharing access. The script does not change permissions.

Rerunning the same project returns an existing converted copy instead of creating another. This relies on a private Drive app property, so keep using the same Apps Script project for repeat runs. If it reports multiple matches, review those copies manually.

There is no schedule or trigger in this example. Run it manually, inspect the output, and confirm the Sheet opens before moving to the monitoring setup.

## Official references

- [Advanced Drive service for Apps Script](https://developers.google.com/apps-script/advanced/drive)
- [Convert uploaded files to Google Workspace types](https://developers.google.com/workspace/drive/api/guides/manage-uploads)
- [Search Drive files with private app properties](https://developers.google.com/workspace/drive/api/guides/search-files)
- [Apps Script authorization](https://developers.google.com/apps-script/guides/services/authorization)
