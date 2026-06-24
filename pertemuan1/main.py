import tkinter as tk

# ================= WINDOW =================
root = tk.Tk()
root.title("My Profile")
root.geometry("550x600")
root.configure(bg="#EAF8FF")
root.resizable(False, False)

# ================= CARD =================
card = tk.Frame(
    root,
    bg="white",
    width=420,
    height=500
)
card.place(relx=0.5, rely=0.5, anchor="center")

# ================= HEADER =================
header = tk.Frame(
    card,
    bg="#0077B6",
    height=120
)
header.pack(fill="x")

title = tk.Label(
    header,
    text="MY PROFILE",
    font=("Segoe UI", 20, "bold"),
    fg="white",
    bg="#0077B6"
)
title.pack(pady=(25, 5))

subtitle = tk.Label(
    header,
    text="Information Systems Student",
    font=("Segoe UI", 10),
    fg="#CAF0F8",
    bg="#0077B6"
)
subtitle.pack()

# ================= NAME =================
name = tk.Label(
    card,
    text="Adilah Nazifah",
    font=("Segoe UI", 18, "bold"),
    fg="#023E8A",
    bg="white"
)
name.pack(pady=(30, 5))

line = tk.Frame(card, bg="#90E0EF", height=2, width=250)
line.pack()

# ================= BIODATA =================
info_frame = tk.Frame(card, bg="white")
info_frame.pack(pady=25)

labels = [
    ("👤 Name", "Adilah Nazifah"),
    ("🎂 Age", "21 years old"),
    ("📍 Location", "Depok"),
    ("🎓 Major", "Information Systems"),
    ("📚 Semester", "6"),
    ("💻 Skills", "Python, SQL, HTML, CSS, Mengarang"),
    ("🎵 Hobby", "Music & Sleep"),
    ("✨ Motto", "Keep Calm")
]

for key, value in labels:

    left = tk.Label(
        info_frame,
        text=key,
        font=("Segoe UI", 11),
        fg="#0077B6",
        bg="white",
        width=14,
        anchor="w"
    )
    left.grid(row=labels.index((key, value)), column=0, pady=6)

    colon = tk.Label(
        info_frame,
        text=":",
        font=("Segoe UI", 11, "bold"),
        fg="#0077B6",
        bg="white"
    )
    colon.grid(row=labels.index((key, value)), column=1)

    right = tk.Label(
        info_frame,
        text=value,
        font=("Segoe UI", 11),
        fg="#3A506B",
        bg="white",
        anchor="w"
    )
    right.grid(row=labels.index((key, value)), column=2, padx=10)

# ================= FOOTER =================
footer_line = tk.Frame(
    card,
    bg="#90E0EF",
    height=1,
    width=320
)
footer_line.pack(pady=(15, 10))

footer = tk.Label(
    card,
    text="Made with Python and Tkinter",
    font=("Segoe UI", 9, "italic"),
    fg="#48CAE4",
    bg="white"
)
footer.pack()

root.mainloop()