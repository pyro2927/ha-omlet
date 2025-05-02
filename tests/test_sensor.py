"""Test the Omlet sensor component."""
import json
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock

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
def device_response():
    """Load device response from JSON file."""
    with open(Path(__file__).parent / "fixtures" / "device_response.json") as f:
        return json.load(f)

@pytest.fixture
def mock_coordinator(device_response):
    """Create a mock coordinator with device response data."""
    coordinator = MagicMock()
    # Transform device response to match the structure in __init__.py
    device_data = {}
    for device in device_response:
        device_id = device["deviceId"]
        device_data[device_id] = {
            "device_id": device_id,
            "name": device.get("name", f"Omlet Device {device_id}"),
            "connected": True,
            "battery_level": device.get("state", {}).get("general", {}).get("batteryLevel"),
            "door_state": device.get("state", {}).get("door", {}).get("state"),
            "light_state": device.get("state", {}).get("light", {}).get("state"),
            "light_level": device.get("state", {}).get("door", {}).get("lightLevel"),
            "last_update": device.get("state", {}).get("general", {}).get("firmwareLastCheck"),
            "configuration": device.get("configuration", {}),
            "state": device.get("state", {})
        }
    coordinator.data = device_data
    coordinator.get_device_info = MagicMock(side_effect=lambda device_id: coordinator.data[device_id])
    coordinator.api = AsyncMock()
    coordinator.api.get_devices = AsyncMock(return_value=device_response)
    coordinator.async_refresh = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()
    return coordinator

@pytest.mark.asyncio
async def test_get_device_info(mock_coordinator):
    """Test getting device info from coordinator."""
    device_id = "kyWNebOzK4Kh63gC"
    device_info = mock_coordinator.get_device_info(device_id)
    assert device_info['name'] == "Erin's autodoor"

@pytest.fixture
def mock_hass():
    """Create a mock Home Assistant instance."""
    with patch("homeassistant.core.HomeAssistant") as mock:
        yield mock

@pytest.mark.asyncio
async def test_battery_sensor(mock_coordinator, mock_hass):
    """Test the battery sensor."""
    sensor = OmletBatterySensor(mock_coordinator, "kyWNebOzK4Kh63gC", "test_config_entry")
    assert sensor.device_class == SensorDeviceClass.BATTERY

@pytest.mark.asyncio
async def test_light_state_sensor(mock_coordinator, mock_hass):
    """Test the light state sensor."""
    sensor = OmletLightStateSensor(mock_coordinator, "kyWNebOzK4Kh63gC", "test_config_entry")
    assert sensor.device_class == SensorDeviceClass.ENUM

@pytest.mark.asyncio
async def test_light_level_sensor(mock_coordinator, mock_hass):
    """Test the light level sensor."""
    sensor = OmletLightLevelSensor(mock_coordinator, "kyWNebOzK4Kh63gC", "test_config_entry")
    assert sensor.device_class == SensorDeviceClass.ILLUMINANCE

@pytest.mark.asyncio
async def test_last_open_time_sensor(mock_coordinator, mock_hass):
    """Test the last open time sensor."""
    sensor = OmletLastOpenTimeSensor(mock_coordinator, "kyWNebOzK4Kh63gC", "test_config_entry")
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert isinstance(sensor.native_value, datetime)
    # The time should be converted to the configured timezone
    assert sensor.native_value.tzinfo == dt_util.get_time_zone("America/New_York")
    assert sensor.native_value.isoformat() == "2025-05-02T06:28:57-04:00"
    

@pytest.mark.asyncio
async def test_last_close_time_sensor(mock_coordinator, mock_hass):
    """Test the last close time sensor."""
    sensor = OmletLastCloseTimeSensor(mock_coordinator, "kyWNebOzK4Kh63gC", "test_config_entry")
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert isinstance(sensor.native_value, datetime)
    # The time should be converted to the configured timezone
    assert sensor.native_value.tzinfo == dt_util.get_time_zone("America/New_York")
    assert sensor.native_value.isoformat() == "2025-05-01T19:59:57-04:00"

# @pytest.mark.asyncio
# async def test_coordinator_refresh(mock_coordinator, mock_hass):
#     """Test that the coordinator refreshes data from the API."""
#     await mock_coordinator.async_refresh()
#     mock_coordinator.api.get_devices.assert_called_once() 