import tkinter as tk
import csv, functools, pdfplumber

from tkinter import filedialog
from deepl import DeepLCLI
from pdfminer.high_level import extract_text
from docx import Document
from langdetect import detect

button_list = []

def translate_text(part, button):
    start_index = (part - 1) * 3000
    end_index = part * 3000
    input_text = text_entry.get("1.0", "end-1c")[start_index:end_index]

    deepl = DeepLCLI(source_lang.get(), target_lang.get())
    try:
        translated_text = deepl.translate(input_text)
        output_text.insert("end", translated_text + "\n")

    except Exception as e:
        output_text.insert("end", f"Error translating Part {part}\n")
        
    button.destroy()
    activate_next_button(part)

def translate_text_solo():
    input_text = text_entry.get("1.0", "end-1c")
    deepl = DeepLCLI(source_lang.get(), target_lang.get())
    translated_text = deepl.translate(input_text)
    output_text.delete("1.0", "end")
    output_text.insert("end", translated_text + "\n")
        

def button_click_handler(part, button):
    translate_text(part, button)

def activate_next_button(current_part):
    if current_part < len(button_list):
        next_button = button_list[current_part]
        next_button.config(state=tk.NORMAL)

def extract_text_from_csv(file_path):
    encodings = ['utf-8', 'iso-8859-9', 'windows-1254']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                reader = csv.reader(file)
                text = ""
                for row in reader:
                    if len(row) > 0:
                        text += row[0] + "\n" 
                return text
        except UnicodeDecodeError:
            continue
    
    raise ValueError("Unable to decode the CSV file using supported encodings.")
    
def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

def extract_text_from_word(file_path):
    document = Document(file_path)
    paragraphs = document.paragraphs
    text = "\n".join([paragraph.text for paragraph in paragraphs])
    return text

def extract_text_from_txt(file_path):
    with open(file_path, "r") as file:
        text = file.read()
        return text

