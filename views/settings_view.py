import customtkinter

class ComboBoxView(customtkinter.CTkFrame):
    def __init__(self, parent, controller, index, key, value_config, combobox_data):
        super().__init__(parent)
        self.controller = controller
        self.key = key
        
        self.checkbox_var = customtkinter.StringVar(value=value_config.get('checkbox_value'))

        self.check_box = customtkinter.CTkCheckBox(
            master=parent, text=value_config.get('label'),
            variable=self.checkbox_var,
            onvalue='on',
            offvalue='off',
            command=self.controller.on_input_changed
        )
        self.check_box.grid(row=index, column=0, pady=8, sticky="wn")

        self.combobox_var = customtkinter.StringVar(value=value_config.get('value'))

        self.combo_box = customtkinter.CTkComboBox(
            master=parent, 
            values=combobox_data,
            variable=self.combobox_var,
            command=lambda x: self.controller.on_input_changed()
        )
        
        self.combo_box.grid(row=index+1, column=0, pady=8, sticky="ewn")

        if self.checkbox_var.get() == "off":
            self.combo_box.grid_remove()
            
    def update_visibility(self):
        if self.checkbox_var.get() == "on":
             self.combo_box.grid()
        else:
             self.combo_box.grid_remove()

    def get_state(self):
        return {
            "checkbox_value": self.checkbox_var.get(),
            "value": self.combobox_var.get()
        }


class EntryView(customtkinter.CTkFrame):
    def __init__(self, parent, controller, index, key, value_config):
        super().__init__(parent)
        self.controller = controller
        self.key = key

        self.checkbox_var = customtkinter.StringVar(value=value_config.get('checkbox_value'))

        self.check_box = customtkinter.CTkCheckBox(
            master=parent, text=value_config.get('label'),
            variable=self.checkbox_var,
            onvalue='on',
            offvalue='off',
            command=self.controller.on_input_changed
        )
        self.check_box.grid(row=index, column=0, pady=8, sticky="wn")

        self.entry_var = customtkinter.StringVar(value=value_config.get('value'))

        self.entry = customtkinter.CTkEntry(master=parent, textvariable=self.entry_var)
        self.entry.grid(row=index+1, column=0, pady=8, sticky="ewn")

        # Bind key release to controller
        self.entry.bind("<KeyRelease>", lambda event: self.controller.on_input_changed())

        if self.checkbox_var.get() == "off":
            self.entry.grid_remove()
            
    def update_visibility(self):
        if self.checkbox_var.get() == "on":
             self.entry.grid()
        else:
             self.entry.grid_remove()

    def get_state(self):
        return {
            "checkbox_value": self.checkbox_var.get(),
            "value": self.entry_var.get()
        }

class SettingsView(customtkinter.CTkFrame):
    def __init__(self, parent, controller, settings_config: dict, templates: dict, locales: dict, product_templates: dict):
        super().__init__(parent)
        self.controller = controller

        self.container = customtkinter.CTkFrame(master=parent, corner_radius=parent.frame_corner_radius, fg_color="transparent")
        self.container.grid(row=0, column=2, sticky="news")
        self.container.grid_rowconfigure((0), weight=1)
        self.container.grid_columnconfigure((0), weight=1)

        # Scrollable frame for settings
        self.settings_box_frame = customtkinter.CTkScrollableFrame(master=self.container, corner_radius=parent.frame_corner_radius)
        self.settings_box_frame.grid(row=0, column=0, padx=parent.frame_padx, pady=parent.frame_pady, sticky="news")
        self.settings_box_frame.grid_rowconfigure((0), weight=1)
        self.settings_box_frame.grid_columnconfigure((0), weight=1)

        # Dictionary to store dynamically created frames
        self.fields = {}

        # Loop through all settings definitions
        for i, (key, value) in enumerate(settings_config.items()):
            index = i * 2

            if value['type'] == 'combobox':
                # Determine correct dropdown data
                combo_data = []
                data_attr = value.get('data')
                if data_attr == 'data_locale':
                    combo_data = list(locales.keys())
                elif data_attr == 'data_templates':
                    combo_data = list(templates.keys())
                elif data_attr == 'data_product_templates':
                    combo_data = list(product_templates.keys())

                field = ComboBoxView(self.settings_box_frame, self.controller, index, key, value, combo_data)
        
            elif value['type'] == 'entry':
                field = EntryView(self.settings_box_frame, self.controller, index, key, value)
            
            self.fields[key] = field

    def get_state(self) -> dict:
        """Pull API getter for all dynamic fields"""
        state = {}
        for key, field in self.fields.items():
            state[key] = field.get_state()
        return state

    def update_view(self, config_settings: dict):
        """Update values and visibility from configuration model"""
        for key, field in self.fields.items():
            if key in config_settings:
                # Update underlying view states
                field.checkbox_var.set(config_settings[key].get("checkbox_value"))
                if hasattr(field, "entry_var"):
                    field.entry_var.set(config_settings[key].get("value"))
                elif hasattr(field, "combobox_var"):
                    field.combobox_var.set(config_settings[key].get("value"))
                    
                field.update_visibility()
