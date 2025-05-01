"""The Omlet integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import OmletAPI
from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SWITCH, Platform.COVER]
SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Omlet from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    api = OmletAPI(entry.data["api_key"])
    coordinator = OmletDataUpdateCoordinator(hass, api, entry.entry_id)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator = hass.data[DOMAIN][entry.entry_id]
        await coordinator.api.close()
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

class OmletDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Omlet data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: OmletAPI,
        config_entry_id: str,
    ) -> None:
        """Initialize the data updater."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.api = api
        self.devices = {}
        self.config_entry_id = config_entry_id

    def get_device_info(self, device_id: str, config_entry_id: str) -> DeviceInfo:
        """Get device info for a device."""
        device_data = self.data.get(device_id, {})
        return DeviceInfo(
            config_entry_id=config_entry_id,
            identifiers={(DOMAIN, device_id)},
            name=device_data.get("name", f"Omlet Device {device_id}"),
            manufacturer="Omlet",
            model="Smart Coop",
            sw_version=device_data.get("state", {}).get("general", {}).get("firmwareVersion", "Unknown"),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from Omlet."""
        try:
            devices = await self.api.get_devices()
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
                    "light_level": device.get("state", {}).get("door", {}).get("lightLevel"),
                    "last_update": device.get("state", {}).get("general", {}).get("firmwareLastCheck"),
                    "configuration": device.get("configuration", {}),
                    "state": device.get("state", {})
                }
                # make sure to register the device in the device registry
                dr.async_get(self.hass).async_get_or_create(
                    config_entry_id=self.config_entry_id,
                    identifiers={(DOMAIN, device_id)},
                    name=device.get("name", f"Omlet Device {device_id}"),
                    manufacturer="Omlet",
                    model="Smart Coop",
                    sw_version=device.get("state", {}).get("general", {}).get("firmwareVersion", "Unknown")
                )
            
            return device_data
        except Exception as err:
            _LOGGER.error("Error fetching Omlet data: %s", err)
            raise