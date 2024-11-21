import requests
import zipfile
import os
from langfuse.decorators import observe
from langfuse.openai import openai
from dotenv import load_dotenv

load_dotenv()

def download_file(url):
    temp_zip = "pliki_z_fabryki.zip"
    response = requests.get(url)
    with open(temp_zip, 'wb') as f:
        f.write(response.content)
    return temp_zip

def extract_zip(zip_path):
    extract_path = "rozpakowane_pliki"
    if os.path.exists(extract_path):
        for file in os.listdir(extract_path):
            os.remove(os.path.join(extract_path, file))
    else:
        os.makedirs(extract_path)
            
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    os.remove(zip_path)
    return extract_path

def sort_files_by_type(directory):
    txt_files = []
    png_files = []
    mp3_files = []
    
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            txt_files.append(os.path.join(directory, file))
        elif file.endswith(".png"):
            png_files.append(os.path.join(directory, file))
        elif file.endswith(".mp3"):
            mp3_files.append(os.path.join(directory, file))
    
    return txt_files, png_files, mp3_files

@observe()
def analyze_txt_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Przeanalizuj poniższy tekst i określ czy zawiera informacje o: 1) schwytanych ludziach/śladach ich obecności, 2) naprawionych usterkach sprzętowych (hardware). Odpowiedz tylko: 'people', 'hardware' lub 'none'."},
            {"role": "user", "content": content}
        ],
        name="content-classification",
    )
    
    return response.choices[0].message.content.strip().lower(), os.path.basename(file_path)

def main():
    url = os.getenv('FILE_URL')
    zip_path = download_file(url)
    if not zip_path:
        return
    
    extract_path = extract_zip(zip_path)
    if not extract_path:
        return
        
    txt_files, png_files, mp3_files = sort_files_by_type(extract_path)
    print(f"Znaleziono:\n{len(txt_files)} plików TXT\n{len(png_files)} plików PNG\n{len(mp3_files)} plików MP3")
    
    result = {"people": [], "hardware": []}
    
    for txt_file in txt_files:
        category, filename = analyze_txt_content(txt_file)
        if category in ["people", "hardware"]:
            result[category].append(filename)
    
    print(result)
    openai.flush_langfuse()

if __name__ == "__main__":
    main()