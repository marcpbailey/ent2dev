# __init__.py

from __future__ import annotations

import asyncio
import logging
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import (
    device_registry as dr,
    entity_registry as er,
    area_registry as ar,
)
from homeassistant.helpers.entity_registry import EVENT_ENTITY_REGISTRY_UPDATED
from homeassistant.helpers.device_registry import EVENT_DEVICE_REGISTRY_UPDATED
from .const import DOMAIN, PLATFORMS, ATTRIBUTES

LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    # Set up the Entity Device Mapper integration.
    # We don't set up via YAML, only config entries
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    LOGGER.info("Entity Device Mapper: setting up entry %s", entry.entry_id)

    device_reg = dr.async_get(hass)
    entity_reg = er.async_get(hass)
    area_reg = ar.async_get(hass)

    entity_to_device_list = await build_entity_map(device_reg, entity_reg, area_reg)

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    hass.data[DOMAIN][entry.entry_id] = {
        "entity_to_device": entity_to_device_list,
        "sensor_entity": None,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    @callback
    def registry_updated_callback(event):
        LOGGER.info(
            "Entity or Device registry updated, rebuilding map for entry %s...",
            entry.entry_id,
        )
        asyncio.create_task(rebuild_map_and_update_sensor(hass, entry))

    hass.bus.async_listen(EVENT_ENTITY_REGISTRY_UPDATED, registry_updated_callback)
    hass.bus.async_listen(EVENT_DEVICE_REGISTRY_UPDATED, registry_updated_callback)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Unload a config entry
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

async def build_entity_map(device_reg: dr.DeviceRegistry, entity_reg: er.EntityRegistry, area_reg: ar.AreaRegistry) -> list[dict]:
    entity_to_device_list = []

    for entity_id, entry in entity_reg.entities.items():
        # Skip entities without a valid device_id
        device_id = entry.device_id
        if not device_id:
            continue  # Skip entities without a device_id

        device = device_reg.async_get(device_id)

        record = {
            "entity_id": entity_id,
            "device_id": device_id,
        }

        for attr, default_value in ATTRIBUTES.items():
            if attr == "friendly_name":
                if device:
                    # Use 'name_by_user' if available, else fallback to 'name'
                    name_by_user = getattr(device, "name_by_user", None)
                    name = getattr(device, "name", None)
                    record["friendly_name"] = name_by_user or name or default_value
                else:
                    record["friendly_name"] = default_value
            elif attr == "area_name":
                if device and device.area_id:
                    area = area_reg.async_get_area(device.area_id)
                    record["area_name"] = area.name if area else default_value
                else:
                    record["area_name"] = default_value
            else:
                if device:
                    value = getattr(device, attr, None)
                    record[attr] = value if value not in [None, ""] else default_value
                else:
                    record[attr] = default_value

        entity_to_device_list.append(record)

    return entity_to_device_list

async def rebuild_map_and_update_sensor(hass: HomeAssistant, entry: ConfigEntry):
    # Rebuild the entity map and update the sensor entity.
    device_reg = dr.async_get(hass)
    entity_reg = er.async_get(hass)
    area_reg = ar.async_get(hass)
    entity_to_device_list = await build_entity_map(device_reg, entity_reg, area_reg)

    hass.data[DOMAIN][entry.entry_id]["entity_to_device"] = entity_to_device_list

    sensor_entity = hass.data[DOMAIN][entry.entry_id]["sensor_entity"]
    if sensor_entity:
        sensor_entity.async_write_ha_state()