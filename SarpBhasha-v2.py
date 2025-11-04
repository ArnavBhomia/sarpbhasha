import customtkinter as ctk
from deep_translator import GoogleTranslator
from gtts import gTTS
from playsound import playsound
import pyperclip
import os
import sys

# main application window
app = ctk.CTk()
app.title("SarpBhasha")
app.geometry("900x700") # window size
ctk.set_appearance_mode("light")  # default appearance

# language data
languages = ["English", "Spanish", "French", "German", "Hindi", "Chinese (simplified)", "Japanese"]
lang_codes = {
    "English": "en", 
    "Spanish": "es", 
    "French": "fr", 
    "German": "de", 
    "Hindi": "hi", 
    "Chinese (simplified)": "zh-CN", 
    "Japanese": "ja"
}
source_languages = ["Auto Detect"] + languages
target_languages = languages

# custom fonts
APP_FONT_FAMILY = "Arial"

# font size
combo_font = ctk.CTkFont(family=APP_FONT_FAMILY, size=int(14 * 1.5))
swap_font = ctk.CTkFont(family=APP_FONT_FAMILY, size=int(16 * 1.5))
text_box_font = ctk.CTkFont(family=APP_FONT_FAMILY, size=int(14 * 2))
button_font = ctk.CTkFont(family=APP_FONT_FAMILY, size=int(14 * 1.5))

# title font
title_font = ctk.CTkFont(family=APP_FONT_FAMILY, size=24, weight="bold")

# pyinstaller helper function
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# code to load the icon
icon_path = resource_path("SarpBhasha-Logo.ico")
app.iconbitmap(icon_path)

# core functions

def toggle_mode():
    """Toggles between light and dark mode."""
    if mode_switch.get() == 1: # 1 is 'on'
        ctk.set_appearance_mode("dark")
    else: # 0 is 'off'
        ctk.set_appearance_mode("light")

def handle_translate():
    original_text = source_text.get("1.0", "end-1c")
    if not original_text.strip():
        return
    source_lang_str = source_lang_combo.get()
    target_lang_str = target_lang_combo.get()
    src_code = "auto" if source_lang_str == "Auto Detect" else lang_codes[source_lang_str]
    tgt_code = lang_codes[target_lang_str]
    target_text.delete("1.0", "end")
    try:
        translated_text = GoogleTranslator(source=src_code, target=tgt_code).translate(original_text)
        target_text.insert("1.0", translated_text)
    except Exception as e:
        target_text.insert("1.0", f"Error: No internet connection or service issue.\n\nDetails: {e}")

def handle_swap():
    src = source_text.get("1.0", "end-1c")
    tgt = target_text.get("1.0", "end-1c")
    source_text.delete("1.0", "end")
    target_text.delete("1.0", "end")
    source_text.insert("1.0", tgt)
    target_text.insert("1.0", src)
    src_lang = source_lang_combo.get()
    tgt_lang = target_lang_combo.get()
    if src_lang != "Auto Detect" and tgt_lang in source_languages:
        source_lang_combo.set(tgt_lang)
        target_lang_combo.set(src_lang)

def handle_clear():
    source_text.delete("1.0", "end")
    target_text.delete("1.0", "end")

def handle_copy(target_widget):
    text = target_widget.get("1.0", "end-1c")
    if text.strip():
        pyperclip.copy(text)

def handle_listen(target_widget, lang_key_str):
    text = target_widget.get("1.0", "end-1c")
    if not text.strip():
        return
    try:
        lang_str = lang_key_str.get()
        lang_code = 'en' if lang_str == "Auto Detect" else lang_codes[lang_str]
        tts = gTTS(text=text, lang=lang_code, slow=False)
        temp_file = "speech.mp3"
        tts.save(temp_file)
        playsound(temp_file)
        os.remove(temp_file)
    except Exception as e:
        print(f"TTS Error: {e}")

# graphic user interface (gui) components

# main frame
main_frame = ctk.CTkFrame(app)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# configure the main_frame's grid: 3 columns
main_frame.grid_columnconfigure((0, 2), weight=1) 
main_frame.grid_columnconfigure(1, weight=0)
main_frame.grid_rowconfigure(2, weight=1) 

