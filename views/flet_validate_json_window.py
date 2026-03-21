import flet as ft

class FletValidateJsonWindow:
    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller
        
        self.json_field = ft.TextField(
            label="Generated JSON Payload",
            multiline=True,
            read_only=True,
            expand=True,
            min_lines=10,
            max_lines=20,
            text_style=ft.TextStyle(font_family="monospace", size=12),
            bgcolor="#0D1117",
            border_color="#30363D",
        )

        self.dialog = ft.AlertDialog(
            title=ft.Text("JSON Validator", color="#58A6FF"),
            bgcolor="#0D1117",
            content=ft.Container(
                content=self.json_field,
                width=500,
                height=400,
            ),
            actions=[
                ft.TextButton("Close", on_click=lambda _: self.controller.close_validate_json()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def get_dialog(self):
        return self.dialog

    def set_json_content(self, json_str: str):
        self.json_field.value = json_str

    def focus(self):
        pass # Not applicable in dialog mode the same way
