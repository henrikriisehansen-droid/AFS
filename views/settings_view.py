import customtkinter

# ---------------------------------------------------------------------------
# Base mixin shared by both field types
# ---------------------------------------------------------------------------
class _FieldView(customtkinter.CTkFrame):
    """Shared behaviour for EntryView and ComboBoxView."""

    def __init__(self, parent, controller, index: int, key: str, value_config: dict):
        super().__init__(parent)
        self.controller = controller
        self.key = key
        self._last_visible: bool | None = None  # dirty-check cache

        self.checkbox_var = customtkinter.StringVar(value=value_config.get('checkbox_value', 'off'))

        self.check_box = customtkinter.CTkCheckBox(
            master=parent, text=value_config.get('label', key),
            variable=self.checkbox_var,
            onvalue='on', offvalue='off',
            command=self.controller.on_input_changed
        )
        self.check_box.grid(row=index, column=0, pady=8, sticky="wn")

    def update_visibility(self):
        """Only touch the grid manager when visibility actually changes."""
        visible = self.checkbox_var.get() == "on"
        if visible == self._last_visible:
            return
        self._last_visible = visible
        if visible:
            self._widget.grid()
        else:
            self._widget.grid_remove()

    def get_state(self) -> dict:
        return {
            "checkbox_value": self.checkbox_var.get(),
            "value": self._var.get(),
        }


# ---------------------------------------------------------------------------
# Concrete field types
# ---------------------------------------------------------------------------
class ComboBoxView(_FieldView):
    def __init__(self, parent, controller, index: int, key: str, value_config: dict, combobox_data: list):
        super().__init__(parent, controller, index, key, value_config)

        self.combobox_var = customtkinter.StringVar(value=value_config.get('value', ''))
        self._var = self.combobox_var  # used by base get_state()

        self.combo_box = customtkinter.CTkComboBox(
            master=parent,
            values=combobox_data,
            variable=self.combobox_var,
            command=lambda _x: self.controller.on_input_changed()
        )
        self.combo_box.grid(row=index + 1, column=0, pady=8, sticky="ewn")
        self._widget = self.combo_box  # used by base update_visibility()

        self.update_visibility()   # initialise grid state


class EntryView(_FieldView):
    def __init__(self, parent, controller, index: int, key: str, value_config: dict):
        super().__init__(parent, controller, index, key, value_config)

        self.entry_var = customtkinter.StringVar(value=value_config.get('value', ''))
        self._var = self.entry_var  # used by base get_state()

        self.entry = customtkinter.CTkEntry(master=parent, textvariable=self.entry_var)
        self.entry.grid(row=index + 1, column=0, pady=8, sticky="ewn")
        self._widget = self.entry  # used by base update_visibility()

        # Only bind to the entry widget itself, not to the root window
        self.entry.bind("<KeyRelease>", lambda _e: self.controller.on_input_changed())

        self.update_visibility()   # initialise grid state


# ---------------------------------------------------------------------------
# Container / panel
# ---------------------------------------------------------------------------
class SettingsView(customtkinter.CTkFrame):
    def __init__(
        self,
        parent,
        controller,
        settings_config: dict,
        templates: dict,
        locales: dict,
        product_templates: dict,
    ):
        super().__init__(parent)
        self.controller = controller
        self._updating = False   # re-entrancy guard for update_view()

        self.container = customtkinter.CTkFrame(
            master=parent, corner_radius=parent.frame_corner_radius, fg_color="transparent"
        )
        self.container.grid(row=0, column=2, sticky="news")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.settings_box_frame = customtkinter.CTkScrollableFrame(
            master=self.container, corner_radius=parent.frame_corner_radius
        )
        self.settings_box_frame.grid(
            row=0, column=0,
            padx=parent.frame_padx, pady=parent.frame_pady,
            sticky="news"
        )
        self.settings_box_frame.grid_rowconfigure(0, weight=1)
        self.settings_box_frame.grid_columnconfigure(0, weight=1)

        # Build combo-data lookup once, not per-field
        _combo_data_map = {
            'data_locale':            list(locales.keys()),
            'data_templates':         list(templates.keys()),
            'data_product_templates': list(product_templates.keys()),
        }

        self.fields: dict[str, _FieldView] = {}

        for i, (key, value) in enumerate(settings_config.items()):
            index = i * 2
            field_type = value.get('type')

            if field_type == 'combobox':
                combo_data = _combo_data_map.get(value.get('data', ''), [])
                field = ComboBoxView(
                    self.settings_box_frame, controller, index, key, value, combo_data
                )
            elif field_type == 'entry':
                field = EntryView(
                    self.settings_box_frame, controller, index, key, value
                )
            else:
                continue

            self.fields[key] = field

    # -----------------------------------------------------------------------
    # Pull API
    # -----------------------------------------------------------------------
    def get_state(self) -> dict:
        """Return current UI state for all fields."""
        return {key: field.get_state() for key, field in self.fields.items()}

    # -----------------------------------------------------------------------
    # Push (model → view)
    # -----------------------------------------------------------------------
    def update_view(self, config_settings: dict):
        """Sync field values & visibility from model. Re-entrancy safe."""
        if self._updating:
            return
        self._updating = True
        try:
            for key, field in self.fields.items():
                cfg = config_settings.get(key)
                if cfg is None:
                    continue
                # Only write to StringVar when the value has actually changed
                new_cb = cfg.get("checkbox_value", "off")
                if field.checkbox_var.get() != new_cb:
                    field.checkbox_var.set(new_cb)

                new_val = cfg.get("value", "")
                if field._var.get() != new_val:
                    field._var.set(new_val)

                field.update_visibility()
        finally:
            self._updating = False
