def build_prompt_for_image():
#     pmpt = """You are a highly accurate contract analyst that extracts structured fields from **legal contract documents**.

# Your task is to extract structured values **only from the visible content of the current page** of the contract.

# ---
# INSTRUCTIONS:
# 1. Carefully read the entire page.
# 2. Extract only the specified fields below.
# 3. Return only the extracted values in **valid JSON** format.
# 4. Do not include keys if the value is not found. Omit them entirely from the output. Do not use empty strings ("") as placeholders. Output only the fields that were explicitly and clearly found on the page
# 5. Do **not** guess. Return information only if it's **explicitly mentioned**.
# 6. Format nested sections (like costing or signers) using JSON objects or lists as needed.
# 7. No markdown, no explanations — only raw JSON.
# ---

# FIELDS TO EXTRACT: (Do not change key names or formatting. Always return the following fixed field names exactly as shown)

# 1. `"Company Name"`: Must be a formal, registered organization name. If only individuals (e.g., caregivers, clients) are listed, omit this field.

# 2. `"Address"`: Full postal or official address of the company. Prefer the address near the start or end of the document.

# 3. `"Services provided by the company"`: A JSON object where each key is a category or service, and the value is a list of bullet-point style service descriptions under that category.

# 4. `"Costing of services provided by company"`: 
#    - A JSON object with service names as keys. 
#    - Each service contains a nested JSON:
#      - `"Cost (Monthly)"`
#      - `"Billing Cycle"`
#    - Outside the services, also extract:
#      - `"Total Estimated Annual Cost"`
#      - `"Payment Terms"`

# 5. `"Who has signed the contract"`: 
#    - A JSON object with keys: `"Client"` and `"Company"`
#    - Each contains:
#      - `"Name"`: Signer's full name
#      - `"Title"`: Official role

# 6. `"Expiry / Termination / End Date of contract"`: Final validity date or mention of auto-renewal.

# 7. `"Termination Clause of the contract"`: Exact sentence or paragraph describing the termination process.

# ---
# RULES:
# - Output only the fields you find on this page.
# - Skip keys that are not present.
# - JSON only. No extra text or formatting.
# ---
# """
#     return pmpt



  pmpt="""
You are reading one page of a legal contract.
Your job is to extract and return only the clearly visible, explicitly stated values for the fields listed below.


STRICT EXTRACTION RULES:
- Read all visible text carefully.
- Return only what is clearly stated or labeled. Do not guess, paraphrase, or infer.
- Output must be a valid JSON object — no trailing commas, no extra text, no markdown.
- If a field is not explicitly stated, omit it entirely — do not include it with an empty value or null.
- Never treat the signature date as expiry or termination date unless it is clearly labeled as such.
- For nested structures like costing or signers:
- Return only the subfields that are present (e.g., "Name" or "Title")
- Do not skip the whole section if some subfields are missing


SPECIAL RULES:
- "Company Name" must be the company providing services, not the client. Avoid extracting the client name even if it appears more prominently.
- "Address" must be for the company providing services, not the client's address. Even partial addresses (e.g., city, office location) should be extracted if clearly tied to the service provider.
- "Services provided by the company" should include only actual service categories (e.g., "Software Development", "Cloud Support"). Do not include compliance, confidentiality, or legal obligations unless they are framed as actual deliverables.


FIELDS TO EXTRACT: (Use these exact key names)

1. "Company Name": Name of the company giving services (not the client)
2. "Address": Address of the company providing the services
3. "Services provided by the company": JSON object with categories as keys and lists of bullet-point services
4. "Costing of services provided by company":
Each service is a key with:
"Cost (Monthly)"
"Billing Cycle"

Also include:
"Total Estimated Annual Cost"
"Payment Terms"

5. "Who has signed the contract":
JSON object with keys "Client" and "Company", each optionally containing:
"Name"
"Title"

6. "Expiry / Termination / End Date of contract": Only if clearly labeled
7. "Termination Clause of the contract": extract the exact sentence or paragraph that explains how the contract can end

Return only the fields that are clearly present on this page in valid JSON format.
"""
  return pmpt