# Factory Reports Analysis

## What This Script Does
This script is designed to process daily reports from a factory. These reports are in different formats (TXT, PNG, MP3) and contain a mix of technical data and security notes. The goal of the script is to identify and categorize specific information:

1. **Captured Individuals or Traces of Their Presence:**
   - Extracts details about people who were captured or evidence of their activities.

2. **Hardware Repairs:**
   - Focuses on fixed hardware issues while ignoring software-related problems.

3. **File Exclusions:**
   - Skips irrelevant files, including those in the "facts" folder.

The script outputs a structured JSON file that categorizes the identified information:
```json
{
    "people": ["file1.txt", "file2.mp3", "fileN.png"],
    "hardware": ["file4.txt", "file5.png", "file6.mp3"]
}
```

## How It Works
- **Download and Extraction:**
  - Retrieves a ZIP file containing the factory data and extracts its contents.
- **File Categorization:**
  - Processes text files, images, and audio recordings to identify relevant information.
  - Uses AI models to analyze content and determine if it pertains to the task.
- **Result Compilation:**
  - Generates an organized JSON file with categorized results.

## Requirements
- **Python Version:**
  - Python 3.7 or higher.
- **Dependencies:**
  - Install required packages with:
    ```bash
    pip install -r requirements.txt
    ```
- **API Keys:**
  - Add your keys to a `.env` file:
    - `GROQ_API_KEY` for transcription.
    - `OPENAI_API_KEY` for analysis.
    - `REPORT_API_KEY` for result submission.

## Who This Script Is For
This script is ideal for anyone needing to:
- Process large sets of mixed-format data.
- Use AI to extract meaningful insights from text, images, and audio.
- Organize and categorize information efficiently.
