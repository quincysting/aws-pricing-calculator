# Troubleshooting

## $0.00 Cost Display

**Symptom:** Calculator URL opens but all services show $0.00.

**Cause:** Empty `calculationComponents` or missing `serviceCost.monthly`.

**Fix:**
1. Ensure `calculationComponents` is fully populated (not `{}`)
2. Ensure `serviceCost.monthly` contains the pre-calculated cost
3. The calculator does NOT recalculate costs on load — it displays `serviceCost.monthly` as-is

## Read-Only Warning

**Symptom:** Blue bar warning: "One or more services in your estimate are not
compatible with the latest calculator release(s) and are available as read-only."

**Causes:**
1. **Version mismatch:** `version` field doesn't match the current service definition version
2. **`columnFormIPM` format mismatch:** The column form structure doesn't match what the calculator expects
3. **Deprecated service fields:** Using old field names or removed options

**Fix:**
1. Always fetch the current version via `calc_discover.py` before building
2. For `columnFormIPM` services (AppStream, RDS, MSK, OpenSearch), use the exact
   format from `service_formats.md` — these are the most sensitive to format changes
3. Tier 2 services (AppStream, RDS Oracle, MSK, OpenSearch) are more likely to
   show read-only due to `columnFormIPM` complexity

**Note:** Read-only services still display correct costs, they just can't be
edited in the calculator UI. This is acceptable for cost presentation purposes.

## Python SSL Errors

**Symptom:** `ssl.SSLCertVerificationError` or `urllib.error.URLError` when
fetching CloudFront URLs with Python `requests` or `urllib`.

**Cause:** Python 3.14 changed SSL certificate handling, breaking connections
to some CloudFront distributions.

**Fix:** Always use `curl` subprocess via `calc_utils.curl_get()` and
`calc_utils.curl_post()`. These bypass Python's SSL stack entirely.

## Version Mismatch

**Symptom:** Services appear but show unexpected behavior or read-only warning.

**Cause:** Hardcoded version numbers that have since been updated.

**Fix:** Always fetch the current version from the service definition:
```python
from calc_discover import discover_service
schema = discover_service("ec2Enhancement")
current_version = schema["version"]  # e.g., "0.0.68"
```

## Save API Errors

**Symptom:** `curl_post` raises an error or returns unexpected response.

**Common causes:**
1. Missing Origin/Referer headers (CORS error)
2. Malformed JSON in the estimate
3. Estimate too large (unlikely but possible)

**Fix:**
1. Ensure using `calc_utils.curl_post()` which includes required headers
2. Validate JSON with `json.loads(json.dumps(estimate))` before sending
3. Check that all UUID fields are valid strings

## Service Code Not Found

**Symptom:** `calc_discover.py` returns 404 or empty response for a service code.

**Fix:**
1. Run `calc_discover.py --list` to see all valid service codes
2. Service codes are case-sensitive and use camelCase (e.g., `ec2Enhancement`, not `EC2` or `ec2`)
3. Common non-obvious service codes:
   - EC2 -> `ec2Enhancement`
   - AppStream -> `amazonAppStream`
   - EBS -> `amazonElasticBlockStore`
   - Flink -> `amazonKinesisDataAnalytics`
   - OpenSearch -> `amazonElasticsearchService`
   - Secrets Manager -> `awsSecretsManager`
