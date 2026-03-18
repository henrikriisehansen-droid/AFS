import toml
import os
import sys

class ConfigManager:
    def __init__(self, config_filename: str = "config.toml"):
        # Resolve path relative to executable if frozen, or relative to script if not
        if getattr(sys, 'frozen', False):
            # If it's a bundle, the executable is in Contents/MacOS/
            # and we might want the config next to the .app or inside?
            # Usually, next to the .app is better for "portable" apps.
            # But inside the .app/Contents/Resources is for fixed data.
            # Let's go with the directory containing the .app (or the exe).
            exec_dir = os.path.dirname(sys.executable)
            if '.app/Contents/MacOS' in exec_dir:
                # Go up to the directory containing the .app
                self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(exec_dir))), config_filename)
            else:
                self.config_path = os.path.join(exec_dir, config_filename)
        else:
            self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), config_filename)
        
        self.data = None

        if not os.path.exists(self.config_path):
            self.data = self._default_config()
            self.save_config(self.data)
        else:
            self._load_config()

    def _load_config(self):
        try:
            with open(self.config_path, "r") as f:
                self.data = toml.load(f)
        except FileNotFoundError:
            print(f"Error: {self.config_path} not found")
            self.data = self._default_config()
        except toml.decoder.TomlDecodeError as e:
            print(f"Error decoding TOML: {e}")
            self.data = self._default_config()

    def save_config(self, config_data: dict):
        self.data = config_data
        with open(self.config_path, "w") as f:
            toml.dump(self.data, f)

    def get_config(self) -> dict:
        return self.data

    def _default_config(self):
        data = {
            "config": {
                "afs_email": "domain@trustpilot.com",
                "email_subject": "test email subject",
                "bcc_email": "anotherEmail@gmail.com",
                "invitation_type": "service review",
                "agentmail_api_key": "",
                "agentmail_inbox_id": "",
                "sendAfsDirect": "off",
                "randomReferenceNumber": "off"
            },
            "locale": {
                "en-US": "www.trustpilot.com",
                "de-AT": "at.trustpilot.com",
                "en-AU": "au.trustpilot.com",
                "pt-BR": "br.trustpilot.com",
                "en-CA": "ca.trustpilot.com",
                "de-CH": "ch.trustpilot.com",
                "de-DE": "de.trustpilot.com",
                "da-DK": "dk.trustpilot.com",
                "es-ES": "es.trustpilot.com",
                "fi-FI": "fi.trustpilot.com",
                "fr-FR": "fr.trustpilot.com",
                "fr-BE": "fr-be.trustpilot.com",
                "en-IE": "ie.trustpilot.com",
                "it-IT": "it.trustpilot.com",
                "ja-JP": "jp.trustpilot.com",
                "nl-NL": "nl.trustpilot.com",
                "nl-BE": "nl-be.trustpilot.com",
                "nb-NO": "no.trustpilot.com",
                "en-NZ": "nz.trustpilot.com",
                "pl-PL": "pl.trustpilot.com",
                "pt-PT": "pt.trustpilot.com",
                "sv-SE": "se.trustpilot.com",
                "en-GB": "uk.trustpilot.com"
            },
            "templates": {
                "English - Service reviews": "529c0abfefb96008b894ad02",
                "Danish - Service reviews": "5278a72d0da2b11ee0f0088c",
                "Dutch - Service reviews": "529c0b84748a510aa8cb03e3",
                "Finnish - Service reviews": "529c0bd4dec7e10ed0ba75ce",
                "French - Service reviews": "529c0bd6748a510aa8cb03e4",
                "German - Service reviews": "5278a79c0da2b11ee0f0088e",
                "Italian - Service reviews": "5278a7700da2b11ee0f0088d",
                "Japanese - Service reviews": "5469e6b009dd3a0b08a6f341",
                "Norwegian - Service reviews": "529c0b06dec7e10ed0ba75cb",
                "Polish - Service reviews": "5385f1ad748a510cf820e3e4",
                "Portuguese - Service reviews": "5630afb41088c2088c06c462",
                "Portuguese (Brazil) - Service reviews": "5489736809dd3a0688d5cba6",
                "Spanish - Service reviews": "529469ffefb9600ddce7a2d7",
                "Swedish - Service reviews": "529c0b40dec7e10ed0ba75cc"
            },
            "productTemplates": {
                "English - Optimized for product reviews": "5c17c7ebb565bb0001046fbd",
                "Danish - Optimized for product reviews": "5c505b600e0d37000127c6ff",
                "Dutch - Optimized for product reviews": "5c5b121464c50a0001c5a55a",
                "Finnish - Optimized for product reviews": "5c5b1351048417000135ad6f",
                "French - Optimized for product reviews": "5c5b1311f366710001540aaa",
                "German - Optimized for product reviews": "5c50357526f61800019768ca",
                "Italian - Optimized for product reviews": "5c5b12ce3501e50001628e88",
                "Japanese - Optimized for product reviews": "5c5b1292d098210001a66f32",
                "Norwegian - Optimized for product reviews": "5c5b11ba47ad0f0001f388da",
                "Polish - Optimized for product reviews": "5c5b10dd47942a0001639034",
                "Portuguese - Optimized for product reviews": "5c5b0fd73b442a000141e542",
                "Portuguese (Brazil) - Optimized for product reviews": "5c5b143d6cdcf00001a8f174",
                "Spanish - Optimized for product reviews": "5c5b13c49d4c8600019d8de3",
                "Swedish - Optimized for product reviews": "5c5b0e17d036820001e42b25"
            },
            "payload": {
                "html": "<html>\n<head>\n<script type='application/json+trustpilot'>\n{\n \"recipientEmail\": \"recipientEmail@gmail.com\",\n \"recipientName\": \"john doe\",\n \"referenceId\": \"1234\"\n}\n</script>\n</head>\n<body>\n<p>Hi!<br>\nHow are you?<br>\n</p>\n</body>\n</html>"
            },
            "settings": {
                "recipientEmail":{"type": "entry","label": "Recipient Email","checkbox_value":"on","value":"recipientEmail@gmail.com","basePayload":True},
                "recipientName":{"type": "entry","label": "Recipient Name","checkbox_value":"on","value":"john doe","basePayload":True},
                "referenceId":{"type": "entry","label": "Reference Id","checkbox_value":"on","value":"1234","basePayload":True},
                "locale":{"type": "combobox","label": "Locale","value":"en-US","checkbox_value":"off","data":"data_locale","basePayload":True},
                "locationId":{"type": "entry","label": "Location ID","checkbox_value":"off","value":"12345","basePayload":True},
                "tags":{"type": "entry","label": "Tags","checkbox_value":"off","value":"testTag,testtag2","basePayload":True},
                "templateId":{"type": "combobox","label": "Template","value":"English - Service reviews","checkbox_value":"off","data":"data_templates","basePayload":True},
                "senderEmail":{"type": "entry","label": "Sender Email","checkbox_value":"off","value":"sender@gmail.com","basePayload":True},
                "senderName":{"type": "entry","label": "Sender Name","checkbox_value":"off","value":"john doe","basePayload":True},
                "replyTo":{"type": "entry","label": "Reply To","checkbox_value":"off","value":"reply@gmail.com","basePayload":True},
                "preferredSendTime":{"type": "entry","label": "Preferred Send Time","checkbox_value":"off","value":"0","basePayload":True},
                "productReviewInvitationPreferredSendTime":{"type": "entry","label": "Product Review Invitation Preferred Send Time","checkbox_value":"off","value":"0","basePayload":True},
                "productReviewInvitationTemplateId":{"type": "combobox","label": "Product Review Invitation Template","checkbox_value":"off","value":"English - Optimized for product reviews","data":"data_product_templates","basePayload":True},
                "productSkus":{"type": "entry","label": "Product SKUs","checkbox_value":"off","value":"1234,1234","basePayload":False},
                "productUrl": {"type": "entry","label": "productUrl","checkbox_value":"off","value":"http://www.mycompanystore.com/products/12345.html","basePayload":False},
                "imageUrl": {"type": "entry","label": "imageUrl","checkbox_value":"off","value":"http://www.mycompanystore.com/products/images/12345.jpg","basePayload":False},
                "name": {"type": "entry","label": "Product name","checkbox_value":"off","value":"Metal Toy Car","basePayload":False},
                "sku": {"type": "entry","label": "Product SKU","checkbox_value":"off","value":"ABC-1234","basePayload":False},
                "gtin": {"type": "entry","label": "Product GTIN","checkbox_value":"off","value":"01234567890","basePayload":False},
                "mpn":{"type": "entry","label": "Product MPN","checkbox_value":"off","value":"7TX1641","basePayload":False},
                "brand": {"type": "entry","label": "Product brand","checkbox_value":"off","value":"Acme","basePayload":False},
                "productCategoryGoogleId": {"type": "entry","label": "productCategoryGoogleId","checkbox_value":"off","value":"1234","basePayload":False}
            }
        }
        return data
