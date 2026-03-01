#!/usr/bin/env python3
"""
AWS Pricing Calculator service schema discovery.

Fetches live service definitions from CloudFront and extracts all configurable
calculationComponent fields with their IDs, types, options, and defaults.

Usage:
  python calc_discover.py ec2Enhancement amazonS3
  python calc_discover.py --list
  python calc_discover.py ec2Enhancement --schema schema.json
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from calc_utils import curl_get, MANIFEST_URL, SERVICE_DEF_URL
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from calc_utils import curl_get, MANIFEST_URL, SERVICE_DEF_URL

# Component types that represent user-configurable inputs
INPUT_TYPES = {
    "input", "dropdown", "radioButton", "checkBox", "toggle",
    "columnForm", "instanceSearch", "advancedPricingStrategy", "dataTransfer",
}

# Sub-types that are alerts/headers, not real inputs
SKIP_SUBTYPES = {"alert", "headerText", "condition"}


def extract_components(data):
    """Recursively extract all configurable components from a service definition."""
    components = []
    if isinstance(data, dict):
        ctype = data.get("type", "")
        subtype = data.get("subType", "")
        if "id" in data and ctype in INPUT_TYPES and subtype not in SKIP_SUBTYPES:
            components.append(data)
        for v in data.values():
            components.extend(extract_components(v))
    elif isinstance(data, list):
        for item in data:
            components.extend(extract_components(item))
    return components


def get_component_info(comp):
    """Extract key info from a component definition."""
    cid = comp.get("id", "")
    ctype = comp.get("type", "")
    subtype = comp.get("subType", "")
    label = comp.get("label", comp.get("name", ""))

    options = []
    for opt_key in ("options", "dropDownSize"):
        if opt_key in comp:
            for o in comp[opt_key]:
                val = o.get("value", o.get("id", ""))
                lbl = o.get("label", val)
                options.append(f"{val} ({lbl})" if lbl != val else val)

    default = comp.get("initialState", comp.get("defaultValue", ""))
    validations = comp.get("validations", {})

    return {
        "id": cid,
        "type": f"{ctype}/{subtype}" if subtype else ctype,
        "label": label,
        "options": options,
        "default": default,
        "required": validations.get("required", False),
    }


def discover_service(code):
    """Discover a single service schema."""
    defn = curl_get(SERVICE_DEF_URL.format(code=code))

    service_name = defn.get("serviceName", code)
    version = defn.get("version", "?")

    templates = defn.get("templates", [])
    template_id = "?"
    template_version = version
    if templates:
        template_id = templates[0].get("id", "?")
        template_version = templates[0].get("version", version)

    comps = extract_components(defn)

    seen_ids = set()
    unique_comps = []
    for c in comps:
        if c["id"] not in seen_ids:
            seen_ids.add(c["id"])
            unique_comps.append(c)

    comp_infos = [get_component_info(c) for c in unique_comps]

    return {
        "serviceName": service_name,
        "serviceCode": code,
        "templateId": template_id,
        "version": template_version or version,
        "components": comp_infos,
    }


def list_services():
    """List all active configurable services from the manifest."""
    manifest = curl_get(MANIFEST_URL)
    services = manifest.get("awsServices", [])
    return [
        {"serviceCode": s["serviceCode"], "name": s["name"].strip()}
        for s in services
        if s.get("isActive") == "true" and not s.get("disableConfigure", False)
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Discover AWS Pricing Calculator service schemas",
    )
    parser.add_argument("services", nargs="*", help="Service codes to discover")
    parser.add_argument("--list", action="store_true", help="List all active services")
    parser.add_argument("--schema", help="Save schema JSON to file")
    args = parser.parse_args()

    if args.list:
        print("Fetching AWS Pricing Calculator manifest...")
        active = list_services()
        print(f"\nActive configurable services: {len(active)}\n")
        print(f"{'Service Code':<45} {'Service Name'}")
        print("-" * 90)
        for s in sorted(active, key=lambda x: x["name"]):
            print(f"  {s['serviceCode']:<45} {s['name']}")
        return

    if not args.services:
        parser.print_help()
        sys.exit(1)

    all_schemas = {}
    for code in args.services:
        print(f"\nDiscovering: {code}")
        try:
            schema = discover_service(code)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

        all_schemas[code] = schema
        print(f"  Service: {schema['serviceName']}")
        print(f"  Template: {schema['templateId']} (v{schema['version']})")
        print(f"  Components: {len(schema['components'])}")
        print()
        for ci in schema["components"]:
            opts = f"  options: {ci['options'][:5]}" if ci["options"] else ""
            req = " [REQUIRED]" if ci["required"] else ""
            print(f"    {ci['id']:<42} {ci['type']:<25} {ci['label'][:40]}{req}{opts}")

    if args.schema and all_schemas:
        with open(args.schema, "w") as f:
            json.dump(all_schemas, f, indent=2)
        print(f"\nSchema saved to: {args.schema}")


if __name__ == "__main__":
    main()
