from tkinterdnd2 import DND_FILES, TkinterDnD
import model
import tkinter as tk
from PIL import Image
from tkinter import filedialog, messagebox

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Writer Verification App using Machine Learning")
        self.root.geometry("900x500")

        self.img1_path = None
        self.img2_path = None

        # Layout Frames
        left_frame = tk.Frame(root)
        left_frame.pack(side="left", padx=20, pady=10, fill="both", expand=True)

        right_frame = tk.Frame(root)
        right_frame.pack(side="right", padx=10, pady=10, fill="y")

        # Left Panel
        tk.Label(left_frame, text="Drag and Drop Handwriting Image Files below to Verify Writer", font=("Arial", 12, "bold")).pack(pady=5)

        self.drop_frame = tk.Label(left_frame, text="Drop Here", bg="#ddd", width=50, height=15, borderwidth=2, relief="ridge")
        self.drop_frame.pack(pady=10)
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.handle_drop)

        tk.Button(left_frame, text="CLEAR", command=self.clear).pack(pady=5)
        tk.Button(left_frame, text="Check Similarity", command=self.check_similarity).pack(pady=10)

        self.result_label = tk.Label(left_frame, text="", font=("Arial", 16))
        self.result_label.pack(pady=10)

        # Right Panel
        tk.Label(right_frame, text="Prediction History", font=("Arial", 12, "bold")).pack(pady=5)
        self.history_text = tk.Text(right_frame, width=60, height=25, borderwidth=2, relief="groove")
        self.history_text.pack(fill="both", expand=True, padx=10)

        # Tag configurations for colored rows
        self.history_text.tag_configure("same", background="#c9f7c9")      # light green
        self.history_text.tag_configure("different", background="#f7c9c9")  # light red

    def handle_drop(self, event):
        paths = self.root.tk.splitlist(event.data)
        valid_paths = [p.strip('{}') for p in paths if p.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if len(valid_paths) > 3:
            self.clear()
            self.drop_frame.config(text="Drop Here")
            return

        for filepath in valid_paths:
            if not self.img1_path:
                self.img1_path = filepath
            elif not self.img2_path:
                self.img2_path = filepath
            else:
                break

        img1 = self.img1_path.split("/")[-1] if self.img1_path else ""
        img2 = self.img2_path.split("/")[-1] if self.img2_path else ""
        self.drop_frame.config(text=f"Image 1: {img1}\nImage 2: {img2}")

    def check_similarity(self):
        if not self.img1_path or not self.img2_path:
            messagebox.showwarning("Missing Images", "Please load exactly 2 Handwriting Images.")
            return

        try:
            img1 = Image.open(self.img1_path).convert("RGB")
            img2 = Image.open(self.img2_path).convert("RGB")

            result = model.predict(img1, img2)

            self.result_label.config(
                text=f"Result: {result}",
                fg="green" if result == "Same Writer" else "red"
            )

            # Add to history with color
            file1 = self.img1_path.split("/")[-1]
            file2 = self.img2_path.split("/")[-1]
            entry = f" {file1} | {file2} : {result}\n"
            tag = "same" if result == "Same Writer" else "different"

            self.history_text.config(state="normal")
            self.history_text.insert(tk.END, entry, tag)
            self.history_text.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Could not compare images.\n{e}")

    def clear(self):
        self.img1_path = None
        self.img2_path = None
        self.result_label.config(text="")
        self.drop_frame.config(text="Drop Here")

def main():
    root = TkinterDnD.Tk()
    ui = GUI(root)
    root.mainloop()

main()
