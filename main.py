import customtkinter as ctk
import tkinter.messagebox as messagebox
import os
from PIL import Image
from frames.home_frame import HomeFrame
from frames.inventory_frame import InventoryFrame
from frames.admin_panel_frame import AdminPanelFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SYS")
        self.geometry("700x450")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #pegando imagens
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "rocket.png")), size=(26, 26))

        self.home_image = ctk.CTkImage(dark_image=Image.open(os.path.join(image_path, "home_dark.png")), light_image=Image.open(os.path.join(image_path, "home_light.png")))

        self.inventory_image = ctk.CTkImage(dark_image=Image.open(os.path.join(image_path, "inventory_dark.png")), light_image=Image.open(os.path.join(image_path, "inventory_light.png")))

        self.admin_image = ctk.CTkImage(dark_image=Image.open(os.path.join(image_path, "admin_panel_dark.png")), light_image=Image.open(os.path.join(image_path, "admin_panel_light.png")))

        # Botões de navegação
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # GRID COM LOGO
        self.nav_frame_label = ctk.CTkLabel(self.navigation_frame, text="Gestão De Estoque", image=self.logo_image, compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.nav_frame_label.grid(row=0, column=0, pady=20, padx=20)


        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="home", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")


        self.inventory_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="inventory", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.inventory_image, anchor="w", command=self.inventory_button_event)
        self.inventory_button.grid(row=2, column=0, sticky="ew")


        self.admin_panel_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="admin_panel", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.admin_image, anchor="w", command=self.admin_panel_button_event)
        self.admin_panel_button.grid(row=3, column=0, sticky="ew")


        #TEMAS

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, pady=20, padx=20, sticky="s")


        #FRAMES
        self.home_frame = HomeFrame(self, corner_radius=0, fg_color="transparent")
        self.inventory_frame = InventoryFrame(self, corner_radius=0, fg_color="transparent")
        self.admin_panel_frame = AdminPanelFrame(self, corner_radius=0, fg_color="transparent")



        #WIDGETS FRAMES

        

        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
    # Esconder todos os frames primeiro
        self.home_frame.grid_forget()
        self.inventory_frame.grid_forget()
        self.admin_panel_frame.grid_forget()

        # Ativar o frame correto
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
            self.home_button.configure(fg_color=("gray75", "gray25"))
            self.inventory_button.configure(fg_color="transparent")
            self.admin_panel_button.configure(fg_color="transparent")
        elif name == "inventory":
            self.inventory_frame.grid(row=0, column=1, sticky="nsew")
            self.home_button.configure(fg_color="transparent")
            self.inventory_button.configure(fg_color=("gray75", "gray25"))
            self.admin_panel_button.configure(fg_color="transparent")
        elif name == "admin_panel":
            self.admin_panel_frame.grid(row=0, column=1, sticky="nsew")
            self.home_button.configure(fg_color="transparent")
            self.inventory_button.configure(fg_color="transparent")
            self.admin_panel_button.configure(fg_color=("gray75", "gray25"))

                
         


         

    def admin_panel_button_event(self):
        self.select_frame_by_name("admin_panel")            

    def home_button_event(self):
        self.select_frame_by_name("home")

    def inventory_button_event(self):       
        self.select_frame_by_name("inventory")

    def change_appearance_mode_event(self, new_appearence_mode):
        ctk.set_appearance_mode(new_appearence_mode)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
