import customtkinter
from views.menu_view import MenuView
from views.email_view import EmailView
from views.settings_view import SettingsView

class MainView(customtkinter.CTk):
    def __init__(self, controller, config_model):
        super().__init__()
        
        self.controller = controller

        # Frame padding and styling
        self.frame_padx: int = 8
        self.frame_pady: int = 8
        self.frame_corner_radius: int = 20

        self.element_padx: int = 8
        self.element_pady: int = 8

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")   

        self.title("AFS - validator")
        self.geometry("1000x600")
        
        self.font = customtkinter.CTkFont(family="roboto", size=12, weight="bold")
        self.header_font = customtkinter.CTkFont(family="roboto", size=16, weight="bold")
        
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0), weight=1)

        data = config_model.get_config()
        
        # menu frame
        self.menu_view = MenuView(self, controller)

        # email frame
        self.email_view = EmailView(self)

        # settings frame 
        self.settings_view = SettingsView(
            self, 
            controller, 
            data.get("settings", {}),
            data.get("templates", {}),
            data.get("locale", {}),
            data.get("productTemplates", {})
        )

        # Base bindings
        self.bind("<KeyRelease>", lambda event: self.controller.on_input_changed())
        
        # Initial updates
        self.update_components(data)
        
    def update_components(self, complete_config_data: dict):
        """Called by controller to push updates to all passive UI components"""
        config = complete_config_data.get("config", {})
        settings = complete_config_data.get("settings", {})
        
        self.menu_view.update_view(config, settings)
        self.settings_view.update_view(settings)
        
        self.email_view.set_content(complete_config_data.get("payload", {}).get("html", ""))
