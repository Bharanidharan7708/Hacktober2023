import os
import re

def clean_txt_files(directory_path):
    if not os.path.isdir(directory_path):
        print(f"Directory '{directory_path}' not found.")
        return

    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:  
                content = file.read()

                cleaned_content = re.sub(r"[^\w\s%$\n]", "", content)
                cleaned_content = re.sub(r"(\n\s*){2,}", "\n\n", cleaned_content)  

            with open(file_path, "w", encoding="utf-8") as file:  
                file.write(cleaned_content)

            print(f"File '{filename}' cleaned successfully.")

directory_path = r"C:\Users\Lenovo\Desktop\Experiments\Scrapper\test_dir"
clean_txt_files(directory_path)
