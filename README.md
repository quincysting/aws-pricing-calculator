# AWS Pricing Calculator Skill

Generate shareable [AWS Pricing Calculator](https://calculator.aws) URLs from architecture descriptions, blog posts, or solution documents — ready for MAP (Migration Acceleration Program) funding applications, customer proposals, and internal cost reviews.

**How is this different from the AWS Pricing MCP?** The AWS Pricing MCP looks up unit prices (e.g., "$0.0416/hr for m5.xlarge"). This skill goes end-to-end: it discovers calculator schemas, looks up prices, builds the full estimate JSON with `calculationComponents`, and POSTs to the AWS Save API to produce a shareable calculator URL that stakeholders can open, review, and edit in the browser.

## Install

```bash
npx skills add quincysting/aws-pricing-calculator
```

## Prerequisites

| Prerequisite | Required For | Notes |
|---|---|---|
| Python 3 | CLI scripts | stdlib only, no `pip install` needed |
| curl | CLI scripts | avoids Python SSL issues with CloudFront |
| [AWS Pricing MCP Server](https://github.com/awslabs/mcp/tree/main/src/aws-pricing-mcp-server) | Skill workflow | `get_pricing` for real price lookups |

The CLI scripts work standalone without the MCP (you provide costs manually in the spec), but the full `/aws-pricing-calculator` skill workflow requires it for automatic price lookups.

## What It Does

1. **Extracts services** from architecture docs, blog posts, or descriptions
2. **Discovers schemas** from live AWS calculator service definitions
3. **Looks up real pricing** via AWS Pricing API
4. **Builds estimate JSON** with correct `calculationComponents`
5. **Saves to AWS** and returns a shareable calculator URL

## Supported Services

These tiers describe how the generated calculator URL behaves in the browser, not usage limits.
You can include as many services as you want in an estimate.

**Tier 1 (fully editable):** EC2, EBS, Flink, S3, Secrets Manager
- Opens normally in the calculator — users can click and edit all fields
- Uses simple `calculationComponents` format with proven, stable schemas

**Tier 2 (may show read-only):** AppStream, RDS Oracle, MSK, OpenSearch
- May show a blue "read-only" warning banner in the calculator UI
- Costs still display correctly, users just cannot edit fields inline
- Uses `columnFormIPM` format which is sensitive to version changes

**Other services:** The skill can discover schemas for all 430+ AWS services
via `calc_discover.py`. Services not listed above have not been pre-tested,
so their `calculationComponents` format is not yet documented.

## Usage

Invoke via `/aws-pricing-calculator` or use trigger phrases:

- "Create an AWS cost estimate for this architecture"
- "Generate a pricing calculator URL for this blog post"
- "Cost this architecture on AWS"

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/calc_utils.py` | Shared curl helpers, UUID, constants, region map |
| `scripts/calc_discover.py` | Fetch service defs, extract configurable components |
| `scripts/calc_build.py` | Build estimate JSON from a spec file |
| `scripts/calc_save.py` | POST to Save API, return shareable URL |

## Standalone CLI

```bash
# Discover service schemas
python3 scripts/calc_discover.py ec2Enhancement amazonS3

# List all available services
python3 scripts/calc_discover.py --list

# Build estimate from spec
python3 scripts/calc_build.py spec.json -o estimate.json

# Save and get calculator URL
python3 scripts/calc_save.py estimate.json
```

## License

MIT
