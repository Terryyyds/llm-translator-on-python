"""
    An handy AI Translator Tool powered by AI.
    Author: Yu Deng
    Date: 1 September 2023

    OpenAI and tkinter library are required to run this program.
        >> pip install openai
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import traceback
import asyncio
import time
import matplotlib.pyplot as plt
import openai


class TranslatorApp:
    """
    Encapsulate UI in a class to manage UI elements.
    """
    def __init__(self, root):
        """
        initialize the translator app UI.
        """
        self.root = root
        self.api_key = None
        self.api_input = None
        self.openai_api_key = ""
        self.translation_history = []

        # Change window size to fit new layout
        self.root.geometry('650x450')
        self.root.title("AI Translator")

        # Create the main frame container
        mainframe = ttk.Frame(self.root)
        mainframe.pack(fill=tk.BOTH, expand=1)

        # Create left and right panels
        left_panel = ttk.Frame(mainframe)
        right_panel = ttk.Frame(mainframe)

        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Set source text input on the left panel
        self.source_text = tk.Text(left_panel, height=20, width=20)
        self.source_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)
        self.source_text.insert(tk.END, "")

        # Show translation results in the right panel
        self.translated_text = tk.Text(right_panel, height=20, width=20)
        self.translated_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)
        self.translated_text.configure(state='disabled')

        # Create 2 tags to display word count
        self.source_character_count = ttk.Label(left_panel, text="")
        self.source_character_count.pack(side=tk.BOTTOM, fill=tk.X)
        self.translated_character_count = ttk.Label(right_panel, text="")
        self.translated_character_count.pack(side=tk.BOTTOM, fill=tk.X)
        self.source_text.bind("<KeyRelease>", self.update_source_character_count)

        # Buttons and other options are placed below
        options_frame = ttk.Frame(self.root)
        options_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        self.source_lang_label = ttk.Label(options_frame, text="Source Language:")
        self.source_lang_input = ttk.Entry(options_frame, width=15)
        self.source_lang_input.insert(0, "[Auto Detect]")
        self.target_lang_label = ttk.Label(options_frame, text="Target Language:")
        self.target_lang_input = ttk.Combobox(options_frame, values=['English', 'Chinese', 'Spanish', 'Japanese', 'Russian', 'Italian', 'German', 'French', 'Other'])
        self.target_lang_input.set("English")
        self.target_lang_input.bind('<FocusOut>', self.validate_language_input)
        # Buttons
        self.translate_button = ttk.Button(options_frame, text="Translate", command=self.on_translate_click)
        self.api_key_button = ttk.Button(options_frame, text="Set API Key", command=self.on_api_key_click)
        self.history_button = ttk.Button(options_frame, text="History", command=self.show_history)
        self.usage_chart_button = ttk.Button(options_frame, text="Usage Chart", command=self.show_usage_chart)

        # Use grid for layout
        self.source_lang_label.grid(column=0, row=0, padx=5, pady=5, sticky='ew')
        self.source_lang_input.grid(column=1, row=0, padx=5, pady=5, sticky='ew')
        self.target_lang_label.grid(column=2, row=0, padx=5, pady=5, sticky='ew')
        self.target_lang_input.grid(column=3, row=0, padx=5, pady=5, sticky='ew')
        self.translate_button.grid(column=4, row=0, padx=5, pady=5, sticky='ew')
        self.api_key_button.grid(column=0, row=1, padx=5, pady=5, sticky='ew')
        self.history_button.grid(column=2, row=1, padx=5, pady=5, sticky='ew')
        self.usage_chart_button.grid(column=1, row=1, padx=5, pady=5, sticky='ew')

        for i in range(5):
            options_frame.columnconfigure(i, weight=1, uniform="col")
        for i in range(2):
            options_frame.rowconfigure(i, weight=1, uniform="row")

        self.root.configure(padx=10, pady=10)
        self.import_api_key()

    def validate_language_input(self, event=None):
        """
        Verify that the language entered by the user is valid.
        """
        if not self.target_lang_input.get().strip():
            tk.messagebox.showerror("Invalid Input", "Please input a valid target language.")
            self.target_lang_input.set("English")
            return False
        return True


    def on_translate_click(self):
        """
        process translate button click.
        """
        if self.openai_api_key == "": #Handling when API key is empty
            tk.messagebox.showerror("Error", "API Key is empty. Please set your API Key first.")
            return
        if not self.source_text.get("1.0", 'end-1c').strip(): # Handlingtranslation source input is empty.
            tk.messagebox.showerror("Error", "Source text is empty. Please input source text.")
            return
        if not self.validate_language_input(): # Handling when the target language input is empty
            tk.messagebox.showerror("Invalid Input", "Please input a valid target language.")
            return

        # Disable button to prevent users from clicking multiple times
        # display messages being translated
        self.translate_button.config(text="Translating", state="disabled")
        # Start a new thread to avoid blocking the UI
        translate_thread = threading.Thread(target=self.async_translation, daemon=True)
        translate_thread.start()

    def async_translation(self):
        """
        Handle the translation asynchronously.
        """
        # Create a new loop for the new thread
        translation_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(translation_loop)
        try:
            translation_loop.run_until_complete(self.handle_translation())
        finally:
            translation_loop.close()

    async def handle_translation(self):
        """
        The actual asynchronous translation task.
        """
        try:
            # Get the text entered by the user from the source text box
            source_text = self.source_text.get("1.0", tk.END).strip()
            source_language = self.source_lang_input.get()
            target_language = self.target_lang_input.get()

            # Returns the translated string
            translated_text = await self.translate_text(source_text, source_language, target_language)

            # Update translated text boxes
            self.translated_text.configure(state='normal')
            self.translated_text.delete("1.0", tk.END)
            self.translated_text.insert("1.0", translated_text)
            self.translated_text.configure(state='disabled')
            self.update_translated_character_count(translated_text)
            non_space_characters = sum([1 for char in source_text if not char.isspace()])
            # Queries and results saved to history
            history_entry = {
                'source': source_text,
                'translation': translated_text,
                'time': time.strftime("%Y-%m-%d %H:%M:%S"), 
                'source_char_count': non_space_characters,
            }
            self.translation_history.append(history_entry)

        except openai.error.AuthenticationError:
            # If authentication fails, prompt the user
            tk.messagebox.showerror("Error", "Authentication failed. Please check API key.")
        except Exception as e:
            # Other exceptions, displaying error messages to the user
            error_message = "".join(traceback.TracebackException.from_exception(e).format())
            messagebox.showerror("Error", f"An error occurred: {error_message}")

        finally:
            self.translate_button.config(text="Translate", state="normal")

    def on_api_key_click(self):
        """
        process api key button click.
        """
        self.get_api_key_window()

    async def translate_text(self, source_text, source_language, target_language):
        """
        set api parameters.
        """
        prompt = f"Translate the following text to '{target_language}': {source_text}. Provide translated texts only, no other information."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates text. Provide translated texts only, no other information."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        translation = response.choices[0].message.content.strip()
        return translation

    def get_api_key_window(self):
        """
        Open a window to get API key from user input.
        """
        get_api_key_window = tk.Toplevel(self.root)
        get_api_key_window.title("Set API Key")
        get_api_key_window.geometry('250x150')
        api_label = ttk.Label(get_api_key_window, text="Enter your OpenAI API key here:")
        api_label.pack(pady=10)
        self.api_input = ttk.Entry(get_api_key_window)
        self.api_input.pack(pady=10)

        if self.openai_api_key == "":
            self.api_input.insert(0, "")
        else:
            self.api_input.insert(0, self.openai_api_key)

        button_frame = ttk.Frame(get_api_key_window)
        button_frame.pack(fill=tk.X, pady=10)

        save_button = ttk.Button(button_frame, text="Save Key", command=self.set_api_key)
        save_button.pack(side=tk.LEFT, padx=10, expand=True)

        clear_button = ttk.Button(button_frame, text="Test Key", command=self.test_api_key)
        clear_button.pack(side=tk.LEFT, padx=10, expand=True)

        get_api_key_window.lift()


    def test_api_key(self):
        """
        Test the provided OpenAI API key for validity by making a sample API call.
        """
        try:
            # Use user-entered API key
            test_api_key = self.api_input.get()
            openai.api_key = test_api_key
            openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello, who are you?"}
                ],
                max_tokens=5
            )
            tk.messagebox.showinfo("Success", "API key is valid.")

        except openai.error.AuthenticationError:
            tk.messagebox.showerror("Failed", "Authentication failed. Invalid API key.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def set_api_key(self):
        """
        set openai api key.
        """
        try:
            api_key_file = open('api_key.txt', 'w', encoding='utf-8')
            api_key_file.write(self.api_input.get())
            api_key_file.close()
            self.openai_api_key = self.api_input.get()
            openai.api_key = self.openai_api_key
            tk.messagebox.showinfo("Success", "API key is set. ")
        except IOError as e:
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def import_api_key(self):
        """
        Check and import API key from an external file.
        """
        try:
            api_key_file = open('api_key.txt', 'r', encoding='utf-8')
            api_key = api_key_file.read().strip()
            api_key_file.close()
            if not api_key:
                tk.messagebox.showerror("", "API key error. Please set your API Key manually.")
            else:
                self.openai_api_key = api_key
                openai.api_key = self.openai_api_key
        except FileNotFoundError:
            pass
        except IOError as e:
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_source_character_count(self, event):
        """
        Counts the number of words in the text box and updates the label.
        """
        text = self.source_text.get("1.0", tk.END)
        character_count = sum([1 for char in text if not char.isspace()])
        self.source_character_count['text'] = f" · Character Count: {character_count}"

    def update_translated_character_count(self, text):
        """
        Updated word count statistics for translated text.
        """
        character_count = sum([1 for char in text if not char.isspace()])
        self.translated_character_count['text'] = f" · Character Count: {character_count}"

    def show_history(self):
        """
        Creates a new window to display the user's translation history.
        """
        history_window = tk.Toplevel(self.root)
        history_window.title("Translation History")
        scrollbar = ttk.Scrollbar(history_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        history_listbox = tk.Listbox(history_window, yscrollcommand=scrollbar.set, width=80)

        # Add history to the list box
        for entry in self.translation_history:
            history_listbox.insert(tk.END, f"{entry['time']} | {entry['source_char_count']} Characters | {entry['source']} -> {entry['translation']}")

        history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=history_listbox.yview)

    def show_usage_chart(self):
        """
        A line graph showing usage.
        """
        # Check for history
        if not self.translation_history:
            tk.messagebox.showinfo("No data", "No usage data available.")
            return
        # Get all character count records
        char_counts = [record['source_char_count'] for record in self.translation_history]
        plt.figure("Translation Usage Chart")
        plt.title("Character Count per Translation")
        translation_numbers = range(1, len(char_counts) + 1)
        plt.plot(translation_numbers, char_counts, marker='o')
        plt.xlabel("Translation Number")
        plt.ylabel("Number of Characters")
        plt.xticks(translation_numbers)
        plt.yticks(char_counts)
        plt.tight_layout()
        plt.show()

def main():
    """
    main function. Lunch the translator app.
    """
    app = tk.Tk()
    TranslatorApp(app)
    app.mainloop()

if __name__ == "__main__":
    main()
