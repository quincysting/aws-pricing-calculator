#!/usr/bin/env python3
"""
Build AWS Pricing Calculator estimate JSON from a spec file.

Spec format (JSON):
{
  "name": "My Estimate",
  "groups": [
    {
      "name": "Production",
      "services": [
        {
          "serviceCode": "ec2Enhancement",
          "serviceName": "Amazon EC2",
          "estimateFor": "template",
          "version": "0.0.68",
          "region": "us-east-1",
          "monthlyCost": 175.20,
          "configSummary": "1x m5.xlarge Linux On-Demand",
          "calculationComponents": { ... }
        }
      ]
    }
  ]
}

Usage:
  python calc_build.py spec.json
  python calc_build.py spec.json -o estimate.json
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from calc_utils import make_uuid, region_name
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from calc_utils import make_uuid, region_name


def build_service(service_code, estimate_for, version, region,
                  calculation_components, monthly_cost, service_name=None,
                  config_summary=""):
    """Build a single service entry for the estimate."""
    return {
        "calculationComponents": calculation_components,
        "serviceCode": service_code,
        "region": region,
        "estimateFor": estimate_for,
        "version": version,
        "description": None,
        "serviceCost": {"monthly": round(monthly_cost, 2), "upfront": 0},
        "serviceName": service_name or service_code,
        "regionName": region_name(region),
        "configSummary": config_summary,
    }


def build_group(name, services_list):
    """Build a group from a list of service dicts. Returns (group_id, group_dict)."""
    services = {}
    group_monthly = 0.0

    for svc_spec in services_list:
        sid = f"{svc_spec['serviceCode']}-{make_uuid()}"
        svc = build_service(
            service_code=svc_spec["serviceCode"],
            estimate_for=svc_spec["estimateFor"],
            version=svc_spec["version"],
            region=svc_spec.get("region", "us-east-1"),
            calculation_components=svc_spec["calculationComponents"],
            monthly_cost=svc_spec.get("monthlyCost", 0),
            service_name=svc_spec.get("serviceName"),
            config_summary=svc_spec.get("configSummary", ""),
        )
        services[sid] = svc
        group_monthly += svc_spec.get("monthlyCost", 0)

    gid = f"grp-{make_uuid()}"
    group = {
        "name": name,
        "services": services,
        "groups": {},
        "groupSubtotal": {},
        "totalCost": {"monthly": round(group_monthly, 2), "upfront": 0},
    }
    return gid, group


def build_estimate(name, groups_list):
    """Build the full estimate envelope from a list of (group_name, services_list) tuples."""
    groups = {}
    total_monthly = 0.0

    for group_name, services_list in groups_list:
        gid, group = build_group(group_name, services_list)
        groups[gid] = group
        total_monthly += group["totalCost"]["monthly"]

    return {
        "name": name,
        "services": {},
        "groups": groups,
        "groupSubtotal": {},
        "totalCost": {"monthly": round(total_monthly, 2), "upfront": 0},
        "support": {},
        "metaData": {
            "locale": "en_US",
            "currency": "USD",
            "createdOn": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "source": "calculator-platform",
        },
    }


def build_from_spec(spec_path):
    """Read a JSON spec file and build the estimate dict."""
    with open(spec_path, "r") as f:
        spec = json.load(f)

    groups_list = []
    for group in spec.get("groups", []):
        groups_list.append((group["name"], group["services"]))

    return build_estimate(spec.get("name", "Estimate"), groups_list)


def main():
    parser = argparse.ArgumentParser(
        description="Build AWS Pricing Calculator estimate from spec JSON",
    )
    parser.add_argument("spec", help="Path to spec JSON file")
    parser.add_argument("-o", "--output", help="Output estimate JSON path")
    args = parser.parse_args()

    estimate = build_from_spec(args.spec)

    total = estimate["totalCost"]["monthly"]
    total_services = sum(len(g["services"]) for g in estimate["groups"].values())
    print(f"Estimate: {estimate['name']}")
    print(f"Groups: {len(estimate['groups'])}")
    print(f"Services: {total_services}")
    print(f"Monthly: ${total:,.2f}")
    print(f"Annual:  ${total * 12:,.2f}")
    print()
    for gid, g in estimate["groups"].items():
        print(f"  {g['name']}: ${g['totalCost']['monthly']:,.2f}/mo")
        for sid, svc in g["services"].items():
            print(f"    - {svc['serviceName']}: ${svc['serviceCost']['monthly']:,.2f}/mo")

    output_path = args.output or args.spec.replace(".json", "_estimate.json")
    with open(output_path, "w") as f:
        json.dump(estimate, f, indent=2)
    print(f"\nSaved: {output_path}")


if __name__ == "__main__":
    main()
