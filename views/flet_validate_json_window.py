import flet as ft

class FletValidateJsonWindow:
    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller
        
        self.json_field = ft.TextField(
            label="JSON Snippet",
            multiline=True,
            expand=True,
            text_style=ft.TextStyle(font_family="monospace", size=12),
            bgcolor="#0D1117",
            border_color="#30363D",
            border=ft.InputBorder.NONE, # Using container border for cleaner Look
        )

        # Result field - Read-only
        self.result_field = ft.TextField(
            label="Validation Result",
            multiline=True,
            read_only=True,
            expand=True,
            text_style=ft.TextStyle(font_family="monospace", size=12),
            bgcolor="#0D1117",
            border_color="#30363D",
        )

        # Validation Button
        self.validate_button = ft.ElevatedButton(
            "Validate JSON",
            icon=ft.icons.CHECK_CIRCLE,
            on_click=lambda _: self.perform_validation(),
            style=ft.ButtonStyle(
                color="#FFFFFF",
                bgcolor="#1F6FEB", # GitHub primary blue
                shape=ft.RoundedRectangleBorder(radius=6),
            ),
            width=500, # Fill left column width
        )

        self.dialog = ft.AlertDialog(
            title=ft.Text("Validate JSON", color="#58A6FF", weight=ft.FontWeight.BOLD),
            bgcolor="#0D1117",
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        # Left Column: JSON Data & Button
                        ft.Column(
                            controls=[
                                ft.Text("JSON Data", weight=ft.FontWeight.BOLD),
                                ft.Container(
                                    content=self.json_field,
                                    expand=True,
                                    bgcolor="#0D1117",
                                    border=ft.border.all(1, "#30363D"),
                                    border_radius=10,
                                    padding=10,
                                ),
                                self.validate_button,
                            ],
                            expand=True,
                            spacing=10,
                        ),
                        # Right Column: Validation Result
                        ft.Column(
                            controls=[
                                ft.Text("Validation Result", weight=ft.FontWeight.BOLD),
                                ft.Container(
                                    content=self.result_field,
                                    expand=True,
                                    bgcolor="#0D1117",
                                    border=ft.border.all(1, "#30363D"),
                                    border_radius=10,
                                    padding=10,
                                ),
                            ],
                            expand=True,
                            spacing=10,
                        ),
                    ],
                    spacing=20,
                    expand=True,
                ),
                width=1000,
                height=600,
            ),
            actions=[
                ft.TextButton("Close", on_click=lambda _: self.controller.close_validate_json(), style=ft.ButtonStyle(color="#58A6FF")),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def perform_validation(self):
        json_str = self.json_field.value
        is_valid, message = self.controller.validate_json(json_str)
        
        self.result_field.value = message
        self.result_field.border_color = ft.colors.GREEN_400 if is_valid else ft.colors.RED_400
        self.page.update()

    def get_dialog(self):
        return self.dialog

    def set_json_content(self, json_str: str):
        self.json_field.value = json_str

    def focus(self):
        pass # Not applicable in dialog mode the same way
