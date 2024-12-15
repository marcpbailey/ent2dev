# custom_components/ent2dev/sensor.py

from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, SENSOR_ENTITY_ID

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Entity Device Map sensor."""
    sensor = EntityDeviceMapSensor(hass, entry)
    async_add_entities([sensor], True)
    hass.data[DOMAIN][entry.entry_id]["sensor_entity"] = sensor

class EntityDeviceMapSensor(SensorEntity):
    """Representation of the Entity Device Map sensor."""

    def __init__(self, hass, entry):
        """Initialize the sensor."""
        self._hass = hass
        self._entry = entry
        self._attr_name = "Entity Device Map"
        self._attr_unique_id = SENSOR_ENTITY_ID
        self._attr_attribution = "Powered by ent2dev"

    @property
    def state(self):
        """Return the state of the sensor."""
        return "active"

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        data = self._hass.data.get(DOMAIN, {})
        entry_data = data.get(self._entry.entry_id, {})
        entity_to_device = entry_data.get("entity_to_device", [])
        return {"mapping": entity_to_device}