import tkinter as tk

from tools.login import LoginPage

if __name__ == "__main__":
    # Initializing an object
    root = tk.Tk()

    # tkinter window
    root.title("Library Management System")

    # Top Left Frame
    book_list_frame = tk.Frame(root, width=970, height=350, bg="white")
    book_list_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    # Top Right Frame
    login_frame = tk.Frame(root, width=510, height=150, bg="white")
    login_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    # Bottom Left Box
    lower_left = tk.Frame(root, width=200, height=200, bg="white")
    lower_left.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    lower_left.pack_propagate(False)

    # Bottom Right Box
    lower_right = tk.Frame(root, width=200, height=200, bg="white")
    lower_right.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")

    # Top Right Buttons
    lg = LoginPage(root, book_list_frame, login_frame, lower_right, lower_left)

    # Login Button
    login_button = tk.Button(
        login_frame,
        width=28,
        height=2,
        text="Login",
        command=lg.login_,
    )
    login_button.pack(padx=2, pady=5, anchor="center")

    # New User Registration Button
    registration_button = tk.Button(
        login_frame,
        width=28,
        height=2,
        text="Register",
        command=lg.user_registration,
    )
    registration_button.pack(pady=5, anchor="center")

    root.mainloop()
