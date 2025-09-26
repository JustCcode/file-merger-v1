import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class FileMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🗂 File Merger")
        self.root.geometry("700x470")
        self.root.configure(bg="#f0f2f5")
        self.files = []

        self.create_title()
        self.create_widgets()
        self.create_credits()

    def create_title(self):
        # Добавляем заголовок программы с версией
        title = tk.Label(self.root, text="🗂 File Merger v0.1", font=("Arial", 18, "bold"), bg="#f0f2f5", fg="#0d47a1")
        title.pack(pady=10)

    def create_widgets(self):
        tk.Label(self.root, text="Объединение текстовых файлов", font=("Arial", 16, "bold"), bg="#f0f2f5").pack(pady=5)

        main_frame = tk.Frame(self.root, bg="#f0f2f5")
        main_frame.pack(fill='both', expand=True, padx=10)

        list_frame = tk.LabelFrame(main_frame, text="Выбранные файлы", bg="#f0f2f5", font=("Arial", 11))
        list_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        self.listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, font=("Arial", 10))
        self.listbox.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side='left', fill='y')
        self.listbox.config(yscrollcommand=scrollbar.set)

        btn_frame = tk.Frame(main_frame, bg="#f0f2f5")
        btn_frame.pack(side='left', fill='y', padx=5, pady=5)

        btn_style = {"font": ("Arial", 10), "bg": "#4a90e2", "fg": "white", "activebackground": "#357ABD", "bd": 0, "height":2, "width":20}
        tk.Button(btn_frame, text="Добавить файлы", command=self.add_files, **btn_style).pack(pady=5)
        tk.Button(btn_frame, text="Удалить выбранный", command=self.remove_file, **btn_style).pack(pady=5)
        tk.Button(btn_frame, text="Переместить вверх", command=lambda: self.move_file(-1), **btn_style).pack(pady=5)
        tk.Button(btn_frame, text="Переместить вниз", command=lambda: self.move_file(1), **btn_style).pack(pady=5)
        tk.Button(btn_frame, text="Сбросить список", command=self.reset_list, **btn_style).pack(pady=5)
        tk.Button(btn_frame, text="Объединить файлы", command=self.merge_files, **btn_style).pack(pady=20)

        enc_frame = tk.Frame(self.root, bg="#f0f2f5")
        enc_frame.pack(pady=10)
        tk.Label(enc_frame, text="Кодировка:", bg="#f0f2f5", font=("Arial", 11)).pack(side='left', padx=5)
        self.encoding_var = tk.StringVar(value="utf-8")
        self.encoding_combo = ttk.Combobox(enc_frame, textvariable=self.encoding_var, values=["utf-8", "windows-1251", "latin1"], font=("Arial", 10), width=15)
        self.encoding_combo.pack(side='left', padx=5)

    def create_credits(self):
        credits = tk.Label(self.root, text="Разработано JustC, telegram: justclive", font=("Arial", 11, "bold"), bg="#f0f2f5", fg="#1a237e")
        credits.pack(side='bottom', pady=5)

    def add_files(self):
        new_files = filedialog.askopenfilenames(title="Выберите файлы")
        for f in new_files:
            if f not in self.files:
                self.files.append(f)
                self.listbox.insert(tk.END, f)

    def remove_file(self):
        sel = self.listbox.curselection()
        if sel:
            idx = sel[0]
            self.listbox.delete(idx)
            self.files.pop(idx)

    def move_file(self, direction):
        sel = self.listbox.curselection()
        if sel:
            idx = sel[0]
            new_idx = idx + direction
            if 0 <= new_idx < len(self.files):
                self.files[idx], self.files[new_idx] = self.files[new_idx], self.files[idx]
                self.listbox.delete(0, tk.END)
                for f in self.files:
                    self.listbox.insert(tk.END, f)
                self.listbox.select_set(new_idx)

    def reset_list(self):
        self.listbox.delete(0, tk.END)
        self.files = []

    def merge_files(self):
        if not self.files:
            messagebox.showwarning("Внимание", "Нет выбранных файлов!")
            return

        output_file = filedialog.asksaveasfilename(title="Сохранить как", defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt")])
        if not output_file:
            return

        try:
            with open(output_file, 'w', encoding=self.encoding_var.get()) as outfile:
                for file in self.files:
                    with open(file, 'r', encoding=self.encoding_var.get()) as infile:
                        content = infile.read().strip()
                        if content:
                            outfile.write(content + "\n\n")
            messagebox.showinfo("Успех", f"Файлы объединены в {output_file}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

root = tk.Tk()
app = FileMergerApp(root)
root.mainloop()
