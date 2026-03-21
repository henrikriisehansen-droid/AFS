import flet as ft

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

    def get_state(self):
        return {
            "agentmail_api_key": self.api_key_field.value,
            "agentmail_inbox_id": self.inbox_id_field.value,
            "sendAfsDirect": "on" if self.send_afs_direct_switch.value else "off",
            "randomReferenceNumber": "on" if self.random_ref_switch.value else "off",
        }

    def save_and_close(self, e):
        # The controller will pull the state when we call close_settings
        self.controller.close_settings()
