"""The Kstar Solar Inverter integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .kstar_api import KstarSolarAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the Kstar Solar Inverter component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Kstar Solar Inverter from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create API client based on configuration
    api = KstarSolarAPI(
        host=entry.data["host"],
        station_id=entry.data["station_id"],
        refresh_token=entry.data["refresh_token"],
    )
    _LOGGER.info("使用刷新令牌认证方式")

    # Test the connection
    try:
        await hass.async_add_executor_job(api.get_station_data)
    except Exception as ex:
        _LOGGER.error("Failed to connect to Kstar Solar API: %s", ex)
        raise ConfigEntryNotReady from ex

    hass.data[DOMAIN][entry.entry_id] = api

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        api = hass.data[DOMAIN].pop(entry.entry_id)
        api.close()

    return unload_ok


# Import config flow to register it
from . import config_flow 