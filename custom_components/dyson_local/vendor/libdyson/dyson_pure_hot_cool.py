"""Dyson Pure Hot+Cool device."""

from typing import Optional

from .dyson_device import DysonHeatingDevice
from .dyson_pure_cool import DysonPureCoolBase

from .const import HotCoolOscillationMode

class DysonPureHotCool(DysonPureCoolBase, DysonHeatingDevice):
    """Dyson Pure Hot+Cool device."""

    @property
    def oscillation(self) -> bool:
        """Return oscillation status."""
        return self._get_field_value(self._status, "oson") == "ON"

    @property
    def oscillation_mode(self) -> HotCoolOscillationMode:
        """Return oscillation mode."""
        return HotCoolOscillationMode(self._get_field_value(self._status, "ancp"))

    def enable_oscillation(
        self, oscillation_mode: Optional[HotCoolOscillationMode] = None
    ) -> None:
        """Turn on oscillation."""
        if oscillation_mode is None:
            oscillation_mode = self.oscillation_mode

        self._set_configuration(oson="ON", fpwr="ON", ancp=oscillation_mode.value)

    def disable_oscillation(self) -> None:
        """Turn off oscillation."""
        self._set_configuration(oson="OFF")
