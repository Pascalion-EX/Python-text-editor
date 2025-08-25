import customtkinter as ctk
from tkinter import font
from tkinter.filedialog import asksaveasfilename, askopenfilename


def save_file(window, text_edit):
    filepath = asksaveasfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    with open(filepath, "w") as f:
        content = text_edit.get("1.0", "end-1c")
        f.write(content)
        window.title(f"Open File: {filepath}")


def open_file(window, text_edit):
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    text_edit.delete("1.0", "end")
    with open(filepath, "r") as f:
        content = f.read()
        text_edit.insert("1.0", content)
    window.title(f"Open File: {filepath}")


def custom_undo(text_edit):
    try:
        text_edit.edit_undo()
    except:
        pass


def custom_redo(text_edit):
    try:
        text_edit.edit_redo()
    except:
        pass


def open_font_window(text_edit):
    font_win = ctk.CTkToplevel()
    font_win.title("Choose Font")
    font_win.geometry("600x600")

    fonts = list(font.families())
    fonts.sort()

    label = ctk.CTkLabel(font_win, text="Select Font:")
    label.pack(pady=5)

    font_listbox = ctk.CTkTextbox(font_win, height=200, width=200)
    for f in fonts:
        font_listbox.insert("end", f + "\n")
    font_listbox.configure(state="disabled")
    font_listbox.pack(padx=10, pady=5, fill="both", expand=True)

    size_label = ctk.CTkLabel(font_win, text="Font Size:")
    size_label.pack(pady=(10, 0))
    size_var = ctk.StringVar(value="18")
    size_entry = ctk.CTkEntry(font_win, textvariable=size_var, width=80)
    size_entry.pack(pady=5)

    selected_font = ctk.StringVar(value="Arial")
    selected_label = ctk.CTkLabel(font_win, textvariable=selected_font)
    selected_label.pack(pady=5)
    def on_click(event):
        try:
            index = font_listbox.index("@%s,%s linestart" % (event.x, event.y))
            line = font_listbox.get(index, index + " lineend").strip()
            if line:
                selected_font.set(line)
        except:
            pass

    font_listbox.bind("<Button-1>", on_click)
    def apply_font():
        try:
            size = int(size_var.get())
        except ValueError:
            size = 18
        fnt = selected_font.get()
        text_edit.configure(font=(fnt, size))
        font_win.destroy()

    apply_btn = ctk.CTkButton(font_win, text="Apply", command=apply_font)
    apply_btn.pack(pady=10)


def setup_hotkeys(window, text_edit):
    text_edit.configure(undo=True, autoseparators=True, maxundo=-1)
    text_edit.bind("<Control-s>", lambda e: save_file(window, text_edit))
    text_edit.bind("<Control-o>", lambda e: open_file(window, text_edit))
    text_edit.bind("<Control-z>", lambda e: custom_undo(text_edit))
    text_edit.bind("<Control-y>", lambda e: custom_redo(text_edit))
    text_edit.bind("<Control-a>", lambda e: text_edit.tag_add("sel", "1.0", "end"))
    def select_all(event):
        text_edit.tag_add("sel", "1.0", "end")
        return "break"

    text_edit.bind("<Control-a>", select_all)
    text_edit.bind("<Control-c>", lambda e: text_edit.event_generate("<<Copy>>"))
    text_edit.bind("<Control-x>", lambda e: text_edit.event_generate("<<Cut>>"))
    text_edit.bind("<Control-v>", lambda e: text_edit.event_generate("<<Paste>>"))


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    window = ctk.CTk()
    window.title("Pascsl")
    window.geometry("1200x1200")
    toolbar = ctk.CTkFrame(window)
    toolbar.pack(side="top", fill="x")
    Text = ctk.CTkTextbox(window, font=("Braven", 18))
    Text.pack(fill="both", expand=True, padx=5, pady=5)
    setup_hotkeys(window, Text)
    save_button = ctk.CTkButton(toolbar, text="💾 Save", command=lambda: save_file(window, Text))
    save_button.pack(side="left", padx=5, pady=5)

    open_button = ctk.CTkButton(toolbar, text="📂 Open", command=lambda: open_file(window, Text))
    open_button.pack(side="left", padx=5, pady=5)

    undo_button = ctk.CTkButton(toolbar, text="↩ Undo", command=lambda: custom_undo(Text))
    undo_button.pack(side="left", padx=5, pady=5)

    redo_button = ctk.CTkButton(toolbar, text="↪ Redo", command=lambda: custom_redo(Text))
    redo_button.pack(side="left", padx=5, pady=5)

    font_button = ctk.CTkButton(toolbar, text="🔤 Font", command=lambda: open_font_window(Text))
    font_button.pack(side="left", padx=5, pady=5)

    window.mainloop()


main()