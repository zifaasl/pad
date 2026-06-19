import tkinter as tk

# Window
root = tk.Tk()
root.title("My Profile")
root.geometry("500x500")
root.config(bg="#DFF6FF")

# Card utama
card = tk.Frame(
    root,
    bg="white",
    width=380,
    height=400,
    highlightthickness=0
)
card.place(relx=0.5, rely=0.5, anchor="center")

# Judul
title = tk.Label(
    card,
    text="MY PROFILE",
    font=("Segoe UI", 20, "bold"),
    fg="#0077B6",
    bg="white"
)
title.pack(pady=(25, 5))

# Garis kecil
line = tk.Frame(card, bg="#90E0EF", height=2, width=200)
line.pack()

# Biodata
info = (
    f"{'👤 Name':<15}: Adilah Nazifah\n"
    f"{'🎂 Age':<15}: 21 years old\n"
    f"{'📍 Location':<15}: Depok\n"
    f"{'🎓 Major':<15}: Information Systems\n"
    f"{'📚 Semester':<15}: 6\n"
    f"{'💻 Skills':<15}: Python, SQL, HTML, CSS\n"
    f"{'🎵 Hobby':<15}: Music & Sleep\n"
    f"{'✨ Motto':<15}: Keep Learning"
)

# Deskripsi
desc = tk.Label(
    card,
    text="Information Systems Student",
    font=("Segoe UI", 10),
    fg="#7F8C8D",
    bg="white"
)
desc.pack()

# Biodata
info = (
    f"{'👤 Name':<15}: Adilah Nazifah\n"
    f"{'🎂 Age':<15}: 21 years old\n"
    f"{'📍 Location':<15}: Depok\n"
    f"{'🎓 Major':<15}: Information Systems\n"
    f"{'📚 Semester':<15}: 6\n"
    f"{'💻 Skills':<15}: Python, SQL, HTML, CSS\n"
    f"{'🎵 Hobby':<15}: Music & Sleep\n"
    f"{'✨ Motto':<15}: Keep Calm"
)

profile = tk.Label(
    card,
    text=info,
    justify="left",
    anchor="w",
    font=("Segoe UI", 11),
    fg="#34495E",
    bg="white"
)
profile.pack(pady=25)

# Footer
footer = tk.Label(
    card,
    text="Made with Python",
    font=("Segoe UI", 9, "italic"),
    fg="#0096C7",
    bg="white"
)
footer.pack(side="bottom", pady=20)

root.mainloop()