# import re
# from typing import List

# def split_into_contracts(text: str) -> List[str]:
#     parts = re.split(r"(?m)^(This (?:Agreement|Contract|Lease)[^\n]+)", text)
#     contracts = []
#     for i in range(1, len(parts), 2):
#         contracts.append(parts[i] + parts[i+1])
#     return contracts if contracts else [text]


def chunk_contract(text: str, max_length: int = 300000) -> list:
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) > max_length:
            chunks.append(current_chunk)
            current_chunk = para
        else:
            current_chunk += "\n\n" + para
    if current_chunk:
        chunks.append(current_chunk)
    return chunks
