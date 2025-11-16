from collections import defaultdict
from typing import List, Dict, Any

def merge_field_outputs(pages: List[Dict[str, Any]]) -> Dict[str, Any]:
    merged = {
        "Company Name": "",
        "Address": "",
        "Services provided by the company": defaultdict(list),
        "Costing of services provided by company": {
            "Total Estimated Annual Cost": "",
            "Payment Terms": ""
        },
        "Who has signed the contract": {
            "Company": {"Name": "", "Title": ""},
            "Client": {"Name": "", "Title": ""}
        },
        "Expiry / Termination / End Date of contract": "",
        "Termination Clause of the contract": ""
    }

    for page in pages:
        if not isinstance(page, dict):
            continue

        # Simple fields (only if not already set)
        for key in [
            "Company Name",
            "Address",
            "Expiry / Termination / End Date of contract",
            "Termination Clause of the contract"
        ]:
            if page.get(key) and not merged[key]:
                merged[key] = page[key]

        # Merge services
        services = page.get("Services provided by the company", {})
        for category, points in services.items():
            if isinstance(points, list):
                existing = merged["Services provided by the company"][category]
                merged["Services provided by the company"][category] = list(set(existing + points))

        # Merge costing
        costing = page.get("Costing of services provided by company", {})
        for key, val in costing.items():
            if key in ["Total Estimated Annual Cost", "Payment Terms"]:
                if val and not merged["Costing of services provided by company"].get(key):
                    merged["Costing of services provided by company"][key] = val
            elif isinstance(val, dict):
                merged_service = merged["Costing of services provided by company"].setdefault(key, {})
                for subkey in ["Cost (Monthly)", "Billing Cycle"]:
                    if val.get(subkey) and not merged_service.get(subkey):
                        merged_service[subkey] = val[subkey]

        # Merge signers
        signers = page.get("Who has signed the contract", {})
        for party in ["Company", "Client"]:
            party_info = signers.get(party, {})
            if party_info.get("Name") and not merged["Who has signed the contract"][party]["Name"]:
                merged["Who has signed the contract"][party]["Name"] = party_info["Name"]
            if party_info.get("Title") and not merged["Who has signed the contract"][party]["Title"]:
                merged["Who has signed the contract"][party]["Title"] = party_info["Title"]

    # Convert defaultdict to dict
    merged["Services provided by the company"] = dict(merged["Services provided by the company"])
    return merged
