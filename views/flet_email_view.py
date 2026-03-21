import flet as ft

class FletEmailView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        
        # Email body text box
        self.email_body = ft.TextField(
            label="Email Preview / Payload",
            multiline=True,
            expand=True,
            read_only=False,
            text_style=ft.TextStyle(font_family="monospace", size=12),
            border=ft.InputBorder.NONE,
            bgcolor="#0D1117",
            on_change=lambda _: self.page.update()
        )

    def build(self):
        return ft.Column(
            controls=[
                ft.Text("Payload Preview", size=24, weight=ft.FontWeight.BOLD, color="#58A6FF"),
                ft.Container(
                    content=self.email_body,
                    border=ft.border.all(1, "#30363D"),
                    border_radius=6,
                    expand=True,
                ),
            ],
            expand=True,
            spacing=10,
        )

    def set_content(self, html_content: str):
        self.email_body.value = html_content
        if self.page:
            self.update()
        
    def get_content(self) -> str:
        return self.email_body.value
