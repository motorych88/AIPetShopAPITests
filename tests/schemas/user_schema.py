USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "minimum": 0
        },
        "username": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "firstName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "lastName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "email": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        "password": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "phone": {
            "type": "string",
            "maxLength": 11
        },
        "userStatus": {
            "type": "integer",
            "minimum": 0
        },

    },
    "required": ["id", "username", "firstName", "lastName", "email", "password", "phone", "userStatus"],
}
