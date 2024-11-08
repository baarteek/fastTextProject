import customtkinter as ctk
from ui.main_window import MainWindow

def main():
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("Fast Text Project")

    main_window = MainWindow(master=app)
    main_window.pack(fill="both", expand=True)

    app.mainloop()

if __name__ == "__main__":
    main()