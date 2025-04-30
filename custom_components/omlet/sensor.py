"""Support for Omlet sensors."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    ATTR_BATTERY_LEVEL,
    ATTR_CONNECTED,
    ATTR_LAST_UPDATE,
    ATTR_LIGHT_LEVEL,
    ATTR_LIGHT_STATE,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Omlet sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    # Create sensors for each device
    entities = []
    for device_id, device_data in coordinator.data.items():
        entities.extend([
            OmletBatterySensor(coordinator, device_id),
            OmletLightStateSensor(coordinator, device_id),
            OmletLightLevelSensor(coordinator, device_id),
        ])
    
    async_add_entities(entities)

class OmletSensor(CoordinatorEntity, SensorEntity):
    """Base class for Omlet sensors."""

    def __init__(self, coordinator: DataUpdateCoordinator, device_id: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_has_entity_name = True
        self._attr_native_value = None
        self._attr_device_info = coordinator.get_device_info(device_id)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self.coordinator.data is not None
            and self._device_id in self.coordinator.data
            and self.coordinator.data[self._device_id].get(ATTR_CONNECTED, False)
        )

class OmletBatterySensor(OmletSensor):
    """Representation of an Omlet battery sensor."""

    _attr_name = "Battery"
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.coordinator.data[self._device_id].get(ATTR_BATTERY_LEVEL)

class OmletLightStateSensor(OmletSensor):
    """Representation of an Omlet light state sensor."""

    _attr_name = "Light State"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = ["on", "off"]

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.coordinator.data[self._device_id].get(ATTR_LIGHT_STATE)

class OmletLightLevelSensor(OmletSensor):
    """Representation of an Omlet light level sensor."""

    _attr_name = "Light Level"
    _attr_device_class = SensorDeviceClass.ILLUMINANCE
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.coordinator.data[self._device_id].get(ATTR_LIGHT_LEVEL)