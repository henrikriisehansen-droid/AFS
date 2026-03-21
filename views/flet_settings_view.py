import flet as ft

class FletSettingsView(ft.UserControl):
    def __init__(
        self,
        page: ft.Page,
        controller,
        settings_config: dict,
        templates: dict,
        locales: dict,
        product_templates: dict,
    ):
        super().__init__()
        self.page = page
        self.controller = controller
        self._updating = False

        # Build combo-data lookup once
        self._combo_data_map = {
            'data_locale':            list(locales.keys()),
            'data_templates':         list(templates.keys()),
            'data_product_templates': list(product_templates.keys()),
        }

        self.fields = {} # Stores Flet controls for each setting
        self.field_containers = {} # Stores containers to toggle visibility

        # Initial build of fields
        self._setup_fields(settings_config)

    def _setup_fields(self, settings_config):
        for key, value in settings_config.items():
            label = value.get('label', key)
            checkbox_value = value.get('checkbox_value', 'off') == 'on'
            field_type = value.get('type')
            current_value = value.get('value', '')

            # Checkbox
            checkbox = ft.Checkbox(
                label=label,
                value=checkbox_value,
                on_change=lambda _: self.controller.on_input_changed()
            )

            # Field (TextField or Dropdown)
            if field_type == 'combobox':
                options = [ft.dropdown.Option(opt) for opt in self._combo_data_map.get(value.get('data', ''), [])]
                field_control = ft.Dropdown(
                    value=current_value,
                    options=options,
                    on_change=lambda _: self.controller.on_input_changed(),
                    visible=checkbox_value,
                    border_color="#30363D",
                    focused_border_color="#1F6FEB",
                )
            else: # entry
                field_control = ft.TextField(
                    value=current_value,
                    on_change=lambda _: self.controller.on_input_changed(),
                    visible=checkbox_value,
                    border_color="#30363D",
                    focused_border_color="#1F6FEB",
                )

            self.fields[key] = {
                'checkbox': checkbox,
                'field': field_control,
                'container': None # Will be set in build()
            }

    def build(self):
        settings_controls = []
        for key, field_group in self.fields.items():
            container = ft.Container(
                content=ft.Column(
                    controls=[
                        field_group['checkbox'],
                        ft.Container(
                            content=field_group['field'],
                            padding=ft.padding.only(left=25, top=5, bottom=5),
                            visible=field_group['checkbox'].value
                        )
                    ],
                    spacing=0
                ),
                padding=10,
                border_radius=6,
                bgcolor="#0D1117" if field_group['checkbox'].value else None,
                border=ft.border.all(1, "#30363D") if field_group['checkbox'].value else None,
            )
            field_group['container'] = container
            settings_controls.append(container)

        return ft.Column(
            controls=[
                ft.Text("Parameters", size=24, weight=ft.FontWeight.BOLD, color="#58A6FF"),
                ft.Column(
                    controls=settings_controls,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                )
            ],
            expand=True,
            spacing=10,
        )

    def get_state(self) -> dict:
        state = {}
        for key, field_group in self.fields.items():
            state[key] = {
                "checkbox_value": "on" if field_group['checkbox'].value else "off",
                "value": field_group['field'].value
            }
        return state

    def update_view(self, config_settings: dict):
        if self._updating:
            return
        self._updating = True
        try:
            for key, field_group in self.fields.items():
                cfg = config_settings.get(key)
                if cfg is None:
                    continue
                
                new_cb = cfg.get("checkbox_value", "off") == "on"
                if field_group['checkbox'].value != new_cb:
                    field_group['checkbox'].value = new_cb
                
                new_val = cfg.get("value", "")
                if field_group['field'].value != new_val:
                    field_group['field'].value = new_val
                
                # Update visibility of the container/field based on checkbox
                field_group['field'].visible = new_cb
                
                # Update container background for visual feedback
                if field_group['container']:
                    field_group['container'].bgcolor = "#0D1117" if new_cb else None
                    field_group['container'].border = ft.border.all(1, "#30363D") if new_cb else None
                    # Also update the inner container's visibility
                    field_group['container'].content.controls[1].visible = new_cb
            
            if self.page:
                self.update()
        finally:
            self._updating = False
