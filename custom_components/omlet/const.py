"""Constants for the Omlet integration."""

DOMAIN = "omlet"

# API Configuration
API_BASE_URL = "https://x107.omlet.co.uk/api/v1"
API_ENDPOINTS = {
    "devices": "/device",
    "device": "/device/{device_id}",
    "device_config": "/device/{device_id}/configuration",
    "device_action": "/device/{device_id}/action/{action}",
}

# Device States
DOOR_STATE_OPEN = "open"
DOOR_STATE_CLOSED = "closed"
DOOR_STATE_OPENING = "onpending"
DOOR_STATE_CLOSING = "closepending"

# Device Actions
ACTION_OPEN = "open"
ACTION_CLOSE = "close"
ACTION_STOP = "stop"
ACTION_LIGHT_ON = "light_on"
ACTION_LIGHT_OFF = "light_off"

# Configuration
CONF_API_KEY = "api_key"
CONF_DEVICE_ID = "device_id"

# Device Attributes
ATTR_BATTERY_LEVEL = "battery_level"
ATTR_CONNECTED = "connected"
ATTR_LAST_UPDATE = "last_update"
ATTR_DOOR_STATE = "door_state"
ATTR_LIGHT_STATE = "light_state"
ATTR_LIGHT_LEVEL = "light_level"