import tkinter as tk
from tkinter import font

import pyqrcode as qr


class QrCodeGenerator:
    def __init__(self):
        pass

    def create_qr(self):
        code = qr.create("www.linkedin.com/in/ansari-ehteesham-aqeel")
        code_xbm = code.xbm(scale=5)
        code_img = tk.BitmapImage(data=code_xbm)
        return code_img

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def display_qr(self, root, state=False):
        if state == True:
            self.clear_frame(root)
        custom_font = font.Font(family="Arial", size=14, weight="bold")
        img = self.create_qr()
        img_text_label = tk.Label(
            root,
            text="Scan to Get Owner LinkedIn",
            wraplength=200,
            font=custom_font,
            bg="white",
        )
        img_text_label.pack()

        img_label = tk.Label(root, image=img, bg="white")
        img_label.pack()
        root.mainloop()
