"""Support for Omlet covers."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.cover import (
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    ACTION_CLOSE,
    ACTION_OPEN,
    ACTION_STOP,
    ATTR_CONNECTED,
    ATTR_DOOR_STATE,
    DOOR_STATE_CLOSED,
    DOOR_STATE_CLOSING,
    DOOR_STATE_OPEN,
    DOOR_STATE_OPENING,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Omlet covers."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    # Create covers for each device
    entities = []
    for device_id, device_data in coordinator.data.items():
        # Only create door covers for devices that have a door state
        if ATTR_DOOR_STATE in device_data:
            entities.append(OmletCover(coordinator, device_id, config_entry.entry_id))
    
    async_add_entities(entities)

class OmletCover(CoordinatorEntity, CoverEntity):
    """Representation of an Omlet door cover."""

    _attr_name = "Door"
    _attr_has_entity_name = True
    _attr_device_class = CoverDeviceClass.DOOR
    _attr_supported_features = (
        CoverEntityFeature.OPEN
        | CoverEntityFeature.CLOSE
    )

    def __init__(self, coordinator: DataUpdateCoordinator, device_id: str, config_entry_id: str) -> None:
        """Initialize the cover."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._config_entry_id = config_entry_id
        self._attr_unique_id = f"{device_id}_door"

    @property
    def device_info(self) -> DeviceInfo:
        """Get the device info."""
        return self.coordinator.get_device_info(self._device_id)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self.coordinator.data is not None
            and self._device_id in self.coordinator.data
            and self.coordinator.data[self._device_id].get(ATTR_CONNECTED, False)
        )

    @property
    def device_data(self) -> dict:
        """Get the device data."""
        if not self.available:
            return {}
        return self.coordinator.data.get(self._device_id, {})

    @property
    def is_closed(self) -> bool | None:
        """Return if the cover is closed."""
        if not self.available:
            return None
        return self.coordinator.data[self._device_id].get(ATTR_DOOR_STATE) in [DOOR_STATE_CLOSED]

    @property
    def is_opening(self) -> bool:
        """Return if the cover is opening."""
        if not self.available:
            return False
        return self.coordinator.data[self._device_id].get(ATTR_DOOR_STATE) in [DOOR_STATE_OPENING]

    @property
    def is_closing(self) -> bool:
        """Return if the cover is closing."""
        if not self.available:
            return False
        return self.coordinator.data[self._device_id].get(ATTR_DOOR_STATE) in [DOOR_STATE_CLOSING]

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open the door."""
        await self.coordinator.api.perform_action(
            self._device_id, ACTION_OPEN
        )
        await self.coordinator.async_request_refresh()

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close the door."""
        await self.coordinator.api.perform_action(
            self._device_id, ACTION_CLOSE
        )
        await self.coordinator.async_request_refresh()