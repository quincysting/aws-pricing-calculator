# AWS Pricing Calculator Skill

Generate shareable [AWS Pricing Calculator](https://calculator.aws) URLs from architecture descriptions, blog posts, or solution documents.

## Install

```bash
npx skills add quincysting/aws-pricing-calculator
```

## What It Does

1. **Extracts services** from architecture docs, blog posts, or descriptions
2. **Discovers schemas** from live AWS calculator service definitions
3. **Looks up real pricing** via AWS Pricing API
4. **Builds estimate JSON** with correct `calculationComponents`
5. **Saves to AWS** and returns a shareable calculator URL

## Supported Services

**Tier 1 (fully editable):** EC2, EBS, Flink, S3, Secrets Manager

**Tier 2 (may show read-only):** AppStream, RDS Oracle, MSK, OpenSearch

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
python scripts/calc_discover.py ec2Enhancement amazonS3

# List all available services
python scripts/calc_discover.py --list

# Build estimate from spec
python scripts/calc_build.py spec.json -o estimate.json

# Save and get calculator URL
python scripts/calc_save.py estimate.json
```

## License

MIT
