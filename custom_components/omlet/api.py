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
        """Enter the async context manager."""
        await self.ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the async context manager."""
        await self.close()

    async def ensure_session(self) -> None:
        """Ensure the session is initialized."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self._api_key}"},
                timeout=self._timeout,
            )

    async def close(self) -> None:
        """Close the session."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def get_devices(self) -> list[dict]:
        """Get all devices with their state and configuration."""
        await self.ensure_session()
        
        async with self._session.get(f"{API_BASE_URL}{API_ENDPOINTS['devices']}") as response:
            response.raise_for_status()
            return await response.json()

    async def get_device(self, device_id: str) -> dict:
        """Get device details."""
        await self.ensure_session()
        
        async with self._session.get(
            f"{API_BASE_URL}{API_ENDPOINTS['device'].format(device_id=device_id)}"
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def get_device_config(self, device_id: str) -> dict:
        """Get device configuration."""
        await self.ensure_session()
        
        async with self._session.get(
            f"{API_BASE_URL}{API_ENDPOINTS['device_config'].format(device_id=device_id)}"
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def perform_action(self, device_id: str, action: str) -> dict:
        """Perform an action on the device."""
        await self.ensure_session()
        
        async with self._session.post(
            f"{API_BASE_URL}{API_ENDPOINTS['device_action'].format(device_id=device_id, action=action)}"
        ) as response:
            response.raise_for_status()
            if response.status == 204:
                return {}
            return await response.json()