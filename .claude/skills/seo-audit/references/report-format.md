# findings.json

```json
{
  "site": "client-store",
  "url": "https://example.com",
  "date": "2026-11-12",
  "platform": "shopify",
  "mode": "report-only | fix-preview | fix-admin-prep",
  "access": {"link": true, "password_protected": false, "code": false, "admin": false, "written_permission": false},
  "preview_link": true,
  "pages_audited": ["https://example.com/", "..."],
  "not_checked": ["Speed (Lighthouse not run)", "..."],
  "summary": "Plain-language paragraph.",
  "recommendations": ["Top action 1", "Top action 2"],
  "findings": [
    {"page": "https://example.com/", "check": "Meta description", "found": "Missing", "why": "Google may show random text.",
     "action": "Write a 70 to 160 character description.", "severity": "Medium",
     "label": "Done in the admin", "steps": ["Admin > ... (menu names may differ)"], "to_confirm": false}
  ]
}
```
`label` must be one of: `We fix`, `Done in the admin`, `Platform limit`, `Client's decision`. `severity`: `High`, `Medium`, `Low`. Add `workaround` for a Platform limit. `found` must come from the collected facts.
