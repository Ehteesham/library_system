import tkinter as tk
from tkinter import font

import pyqrcode as qr


class QrCodeGenerator:
    def __init__(self, login_frame):
        self.login_frame = login_frame

    def create_qr(self):
        code = qr.create("www.linkedin.com/in/ansari-ehteesham-aqeel")
        code_xbm = code.xbm(scale=5)
        code_img = tk.BitmapImage(data=code_xbm)
        return code_img

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def display_qr(self, state=False):
        if state == True:
            self.clear_frame(self.login_frame)
        custom_font = font.Font(family="Arial", size=14, weight="bold")
        img = self.create_qr()
        img_text_label = tk.Label(
            self.login_frame,
            text="Scan to Get Owner LinkedIn",
            wraplength=200,
            font=custom_font,
            bg="white",
        )
        img_text_label.pack()
        img_label = tk.Label(self.login_frame, image=img, bg="white")
        img_label.pack()
        self.login_frame.mainloop()

    def getqr(self, df, book_name):
        self.clear_frame(self.login_frame)
        link_value = df[df["Book Name"] == book_name]["QR Code"].iloc[0]
        code = tk.BitmapImage(data=link_value)
        custom_font = font.Font(family="Arial", size=14, weight="bold")
        img_text_label = tk.Label(
            self.login_frame,
            text="Scan To Get Book",
            wraplength=200,
            font=custom_font,
            bg="white",
        )
        img_text_label.pack()
        img_label = tk.Label(self.login_frame, image=code, bg="white")
        img_label.pack()
        self.login_frame.mainloop()
