from scraper import scrape_and_save
from doc_processing import build_index
from bizbot import run_chatbot

def main():
    print("\nWelcome to BizBot, a helpful assistant to enable you answer anything from a website")
    web_link = input("Enter the website you want to know about: ").strip()

    k_base_name=scrape_and_save(web_link)
    build_index(k_base_name)
    run_chatbot(k_base_name)

if __name__ == "__main__":
    main()
