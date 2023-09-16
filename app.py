import tkinter as tk

from inventory_management_system import InventoryMangement
from login import LoginPage

# Initializing an object
root = tk.Tk()
lg = LoginPage(root)

# Adjusting tkinter window
root.title("Library Management System")
root_width = 1000
root_height = 500

root.geometry(f"{root_width}x{root_height}")

# Top Left Frame
book_list_frame = tk.Frame(root, width=750, height=350, bg="darkgray")
book_list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Top Right Frame
login_frame = tk.Frame(root, width=350, height=150, bg="white")
login_frame.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

# Bottom Box
lower_frame = tk.Frame(root, width=400, height=200, bg="white")
lower_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Top Right Buttons

# Login Button
login_button = tk.Button(
    login_frame,
    width=25,
    height=2,
    text="Login",
    command=lambda: lg.login_(login_frame, lower_frame, book_list_frame),
)
login_button.pack(padx=2, pady=5, anchor="center")

# New User Registration Button
registration_button = tk.Button(
    login_frame,
    width=25,
    height=2,
    text="Register",
    command=lambda: lg.user_registration(login_frame),
)
registration_button.pack(pady=5, anchor="center")

root.mainloop()
