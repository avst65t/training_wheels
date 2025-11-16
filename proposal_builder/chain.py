import json
import subprocess
from openai import OpenAI

client = OpenAI()

# -------------------
# 1. Helper to call LLM
# -------------------
def run_llm(prompt: str, model="gpt-4.1-mini") -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return resp.choices[0].message.content


# -------------------
# 2. Pipeline steps
# -------------------
def step1_requirements(transcription: str) -> dict:
    prompt = f"""
    Extract requirements from this transcription:
    {transcription}

    Return JSON like:
    {{
      "services": ["..."],
      "nodes": ["..."],
      "edges": [ ["nodeA", "nodeB"] ]
    }}
    """
    return json.loads(run_llm(prompt))


def step2_diagram_json(requirements: dict) -> dict:
    prompt = f"""
    Convert these requirements into a diagram JSON with coordinates:

    {json.dumps(requirements, indent=2)}

    Format:
    {{
      "nodes": [
        {{"id": "node1", "label": "Service A", "x": 100, "y": 200}},
        {{"id": "node2", "label": "Service B", "x": 400, "y": 200}}
      ],
      "edges": [
        {{"from": "node1", "to": "node2"}}
      ]
    }}
    """
    return json.loads(run_llm(prompt))


def step3_generate_pptx_code(diagram_json: dict) -> str:
    prompt = f"""
    Generate Python code using python-pptx to draw this diagram:

    {json.dumps(diagram_json, indent=2)}

    Requirements:
    - Create a blank slide
    - Add rectangles for nodes at (x, y) scaled reasonably
    - Add connectors for edges
    - Save file as "proposal_diagram.pptx"
    - Do not include imports, only the code body
    """
    return run_llm(prompt)


# -------------------
# 3. Runner
# -------------------
if __name__ == "__main__":
    transcription = """
    Our proposal includes a frontend service, a backend API, and a database.
    The frontend connects to the backend API, and the backend API connects to the database.
    """

    print("Step 1: Requirements extraction...")
    requirements = step1_requirements(transcription)

    print("Step 2: Diagram JSON generation...")
    diagram_json = step2_diagram_json(requirements)

    print("Step 3: PPTX code generation...")
    pptx_code = step3_generate_pptx_code(diagram_json)

    # Save generated code
    with open("generate_pptx.py", "w") as f:
        f.write("from pptx import Presentation\n")
        f.write("from pptx.util import Inches, Pt\n")
        f.write("import json\n\n")
        f.write(pptx_code)

    print("Running generated PPTX code...")
    subprocess.run(["python", "generate_pptx.py"], check=True)

    print("✅ Proposal diagram saved as proposal_diagram.pptx")
