FIELDS = [
    "Company Name", "Address", "Services",
    "Costing", "who has signed the contract", "Expiry/ termination or end date",
    "Termination Clause"
]

def build_prompt(text: str) -> str:
    return (
        "You are a contract parser. Extract the following fields from the contract carefully and accurately:\n" +
        "\n".join(f"- {f}" for f in FIELDS) +
        "\nReturn JSON only.\n\nCONTRACT:\n" + text
    )
