"""The Omlet integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import OmletAPI
from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SWITCH]
SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Omlet from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    api = OmletAPI(entry.data["api_key"])
    coordinator = OmletDataUpdateCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

class OmletDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Omlet data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: OmletAPI,
    ) -> None:
        """Initialize the data updater."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.api = api

    async def _async_update_data(self) -> dict:
        """Fetch data from Omlet."""
        try:
            async with self.api as api:
                devices = await api.get_devices()
                device_data = {}
                
                for device in devices:
                    device_id = device["deviceId"]
                    # Use the device data directly from the /device endpoint
                    device_data[device_id] = {
                        "device_id": device_id,
                        "name": device.get("name", f"Omlet Device {device_id}"),
                        "connected": True,  # Assume connected if we got data
                        "battery_level": device.get("state", {}).get("general", {}).get("batteryLevel"),
                        "door_state": device.get("state", {}).get("door", {}).get("state"),
                        "light_state": device.get("state", {}).get("light", {}).get("state"),
                        "temperature": device.get("state", {}).get("general", {}).get("temperature"),
                        "humidity": device.get("state", {}).get("general", {}).get("humidity"),
                        "light_level": device.get("state", {}).get("door", {}).get("lightLevel"),
                        "last_update": device.get("state", {}).get("general", {}).get("firmwareLastCheck"),
                        "configuration": device.get("configuration", {}),
                        "state": device.get("state", {})
                    }
                
                return device_data
        except Exception as err:
            _LOGGER.error("Error fetching Omlet data: %s", err)
            raise