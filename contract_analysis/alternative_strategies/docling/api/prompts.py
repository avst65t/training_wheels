def build_prompt(text: str) -> str:
    pmpt=f"""You are a highly accurate AI system trained to extract structured fields from legal contracts.

Follow the instructions step-by-step:

---
STEP 1: Read the entire contract carefully.
STEP 2: Search for the following fields. For each, identify the best match from the contract.
STEP 3: Output a clean JSON object with exact field names below.
STEP 4: If a value is not found, use an empty string (""). Do not guess.
STEP 5: For multi-line or nested information (like Costing or Signers), extract as dictionary or list
---

FIELDS TO EXTRACT:
1. "Company Name": Full legal name of the company that is party to the contract.
2. "Address": Official address of the company, typically found at the start or end.
3. "Services provided by the company"
4. "Costing of services provided by company"
5. "Who has signed the contract": Names and titles of individuals who signed from each side.
6. "Expiry / Termination / End Date of contract": Final date of contract validity or automatic renewal clause.
7. "Termination Clause of the contract": Extract full paragraph or sentence that describes how to terminate.

---
RULES:
- OUTPUT ONLY VALID JSON — no extra text, no markdown.
- Do not explain anything.
- Do not hallucinate values.
- Return exactly these 7 keys. No missing, no extra.
---

CONTRACT:
{text}"""
    return (pmpt)
