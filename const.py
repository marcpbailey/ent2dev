### const.py

Defines constants such as `DOMAIN`, `PLATFORMS`, `SENSOR_ENTITY_ID`, and the `ATTRIBUTES` dictionary that specifies which device attributes to include.

```python
# custom_components/ent2dev/const.py

DOMAIN = "ent2dev"
PLATFORMS = ["sensor"]

# SENSOR_ENTITY_ID is used as the unique ID for the sensor entity
SENSOR_ENTITY_ID = "sensor.entity_device_map"

# ATTRIBUTES is a dict of attribute_name -> default_value.
# These keys are tried as device attributes via getattr(device, attr, "unknown key").
# Special case: "friendly_name" is handled by combining "name" and "name_by_user" if present.
#
# Example attributes that are valid device fields:
#   - friendly_name
#   - manufacturer
#   - model
#
# If friendly_name is included here, the code will populate it using device.name,
# overriding with device.name_by_user if available.
#
ATTRIBUTES = {
    "friendly_name": "Unknown Device",
    "manufacturer": "Unknown Manufacturer",
    "model": "Unknown Model",
    "area_id": "No Area",
    "area_name": "No Area Name",
}