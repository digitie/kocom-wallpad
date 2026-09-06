"""Base platform for Kocom Wallpad."""

from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity, RestoredExtraData
from homeassistant.core import callback
from homeassistant.const import Platform
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.components.light import LightEntityDescription
from homeassistant.components.switch import SwitchEntityDescription
from homeassistant.components.climate import ClimateEntityDescription
from homeassistant.components.fan import FanEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.binary_sensor import BinarySensorEntityDescription

from .const import DOMAIN, DeviceType, SubType


ENTITY_DESCRIPTION_MAP = {
    Platform.LIGHT: LightEntityDescription,
    Platform.SWITCH: SwitchEntityDescription,
    Platform.CLIMATE: ClimateEntityDescription,
    Platform.FAN: FanEntityDescription,
    Platform.SENSOR: SensorEntityDescription,
    Platform.BINARY_SENSOR: BinarySensorEntityDescription
}


class KocomBaseEntity(RestoreEntity):
    """Base class for Kocom entities."""

    _attr_should_poll = False  # push-only: all updates arrive via the gateway dispatcher

    def __init__(self, gateway, device) -> None:
        """Initialize the base entity."""
        super().__init__()
        self.gateway = gateway
        self._device = device
        self._unsubs: list[callable] = []

        # NOTE: keyed by the config entry id (stable across host/IP changes),
        # not self.gateway.host. Changing this after entities already exist
        # is itself a breaking change for those installs - see PR notes.
        self._attr_unique_id = f"{device.key.unique_id}:{self.gateway.entry.entry_id}"
        self.entity_description = ENTITY_DESCRIPTION_MAP[self._device.platform](
            key=self.format_key,
            has_entity_name=True,
            translation_key=self.format_key,
            translation_placeholders={"id": self.format_translation_placeholders}
        )
        self._attr_device_info = DeviceInfo(
            connections={(self.gateway.host, self.unique_id)},
            identifiers={(DOMAIN, f"{self.gateway.entry.entry_id}_{self.format_identifiers}")},
            manufacturer="KOCOM Co., Ltd",
            model="Smart Wallpad",
            name=f"{self.format_identifiers}",
            via_device=(DOMAIN, str(self.gateway.host)),
        )
        
    @property
    def format_key(self) -> str:
        if self._device.key.sub_type == SubType.NONE:
            return self._device.key.device_type.name.lower()
        else:
            return f"{self._device.key.device_type.name.lower()}-{self._device.key.sub_type.name.lower()}"

    @property
    def format_translation_placeholders(self) -> str:
        if self._device.key.sub_type == SubType.NONE:
            return f"{str(self._device.key.room_index)}-{str(self._device.key.device_index)}"
        else:
            return f"{str(self._device.key.room_index)}-{str(self._device.key.device_index)}"

    @property
    def format_identifiers(self) -> str:
        if self._device.key.device_type in {
            DeviceType.VENTILATION, DeviceType.GASVALVE, DeviceType.ELEVATOR, DeviceType.MOTION
        }:
            return f"KOCOM"
        elif self._device.key.device_type in {
            DeviceType.LIGHT, DeviceType.LIGHTCUTOFF, DeviceType.DIMMINGLIGHT
        }:
            return f"KOCOM LIGHT"
        else:
            return f"KOCOM {self._device.key.device_type.name}"

    @property
    def available(self) -> bool:
        return self.gateway.conn._is_connected()

    async def async_added_to_hass(self):
        sig = self.gateway.async_signal_device_updated(self._device.key.unique_id)

        @callback
        def _handle_update(dev):
            self._device = dev
            self.update_from_state()
        self._unsubs.append(async_dispatcher_connect(self.hass, sig, _handle_update))

    async def async_will_remove_from_hass(self) -> None:
        for unsub in self._unsubs:
            try:
                unsub()
            except Exception:
                pass
        self._unsubs.clear()

    @callback
    def update_from_state(self) -> None:
        self.async_write_ha_state()

    # Keys in KocomController._device_storage that aren't scoped to one
    # device's unique_id (shared across all ventilation/elevator entities).
    _GLOBAL_STORAGE_KEYS = ("ventil_feature", "ventil_modes", "available_floor")

    @property
    def extra_restore_state_data(self) -> RestoredExtraData:
        uid = self._device.key.unique_id
        full_storage = self.gateway.controller._device_storage
        own_storage = {
            k: v for k, v in full_storage.items()
            if k.startswith(f"{uid}_") or k in self._GLOBAL_STORAGE_KEYS
        }
        return RestoredExtraData({
            "packet": getattr(self._device, "_packet", bytes()).hex(),
            "device_storage": own_storage
        })
