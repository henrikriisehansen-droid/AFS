import flet as ft
from views.flet_menu_view import FletMenuView
from views.flet_email_view import FletEmailView
from views.flet_settings_view import FletSettingsView

class FletView(ft.UserControl):
    def __init__(self, page: ft.Page, controller, config_model):
        super().__init__()
        self.page = page
        self.controller = controller
        self.config_model = config_model
        
        data = config_model.get_config()
        
        # Initialize sub-views
        self.menu_view = FletMenuView(self.page, self.controller)
        self.email_view = FletEmailView(self.page)
        self.settings_view = FletSettingsView(
            self.page, 
            self.controller, 
            data.get("settings", {}),
            data.get("templates", {}),
            data.get("locale", {}),
            data.get("productTemplates", {})
        )

    def build(self):
        # GitHub-style panel container
        def panel_container(content, expand_val):
            return ft.Container(
                content=content,
                padding=20,
                border=ft.border.all(1, "#30363D"),
                border_radius=6,
                bgcolor="#0D1117",
                expand=expand_val,
            )

        return ft.Row(
            controls=[
                panel_container(self.menu_view, 1),
                panel_container(self.email_view, 2),
                panel_container(self.settings_view, 1),
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=15,
        )

    def update_components(self, complete_config_data: dict):
        """Called by controller to push updates to all passive UI components"""
        config = complete_config_data.get("config", {})
        settings = complete_config_data.get("settings", {})
        
        self.menu_view.update_view(config, settings)
        self.settings_view.update_view(settings)
        
        self.email_view.set_content(complete_config_data.get("payload", {}).get("html", ""))
        self.page.update()
