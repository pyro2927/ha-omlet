"""Support for Omlet switches."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    ACTION_CLOSE,
    ACTION_LIGHT_OFF,
    ACTION_LIGHT_ON,
    ACTION_OPEN,
    ACTION_STOP,
    ATTR_CONNECTED,
    ATTR_DOOR_STATE,
    ATTR_LIGHT_STATE,
    DOOR_STATE_CLOSED,
    DOOR_STATE_OPEN,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Omlet switches."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    # Create switches for each device
    entities = []
    for device_id, device_data in coordinator.data.items():
        # Only create door switches for devices that have a door state
        # if ATTR_DOOR_STATE in device_data:
        #     entities.append(OmletDoorSwitch(coordinator, device_id))
        
        # Only create light switches for devices that have a light state
        if ATTR_LIGHT_STATE in device_data:
            entities.append(OmletLightSwitch(coordinator, device_id))
    
    async_add_entities(entities)

class OmletSwitch(CoordinatorEntity, SwitchEntity):
    """Base class for Omlet switches."""

    def __init__(self, coordinator: DataUpdateCoordinator, device_id: str) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_has_entity_name = True
        self._attr_is_on = False

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self.coordinator.data is not None
            and self._device_id in self.coordinator.data
            and self.coordinator.data[self._device_id].get(ATTR_CONNECTED, False)
        )

class OmletDoorSwitch(OmletSwitch):
    """Representation of an Omlet door switch."""

    _attr_name = "Door"
    _attr_icon = "mdi:door"

    @property
    def is_on(self) -> bool:
        """Return true if door is open."""
        return self.coordinator.data[self._device_id].get(ATTR_DOOR_STATE) == DOOR_STATE_OPEN

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Open the door."""
        await self.coordinator.api.perform_action(
            self._device_id, ACTION_OPEN
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Close the door."""
        await self.coordinator.api.perform_action(
            self._device_id, ACTION_CLOSE
        )
        await self.coordinator.async_request_refresh()

class OmletLightSwitch(OmletSwitch):
    """Representation of an Omlet light switch."""

    _attr_name = "Light"
    _attr_icon = "mdi:lightbulb"

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self.coordinator.data[self._device_id].get(ATTR_LIGHT_STATE) == "on"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the light."""
        await self.coordinator.api.perform_action(
            self._device_id, ACTION_LIGHT_ON
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        await self.coordinator.api.perform_action(
            self._device_id, ACTION_LIGHT_OFF
        )
        await self.coordinator.async_request_refresh()