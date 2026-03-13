import customtkinter

class SettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, controller, config_data: dict, settings_data: dict):
        super().__init__()
        self.geometry("400x350")
        
        self.parent = parent
        self.controller = controller

        self.element_padx = 8
        self.element_pady = 8

        self.font = customtkinter.CTkFont(family="roboto", size=12, weight="bold")
        self.header_font = customtkinter.CTkFont(family="roboto", size=16, weight="bold")
        self.title("Settings")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tab_view = TabView(master=self, width=400, height=350, config_data=config_data, controller=controller)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="news")

        self.attributes("-topmost", True) 
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        self.controller.close_settings()
        self.destroy()

    def get_state(self) -> dict: 
        """Pull API getter for window settings"""
        return {
            "agentmail_api_key": self.tab_view.api_key_entry.get(), 
            "agentmail_inbox_id": self.tab_view.inbox_id_entry.get(),
            "sendAfsDirect": self.tab_view.send_afs_direct.get(),
            "randomReferenceNumber": self.tab_view.random_reference_number.get()
        }
    
class TabView(customtkinter.CTkTabview):
    def __init__(self, master, config_data: dict, controller, **kwargs):
        super().__init__(master)
        
        self.controller = controller

        # create tabs
        agentmail_tab_frame = self.add("AgentMail")
        various_tab_frame = self.add("Various settings")

        # --- Configure grids ---
        agentmail_tab_frame.grid_columnconfigure(0, weight=1)
        various_tab_frame.grid_columnconfigure(0, weight=1)
        various_tab_frame.grid_rowconfigure(8, weight=1)

        # --- Add widgets to AgentMail tab ---
        self.api_key_label = customtkinter.CTkLabel(master=agentmail_tab_frame, text="AgentMail API Key:", fg_color="transparent", font=master.font)
        self.api_key_label.grid(row=0, column=0, padx=master.element_padx, pady=master.element_pady, sticky="wn")

        self.api_key_entry = customtkinter.CTkEntry(
            master=agentmail_tab_frame, 
            textvariable=customtkinter.StringVar(value=config_data.get("agentmail_api_key", "")), 
            placeholder_text="sk_am_...",
            show="*"
        )
        self.api_key_entry.grid(row=1, column=0, padx=master.element_padx, pady=master.element_pady, sticky="ewn")
        
        self.inbox_id_label = customtkinter.CTkLabel(master=agentmail_tab_frame, text="Inbox ID:", fg_color="transparent", font=master.font)
        self.inbox_id_label.grid(row=2, column=0, padx=master.element_padx, pady=master.element_pady, sticky="wn")
        
        self.inbox_id_entry = customtkinter.CTkEntry(
            master=agentmail_tab_frame,
            textvariable=customtkinter.StringVar(value=config_data.get("agentmail_inbox_id", "")), 
            placeholder_text="e.g. 1a2b3c..."
        )
        self.inbox_id_entry.grid(row=3, column=0, padx=master.element_padx, pady=master.element_pady, sticky="ewn")

        # Bind events
        for entry in [self.api_key_entry, self.inbox_id_entry]:
            entry.bind("<KeyRelease>", lambda event: self.controller.on_input_changed())

        # Various settings tab
        self.send_afs_direct = customtkinter.CTkCheckBox(
            master=various_tab_frame,
            text="Send AFS Direct",
            onvalue="on",
            offvalue="off",
            command=self.controller.on_input_changed,
            variable=customtkinter.StringVar(value=config_data.get("sendAfsDirect", "off")))
        self.send_afs_direct.grid(row=0, column=0, padx=master.element_padx, pady=8, sticky="w")

        self.random_reference_number = customtkinter.CTkCheckBox(
            master=various_tab_frame,
            text="Generate random reference number",
            onvalue="on",
            offvalue="off",
            command=self.controller.on_input_changed,
            variable=customtkinter.StringVar(value=config_data.get("randomReferenceNumber", "off")))
        self.random_reference_number.grid(row=1, column=0, padx=master.element_padx, pady=8, sticky="w")
