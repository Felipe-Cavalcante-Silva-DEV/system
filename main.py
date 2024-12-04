import sqlite3
import customtkinter as ctk
import os
from PIL import Image
from frames.home_frame import HomeFrame
from frames.inventory_frame import InventoryFrame
from frames.admin_panel_frame import AdminPanelFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SYS")
        self.geometry("275x250")  # Inicialmente com tamanho menor

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Pegando imagens
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

        # TEMAS
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, pady=20, padx=20, sticky="s")
        
        # FRAMES
        self.home_frame = HomeFrame(self, corner_radius=0, fg_color="transparent")
        self.inventory_frame = InventoryFrame(self, corner_radius=0, fg_color="transparent")
        self.admin_panel_frame = AdminPanelFrame(self, corner_radius=0, fg_color="transparent")

        # WIDGETS FRAMES
        self.select_frame_by_name("home")

        # Mostrar a tela de login antes da tela principal
        self.show_login_screen()

    def show_login_screen(self):
        self.login_frame = LoginFrame(self)  # Cria o frame de login
        self.login_frame.grid(row=0, column=0, sticky="nsew")

    def select_frame_by_name(self, name):
        self.home_frame.grid_forget()
        self.inventory_frame.grid_forget()
        self.admin_panel_frame.grid_forget()

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


    
class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configuração para a sidebar com uma coluna e múltiplas linhas
        self.grid_rowconfigure(0, weight=0)  # Linha para os widgets do topo
        self.grid_rowconfigure(1, weight=0)  # Linha para o campo de senha
        self.grid_rowconfigure(2, weight=0)  # Linha para o botão (sem expansão)
        self.grid_rowconfigure(3, weight=1)  # Linha extra para permitir a expansão do restante do espaço
        self.grid_columnconfigure(0, weight=1)

        # Widget de texto do topo
        self.username_label = ctk.CTkLabel(self, text="Usuário:")
        self.username_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.grid(row=0, column=1, padx=20, pady=10, sticky="n")

        self.password_label = ctk.CTkLabel(self, text="Senha:")
        self.password_label.grid(row=1, column=0, padx=20, pady=10, sticky="n")

        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=20, pady=10, sticky="n")

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=20, sticky="n")  # Coloque o botão na linha 2

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.verificar_login(username, password):
            self.master.login_frame.grid_forget()  # Fechar o login frame
            self.master.geometry("1200x750")  # Aumentar o tamanho da janela após o login
            self.master.select_frame_by_name("home")  # Exibir o frame home
        else:
            error_label = ctk.CTkLabel(self, text="Usuário ou senha inválidos", text_color="red")
            error_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="n")

    def verificar_login(self, username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE name = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()

        return user is not None


if __name__ == "__main__":
    app = App()
    app.mainloop()
