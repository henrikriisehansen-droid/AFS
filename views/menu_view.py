import customtkinter

class MenuView(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

         # Column 0: Email settings
        self.set_email_frame = customtkinter.CTkFrame(master=parent, corner_radius=parent.frame_corner_radius, fg_color="transparent")
        self.set_email_frame.grid(row=0, column=0, sticky="news")
        self.set_email_frame.grid_rowconfigure((0, 1, 2), weight=1)
        self.set_email_frame.grid_columnconfigure((0), weight=1)

        # Email entry frame
        self.set_email_frame_entry = customtkinter.CTkFrame(master=self.set_email_frame, corner_radius=parent.frame_corner_radius, fg_color="transparent")
        self.set_email_frame_entry.grid(row=0, column=0, padx=parent.frame_padx, pady=parent.frame_pady, sticky="news")
        self.set_email_frame_entry.grid_rowconfigure((0), weight=1)
        self.set_email_frame_entry.grid_columnconfigure((0), weight=1)

        # Inner frame for email entry
        self.email_frame_entry_inner_frame = customtkinter.CTkFrame(master=self.set_email_frame_entry, corner_radius=parent.frame_corner_radius)
        self.email_frame_entry_inner_frame.grid(row=0, column=0, sticky="new")
        self.email_frame_entry_inner_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.email_frame_entry_inner_frame.grid_columnconfigure((0), weight=1)

        # AFS email label and entry
        self.afs_email_label = customtkinter.CTkLabel(master=self.email_frame_entry_inner_frame, text="AFS email:", fg_color="transparent", font=parent.font)
        self.afs_email_label.grid(row=0, column=0, padx=parent.frame_padx, pady=parent.frame_pady, sticky="ws")

        self.afs_email_entry = customtkinter.CTkEntry(
            master=self.email_frame_entry_inner_frame, 
            placeholder_text="AFS email")
        self.afs_email_entry.grid(row=1, column=0, padx=parent.frame_padx, pady=parent.frame_pady, sticky="ewn")
        
        # Invitation type combobox
        self.combobox_label = customtkinter.CTkLabel(master=self.email_frame_entry_inner_frame, text="Select invitation type:", fg_color="transparent", font=parent.font)
        self.combobox_label.grid(row=2, column=0, padx=parent.frame_padx, pady=parent.frame_pady, sticky="ws")

        self.combobox_var = customtkinter.StringVar(value="Service Review")
        
        # In a pull API, the combo triggers a controller method to do a full state sync
        self.combobox = customtkinter.CTkComboBox(
            master=self.email_frame_entry_inner_frame, 
            values=["Service review", "Service & Product review using SKU", "Service & Product Review(add/update Product Review)"],
            command=lambda x: self.controller.on_input_changed(), 
            variable=self.combobox_var
        )
        self.combobox.grid(row=3, column=0, padx=parent.frame_padx, pady=parent.frame_pady, sticky="ewn")

        # Email Address to,bcc fields
        self.to_label = customtkinter.CTkLabel(master=self.email_frame_entry_inner_frame, text="To: ", fg_color="transparent") 
        self.to_label.grid(row=4, column=0, padx=parent.frame_padx, pady=parent.frame_pady, sticky="ws") 

        self.bcc_label = customtkinter.CTkLabel(master=self.email_frame_entry_inner_frame, text="bcc:", fg_color="transparent")
        self.bcc_label.grid(row=5, column=0, padx=parent.frame_padx, pady=parent.frame_pady, sticky="wn") 

        # Buttons frame
        self.set_email_frame_buttons = customtkinter.CTkFrame(master=self.set_email_frame, corner_radius=parent.frame_corner_radius, fg_color="transparent", bg_color="transparent")
        self.set_email_frame_buttons.grid(row=2, column=0, padx=parent.frame_padx, pady=parent.frame_pady, sticky="sewn")
        self.set_email_frame_buttons.grid_rowconfigure((0), weight=1)
        self.set_email_frame_buttons.grid_columnconfigure((0), weight=1)

        # Inner frame for buttons
        self.email_frame_buttons_inner_frame = customtkinter.CTkFrame(master=self.set_email_frame_buttons, corner_radius=parent.frame_corner_radius)
        self.email_frame_buttons_inner_frame.grid(row=0, column=0, sticky="sew")
        self.email_frame_buttons_inner_frame.grid_rowconfigure((0,1), weight=1)
        self.email_frame_buttons_inner_frame.grid_columnconfigure((0), weight=1)

        # Validate JSON, Settings and send email buttons
        self.validate_json_btn = customtkinter.CTkButton(master=self.email_frame_buttons_inner_frame, text="Validate JSON", command=self.controller.open_validate_json)
        self.validate_json_btn.grid(row=0, column=0, padx=parent.element_padx, pady=parent.element_pady, sticky="ew")

        self.settings_btn = customtkinter.CTkButton(master=self.email_frame_buttons_inner_frame, text="Settings", command=self.controller.open_settings)
        self.settings_btn.grid(row=1, column=0, padx=parent.element_padx, pady=parent.element_pady, sticky="ew")

        self.send_email_btn = customtkinter.CTkButton(master=self.email_frame_buttons_inner_frame, text="Send Email", command=self.controller.send_email)
        self.send_email_btn.grid(row=2, column=0, padx=parent.element_padx, pady=parent.element_pady, sticky="ew")


    def get_state(self) -> dict:
        """Pull API getter"""
        return {
            'afs_email': self.afs_email_entry.get(),
            'invitation_type': self.combobox_var.get()
        }
    
    def update_view(self, config_data: dict, settings_data: dict):
        """Update fields based on main application state"""
        self.afs_email_entry.delete(0, "end")
        self.afs_email_entry.insert(0, config_data.get("afs_email", ""))
        
        self.combobox_var.set(config_data.get("invitation_type", "Service Review"))
        
        if config_data.get("sendAfsDirect") == "on":
            self.to_label.configure(text=f"To: {config_data.get('afs_email', '')}")
            self.bcc_label.grid_remove()
        else:
            recipient = settings_data.get('recipientEmail', {}).get('value', '')
            self.to_label.configure(text=f"To: {recipient}")
            self.bcc_label.configure(text=f"bcc: {config_data.get('afs_email', '')}")
            self.bcc_label.grid()
