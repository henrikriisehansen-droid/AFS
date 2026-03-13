from datetime import datetime, timedelta
from enum import Enum
import random
import string
import json

class PayloadType(Enum):
    SERVICE_REVIEW = "serviceReview"
    SERVICE_AND_PRODUCT_REVIEW = "serviceAndProductReview"
    SERVICE_AND_PRODUCT_REVIEW_SKU = "serviceAndProductReviewWithFollowUp"

class PayloadBuilder:
    """Builds the payload using a clean dictionary approach."""

    def __init__(self, payload_type: PayloadType, templates: dict, product_templates: dict, settings: dict):
        self.payload_type = payload_type
        self.templates = templates
        self.product_templates = product_templates
        self.settings = settings

    def build(self) -> dict:
        """Constructs the final payload dictionary directly based on type."""
        payload = self._build_base_payload()
        
        if self.payload_type == PayloadType.SERVICE_REVIEW:
            return payload
            
        if self.payload_type == PayloadType.SERVICE_AND_PRODUCT_REVIEW:
            payload.update(self._build_product_payload())
            return payload

        if self.payload_type == PayloadType.SERVICE_AND_PRODUCT_REVIEW_SKU:
            payload.update(self._build_product_sku_payload())
            return payload
            
        return payload

    def _build_base_payload(self) -> dict:
        base_payload = {}
        for key, config in self.settings.items():
            if config.get("basePayload") and config.get("checkbox_value") == "on":
                value = config.get("value")
                
                # Format specific fields
                if key == "tags":
                    value = [v.strip() for v in value.split(',') if v.strip()]
                elif key in ["preferredSendTime", "productReviewInvitationPreferredSendTime"]:
                    value = self._get_preferred_send_time(value)
                elif key == "templateId":
                    value = self.templates.get(value, value)
                elif key == "productReviewInvitationTemplateId":
                    value = self.product_templates.get(value, value)
                    
                if value is not None and value != "":
                    base_payload[key] = value
                    
        return base_payload

    def _build_product_payload(self) -> dict:
        s = self.settings
        product = {}
        
        # Only add enabled product fields
        mappings = {
            "productUrl": "productUrl", "imageUrl": "imageUrl", "name": "name",
            "sku": "sku", "gtin": "gtin", "mpn": "mpn", "brand": "brand",
            "productCategoryGoogleId": "productCategoryGoogleId"
        }
        
        for ui_key, payload_key in mappings.items():
            if ui_key in s and s[ui_key].get("checkbox_value") == "on":
                val = s[ui_key].get("value")
                if val:
                    product[payload_key] = val
                    
        return {"products": [product]} if product else {}

    def _build_product_sku_payload(self) -> dict:
        skus_str = self.settings.get("productSkus", {}).get("value", "")
        if self.settings.get("productSkus", {}).get("checkbox_value") == "on":
            skus = [v.strip() for v in skus_str.split(",") if v.strip()]
            if skus:
                return {"productSkus": skus}
        return {}

    def _get_preferred_send_time(self, days: str) -> str:
        """Calculates the preferred send time."""
        if not days or not days.isdigit():
            days = '0'

        if len(str(days)) > 7:
            days = str(days)[:7]
        
        current_date = datetime.now()
        preferred_date = current_date + timedelta(days=int(days))
        return preferred_date.isoformat(timespec="seconds")

def generate_html_payload(payload: dict) -> str:
    sds = json.dumps(payload, indent=1)
    return f"""<html>\n<head>\n<script type='application/json+trustpilot'>\n{sds}\n</script>\n</head>\n<body>\n<p>Hi!<br>\nHow are you?<br>\n</p>\n</body>\n</html>"""

def parse_invitation_type(type_string: str) -> PayloadType:
    mapping = {
        "service review": PayloadType.SERVICE_REVIEW,
        "service & product review(add/update product review)": PayloadType.SERVICE_AND_PRODUCT_REVIEW,
        "service & product review using sku": PayloadType.SERVICE_AND_PRODUCT_REVIEW_SKU
    }
    return mapping.get(type_string.lower(), PayloadType.SERVICE_REVIEW)
