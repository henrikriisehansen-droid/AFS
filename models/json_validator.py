from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError
import json

PAYLOAD_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "recipientEmail": {"type": "string", "format": "email"},
        "recipientName": {"type": "string", "minLength": 1},
        "referenceId": {"type": "string", "minLength": 1},
        "templateId": {"type": "string", "minLength": 1},
        "productReviewInvitationTemplateId": {"type": "string"},
        "locale": {"type": "string", "pattern": "^[a-z]{2}(-[A-Z]{2})?$"},
        "senderEmail": {"type": "string", "format": "email"},
        "senderName": {"type": "string", "minLength": 1},
        "replyTo": {"type": "string", "format": "email"},
        "preferredSendTime": {"type": "string", "format": "date-time"},
        "productReviewInvitationPreferredSendTime": {"type": "string", "format": "date-time"},
        "locationId": {"type": "string", "minLength": 1},
        "tags": {
            "type": "array",
            "items": {"type": "string"}
        },
        "products": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "productUrl": {"type": "string", "format": "uri"},
                    "imageUrl": {"type": "string", "format": "uri"},
                    "name": {"type": "string", "minLength": 1},
                    "sku": {"type": "string"},
                    "gtin": {"type": "string", "pattern": "^[0-9]+$"},
                    "mpn": {"type": "string"},
                    "brand": {"type": "string"},
                    "productCategoryGoogleId": {"type": "string", "pattern": "^[0-9]+$"}
                },
                "required": ["productUrl","imageUrl","name","sku"],
                "additionalProperties": False
            }
        },
        "productSkus": {
            "type": "array",
            "items": {"type": "string"},
            "additionalProperties": False
        }
    },
    "required": [
        "recipientEmail",
        "recipientName",
        "referenceId"
    ],
    "additionalProperties": False
}

def validate_json_string(json_string: str) -> tuple[bool, str]:
    """Validates a JSON string against the schema. Returns (is_valid, error_message)"""
    if not isinstance(json_string, str) or not json_string.strip():
        return False, "No JSON data provided."

    try:
        data = json.loads(json_string)
    except json.JSONDecodeError as e:
        lines = e.doc.splitlines()
        error_line_index = e.lineno - 1
        
        if 0 <= error_line_index < len(lines):
            error_line = lines[error_line_index]
            pointer = ' ' * (e.colno - 1) + '^'
            error_message = (
                f"JSON Formatting Error: {e.msg}\n\n"
                f"Error found at line {e.lineno}, column {e.colno}:\n"
                f"> {error_line}\n"
                f"> {pointer}\n"
            )
        else:
            error_message = f"JSON Error: {e}"
        return False, error_message

    validator = Draft7Validator(PAYLOAD_JSON_SCHEMA)
    errors = list(validator.iter_errors(data))

    if not errors:
        return True, "Validation successful!"

    error_messages = []
    for error in sorted(errors, key=lambda e: e.path):
        error_path_str = " -> ".join(map(str, error.path))
        
        key_value_info = ""
        if error.path and isinstance(error.absolute_path, (list, tuple)) and len(error.absolute_path) > 0:
            key_name = error.path[-1]
            parent_path = list(error.absolute_path)[:-1]
            parent_data = data
            try:
                for p_key in parent_path:
                    parent_data = parent_data[p_key]
                if isinstance(parent_data, dict) and key_name in parent_data:
                    key_value_info = f"  Key: '{key_name}', Value: '{parent_data[key_name]}'"
                elif isinstance(parent_data, list) and isinstance(key_name, int) and key_name < len(parent_data):
                    key_value_info = f"  Index: {key_name}, Value: '{parent_data[key_name]}'"
                else:
                    key_value_info = f"  Concerning Key/Item: '{key_name}'"
            except (KeyError, TypeError, IndexError):
                key_value_info = f"  Concerning Key/Item: '{key_name}' (error accessing parent data)"

        highlighted_error = (
            f"Error: {error.message}\n"
            f"  Path: {error_path_str or 'root'}\n"
            f"{key_value_info}\n"
            f"  Problematic instance part: '{error.instance}'\n"
            f"  Validator: '{error.validator}', Expected: '{error.validator_value}'"
        )
        error_messages.append(highlighted_error)

    text = ["Found validation errors:\n"]
    for msg in error_messages:
        text.append(msg + "\n" + "-"*30)
        
    return False, "\n".join(text)
