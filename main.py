import tkinter as tk

from PIL import Image, ImageTk

from inventory_management_system import InventoryMangement
from login import LoginPage

if __name__ == "__main__":
    root = tk.Tk()
    lg = LoginPage(root)

    root_width = 600
    root_height = 500

    root.geometry(f"{root_width}x{root_height}")
    root.title("Library Management System")

    image_path = "Notebooks\school.png"
    image_pil = Image.open(image_path)
    new_size = (150, 150)
    resized_image = image_pil.resize(new_size)
    image_tk = ImageTk.PhotoImage(resized_image)

    # Create a Label to display the image
    image_label = tk.Label(root, image=image_tk)
    image_label.pack()

    # Top Left box
    book_list_frame = tk.Frame(root, width=400, height=200, bg="lightgray")
    book_list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    canvas = tk.Canvas(book_list_frame, bg="white")
    canvas.pack(fill="both", expand=True)

    label_text = "Library Management System"
    label = tk.Label(
        root, text=label_text, fg="purple", font=("Comic Sans MS", 29, "bold")
    )
    label.pack(pady=10, anchor="center")

    login_button = tk.Button(root, text="Login", command=lg.login_, width=15)
    login_button.pack(pady=10, anchor="center", padx=10)

    registration_button = tk.Button(
        root, text="Register", command=lg.user_registration, width=15
    )
    registration_button.pack(pady=10, anchor="center", padx=10)

    root.mainloop()
