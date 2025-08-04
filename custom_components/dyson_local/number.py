
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.components.number import NumberEntity, NumberDeviceClass

from typing import Callable, Optional

from .vendor.libdyson.const import MessageType
from .vendor.libdyson import (
    DysonPureHotCool,
)

from .const import DATA_DEVICES, DOMAIN

from . import DysonEntity

import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: Callable
) -> None:
    """Set up Dyson button from a config entry."""
    device = hass.data[DOMAIN][DATA_DEVICES][config_entry.entry_id]
    name = config_entry.data[CONF_NAME]

    entities = []

    if isinstance(device, DysonPureHotCool):
        entities.extend(
            [
                DysonOscillationTargetNumber(device, name),
            ]
        )

    async_add_entities(entities)


class DysonOscillationTargetNumber(DysonEntity, NumberEntity):
    _attr_mode = "slider"
    _attr_native_unit_of_measurement = "°"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_device_class = NumberDeviceClass.WIND_DIRECTION
    _MESSAGE_TYPE = MessageType.ENVIRONMENTAL

    def __init__(self, device, name):
        """Initialize the number entity."""
        super().__init__(device, name)

    @property
    def sub_name(self) -> str:
        """Return the name of the number."""
        return "Oscillation Target"

    @property
    def sub_unique_id(self):
        """Return the sensor's unique id."""
        return "oscillation_target"

    @property
    def native_value(self):
        """Get current value"""
        return self._device.oscillation_target

    @property
    def native_step(self):
        """Min value """
        return 1.0

    @property
    def native_min_value(self):
        """Min value """
        return 5.0

    @property
    def native_max_value(self):
        """Max value"""
        return 355.0

    async def async_set_native_value(self, value: float) -> None:
        """Update the target angle."""
        _LOGGER.debug(f"Setting oscillation target to: {value}")
        self._device.set_oscillation_target(value)