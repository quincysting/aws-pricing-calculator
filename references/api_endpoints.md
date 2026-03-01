# API Endpoints

## CloudFront CDN URLs

All service definitions and the save API are served via CloudFront. Use `curl`
subprocess instead of Python `requests` to avoid SSL certificate issues.

### Manifest (service catalog)
```
GET https://d1qsjq9pzbk1k6.cloudfront.net/manifest/en_US.json
```
Returns `{ "awsServices": [ { "serviceCode", "name", "isActive", ... } ] }`

### Service Definition
```
GET https://d1qsjq9pzbk1k6.cloudfront.net/data/{serviceCode}/en_US.json
```
Returns the full service definition including templates, components, validations.
Key fields: `serviceName`, `version`, `templates[0].id`, `templates[0].version`

### Save API
```
POST https://dnd5zrqcec4or.cloudfront.net/Prod/v2/saveAs
```

**Request:**
```
Content-Type: application/json
Origin: https://calculator.aws
Referer: https://calculator.aws/
Body: <estimate JSON>
```

**Response:**
```json
{
  "statusCode": 200,
  "body": "{\"savedKey\": \"abc123def456\"}"
}
```
Note: `body` is a JSON string that must be parsed separately.

### Calculator URL
```
https://calculator.aws/#/estimate?id={savedKey}
```
Open this URL in a browser to view the estimate. The estimate is publicly
accessible to anyone with the URL (no authentication required).

## Request Headers

The Save API requires these headers to accept the request:
- `Content-Type: application/json` — required
- `Origin: https://calculator.aws` — CORS validation
- `Referer: https://calculator.aws/` — CORS validation

Without the Origin/Referer headers, the API returns a CORS error.

## Rate Limits

No documented rate limits, but be reasonable:
- Service definition fetches: cached, lightweight
- Save API: one call per estimate, creates a permanent URL
- Saved estimates do not expire (as of 2026-03)
