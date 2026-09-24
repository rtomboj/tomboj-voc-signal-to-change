# Attribution and prior art

This skill is original instructional work by Rachel Wilde / Tomboj. It uses the Part 1 VOC Benchmark Builder and its published workbook contract as the preceding step in the same project. It does not copy code or prose from external monitoring repositories.

## Platform documentation consulted

| Source | Relevance | Use |
| --- | --- | --- |
| [Google Apps Script container-bound scripts](https://developers.google.com/apps-script/guides/bound) | Accessing the parent Google Sheet | Platform behavior reference only |
| [Google Apps Script installable triggers](https://developers.google.com/apps-script/guides/triggers/installable) | Time-driven triggers, authorization, and trigger ownership | Platform behavior reference only |
| [Google Apps Script external services](https://developers.google.com/apps-script/guides/services/external) | Calling approved external APIs | Platform behavior reference only |
| [Google Apps Script authorization](https://developers.google.com/apps-script/guides/services/authorization) | User authorization and scopes | Platform behavior reference only |
| [Google Apps Script Script service](https://developers.google.com/apps-script/reference/script/script-app) | Trigger visibility for current project and user | Platform behavior reference only |
| [Google Apps Script LockService](https://developers.google.com/apps-script/reference/lock/lock-service) | Preventing overlapping shared-data writes | Platform behavior reference only |
| [Google Apps Script Properties service](https://developers.google.com/apps-script/guides/properties) | Per-script and per-user configuration | Platform behavior reference only; scope is not a promise of secret management |
| [Google Cloud Secret Manager](https://cloud.google.com/secret-manager/docs) | Optional shared secret storage for a team | Platform behavior reference only; requires Cloud project and IAM setup |
| [Google Apps Script quotas](https://developers.google.com/apps-script/guides/services/quotas) | Service limits | Platform behavior reference only; check current limits before use |
| [Google Apps Script Advanced Drive service](https://developers.google.com/apps-script/advanced/drive) | Drive API v3 support in Apps Script | Consulted for the Drive intake example; no code copied |
| [Google Drive upload and conversion guide](https://developers.google.com/workspace/drive/api/guides/manage-uploads) | Converting uploaded Excel/CSV content to Workspace file types | Platform behavior reference only |
| [Google Drive search and custom-property guides](https://developers.google.com/workspace/drive/api/guides/search-files) | Query syntax for idempotent conversion lookup | Platform behavior reference only |
| [Google Workspace MCP configuration](https://developers.google.com/workspace/guides/configure-mcp-servers) | OAuth-based Workspace tools for connected AI clients | Consulted for the field guide; no code copied |
| [OpenAI API authentication](https://platform.openai.com/docs/api-reference/authentication), [Anthropic API authentication](https://docs.anthropic.com/en/api/getting-started), and [Gemini API keys](https://ai.google.dev/gemini-api/docs/api-key) | Provider-specific API credential requirements | Consulted for LLM integration guidance; no keys, code, or prose copied |
| Apps Script and Workspace repositories listed in the [Apps Script and Google Workspace field guide](../../docs/apps-script-workspace-field-guide.md) | Practical examples, libraries, sample projects, and Workspace/MCP tools | Descriptions and latest observed commit dates recorded in the guide; linked for discovery only, no code or prose copied; license assessment is required before reuse |

The [Google Business Profile Reviews Monitor](https://github.com/abhi-ai-marketing/google-business-profile-reviews-monitor-workflow) was noted as prior art but not used as a code source because no license was identified during prior review. No third-party code or prose has been copied or adapted.

## Contributor rule

When third-party material is added later, record its author, URL, license, version or commit, affected files, and whether it was copied, adapted, or consulted only. Preserve required notices. Do not copy from a repository without a compatible explicit license or direct permission.

