# DeeplTkinterUI
This is a Python application that provides a graphical user interface (GUI) for translating text using the Deepl CLI module(unofficial). It utilizes the Tkinter library to create the GUI elements and interacts with various file formats such as PDF, CSV, Word, and Text files.

Thanks to [Deepl CLI (because I can't get an api key because of where I live.)](https://github.com/eggplants/deepl-cli)
and [Azure theme for more modern GUI appearance](https://github.com/rdbende/Azure-ttk-theme)

![Ekran Görüntüsü (1148)](https://github.com/asaykal/DeeplTkinterUI/assets/46647858/ae91f09a-d605-4191-bdba-eb261d7d8aea)
![Ekran Görüntüsü (1149)](https://github.com/asaykal/DeeplTkinterUI/assets/46647858/a34a9f15-949c-4fa2-ad29-3206618cdc6b)

Required Packages
  - pdfplumber
  - python-docx
  - langdetect
  - deepl-cli

Usage

  1-Clone the repository and navigate to the project directory.
  
  2-Run the app.py file using Python: python app.py.
  
  3-The application window will appear with the following components:
  
    -Text Entry: You can paste or type the text you want to translate in this area.
    -Load File Button: Click this button to load a file (PDF, CSV, Word, or Text) containing the text you want to translate.
    -Convert to CSV Button: If you have loaded a file, this button converts the text to CSV format.
    -Translate Button: Translates the text in the Text Entry field using the selected source and target languages.
    -Save Output as CSV Button: Saves the translated output as a CSV file.
    -Source Language Dropdown: Select the source language of the text.
    -Target Language Dropdown: Select the target language for translation.
    -Output Text: Displays the translated text or error messages.
    -Clear Output Button: Clears the contents of the Output Text field.
