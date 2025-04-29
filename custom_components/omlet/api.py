"""API client for Omlet Smart Coop."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
from aiohttp import ClientTimeout

from .const import API_BASE_URL, API_ENDPOINTS

_LOGGER = logging.getLogger(__name__)

class OmletAPI:
    """Omlet API client."""

    def __init__(self, api_key: str) -> None:
        """Initialize the API client."""
        self._api_key = api_key
        self._session: aiohttp.ClientSession | None = None
        self._timeout = ClientTimeout(total=10)

    async def __aenter__(self) -> OmletAPI:
        """Enter async context."""
        self._session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=self._timeout,
        )
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit async context."""
        if self._session:
            await self._session.close()
            self._session = None

    async def get_devices(self) -> list[dict]:
        """Get all devices with their state and configuration."""
        if not self._session:
            raise RuntimeError("Session not initialized")
        
        async with self._session.get(f"{API_BASE_URL}{API_ENDPOINTS['devices']}") as response:
            response.raise_for_status()
            return await response.json()

    async def get_device(self, device_id: str) -> dict:
        """Get device details."""
        if not self._session:
            raise RuntimeError("Session not initialized")
        
        async with self._session.get(
            f"{API_BASE_URL}{API_ENDPOINTS['device'].format(device_id=device_id)}"
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def get_device_config(self, device_id: str) -> dict:
        """Get device configuration."""
        if not self._session:
            raise RuntimeError("Session not initialized")
        
        async with self._session.get(
            f"{API_BASE_URL}{API_ENDPOINTS['device_config'].format(device_id=device_id)}"
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def perform_action(self, device_id: str, action: str) -> dict:
        """Perform an action on the device."""
        if not self._session:
            raise RuntimeError("Session not initialized")
        
        async with self._session.post(
            f"{API_BASE_URL}{API_ENDPOINTS['device_action'].format(device_id=device_id, action=action)}"
        ) as response:
            response.raise_for_status()
            return await response.json() 