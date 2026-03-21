import random
import string
import json
import flet as ft

from models.config_manager import ConfigManager
from models.payload_builder import PayloadBuilder, generate_html_payload, parse_invitation_type
from models.email_service import EmailService
from models.json_validator import validate_json_string

from views.flet_view import FletView
import threading

class MainController:
    def __init__(self, page: ft.Page):
        self.page = page
        # 1. Initialize Model layer
        self.config_manager = ConfigManager()
        
        # 2. Initialize View layer
        self.main_view = FletView(self.page, self, self.config_manager)
        
        # Transient sub-views (repurposed for Flet as Dialogs/Views)
        self.settings_window = None
        self.validate_json_window = None
        
        # State tracking for auto-toggles
        self._last_invitation_type = None
        self._save_timer = None

        # Build initial payload to ensure preview is right
        self._sync_and_rebuild()

    def run(self):
        # In Flet, the "run" logic is handled by flet.app(target=...)
        # We just need to add the view to the page.
        self.page.add(self.main_view)
        # Ensure the main view takes up all available space
        self.main_view.expand = True
        self.page.update()

    def on_closing(self):
        """Handle clean application shutdown."""
        # 1. Cancel any pending saves
        if hasattr(self, '_save_timer') and self._save_timer:
            self._save_timer.cancel()
            self._save_timer = None

        # 2. Ensure latest UI state is pulled into the model and saved SYNC
        try:
            data = self.config_manager.get_config()
            
            # Pull from Menu View
            menu_state = self.main_view.menu_view.get_state()
            data["config"]["afs_email"] = menu_state["afs_email"]
            data["config"]["invitation_type"] = menu_state["invitation_type"]
            
            # Pull from Settings View
            settings_state = self.main_view.settings_view.get_state()
            for key, val_dict in settings_state.items():
                if key in data.get("settings", {}):
                    data["settings"][key]["checkbox_value"] = val_dict["checkbox_value"]
                    data["settings"][key]["value"] = val_dict["value"]

            self.config_manager.save_config(data)
        except Exception as e:
            print(f"Error during final save: {e}")

        self.page.window_close()

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
            
        # --- Auto-Toggle logic for Invitation Types ---
        current_invitation_type = config.get("invitation_type")
        
        if current_invitation_type != self._last_invitation_type:
            # We switched types, apply specific field constraints
            p_type = parse_invitation_type(current_invitation_type)
            
            # First, clean slate all product fields to "off"
            product_fields = [
                "productUrl", "imageUrl", "name", "sku", "gtin", "mpn", 
                "brand", "productCategoryGoogleId", "productSkus", 
                "productReviewInvitationTemplateId"
            ]
            for f in product_fields:
                if f in settings:
                    settings[f]["checkbox_value"] = "off"
            
            # Then enable specific ones based on type
            if p_type.name == "SERVICE_AND_PRODUCT_REVIEW":
                for f in ["productUrl", "imageUrl", "name", "sku", "productReviewInvitationTemplateId"]:
                    if f in settings:
                        settings[f]["checkbox_value"] = "on"
            
            elif p_type.name == "SERVICE_AND_PRODUCT_REVIEW_SKU":
                for f in ["productSkus", "productReviewInvitationTemplateId"]:
                    if f in settings:
                        settings[f]["checkbox_value"] = "on"
                        
            self._last_invitation_type = current_invitation_type
            
        # --- Handle Send AFS Direct toggle ---
        if config.get("sendAfsDirect") == "on":
            # In direct mode, recipientEmail is required to be in the JSON
            if "recipientEmail" in settings:
                settings["recipientEmail"]["checkbox_value"] = "on"
                
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
        
        # Debounced save to disk using threading.Timer
        if hasattr(self, '_save_timer') and self._save_timer:
            self._save_timer.cancel()
        
        self._save_timer = threading.Timer(0.5, lambda: self.config_manager.save_config(data))
        self._save_timer.start()
        
        # Update View to reflect new model state
        self.main_view.update_components(data)


    # --- Settings Window ---

    def open_settings(self):
        # In Flet, we could use an AlertDialog or a new View
        # For simplicity, let's use an AlertDialog with the settings content
        from views.flet_settings_window import FletSettingsWindow
        if not self.settings_window:
            data = self.config_manager.get_config()
            self.settings_window = FletSettingsWindow(self.page, self, data.get("config", {}), data.get("settings", {}))
        
        self.page.dialog = self.settings_window.get_dialog()
        self.page.dialog.open = True
        self.page.update()

    def close_settings(self):
        self.on_input_changed()
        self.settings_window = None
        if self.page.dialog:
            self.page.dialog.open = False
        self.page.update()

    # --- JSON Validator Window ---

    def open_validate_json(self):
        from views.flet_validate_json_window import FletValidateJsonWindow
        if not self.validate_json_window:
            self.validate_json_window = FletValidateJsonWindow(self.page, self)
            html_content = self.main_view.email_view.get_content()
            
            # Extract actual JSON from the commented HTML script block
            json_str = ""
            if '<script type="application/json+trustpilot">' in html_content:
                parts = html_content.split('<script type="application/json+trustpilot">')
                if len(parts) > 1:
                    json_str = parts[1].split("</script>")[0].strip()
            
            self.validate_json_window.set_json_content(json_str)
        
        self.page.dialog = self.validate_json_window.get_dialog()
        self.page.dialog.open = True
        self.page.update()

    def close_validate_json(self):
        self.validate_json_window = None
        if self.page.dialog:
            self.page.dialog.open = False
        self.page.update()

    def validate_json(self, json_str: str) -> tuple[bool, str]:
        """Validate a JSON string using the model layer."""
        return validate_json_string(json_str)

    # --- Email Execution ---

    def send_email(self):
        # Force a sync before sending just in case
        self.on_input_changed()
        
        data = self.config_manager.get_config()
        config = data.get("config", {})
        settings = data.get("settings", {})

        # --- Validate required settings before attempting send ---
        missing = []
        if not config.get("agentmail_api_key", "").strip():
            missing.append("AgentMail API Key (open Settings)")
        if not config.get("agentmail_inbox_id", "").strip():
            missing.append("AgentMail Inbox ID (open Settings)")
        if not config.get("afs_email", "").strip():
            missing.append("AFS Email")
        if config.get("sendAfsDirect") != "on":
            recipient = settings.get("recipientEmail", {}).get("value", "").strip()
            if not recipient:
                missing.append("Recipient Email (enable it in the settings panel)")

        if missing:
            self.show_notification(
                "Cannot send email. The following required values are missing or empty:\n\n• " + "\n• ".join(missing),
                level="warning"
            )
            return

        email_service = EmailService(
            config_data=config,
            settings=settings,
            html_payload=self.main_view.email_view.get_content()
        )
        success = email_service.send_email()

        if success:
            self.show_notification("Email sent successfully!", level="success")
        else:
            self.show_notification(
                "Failed to send the email.\nCheck your AgentMail API Key and Inbox ID in Settings, and review the console for details.",
                level="error"
            )

    def show_notification(self, message: str, level: str = "info"):
        """Show a Flet-native notification using SnackBar."""
        color_map = {
            "error": ft.colors.RED_700,
            "success": ft.colors.GREEN_700,
            "warning": ft.colors.ORANGE_700,
            "info": ft.colors.BLUE_700,
        }
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE),
            bgcolor=color_map.get(level, ft.colors.BLUE_700),
            action="OK",
        )
        self.page.snack_bar.open = True
        self.page.update()
