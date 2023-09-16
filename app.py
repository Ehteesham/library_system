import tkinter as tk
from login import LoginPage


root = tk.Tk()

lg = LoginPage(root)
root.title("Library Management System")
root_width = 1000
root_height = 500

root.geometry(f"{root_width}x{root_height}")

# Top Left Frame
book_list_frame = tk.Frame(root, width=750, height=350, bg="darkgray")
book_list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

canvas = tk.Canvas(book_list_frame, width=750, height=350, bg="white")
canvas.pack(fill="both", expand=True)

# Top Right Frame
login_frame = tk.Frame(root, width=350, height=150, bg="white")
login_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Bottom Box
lower_frame = tk.Frame(root, width=400, height=200, bg="white")
lower_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Top Right Buttons
login_button = tk.Button(login_frame, width=25, height=2, text="Login", command=lambda: lg.login_(login_frame, lower_frame))
login_button.pack(padx=2, pady=5,anchor='center')

registration_button = tk.Button(login_frame, width=25, height=2, text="Register")
registration_button.pack(pady=5,anchor='center')


root.mainloop()
