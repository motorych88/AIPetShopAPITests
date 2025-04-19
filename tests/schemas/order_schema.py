ORDER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "petId": {
            "type": "integer"
        },
        "quantity": {
            "type": "integer"
        },
        "status": {
            "type": "string"
        },
        "complete": {
            "type": "boolean"
        },

    },
    "required": ["id", "petId", "quantity", "status", "complete"],
}
