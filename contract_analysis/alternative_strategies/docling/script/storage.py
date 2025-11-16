def save_text_to_file(text_content: str, filename: str = "output.txt"):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text_content)
        print(f"Text saved to '{filename}'")
    except Exception as e:
        print(f"Error: {e}")
