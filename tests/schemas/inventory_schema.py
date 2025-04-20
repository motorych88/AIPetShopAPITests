INVENTORY_SCHEMA = {
    "type": "object",
    "properties": {
        "approved": {
            "type": "integer",
            "minimum": 0
        },
        "available": {
            "type": "integer",
            "minimum": 0
        },
        "delivered": {
            "type": "integer",
            "minimum": 0
        }

    },
    "required": ["approved", "available", "delivered"],
}
