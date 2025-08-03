"""Sensor platform for Kstar Solar Inverter."""
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
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfPower,
    UnitOfArea,
    UnitOfMass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN, SENSOR_TYPES, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Kstar Solar Inverter sensors."""
    api = hass.data[DOMAIN][entry.entry_id]

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="kstar_solar",
        update_method=api.get_station_data,
        update_interval=SCAN_INTERVAL,
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for sensor_type, sensor_info in SENSOR_TYPES.items():
        entities.append(
            KstarSolarSensor(
                coordinator,
                entry,
                sensor_type,
                sensor_info,
            )
        )

    async_add_entities(entities)


class KstarSolarSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Kstar Solar Inverter sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        sensor_type: str,
        sensor_info: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._sensor_info = sensor_info
        self._attr_name = f"Kstar Solar {sensor_info['name']}"
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"
        self._attr_device_class = self._get_device_class(sensor_info["device_class"])
        self._attr_state_class = self._get_state_class(sensor_type)
        self._attr_native_unit_of_measurement = self._get_unit_of_measurement(
            sensor_info["unit"]
        )
        self._attr_icon = sensor_info["icon"]

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None

        value = self.coordinator.data.get(self._sensor_type)
        if value is None:
            return None

        # Convert to appropriate type
        try:
            if isinstance(value, (int, float)):
                return value
            elif isinstance(value, str):
                # Try to convert string to float
                return float(value)
            else:
                return value
        except (ValueError, TypeError):
            _LOGGER.warning("Could not convert value %s for sensor %s", value, self._sensor_type)
            return None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    def _get_device_class(self, device_class: str) -> SensorDeviceClass | None:
        """Get the device class."""
        if device_class == "power":
            return SensorDeviceClass.POWER
        elif device_class == "energy":
            return SensorDeviceClass.ENERGY
        elif device_class == "monetary":
            return SensorDeviceClass.MONETARY
        elif device_class == "weight":
            return SensorDeviceClass.WEIGHT
        elif device_class == "area":
            return SensorDeviceClass.AREA
        return None

    def _get_state_class(self, sensor_type: str) -> SensorStateClass | None:
        """Get the state class."""
        if sensor_type in ["realPower"]:
            return SensorStateClass.MEASUREMENT
        elif sensor_type in ["dayGeneration", "monthGeneration", "yearGeneration"]:
            return SensorStateClass.TOTAL
        elif sensor_type in ["totalGeneration"]:
            return SensorStateClass.TOTAL_INCREASING
        elif sensor_type in ["dayEarn", "totalEarn"]:
            return SensorStateClass.TOTAL
        elif sensor_type in ["co2", "coal", "forest"]:
            return SensorStateClass.TOTAL
        return None

    def _get_unit_of_measurement(self, unit: str) -> str | None:
        """Get the unit of measurement."""
        if unit == "W":
            return UnitOfPower.WATT
        elif unit == "kWh":
            return UnitOfEnergy.KILO_WATT_HOUR
        elif unit == "元":
            return "元"  # 直接使用字符串，不使用常量
        elif unit == "kg":
            return UnitOfMass.KILOGRAMS
        elif unit == "m²":
            return UnitOfArea.SQUARE_METERS
        return unit 