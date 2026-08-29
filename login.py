import tkinter as tk
from tkinter import messagebox

USERS = {
    "admin": "1234",
    "jadara": "team",
}

# ===============================
# Colors
# ===============================
BG_COLOR = "#0F172A"
CARD_COLOR = "#1E293B"
PRIMARY = "#6366F1"
PRIMARY_HOVER = "#4F46E5"
TEXT = "#F1F5F9"
SUBTEXT = "#94A3B8"
ENTRY_BG = "#334155"

def login():
    username = entry_user.get().strip()
    password = entry_pass.get().strip()

    if username in USERS and USERS[username] == password:
        root.destroy()
        import menu
    else:
        messagebox.showerror("Error", "Invalid username or password")

def on_enter(e):
    btn.config(bg=PRIMARY_HOVER)

def on_leave(e):
    btn.config(bg=PRIMARY)

# ===============================
# Window
# ===============================
root = tk.Tk()
root.title("Sign Language System")
root.state("zoomed")
root.configure(bg=BG_COLOR)

# ===============================
# Title (TOP CENTER)
# ===============================
title = tk.Label(
    root,
    text="Sign Language System",
    font=("Arial", 32, "bold"),
    bg=BG_COLOR,
    fg=TEXT
)
title.pack(pady=40)

# ===============================
# MAIN CONTAINER (CENTER)
# ===============================
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(expand=True)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=0)  # left
main_frame.grid_columnconfigure(2, weight=0)  # right
# ===============================
# LEFT TEXT (Developers)
# ===============================
left = tk.Frame(main_frame, bg=BG_COLOR)
left.grid(row=0, column=0, padx=80)

tk.Label(
    left,
    text="Developed By :",
    font=("Arial", 18, "bold"),
    bg=BG_COLOR,
    fg=TEXT
).pack(anchor="w", pady=10)

tk.Label(left, text="Loay Alatar", font=("Arial", 14),
         bg=BG_COLOR, fg=SUBTEXT).pack(anchor="w")

tk.Label(left, text="Alaa Asfa", font=("Arial", 14),
         bg=BG_COLOR, fg=SUBTEXT).pack(anchor="w")

tk.Label(left, text="Asaad abo Ateyah", font=("Arial", 14),
         bg=BG_COLOR, fg=SUBTEXT).pack(anchor="w")

# ===============================
# LOGIN CARD (CENTER)
# ===============================
card = tk.Frame(main_frame, bg=CARD_COLOR, width=600, height=650)
card.grid(row=0, column=1, padx=40, sticky="nsew")
card.grid_propagate(False)

tk.Label(
    card,
    text="Welcome Back",
    font=("Segoe UI", 28, "bold"),
    bg=CARD_COLOR,
    fg=TEXT
).pack(pady=(40, 15))

tk.Label(
    card,
    text="Login to continue",
    font=("Segoe UI", 14),
    bg=CARD_COLOR,
    fg=SUBTEXT
).pack(pady=(0, 25))

# Username
tk.Label(card, text="Username", bg=CARD_COLOR, fg=TEXT).pack(anchor="w", padx=30)
entry_user = tk.Entry(card, bg=ENTRY_BG, fg="white", relief="flat", font=("Segoe UI", 16))
entry_user.pack(padx=50, pady=12, ipady=12, fill="x")

# Password
tk.Label(card, text="Password", bg=CARD_COLOR, fg=TEXT).pack(anchor="w", padx=30)
entry_pass = tk.Entry(card, show="*", bg=ENTRY_BG, fg="white", relief="flat", font=("Segoe UI", 16))
entry_pass.pack(padx=50, pady=12, ipady=12, fill="x")

# Button
btn = tk.Button(
    card,
    text="Login",
    command=login,
    bg=PRIMARY,
    fg="white",
    font=("Segoe UI", 16, "bold"),
    relief="flat",
    cursor="hand2"
)
btn.pack(padx=50, pady=35, fill="x", ipady=14)

btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)

# ===============================
# RIGHT TEXT
# ===============================
right = tk.Frame(main_frame, bg=BG_COLOR)
right.grid(row=0, column=2, padx=80)

tk.Label(
    right,
    text="Jadara Team Project",
    font=("Arial", 16),
    bg=BG_COLOR,
    fg=SUBTEXT
).pack()

root.mainloop()