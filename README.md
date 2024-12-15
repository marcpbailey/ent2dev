# Entity Device Mapper (`ent2dev`)

**Entity Device Mapper (`ent2dev`)** is a custom Home Assistant (HASS) integration that creates a sensor (`sensor.entity_device_map`) to map each Home Assistant entity to its corresponding device. This sensor aggregates essential device attributes, facilitating easy access and management of entity-device relationships within Home Assistant.

## 🛠️ Features

- **Entity-to-Device Mapping:**  
  Maps each `entity_id` to its associated `device_id` along with key device attributes.

- **Configurable Attributes:**  
  Uses a `const.py` file to define which device attributes to include (e.g., `friendly_name`, `manufacturer`, `model`, `area_name`). This allows easy addition or removal of attributes without modifying the core integration code.

- **Consolidated Naming:**  
  Combines `name` and `name_by_user` into a single `friendly_name` attribute, prioritizing `name_by_user` for a more personalized device name.

- **Dynamic Updates:**  
  Listens for updates in the device and entity registries to automatically rebuild and update the mapping whenever changes occur.

- **Recorder Exclusion:**  
  Excludes the `sensor.entity_device_map` from Home Assistant's Recorder to prevent exceeding attribute size limits and ensure optimal database performance.

## 📁 File Structure
````
ent2dev/
├── custom_components/
│   └── ent2dev/
│       ├── init.py
│       ├── const.py
│       ├── sensor.py
│       └── manifest.json
├── README.md
├── LICENSE
└── .gitignore
````
### 📄 manifest.json

Provides integration metadata including name, version, and dependencies.

### 📄 __init__.py

Handles the setup of the integration, builds the entity-to-device mapping based on the defined attributes, and manages updates by listening to registry changes.

### 📄 sensor.py

Defines a sensor entity (sensor.entity_device_map) that exposes the mapping as a state attribute.

### 📄 const.py

Defines configuration constants like as `DOMAIN`, `PLATFORMS`, `SENSOR_ENTITY_ID`, and the `ATTRIBUTES` dictionary that specifies which device attributes to include.

