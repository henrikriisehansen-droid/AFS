import customtkinter
from settings_window import settingsWindow
from sendEmail import Email
import json
from payload import PayloadBuilder, PayloadType
from itertools import chain
from interface_elements.menu import Menu
from interface_elements.email_frame import Email_frame
from interface_elements.settings_frame import Settings_frame
import random
import string
from validateJSONWindow import ValidateJSON

from tomlParser import Config

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Initialize ConfigParser object and load config.toml
        self.tomlData:Config = Config() 
        self.data:dict = self.tomlData.get_config()

        self.data_config: dict = self.data["config"]
        self.data_locale: dict = self.data["locale"]
        self.data_templates: dict = self.data["templates"]
        self.data_product_templates:dict = self.data["productTemplates"]
        self.data_settings: dict = self.data["settings"]
        

        # Frame padding and styling
        self.frame_padx:int = 8
        self.frame_pady:int = 8
        self.frame_corner_radius:int = 20

        self.element_padx:int = 8
        self.element_pady:int = 8

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")   

        # Initialize email object and set window properties
        self.email:Email = Email()
        self.title("AFS - validator")
        self.geometry("1000x600")
        self.font = customtkinter.CTkFont(family="roboto", size=12, weight="bold")
        self.header_font = customtkinter.CTkFont(family="roboto", size=16, weight="bold")
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0), weight=1)

        # menu frame
        self.menu = Menu(self,**self.data)

        # email frame
        self.email_frame = Email_frame(self)

        # settings frame 
        self.settings_frame = Settings_frame(self)

        self.build_payload()

        # layout
        self.bind("<KeyRelease>",lambda event:self.event_callback(**{"key":event.keysym}))


    def open_validateJSON_callback(self)->None:

        if not hasattr(self,"validataJSON_window"):
            self.validataJSON_window = ValidateJSON(self,**self.data_config)
        else:
            self.validataJSON_window.close_window()
           

    def open_settings_callback(self)-> None:
        
        # open settings window if it's not already opened
        if not hasattr(self,"settings_window"):
            self.settings_window:settingsWindow = settingsWindow(self,**self.data_config)  # create window if its None or destroyed
            
            self.settings_window.bind("<KeyRelease>",lambda event:self.event_callback(**{"key":event.keysym}))
        else:
            self.settings_window.close_window()


    def close_settings_callback(self):
        
        delattr(self,"settings_window")
        
    def close_validateJSON_callback(self):
        
        delattr(self,"validataJSON_window")
        
    def event_callback(self,**kwargs):

        """Update the layout based on the new state of the checkboxes and dropdowns"""

        # 
        if kwargs.get("generateRandomString") == "on":
            self.data["settings"]["referenceId"]["value"] = self.generate_random_string()
            self.settings_frame.frames["referenceId"].value.set(self.data["settings"]["referenceId"]["value"])

        # Create the payload and update the data
        self.get_values()
        self.build_payload()
        self.tomlData.save_config(**self.data)

        # Handle state change for checkboxes and dropdowns
        if kwargs.get("state") == "on":
            kwargs["entry"].grid() 

        if kwargs.get("state") == "off":
            kwargs["entry"].grid_remove()

        #send email
        if kwargs.get("send email"):
           
            self.send_smtp_email()

        
        
    def send_smtp_email(self):

        email = Email(**self.data)
        email.send_email()
       
    def build_payload(self):

        # build the payload
        self.payload = PayloadBuilder(self.get_payload_type(),self.data_templates,self.data_product_templates,**self.data_settings).build()
        self.email_frame.email_body.delete(0.0, "end")
        self.email_frame.email_body.insert(0.0, self.generate_html(self.payload))

        # save the payload
        self.data["payload"]["html"] = self.generate_html(self.payload)

    def get_payload_type(self):

        # map the payload type
        invitation_type:dict = {
            "service review": PayloadType.SERVICE_REVIEW,
            "service & product review(add/update product review)": PayloadType.SERVICE_AND_PRODUCT_REVIEW,
            "service & product review using sku": PayloadType.SERVICE_AND_PRODUCT_REVIEW_SKU
        }

        return invitation_type[str(self.menu.combobox.get()).lower()]

    def get_values(self):
        
        settingsElements:dict = self.settings_frame.frames
       
        for key, value in settingsElements.items():

            self.data_settings[key]['checkbox_value'] = value.checkbox_var.get()
            self.data_settings[key]['value'] = value.value.get()

        smptElements:dict = {}
        
        if hasattr(self,"settings_window"):
            smptElements:dict = self.settings_window._get()

        
        # update the data dictionary with the new merged data
        for key,value in chain(self.menu.get_values().items(),smptElements.items()):

            self.data_config[key] = value

        # update the menu object
        self.menu.set_values(**self.data)

    def generate_html(self, payload):
        
        # payload example data
        # {
        # "recipientEmail": "john_doe@domain.com",
        # "recipientName": "john doe",
        # "referenceId": "1234567890"
        # }

        # create an HTML string using the payload data
        sds = json.dumps(payload, indent=1)
        html = f"""<html>\n<head>\n<script type='application/json+trustpilot'>\n{sds}\n</script>\n</head>\n<body>\n<p>Hi!<br>\nHow are you?<br>\n</p>\n</body>\n</html>"""
         
        return html
    
    def generate_random_string(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

    def copy_link_callback(self):
        self.clipboard_clear()
        self.clipboard_append(self.link.get())
        self.update()

       
        




