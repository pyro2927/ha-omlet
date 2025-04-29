"""Config flow for Omlet integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .api import OmletAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class OmletConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Omlet."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                async with OmletAPI(user_input["api_key"]) as api:
                    # Verify API key by attempting to get devices
                    await api.get_devices()
                return self.async_create_entry(
                    title="Omlet Smart Coop",
                    data={
                        "api_key": user_input["api_key"],
                    },
                )
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("api_key"): str,
                }
            ),
            errors=errors,
        )