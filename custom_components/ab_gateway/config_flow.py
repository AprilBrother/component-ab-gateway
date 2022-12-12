"""Config flow to configure ab gateway component."""

from __future__ import annotations
from collections import OrderedDict
from typing import Any
import voluptuous as vol
import logging

from .const import (
    DOMAIN, 
    DEVICE_NAME, 
    DEFAULT_DISCOVERY,
)

from homeassistant.const import (
    CONF_DISCOVERY,
    CONF_HOST,
    CONF_PASSWORD,
    CONF_PAYLOAD,
    CONF_PORT,
    CONF_PROTOCOL,
    CONF_USERNAME,
)

from homeassistant.components.mqtt import (
    CONF_BROKER,
    CONF_DISCOVERY_PREFIX
)

from homeassistant import config_entries
from homeassistant.components import mqtt

_LOGGER = logging.getLogger(__name__)

STEP_BROKER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_DISCOVERY_PREFIX, default=DOMAIN): str,
    }
)

class ABGatewayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):
        _LOGGER.info("async_step_user");

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return await self.async_step_broker()

    async def async_step_broker(self, user_input=None):
        _LOGGER.info("async_step_broker %s", user_input);

        if user_input is None:
            return self.async_show_form(
                step_id="broker", data_schema=STEP_BROKER_DATA_SCHEMA
            )

        errors = {}
        if CONF_DISCOVERY_PREFIX not in user_input:
            user_input[CONF_DISCOVERY_PREFIX] = DEFAULT_DISCOVERY

        return self.async_create_entry(
            title="", data=user_input
        )


    async def async_step_import(self, user_input=None):
        """Handle import."""
        _LOGGER.debug("async_step_import: %s", user_input)
        return await self.async_step_user(user_input)
