import requests
import zipfile
import os
from utils import get_ai_response, send_answer

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
    text_files = []
    png_files = []
    mp3_files = []

    for file in os.listdir(directory):
        if file.endswith(".txt"):
            text_files.append(os.path.join(directory, file))
        elif file.endswith(".png"):
            png_files.append(os.path.join(directory, file))
        elif file.endswith(".mp3"):
            mp3_files.append(os.path.join(directory, file))
    
    return text_files, png_files, mp3_files

def main():
    url = "https://centrala.ag3nts.org/dane/pliki_z_fabryki.zip"
    
    zip_path = download_file(url)
    if not zip_path:
        return
    
    extract_path = extract_zip(zip_path)
    if not extract_path:
        return
        
    txt_files, png_files, mp3_files = sort_files_by_type(extract_path)
    print(f"Znaleziono:\n{len(txt_files)} plików TXT\n{len(png_files)} plików PNG\n{len(mp3_files)} plików MP3")

if __name__ == "__main__":
    main()