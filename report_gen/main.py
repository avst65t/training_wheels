from langchain_openai import ChatOpenAI
import utils
import template
import config
import time
import logging
from report_generator import create_pdf

def main():
    try:
        s = 1
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        report_content = ""

        llm_model = ChatOpenAI(
            model=config.REPORT_GENERATION_MODEL,
            temperature=config.TEMPERATURE,
            openai_api_key=config.OPENAI_API_KEY,
            openai_api_base=config.OPENAI_BASE_URL,
            streaming=True,
        )

        summ_llm_model = ChatOpenAI(
            model=config.SUMMARIZATION_MODEL,
            temperature=config.TEMPERATURE,
            openai_api_key=config.OPENAI_API_KEY,
            openai_api_base=config.OPENAI_BASE_URL,
            streaming=True,
        )

        logging.info("Initialization done. Report generation process starts!")

        report_structure = template.report_structure
        medical_records = utils.process_md()
        divide_sections = utils.section_division()
        logging.info("Sections preprocessed! Generating medical content now.")

        # for i in range(len(divide_sections)):
        for i in range(2):
            e = s + 1
            per_section = divide_sections[i]

            if s == 1:
                prompt = template.first_prompt(report_structure, per_section, medical_records)
            else:
                prompt = template.iter_full_prompt(s, e, summarized_text, per_section, report_structure, medical_records)

            response = llm_model.invoke(prompt)
            logging.info(f"Response generated! Section {s} to {e} done")

            time.sleep(105)

            summarized_text = utils.summarization(response.content, summ_llm_model)
            s = s + 2
            report_content += response.content + '\n\n\n'

            time.sleep(75)

        with open('raw_content.txt', "w", encoding="utf-8") as f:
            f.write(report_content)

        logging.info("Whole report generated, creating a LaTeX-formatted PDF.")
        create_pdf(config.CHR_FILENAME, report_content)
        logging.info("Report generated successfully!")

    except Exception as e:
        logging.exception("Error during report generation.")

if __name__ == "__main__":
    main()
