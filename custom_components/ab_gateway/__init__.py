""" The "ab gateway" custom component. """

import logging
import asyncio
import voluptuous as vol
import json
import copy
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.reload import async_reload_integration_platforms
from homeassistant.helpers.device_registry import format_mac
from homeassistant.const import (
    SERVICE_RELOAD,
    ATTR_NAME,
    Platform,
)
from homeassistant.components.mqtt import (
    CONF_DISCOVERY_PREFIX,
    CONF_BROKER,
)

from .const import (
    DOMAIN,
    DEFAULT_PREFIX,
    DEVICE_NAME,
)
from . import discovery

_LOGGER = logging.getLogger(__name__)

CONFIG_YAML = {}

async def async_setup(hass, config) -> bool:
    conf: ConfigType | None = config.get(DOMAIN)
    hass.data.setdefault(DOMAIN, {})

    _LOGGER.debug("Async setup AB Gateway")

    if DOMAIN not in config:
        return True

    global CONFIG_YAML
    CONFIG_YAML = json.loads(json.dumps(config[DOMAIN]))
    _LOGGER.debug("Initializing AB Gateway integration (YAML): %s", CONFIG_YAML)

    hass.async_add_job(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}, data=copy.deepcopy(CONFIG_YAML)
        )
    )

    return True

async def async_setup_entry(hass, entry) -> bool:
    _LOGGER.debug("Setup entry: %s", entry.data)
    config = {}

    for key, value in CONFIG_YAML.items():
        config[key] = value

    if CONF_DISCOVERY_PREFIX in entry.data:
        config[CONF_DISCOVERY_PREFIX] =  entry.data[CONF_DISCOVERY_PREFIX]

    if CONF_DISCOVERY_PREFIX not in config:
        config[CONF_DISCOVERY_PREFIX] =  DEFAULT_PREFIX

    await discovery.async_stop(hass)
    hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["queues"] = DiscoveryQueue()

    if entry.unique_id is None:
        hass.config_entries.async_update_entry(
            entry, unique_id = "ab_gateway"
        )

    return await _async_setup_discovery(hass, config, entry)

async def _async_setup_discovery(hass, config, entry) -> None:
    """Try to start the discovery of MQTT devices.
    This method is a coroutine.
    """
    # TODO: pass the config topic
    return await discovery.async_start(hass, config, entry)

async def async_reload_entry(hass, entry) -> None:
    """Reload the config entry when it changed."""
    _LOGGER.debug("Reload entry: %s", entry.entry_id)
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    _LOGGER.debug("async_unload_entry: %s", entry)
    return await discovery.async_stop(hass)

class DiscoveryQueue:
    """Discovery queue."""

    def __init__(self):
        """Init."""
        self.dataqueue = {
            "adv": asyncio.Queue()
        }

    def put(self, queue, msg):
        """Put message to queue"""
        return self.dataqueue[queue].put(msg)

    def get(self, queue):
        """Get queue"""
        return self.dataqueue[queue]

    def clean(self):
        """Clean queue"""
        return self.dataqueue["adv"].put(None)
