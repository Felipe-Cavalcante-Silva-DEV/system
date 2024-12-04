import customtkinter as ctk

class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Widgets do Frame "Home"
        self.title_home = ctk.CTkLabel(self, text="Home page", font=("Arial Bold", 36))
        self.title_home.grid(row=0, column=0, padx=20, pady=20)
