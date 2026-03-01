#!/usr/bin/env python3
"""
Shared utilities for AWS Pricing Calculator automation.

Provides curl-based HTTP helpers (avoids Python SSL issues with CloudFront),
UUID generation, API endpoint constants, and region code mapping.
"""

import json
import subprocess
import uuid

# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------
MANIFEST_URL = "https://d1qsjq9pzbk1k6.cloudfront.net/manifest/en_US.json"
SERVICE_DEF_URL = "https://d1qsjq9pzbk1k6.cloudfront.net/data/{code}/en_US.json"
SAVE_API = "https://dnd5zrqcec4or.cloudfront.net/Prod/v2/saveAs"
CALCULATOR_URL = "https://calculator.aws/#/estimate?id={key}"

# ---------------------------------------------------------------------------
# Region Mapping
# ---------------------------------------------------------------------------
REGION_NAMES = {
    "us-east-1": "US East (N. Virginia)",
    "us-east-2": "US East (Ohio)",
    "us-west-1": "US West (N. California)",
    "us-west-2": "US West (Oregon)",
    "ap-southeast-1": "Asia Pacific (Singapore)",
    "ap-southeast-2": "Asia Pacific (Sydney)",
    "ap-northeast-1": "Asia Pacific (Tokyo)",
    "ap-northeast-2": "Asia Pacific (Seoul)",
    "ap-south-1": "Asia Pacific (Mumbai)",
    "eu-west-1": "Europe (Ireland)",
    "eu-west-2": "Europe (London)",
    "eu-central-1": "Europe (Frankfurt)",
    "eu-north-1": "Europe (Stockholm)",
    "sa-east-1": "South America (Sao Paulo)",
    "ca-central-1": "Canada (Central)",
    "af-south-1": "Africa (Cape Town)",
    "me-south-1": "Middle East (Bahrain)",
}

HOURS_PER_MONTH = 730


def region_name(region_code):
    """Map AWS region code to display name."""
    return REGION_NAMES.get(region_code, region_code)


def make_uuid():
    """Generate a random UUID string."""
    return str(uuid.uuid4())


def curl_get(url, timeout=30):
    """Fetch URL via curl subprocess (avoids Python SSL issues with CloudFront)."""
    result = subprocess.run(
        ["curl", "-s", url],
        capture_output=True, text=True, timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl GET failed for {url}: {result.stderr}")
    return json.loads(result.stdout)


def curl_post(url, data, timeout=30):
    """POST JSON via curl subprocess with required calculator headers."""
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST", url,
            "-H", "Content-Type: application/json",
            "-H", "Origin: https://calculator.aws",
            "-H", "Referer: https://calculator.aws/",
            "-d", json.dumps(data),
        ],
        capture_output=True, text=True, timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl POST failed: {result.stderr}")
    return json.loads(result.stdout)
