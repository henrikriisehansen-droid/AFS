import flet as ft
import random
import string

class FletSettingsWindow:
    def __init__(self, page: ft.Page, controller, config_data: dict, settings_data: dict):
        self.page = page
        self.controller = controller
        
        self.api_key_field = ft.TextField(
            label="AgentMail API Key",
            value=config_data.get("agentmail_api_key", ""),
            password=True,
            can_reveal_password=True,
            focused_border_color="#90CAF9",
        )
        
        self.inbox_id_field = ft.TextField(
            label="AgentMail Inbox ID",
            value=config_data.get("agentmail_inbox_id", ""),
            focused_border_color="#90CAF9",
        )
        
        self.send_afs_direct_switch = ft.Switch(
            label="Send AFS Direct",
            value=config_data.get("sendAfsDirect") == "on",
            active_color="#90CAF9",
        )
        
        self.random_ref_switch = ft.Switch(
            label="Random Reference Number",
            value=config_data.get("randomReferenceNumber") == "on",
            active_color="#90CAF9",
        )

        self.random_products_switch = ft.Switch(
            label="Generate Random Products",
            value=config_data.get("randomProducts") == "on",
            active_color="#90CAF9",
            on_change=self._on_random_products_toggled,
        )

        self.random_products_count = ft.TextField(
            label="Number of Products",
            value=str(config_data.get("randomProductsCount", "3")),
            keyboard_type=ft.KeyboardType.NUMBER,
            focused_border_color="#90CAF9",
            width=200,
            visible=config_data.get("randomProducts") == "on",
        )

        self.dialog = ft.AlertDialog(
            title=ft.Text("Settings", color=ft.colors.PRIMARY),
            bgcolor="#0D1117",
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("AgentMail Configuration", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.PRIMARY),
                        self.api_key_field,
                        self.inbox_id_field,
                        ft.Divider(color="#30363D"),
                        ft.Text("General Options", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.PRIMARY),
                        ft.Row([self.send_afs_direct_switch], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([self.random_ref_switch], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Divider(color="#30363D"),
                        ft.Text("Product Generation", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.PRIMARY),
                        ft.Row([self.random_products_switch], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        self.random_products_count,
                    ],
                    tight=True,
                    spacing=15,
                ),
                width=400,
            ),
            actions=[
                ft.TextButton("Save & Close", on_click=self.save_and_close, style=ft.ButtonStyle(color=ft.colors.PRIMARY)),
                ft.TextButton("Cancel", on_click=lambda _: self.controller.close_settings(), style=ft.ButtonStyle(color=ft.colors.GREY_400)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def get_dialog(self):
        return self.dialog

    def _on_random_products_toggled(self, e):
        self.random_products_count.visible = self.random_products_switch.value
        self.page.update()

    def get_state(self):
        return {
            "agentmail_api_key": self.api_key_field.value,
            "agentmail_inbox_id": self.inbox_id_field.value,
            "sendAfsDirect": "on" if self.send_afs_direct_switch.value else "off",
            "randomReferenceNumber": "on" if self.random_ref_switch.value else "off",
            "randomProducts": "on" if self.random_products_switch.value else "off",
            "randomProductsCount": self.random_products_count.value or "3",
        }

    def save_and_close(self, e):
        # The controller will pull the state when we call close_settings
        self.controller.close_settings()
