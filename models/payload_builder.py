from datetime import datetime, timedelta
from enum import Enum
import random
import string
import json

class PayloadType(Enum):
    SERVICE_REVIEW = "serviceReview"
    SERVICE_AND_PRODUCT_REVIEW = "serviceAndProductReview"
    SERVICE_AND_PRODUCT_REVIEW_SKU = "serviceAndProductReviewWithFollowUp"

RANDOM_PRODUCT_NAMES = [
    "Wireless Bluetooth Headphones", "Organic Cotton T-Shirt", "Stainless Steel Water Bottle",
    "LED Desk Lamp", "Bamboo Cutting Board", "Yoga Mat Pro", "Ceramic Coffee Mug",
    "Leather Wallet", "Running Shoes", "Portable Phone Charger", "Cast Iron Skillet",
    "Noise Cancelling Earbuds", "Canvas Backpack", "Smart Watch Band", "Glass Food Container",
    "Memory Foam Pillow", "Electric Toothbrush", "Silicone Baking Mat", "Titanium Sunglasses",
    "Wool Beanie Hat", "Insulated Lunch Bag", "Digital Kitchen Scale", "Hiking Boots",
    "Plant-Based Protein Bar", "Reusable Shopping Bag", "Aromatherapy Diffuser",
    "Mechanical Keyboard", "Cotton Bed Sheets", "Travel Neck Pillow", "Stainless Steel Tumbler",
]

RANDOM_BRANDS = [
    "Acme", "NovaTech", "EcoLine", "PrimeCraft", "ZenWare", "UrbanEdge",
    "SkyBound", "PureForm", "VoltAge", "TerraGoods", "AquaFlow", "SilkPath",
]

class PayloadBuilder:
    """Builds the payload using a clean dictionary approach."""

    def __init__(self, payload_type: PayloadType, templates: dict, product_templates: dict, settings: dict, config: dict = None):
        self.payload_type = payload_type
        self.templates = templates
        self.product_templates = product_templates
        self.settings = settings
        self.config = config or {}

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
        # Check if random product generation is enabled
        if self.config.get("randomProducts") == "on":
            return self._build_random_products()

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

    def _build_random_products(self) -> dict:
        """Generate N random products for the payload."""
        try:
            count = int(self.config.get("randomProductsCount", "3"))
        except (ValueError, TypeError):
            count = 3
        count = max(1, min(count, 50))  # Clamp between 1-50

        products = []
        used_names = set()

        for i in range(count):
            # Pick a unique-ish product name
            name = random.choice(RANDOM_PRODUCT_NAMES)
            while name in used_names and len(used_names) < len(RANDOM_PRODUCT_NAMES):
                name = random.choice(RANDOM_PRODUCT_NAMES)
            used_names.add(name)

            sku = ''.join(random.choices(string.ascii_uppercase, k=3)) + "-" + ''.join(random.choices(string.digits, k=4))
            product_id = ''.join(random.choices(string.digits, k=5))
            brand = random.choice(RANDOM_BRANDS)

            product = {
                "productUrl": f"http://www.mycompanystore.com/products/{product_id}.html",
                "imageUrl": f"http://www.mycompanystore.com/products/images/{product_id}.jpg",
                "name": name,
                "sku": sku,
                "brand": brand,
            }
            products.append(product)

        return {"products": products} if products else {}

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
    sds = json.dumps(payload, indent=4)
    return f"""<html>
<head>
</head>
<body>
<p>Hi!<br>
How are you?<br>
</p>
<!--
<script type="application/json+trustpilot">
{sds}
</script>
-->
</body>
</html>"""

def parse_invitation_type(type_string: str) -> PayloadType:
    mapping = {
        "service review": PayloadType.SERVICE_REVIEW,
        "service & product review(add/update product review)": PayloadType.SERVICE_AND_PRODUCT_REVIEW,
        "service & product review using sku": PayloadType.SERVICE_AND_PRODUCT_REVIEW_SKU
    }
    return mapping.get(type_string.lower(), PayloadType.SERVICE_REVIEW)
