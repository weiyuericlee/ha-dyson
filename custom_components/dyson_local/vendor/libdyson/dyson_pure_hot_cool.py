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
    def oscillation_angle_low(self) -> int:
        """Return oscillation low angle."""
        return int(self._get_field_value(self._status, "osal"))

    @property
    def oscillation_angle_high(self) -> int:
        """Return oscillation high angle."""
        return int(self._get_field_value(self._status, "osau"))

    @property
    def oscillation_mode(self) -> HotCoolOscillationMode:
        """Return oscillation mode."""
        oscillation = self.oscillation
        angle_low = self.oscillation_angle_low
        angle_high = self.oscillation_angle_high
        oscillation_mode = self._get_field_value(self._status, "ancp")
        if not oscillation:
            return HotCoolOscillationMode.OFF
        elif oscillation_mode == 'CUST':
            angle_diff = angle_high-angle_low
            if angle_diff == 44:
                return HotCoolOscillationMode.DEGREE_45
            elif angle_diff == 90:
                return HotCoolOscillationMode.DEGREE_90
            elif angle_diff == 180:
                return HotCoolOscillationMode.DEGREE_180
            elif angle_diff == 350:
                return HotCoolOscillationMode.DEGREE_350
        else:
            return HotCoolOscillationMode(oscillation_mode)

    def enable_oscillation(
        self, oscillation_mode: Optional[HotCoolOscillationMode] = None
    ) -> None:
        """Turn on oscillation."""
        if oscillation_mode is None:
            oscillation_mode = HotCoolOscillationMode.DEGREE_45
        if oscillation_mode == HotCoolOscillationMode.OFF:
            self._set_configuration(oson="OFF")
        else:
            self._set_configuration(oson="ON", fpwr="ON", ancp=oscillation_mode.value)

    def disable_oscillation(self) -> None:
        """Turn off oscillation."""
        self._set_configuration(oson="OFF")