# row 0: title & dark mode toggle
title_label = ctk.CTkLabel(main_frame, text="SarpBhasha", font=title_font)
title_label.grid(row=0, column=0, columnspan=3, pady=10, padx=10)

mode_switch = ctk.CTkSwitch(main_frame, text="Dark Mode", command=toggle_mode)
mode_switch.grid(row=0, column=2, sticky="ne", padx=10, pady=10) # top right corner
mode_switch.deselect() # initial state is light mode

# row 1: language selectors
combo_height = int(28 * 1.5)
combo_width = int(200 * 1.5)

source_lang_combo = ctk.CTkComboBox(main_frame, 
                                      values=source_languages, 
                                      width=combo_width, 
                                      height=combo_height,
                                      font=combo_font)
source_lang_combo.grid(row=1, column=0, pady=10) 
source_lang_combo.set("Auto Detect")

swap_button_size = int(28 * 1.5)
swap_button = ctk.CTkButton(main_frame, 
                            text="🔁", 
                            command=handle_swap,
                            width=swap_button_size, 
                            height=swap_button_size, 
                            font=swap_font,
                            fg_color="#1c1c84",
                            hover_color="#000068",
                            corner_radius=10) 
swap_button.grid(row=1, column=1, pady=10, padx=20) 

target_lang_combo = ctk.CTkComboBox(main_frame, 
                                      values=target_languages, 
                                      width=combo_width, 
                                      height=combo_height,
                                      font=combo_font)
target_lang_combo.grid(row=1, column=2, pady=10) 
target_lang_combo.set("English")

# row 2: text boxes
source_text = ctk.CTkTextbox(main_frame, 
                             wrap="word", 
                             corner_radius=16, 
                             font=text_box_font) 
source_text.grid(row=2, column=0, sticky="nsew", padx=(10,5), pady=10)

target_text = ctk.CTkTextbox(main_frame, 
                             wrap="word", 
                             corner_radius=16, 
                             font=text_box_font) 
target_text.grid(row=2, column=2, sticky="nsew", padx=(5,10), pady=10)

# row 3: translate and clear buttons
button_height = int(28 * 1.5)

translate_button = ctk.CTkButton(main_frame, 
                                   text="Translate", 
                                   command=handle_translate,
                                   height=button_height,
                                   font=button_font,
                                   fg_color="#00674F",
                                   hover_color="#0A3C30")
translate_button.grid(row=3, column=0, sticky="ew", padx=10, pady=10) 

clear_button = ctk.CTkButton(main_frame, 
                               text="Clear", 
                               command=handle_clear,
                               height=button_height,
                               font=button_font,
                               fg_color="#9B111E",
                               hover_color="#790E18")
clear_button.grid(row=3, column=2, sticky="ew", padx=10, pady=10) 

# row 4: listen and copy buttons
source_actions_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
source_actions_frame.grid(row=4, column=0, sticky="ew", padx=10)

source_listen_button = ctk.CTkButton(source_actions_frame,
                                     text="Listen",
                                     command=lambda: handle_listen(source_text, source_lang_combo),
                                     font=button_font,
                                     fg_color="#536878",
                                     hover_color="#36454f")
source_listen_button.pack(side="left", padx=5, pady=5) 

source_copy_button = ctk.CTkButton(source_actions_frame,
                                   text="Copy",
                                   command=lambda: handle_copy(source_text),
                                   font=button_font,
                                   fg_color="#6e7f80",
                                   hover_color="#586566")
source_copy_button.pack(side="left", padx=5, pady=5) 

target_actions_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
target_actions_frame.grid(row=4, column=2, sticky="ew", padx=10)
target_actions_frame.grid_columnconfigure(0, weight=1) 

target_copy_button = ctk.CTkButton(target_actions_frame,
                                   text="Copy",
                                   command=lambda: handle_copy(target_text),
                                   font=button_font,
                                   fg_color="#6e7f80",
                                   hover_color="#586566")
target_copy_button.pack(side="right", padx=5, pady=5) 

target_listen_button = ctk.CTkButton(target_actions_frame,
                                     text="Listen",
                                     command=lambda: handle_listen(target_text, target_lang_combo),
                                     font=button_font,
                                     fg_color="#536878",
                                     hover_color="#36454f")
target_listen_button.pack(side="right", padx=5, pady=5) 


# run application
app.mainloop()
