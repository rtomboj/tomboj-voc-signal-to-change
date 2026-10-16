# Attribution and provenance

Original Tomboj instructional workflow, mapping method, build record, and test prompt. Sources below were consulted only; no third-party implementation or prose was copied. User-specific design exports and monitoring packages informed requirements but are not included in this public skill.

| Official source | Relevance |
| --- | --- |
| [Apps Script web apps](https://developers.google.com/apps-script/guides/web) | HTML Service entry points, deployment, test versus versioned URLs, execution identity |
| [Bound scripts](https://developers.google.com/apps-script/guides/bound) | Active-container methods are unavailable during web-app execution |
| [Client/server communication](https://developers.google.com/apps-script/guides/html/communication) | Asynchronous RPC, serializable values, public/private server functions |
| [Web app manifest](https://developers.google.com/apps-script/manifest/web-app-api-executable) | DOMAIN differs from ANYONE and anonymous access; execution settings |
| [Session](https://developers.google.com/apps-script/reference/base/session) | Active versus effective user and identity availability |
| [SpreadsheetApp](https://developers.google.com/apps-script/reference/spreadsheet/spreadsheet-app) | Explicit workbook access and authorization requirements |
| [HTML Service restrictions](https://developers.google.com/apps-script/guides/html/restrictions) | Iframe navigation and HTTPS active assets |
| [HTML Service best practices](https://developers.google.com/apps-script/guides/html/best-practices) | HTML/CSS/JS partials and asynchronous data loading |
| [Service authorization](https://developers.google.com/apps-script/guides/services/authorization) | Scope inference, incremental authorization and trigger creator authority |
| [Troubleshooting authorization](https://developers.google.com/apps-script/guides/support/troubleshooting) | Trigger executions cannot present interactive authorization dialogs |

Checked October 16, 2026. Account/admin policy and actual deployment behavior still require live verification. This skill supplies an adaptive build process, not a preconfigured web app or a claim of compatibility with every existing script.
