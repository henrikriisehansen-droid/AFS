import flet as ft

class FletMenuView(ft.UserControl):
    def __init__(self, page: ft.Page, controller):
        super().__init__()
        self.page = page
        self.controller = controller
        
        # UI Elements
        self.afs_email_entry = ft.TextField(
            label="AFS email:",
            hint_text="AFS email",
            border_color="#30363D",
            focused_border_color="#90CAF9",
            on_change=lambda _: self.controller.on_input_changed()
        )
        
        self.combobox = ft.Dropdown(
            label="Select invitation type:",
            options=[
                ft.dropdown.Option("Service review"),
                ft.dropdown.Option("Service & Product review using SKU"),
                ft.dropdown.Option("Service & Product Review(add/update Product Review)"),
            ],
            border_color="#30363D",
            focused_border_color="#90CAF9",
            on_change=lambda _: self.controller.on_input_changed(),
            text_size=12,
        )
        
        self.to_label = ft.Text("To: ", weight=ft.FontWeight.BOLD, no_wrap=False, size=13)
        self.bcc_label = ft.Text("bcc: ", size=11, color=ft.colors.GREY_400, no_wrap=False)
        self.invitation_type_hint = ft.Text("", size=11, color=ft.colors.GREY_500, italic=True)
        
        self.validate_json_btn = ft.ElevatedButton(
            "Validate JSON", 
            icon=ft.icons.CODE,
            on_click=lambda _: self.controller.open_validate_json(),
            style=ft.ButtonStyle(
                color=ft.colors.PRIMARY,
                bgcolor=ft.colors.TRANSPARENT,
                side=ft.BorderSide(1, "#30363D"),
                shape=ft.RoundedRectangleBorder(radius=6),
            )
        )
        self.settings_btn = ft.ElevatedButton(
            "Settings", 
            icon=ft.icons.SETTINGS,
            on_click=lambda _: self.controller.open_settings(),
            style=ft.ButtonStyle(
                color="#90CAF9",
                bgcolor=ft.colors.TRANSPARENT,
                side=ft.BorderSide(1, "#30363D"),
                shape=ft.RoundedRectangleBorder(radius=6),
            )
        )
        self.send_email_btn = ft.ElevatedButton(
            "Send Email", 
            icon=ft.icons.SEND,
            on_click=lambda _: self.controller.send_email(),
            style=ft.ButtonStyle(
                color="#FFFFFF",
                bgcolor="#238636", # GitHub primary green
                shape=ft.RoundedRectangleBorder(radius=6),
            )
        )

    def build(self):
        return ft.Column(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("Email Settings", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PRIMARY),
                        self.afs_email_entry,
                        self.combobox,
                        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    self.to_label,
                                    self.bcc_label,
                                    self.invitation_type_hint,
                                ],
                                spacing=5
                            ),
                            padding=ft.padding.only(left=5, top=5)
                        ),
                    ],
                    spacing=10,
                ),
                ft.Column(
                    controls=[
                        self.validate_json_btn,
                        self.settings_btn,
                        self.send_email_btn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=10,
                )
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
        )

    def get_state(self) -> dict:
        return {
            'afs_email': self.afs_email_entry.value,
            'invitation_type': self.combobox.value
        }
    
    def update_view(self, config_data: dict, settings_data: dict):
        self.afs_email_entry.value = config_data.get("afs_email", "")
        self.combobox.value = config_data.get("invitation_type", "Service review")
        self.invitation_type_hint.value = f"Mode: {self.combobox.value}"
        
        if config_data.get("sendAfsDirect") == "on":
            self.to_label.value = f"To: {config_data.get('afs_email', '')}"
            self.to_label.color = ft.colors.PRIMARY
            self.bcc_label.visible = False
        else:
            recipient = settings_data.get('recipientEmail', {}).get('value', '...')
            self.to_label.value = f"To: {recipient}"
            self.to_label.color = None
            self.bcc_label.value = f"bcc: {config_data.get('afs_email', '')}"
            self.bcc_label.visible = True
        
        if self.page:
            self.update()
