import random
import string
import json

from models.config_manager import ConfigManager
from models.payload_builder import PayloadBuilder, generate_html_payload, parse_invitation_type
from models.email_service import EmailService

from views.main_view import MainView
from views.settings_window import SettingsWindow
from views.validate_json_window import ValidateJsonWindow

class MainController:
    def __init__(self):
        # 1. Initialize Model layer
        self.config_manager = ConfigManager()
        
        # 2. Initialize View layer
        self.main_view = MainView(self, self.config_manager)
        
        # Transient sub-windows
        self.settings_window = None
        self.validate_json_window = None

        # Build initial payload to ensure preview is right
        self._sync_and_rebuild()

    def run(self):
        self.main_view.mainloop()

    # --- Controller Actions (Triggered by Views) ---

    def on_input_changed(self):
        """Pull API implementation: Rebuild state by pulling data from views"""
        
        data = self.config_manager.get_config()
        
        config = data.get("config", {})
        settings = data.get("settings", {})
        
        # 1. Pull data from all active views
        
        # A. Pull from Menu View
        menu_state = self.main_view.menu_view.get_state()
        config["afs_email"] = menu_state["afs_email"]
        config["invitation_type"] = menu_state["invitation_type"]
        
        # B. Pull from Settings View
        settings_state = self.main_view.settings_view.get_state()
        for key, val_dict in settings_state.items():
            if key in settings:
                settings[key]["checkbox_value"] = val_dict["checkbox_value"]
                settings[key]["value"] = val_dict["value"]
                
        # C. Pull from Settings Window (if open)
        if self.settings_window:
            sw_state = self.settings_window.get_state()
            config["agentmail_api_key"] = sw_state["agentmail_api_key"]
            config["agentmail_inbox_id"] = sw_state["agentmail_inbox_id"]
            config["sendAfsDirect"] = sw_state["sendAfsDirect"]
            config["randomReferenceNumber"] = sw_state["randomReferenceNumber"]

        # 2. Business Logic Execution
        
        # Generate random ref number if toggled on
        if config.get("randomReferenceNumber") == "on" and "referenceId" in settings:
            new_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
            settings["referenceId"]["value"] = new_ref
            
        # 3. Synchronize payload construction and save
        self._sync_and_rebuild()


    def _sync_and_rebuild(self):
        """Rebuild constraints and payload based on current internal model data"""
        data = self.config_manager.get_config()
        
        payload_type = parse_invitation_type(data["config"]["invitation_type"])
        
        builder = PayloadBuilder(
            payload_type=payload_type,
            templates=data.get("templates", {}),
            product_templates=data.get("productTemplates", {}),
            settings=data.get("settings", {})
        )
        
        payload_dict = builder.build()
        html_content = generate_html_payload(payload_dict)
        
        data.setdefault("payload", {})["html"] = html_content
        
        # Save to disk
        self.config_manager.save_config(data)
        
        # Update View to reflect new model state
        self.main_view.update_components(data)


    # --- Settings Window ---

    def open_settings(self):
        if not self.settings_window:
            data = self.config_manager.get_config()
            self.settings_window = SettingsWindow(self.main_view, self, data.get("config", {}), data.get("settings", {}))
        else:
            self.settings_window.focus()

    def close_settings(self):
        self.settings_window = None
        self.on_input_changed()

    # --- JSON Validator Window ---

    def open_validate_json(self):
        if not self.validate_json_window:
            self.validate_json_window = ValidateJsonWindow(self.main_view, self)
            html_content = self.main_view.email_view.get_content()
            
            # Extract actual JSON from HTML string for validation
            json_str = ""
            if "<script type='application/json+trustpilot'>" in html_content:
                parts = html_content.split("<script type='application/json+trustpilot'>")
                if len(parts) > 1:
                    json_str = parts[1].split("</script>")[0].strip()
            
            self.validate_json_window.set_json_content(json_str)
        else:
            self.validate_json_window.focus()

    def close_validate_json(self):
        self.validate_json_window = None

    # --- Email Execution ---

    def send_email(self):
        # Force a sync before sending just in case
        self.on_input_changed()
        
        data = self.config_manager.get_config()
        email_service = EmailService(
            config_data=data.get("config", {}),
            settings=data.get("settings", {}),
            html_payload=data.get("payload", {}).get("html", "")
        )
        email_service.send_email()
