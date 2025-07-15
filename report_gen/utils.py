import os
import re
import config
import template
from langchain_openai import ChatOpenAI
import logging

logger = logging.getLogger(__name__)

def process_md():
    dir=config.MARKDOWN_FILES
    a=os.listdir(dir)
    logger.info(f'Number of markdown files found: {len(a)}')

    content = ""
    for filename in os.listdir(dir):
        if filename.endswith(".md"):
            with open(os.path.join(dir, filename), "r", encoding="utf-8") as f:
                content += f.read() + "\n-------------------------------------------------------------------------------------------------\n"

    return content


def section_division():
    sections = re.findall(r'Section \d+.*?(?=\nSection \d+|\nAppendix|\Z)', template.report_structure, re.DOTALL)
    appendices = re.findall(r'Appendix \d+.*?(?=\nAppendix \d+|\Z)', template.report_structure, re.DOTALL)
    chunk_size = 3
    section_chunks = [sections[i:i + chunk_size] for i in range(0, len(sections), chunk_size)]
    appendix_chunks = [appendices[i:i + 2] for i in range(0, len(appendices), 2)]
    final_chunks = section_chunks + appendix_chunks

    per_section=[]
    for i in final_chunks:
        one_section=''
        for j in i:
            one_section+=j
        per_section.append(one_section)

    return per_section


def summarization(generated_text, summ_llm_model):
    summ_prompt=template.summ_prompt(generated_text)
    response = summ_llm_model.invoke(
        summ_prompt,
    )
    summ_text=response.content
    return summ_text