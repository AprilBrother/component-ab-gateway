"""Constants of the AB Gateway component."""

from homeassistant.const import (
    Platform,
)

DOMAIN = "ab_gateway"
DEVICE_NAME = "ab_gateway"

CONF_GATEWAY_ID = "gateway_id"
CONF_UUID = "uuid"
CONF_RESTORE_STATE = "restore_state"
CONF_PERIOD = "period"
CONF_DEVICE_TRACK = "track_device"

DEFAULT_PREFIX = DOMAIN
DEFAULT_DISCOVERY = True
DEFAULT_DISCOVERY_PREFIX = "discovery_prefix"
DEFAULT_RESTORE_STATE = False
DEFAULT_DEVICE_TRACK = False
DEFAULT_PERIOD = 60

INDEX_ADV = 3
INDEX_MAC = 1
INDEX_RSSI = 2
