import os
import tkinter as tk
from tkinter import filedialog, messagebox

def preview_new_names():
    """
    Preview new file names before renaming and show error if fields are empty 
    or no file with selected extension is found.
    """
    folder_path = folder_path_var.get()
    new_name = new_name_var.get()
    file_extension = file_extension_var.get()
    if not folder_path or not new_name:
        messagebox.showerror("Error", "Please fill in all fields!")
        return
    files = sorted([f for f in os.listdir(folder_path) if f.endswith(file_extension)])
    if not files:
        messagebox.showinfo("No Files", f"No files with the extension {file_extension} found.")
        return
    preview_textbox.config(state=tk.NORMAL)
    preview_textbox.delete(1.0, tk.END)
    count = 1
    for file_name in files:
        new_file_name = f"{new_name}_{count}{file_extension}"
        preview_textbox.insert(tk.END, f"{file_name} -> {new_file_name}\n")
        count += 1
    preview_textbox.config(state=tk.DISABLED)

def rename_files():
    """
    Rename files based on user input and show error if fields are empty
    or no file with selected extension is found.
    """
    folder_path = folder_path_var.get()
    new_name = new_name_var.get()
    file_extension = file_extension_var.get()
    if not folder_path or not new_name:
        messagebox.showerror("Error", "Please fill in all fields!")
        return
    files = sorted([f for f in os.listdir(folder_path) if f.endswith(file_extension)])
    if not files:
        messagebox.showinfo("No Files", f"No files with the extension {file_extension} found.")
        return
    count = 1
    for file_name in files:
        old_path = os.path.join(folder_path, file_name)
        if os.path.isfile(old_path):
            new_file_name = f"{new_name}_{count}{file_extension}"
            new_path = os.path.join(folder_path, new_file_name)
            if os.path.exists(new_path):
                messagebox.showerror("Error", f"The file {new_file_name} already exists. Operation aborted.")
                return
            os.rename(old_path, new_path)
            count += 1
    messagebox.showinfo("Success", "Files were successfully renamed!")

def choose_folder():
    """
    Open a folder selection dialog to select a folder
    """
    folder = filedialog.askdirectory()
    if folder:
        folder_path_var.set(folder)

root = tk.Tk()
root.title("File Renamer")

folder_path_var = tk.StringVar()
tk.Label(root, text="Select Folder:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=folder_path_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=choose_folder).grid(row=0, column=2, padx=10, pady=10)

new_name_var = tk.StringVar()
tk.Label(root, text="New Name Pattern:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=new_name_var, width=40).grid(row=1, column=1, padx=10, pady=10)

file_extension_var = tk.StringVar(value=".png")
tk.Label(root, text="File Extension:").grid(row=2, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=file_extension_var, width=40).grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text="Preview New Names", command=preview_new_names).grid(row=3, column=1, padx=10, pady=10)

preview_frame = tk.Frame(root)
preview_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

preview_textbox = tk.Text(preview_frame, height=10, width=60, state=tk.DISABLED, wrap=tk.NONE)
preview_textbox.grid(row=0, column=0)

scrollbar_y = tk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=preview_textbox.yview)
scrollbar_y.grid(row=0, column=1, sticky="ns")

scrollbar_x = tk.Scrollbar(preview_frame, orient=tk.HORIZONTAL, command=preview_textbox.xview)
scrollbar_x.grid(row=1, column=0, sticky="ew")

preview_textbox.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

tk.Button(root, text="Rename Files", command=rename_files).grid(row=5, column=1, padx=10, pady=20)

root.mainloop()