def detect_language(file_path):
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".csv"):
        text = extract_text_from_csv(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_word(file_path)
    elif file_path.endswith(".txt"):
        text = extract_text_from_txt(file_path)
    else:
        raise ValueError("Invalid file format. Please select a valid PDF, CSV, Word, or Text file.")

    return detect(text)

def load_file():
    file_types = [("PDF Files", "*.pdf"), ("CSV Files", "*.csv"), ("Word Files", "*.docx"), ("Text Files", "*.txt")]
    file_path = filedialog.askopenfilename(filetypes=file_types)
    
    if file_path:
        try:
            source_lang.set(detect_language(file_path))
            target_lang.set("nl") 

            if source_lang.get() == target_lang.get():
                raise ValueError("Source and target languages cannot be the same.")

            if file_path.endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif file_path.endswith(".csv"):
                text = extract_text_from_csv(file_path)
            elif file_path.endswith(".docx"):
                text = extract_text_from_word(file_path)
            elif file_path.endswith(".txt"):
                text = extract_text_from_txt(file_path)
            else:
                raise ValueError("Invalid file format. Please select a valid PDF, CSV, Word, RTF, or Text file.")
                
            text_entry.delete("1.0", "end")
            text_entry.insert("1.0", text)
            clear_parts_and_output()
            button_list.clear()  
            create_part_buttons()
            activate_next_button(0)
            convert_button.config(state=tk.NORMAL)
            
        except Exception as e:
            output_text.insert("end", str(e) + "\n")
        
      
            
def convert_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                text = text_entry.get("1.0", "end-1c")
                lines = text.split("\n")
                writer.writerows([[line] for line in lines])
                output_text.insert("end", "File converted to CSV successfully.\n")
        except Exception as e:
            output_text.insert("end", "Error converting the file to CSV.\n")

def save_output_as_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            output_lines = output_text.get("1.0", "end-1c").split("\n")
            writer.writerows([[line] for line in output_lines])

def clear_parts_and_output():
    for widget in buttons_frame.winfo_children():
        widget.destroy()
    output_text.delete("1.0", "end")

def clear_output():
    output_text.delete("1.0", "end")

def create_button_click_handler(part, button):
    button_click_handler = functools.partial(translate_text, part, button)
    return button_click_handler

def create_part_buttons():
    text = text_entry.get("1.0", "end-1c")
    num_parts = (len(text) + 2999) // 3000

    num_columns = 5
    for part in range(1, num_parts + 1):
        row = (part - 1) // num_columns
        column = (part - 1) % num_columns

        part_button = tk.Button(buttons_frame, text=f"Part {part}", width=10, state=tk.DISABLED)
        button_click_handler = functools.partial(translate_text, part, part_button)
        part_button.configure(command=button_click_handler)
        part_button.grid(row=row, column=column, padx=5, pady=5)
        button_list.append(part_button)

    if button_list:
        button_list[0].config(state=tk.NORMAL)


window = tk.Tk()
window.title("Deepl Translator Tkinter UI")
window.iconbitmap("icon.ico")
window.resizable(False, False)

window.tk.call("source", "azure.tcl")
window.tk.call("set_theme", "dark")

text_entry = tk.Text(window, height=10, width=150)
text_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

load_button = tk.Button(window, text="Load File", command=load_file)
load_button.grid(row=1, column=0, padx=5, pady=5)

convert_button = tk.Button(window, text="Convert to CSV", command=convert_to_csv, state=tk.DISABLED)
convert_button.grid(row=1, column=1, padx=5, pady=5)

translate_button = tk.Button(window, text="Translate", command=translate_text_solo)
translate_button.grid(row=1, column=2, padx=5, pady=5)

save_button = tk.Button(window, text="Save Output as CSV", command=save_output_as_csv)
save_button.grid(row=1, column=3, padx=5, pady=5)

translation_lang_frame = tk.Frame(window)
translation_lang_frame.grid(row=2, column=0, columnspan=4, pady=10)

source_lang_label = tk.Label(translation_lang_frame, text="Source Language:")
source_lang_label.grid(row=0, column=0, padx=5, sticky="e")

source_lang = tk.StringVar()
source_lang.set("auto")  
source_lang_menu = tk.OptionMenu(translation_lang_frame, source_lang, "auto", 'id', 'de', 'en', 'lt', 'fr', 'cs', 'lv', 'pt', 'sl', 'et', 'auto', 'ro', 'zh', 'sk', 'it', 'ko', 'pl', 'el', 'es', 'ru', 'nl', 'tr', 'ja', 'uk', 'bg', 'hu', 'sv', 'da', 'fi')
source_lang_menu.grid(row=0, column=1, padx=5, sticky="w")

target_lang_label = tk.Label(translation_lang_frame, text="Target Language:")
target_lang_label.grid(row=0, column=2, padx=5, sticky="e")

target_lang = tk.StringVar()
target_lang.set("nl")  
target_lang_menu = tk.OptionMenu(translation_lang_frame, target_lang, 'zh', 'it', 'id', 'ko', 'pl', 'el', 'es', 'de', 'en', 'ru', 'nl', 'tr', 'ja', 'lt', 'uk', 'bg', 'fr', 'hu', 'cs', 'lv', 'pt', 'sv', 'sl', 'da', 'fi', 'et', 'ro', 'sk')
target_lang_menu.grid(row=0, column=3, padx=5, sticky="w")

output_text = tk.Text(window, height=10, width=150)
output_text.grid(row=3, column=0, padx=10, pady=10, columnspan=4)

clear_button = tk.Button(window, text="Clear Output", command=clear_output)
clear_button.grid(row=4, column=0, padx=5, pady=5)

buttons_frame = tk.Frame(window)
buttons_frame.grid(row=4, column=1, columnspan=3, padx=5, pady=5)

window.update_idletasks() 

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - window.winfo_width()) // 2
y = (screen_height - window.winfo_height()) // 2

window.geometry(f"+{x}+{y}")

window.mainloop()
