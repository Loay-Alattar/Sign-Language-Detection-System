import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os

# ===============================
# Colors
# ===============================
BG_COLOR = "#0F172A"        # dark blue
CARD_COLOR = "#1E293B"      # dark gray-blue
PRIMARY = "#6366F1"         # purple
PRIMARY_HOVER = "#4F46E5"
SECONDARY = "#10B981"       # green
SECONDARY_HOVER = "#059669"
TEXT = "#F1F5F9"
SUBTEXT = "#94A3B8"

# ===============================
# Hover Effects
# ===============================
def on_enter_add(e):
    btn_add.config(bg=PRIMARY_HOVER)

def on_leave_add(e):
    btn_add.config(bg=PRIMARY)

def on_enter_detect(e):
    btn_detect.config(bg=SECONDARY_HOVER)

def on_leave_detect(e):
    btn_detect.config(bg=SECONDARY)

# ===============================
# Run Add Gesture with Progress
# ===============================
def add_gesture():
    import tkinter.simpledialog as sd

    name = sd.askstring("Gesture Name", "Enter gesture name:")
    desc = sd.askstring("Gesture Meaning", "What does it mean?")

    if not name or not desc:
        return

    try:
        from gesture_manager import add_new_gesture
        gesture_id = add_new_gesture(name, desc)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    btn_add.config(state="disabled")
    btn_detect.config(state="disabled")

    progress["value"] = 0
    status_label.config(text="Starting...")

    threading.Thread(
        target=run_pipeline,
        args=(gesture_id,),
        daemon=True
    ).start()

# ===============================
# Pipeline Steps
# ===============================
def run_pipeline(gesture_id):
    try:
        update_progress(20, "Collecting gesture images...")
        os.system(f"python collect_data.py {gesture_id}")

        update_progress(50, "Extracting hand features...")
        os.system("python extract_data.py")

        update_progress(90, "Training model...")
        os.system("python train_model.py")

        update_progress(100, "Training completed successfully")

        root.after(0, lambda: messagebox.showinfo(
            "Done",
            "Gesture added and model trained successfully!"
        ))

        update_progress(0, "Idle")

    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Error", str(e)))

    finally:
        root.after(0, lambda: (
            btn_add.config(state="normal"),
            btn_detect.config(state="normal")
        ))

# ===============================
# Thread-safe Progress Update
# ===============================
def update_progress(value, text):
    root.after(0, lambda: (
        progress.config(value=value),
        status_label.config(text=text)
    ))

# ===============================
# Detect Gesture
# ===============================
def detect_gesture():
    os.system("python detect.py")

# ===============================
# UI Setup
# ===============================
root = tk.Tk()
root.title("Sign Language System")
root.state("zoomed")
root.configure(bg=BG_COLOR)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Custom.Horizontal.TProgressbar",
    troughcolor="#334155",
    background=PRIMARY,
    bordercolor="#334155",
    lightcolor=PRIMARY,
    darkcolor=PRIMARY
)

# ===============================
# Left Side
# ===============================
left = tk.Frame(root, bg=BG_COLOR, width=900)
left.pack(side="left", fill="both")
left.pack_propagate(False)

tk.Label(
    left,
    text="Sign Language System",
    font=("Arial", 32, "bold"),
    bg=BG_COLOR,
    fg=TEXT
).pack(pady=(220, 10))

tk.Label(
    left,
    text="Jadara Team Project",
    font=("Arial", 14),
    bg=BG_COLOR,
    fg=SUBTEXT
).pack()

# ===============================
# Right Side Card
# ===============================
card = tk.Frame(root, bg=CARD_COLOR, width=420)
card.pack(side="right", fill="y", padx=80, pady=80)
card.pack_propagate(False)

tk.Label(
    card,
    text="Main Menu",
    font=("Arial", 22, "bold"),
    bg=CARD_COLOR,
    fg=TEXT
).pack(pady=(60, 10))

tk.Label(
    card,
    text="Choose an option",
    font=("Arial", 11),
    bg=CARD_COLOR,
    fg=SUBTEXT
).pack(pady=(0, 40))

# Container to center buttons
buttons_frame = tk.Frame(card, bg=CARD_COLOR)
buttons_frame.pack(expand=True)

btn_add = tk.Button(
    buttons_frame,
    text="Add New Gesture",
    width=22,
    height=2,
    command=add_gesture,
    font=("Arial", 12, "bold"),
    bg=PRIMARY,
    fg="white",
    activebackground=PRIMARY_HOVER,
    activeforeground="white",
    relief="flat",
    cursor="hand2"
)
btn_add.pack(pady=12)

btn_add.bind("<Enter>", on_enter_add)
btn_add.bind("<Leave>", on_leave_add)

btn_detect = tk.Button(
    buttons_frame,
    text="Detect Gesture",
    width=22,
    height=2,
    command=detect_gesture,
    font=("Arial", 12, "bold"),
    bg=SECONDARY,
    fg="white",
    activebackground=SECONDARY_HOVER,
    activeforeground="white",
    relief="flat",
    cursor="hand2"
)
btn_detect.pack(pady=12)

btn_detect.bind("<Enter>", on_enter_detect)
btn_detect.bind("<Leave>", on_leave_detect)

progress = ttk.Progressbar(
    card,
    orient="horizontal",
    length=300,
    mode="determinate",
    style="Custom.Horizontal.TProgressbar"
)
progress.pack(pady=(10, 8))

status_label = tk.Label(
    card,
    text="Idle",
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=SUBTEXT
)
status_label.pack(pady=(0, 30))

root.mainloop()