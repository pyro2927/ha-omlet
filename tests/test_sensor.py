"""Test the Omlet sensor component."""
from datetime import datetime
from unittest.mock import patch

import pytest
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_registry import EntityRegistry
from homeassistant.util import dt as dt_util

from custom_components.omlet.sensor import (
    OmletBatterySensor,
    OmletLightStateSensor,
    OmletLightLevelSensor,
    OmletLastOpenTimeSensor,
    OmletLastCloseTimeSensor,
)

@pytest.fixture
def mock_coordinator():
    """Create a mock coordinator."""
    with patch("custom_components.omlet.sensor.DataUpdateCoordinator") as mock:
        mock.data = {
            "test_device": {
                "connected": True,
                "batteryLevel": 80,
                "lightState": "on",
                "lightLevel": 50,
                "state": {
                    "door": {
                        "lastOpenTime": "2024-01-01T12:00:00Z",
                        "lastCloseTime": "2024-01-01T13:00:00Z",
                    }
                },
                "configuration": {
                    "general": {
                        "timezone": "America/New_York"
                    }
                }
            }
        }
        yield mock

@pytest.fixture
def mock_hass():
    """Create a mock Home Assistant instance."""
    with patch("homeassistant.core.HomeAssistant") as mock:
        yield mock

@pytest.mark.asyncio
async def test_battery_sensor(mock_coordinator, mock_hass):
    """Test the battery sensor."""
    sensor = OmletBatterySensor(mock_coordinator, "test_device", "test_config_entry")
    assert sensor.device_class == SensorDeviceClass.BATTERY

@pytest.mark.asyncio
async def test_light_state_sensor(mock_coordinator, mock_hass):
    """Test the light state sensor."""
    sensor = OmletLightStateSensor(mock_coordinator, "test_device", "test_config_entry")
    assert sensor.device_class == SensorDeviceClass.ENUM

@pytest.mark.asyncio
async def test_light_level_sensor(mock_coordinator, mock_hass):
    """Test the light level sensor."""
    sensor = OmletLightLevelSensor(mock_coordinator, "test_device", "test_config_entry")
    assert sensor.device_class == SensorDeviceClass.ILLUMINANCE

@pytest.mark.asyncio
async def test_last_open_time_sensor(mock_coordinator, mock_hass):
    """Test the last open time sensor."""
    sensor = OmletLastOpenTimeSensor(mock_coordinator, "test_device", "test_config_entry")
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert isinstance(sensor.native_value, datetime)
    # The time should be converted to the configured timezone
    assert sensor.native_value.tzinfo == dt_util.get_time_zone("America/New_York")

@pytest.mark.asyncio
async def test_last_close_time_sensor(mock_coordinator, mock_hass):
    """Test the last close time sensor."""
    sensor = OmletLastCloseTimeSensor(mock_coordinator, "test_device", "test_config_entry")
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert isinstance(sensor.native_value, datetime)
    # The time should be converted to the configured timezone
    assert sensor.native_value.tzinfo == dt_util.get_time_zone("America/New_York") 