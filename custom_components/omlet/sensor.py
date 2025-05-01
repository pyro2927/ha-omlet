"""Support for Omlet sensors."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import dt as dt_util

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
            OmletBatterySensor(coordinator, device_id, config_entry.entry_id),
            OmletLightStateSensor(coordinator, device_id, config_entry.entry_id),
            OmletLightLevelSensor(coordinator, device_id, config_entry.entry_id),
            OmletLastOpenTimeSensor(coordinator, device_id, config_entry.entry_id),
            OmletLastCloseTimeSensor(coordinator, device_id, config_entry.entry_id),
        ])
    
    async_add_entities(entities)

class OmletSensor(CoordinatorEntity, SensorEntity):
    """Base class for Omlet sensors."""

    def __init__(self, coordinator: DataUpdateCoordinator, device_id: str, config_entry_id: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._config_entry_id = config_entry_id
        self._attr_has_entity_name = True
        self._attr_native_value = None
        self._available = True

    @property
    def device_info(self) -> DeviceInfo:
        """Get the device info."""
        return self.coordinator.get_device_info(self._device_id, self._config_entry_id)

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

class OmletBatterySensor(OmletSensor):
    """Representation of an Omlet battery sensor."""

    _attr_name = "Battery"
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.device_data.get(ATTR_BATTERY_LEVEL)

class OmletLightStateSensor(OmletSensor):
    """Representation of an Omlet light state sensor."""

    _attr_name = "Light State"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = ["on", "off"]

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.device_data.get(ATTR_LIGHT_STATE)

class OmletLightLevelSensor(OmletSensor):
    """Representation of an Omlet light level sensor."""

    _attr_name = "Light Level"
    _attr_device_class = SensorDeviceClass.ILLUMINANCE
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.device_data.get(ATTR_LIGHT_LEVEL)

class OmletLastOpenTimeSensor(OmletSensor):
    """Representation of an Omlet door last open time sensor."""

    _attr_name = "Last Open Time"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        time_str = self.device_data.get("state", {}).get("door", {}).get("lastOpenTime")
        if not time_str:
            return None
        try:
            # Parse the time string as UTC
            dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
            # Get the timezone from the coordinator
            timezone = self.device_data.get("configuration", {}).get("general", {}).get("timezone")
            # Convert to the specified timezone
            return dt.replace(tzinfo=None).astimezone(dt_util.get_time_zone(timezone))
        except (ValueError, TypeError):
            _LOGGER.error("Invalid date format for lastOpenTime: %s", time_str)
            return None

class OmletLastCloseTimeSensor(OmletSensor):
    """Representation of an Omlet door last close time sensor."""

    _attr_name = "Last Close Time"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        time_str = self.device_data.get("state", {}).get("door", {}).get("lastCloseTime")
        if not time_str:
            return None
        try:
            # Parse the time string as UTC
            dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
            # Get the timezone from the coordinator
            timezone = self.device_data.get("configuration", {}).get("general", {}).get("timezone")
            # Convert to the specified timezone
            return dt.replace(tzinfo=None).astimezone(dt_util.get_time_zone(timezone))
        except (ValueError, TypeError):
            _LOGGER.error("Invalid date format for lastCloseTime: %s", time_str)
            return None