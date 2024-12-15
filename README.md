# Entity Device Mapper (`ent2dev`)

**Entity Device Mapper (`ent2dev`)** is a custom Home Assistant (HASS) integration that creates a sensor (`sensor.entity_device_map`) to map each Home Assistant entity to its corresponding device. This sensor makes it easy to look up device information given an entity ID or name, something that is otherwise impossible to do.
The originating use case was to be able to generate a list of devices that are offline or unavailable - something that is  lacking in HomeAssistant's entity-centric UI.

## 🛠️ Features

- **Entity-to-Device Mapping:**  
  Maps each `entity_id` to its associated `device_id` along with key device attributes.

- **Configurable Attributes:**  
  Uses a `const.py` file to define which device attributes to include (e.g., `friendly_name`, `manufacturer`, `model`, `area_name`). This allows easy addition or removal of attributes without modifying the core integration code.

- **Dynamic Updates:**  
  Listens for updates in the device and entity registries to automatically rebuild and update the mapping whenever changes occur.

- **Recorder Exclusion:**  
  For efficiency, the map is generated as a sensor state. It's recommended to excludes `sensor.entity_device_map` from Home Assistant's Recorder in configuration.yaml. The state is transitory and does not need to be retained historically.

## 📁 File Structure
```
ent2dev/
├── custom_components/
│   └── ent2dev/
│       ├── init.py
│       ├── const.py
│       ├── sensor.py
│       └── manifest.json
├── samples/
│   └── helpers.yaml
│   └── sensors.yaml
│   └── cards.yaml
├── README.md
├── LICENSE
└── .gitignore
```
### 📄 manifest.json

Provides integration metadata including name, version, and dependencies.

### 📄 __init__.py

Handles the setup of the integration, builds the entity-to-device mapping based on the defined attributes, and manages updates by listening to registry changes.

### 📄 sensor.py

Defines a sensor entity (sensor.entity_device_map) that exposes the mapping as a state attribute.

### 📄 const.py

Defines configuration constants like as `DOMAIN`, `PLATFORMS`, `SENSOR_ENTITY_ID`, and the `ATTRIBUTES` dictionary that specifies which device attributes to include.

---

## Installation

To install the `ent2dev` Home Assistant integration, follow these steps:

### Step 1: Download the Integration
Download the ZIP file from the GitHub repository or clone it using the following command:

```bash
git clone https://github.com/marcpbailey/ent2dev.git
```

### Step 2: Copy the Files
Unzip the downloaded file if necessary, then copy the `ent2dev` folder into the `custom_components` directory of your Home Assistant setup. If the `custom_components` directory does not exist, create it in the root of your Home Assistant configuration folder.

### Step 3: Configure the Integration
Add the following to your `configuration.yaml` file:

```yaml
ent2dev:
  exclude_recorder: true
```

Edit const.py to configure the attributes you want to map 
(see below)

### Step 4: Configure the Integration

This step prevents the integration's sensor attributes from being recorded in the database to avoid performance issues.

### Step 5: Restart Home Assistant
Restart your Home Assistant instance to load the new integration.


### Step 6: Verify Installation
After restarting, navigate to the "Developer Tools" > "States" section in Home Assistant. Look for the `sensor.entity_device_map` entity to confirm the integration is active.

---
## Configuration

The `ATTRIBUTES` dictionary in `const.py` defines the metadata fields included in the entity-to-device map. This dictionary controls which device attributes are retrieved and allows you to specify default values for each attribute if the actual value is unavailable. It provides flexibility and centralised configuration for the integration without requiring changes to Python code.

### Structure of `ATTRIBUTES`

Each key in the dictionary corresponds to an attribute that can be retrieved from the device registry. The value assigned to each key is the default value to use when the attribute is unavailable.

Example (and default) structure:
```python
ATTRIBUTES = {
    "friendly_name": "Unknown Device",
    "manufacturer": "Unknown Manufacturer",
    "model": "Unknown Model",
    "area_id": "No Area",
    "area_name": "No Area Name",
}
```

### How It Works
- The integration iterates through the keys in `ATTRIBUTES`.
- For each key, it attempts to fetch the corresponding attribute from the device registry.
- If the attribute is unavailable, the default value from `ATTRIBUTES` is used.
- The `area_name` key is treated as a special case: if specified, the integration performs a lookup in the area registry to fetch the area name for the device.

### Adding or Removing Attributes
1. **To Add a New Attribute**:
   - Add the new attribute key to the `ATTRIBUTES` dictionary.
   - Specify the default value to use if the attribute is unavailable.

 Example:
 ```python
 ATTRIBUTES = {
     "name": "Unknown Device",
     "ip_address": "Unknown IP",
 }
 ```
   In this case, the `ip_address` attribute will be included in the map with "Unknown IP" as the default.

2. **To Remove an Attribute**:
   - Delete the attribute key from the `ATTRIBUTES` dictionary.

   Example:
   ```python
   ATTRIBUTES = {
       "name": "Unknown Device",
   }
   ```
   This removes all attributes except `name`.

### Best Practices
- **Keep Default Values Meaningful**: Default values should provide clear indications of missing data, such as "Unknown [Field]" or "Not Available."
- **Avoid State-Related Attributes**: Since the integration only updates when devices or entities are added or removed, avoid including attributes tied to entity states, such as `last_seen`.
- **Optimise for Performance**: Limit the number of attributes to only those necessary for your use case to prevent large sensor payloads.

### Special Handling of Area Name
To enable area name resolution, include the key `area_name` in the `ATTRIBUTES` dictionary. The integration will automatically look up the area name for each device using the `area_id` provided by the device registry.

Example:
```python
ATTRIBUTES = {
    "name": "Unknown Device",
    "area_name": "No Area Name",
}
```

## Samples

The samples folder contains synthetic sensors, an input helper, and a couple of sample cards that demonstrate how to use ent2dev. If you understand HomeAssistant templating you'll find these familiar


---
## Uninstallation

Follow these steps to completely remove the `ent2dev` custom integration from your Home Assistant setup:

### 1. Remove the Integration from Home Assistant
1. Navigate to **Settings** > **Devices & Services** in the Home Assistant UI.
2. Locate the `ent2dev` integration in the list of configured integrations.
3. Select the `ent2dev` integration and click **Delete** or **Remove**.
4. Confirm the deletion when prompted.

### 2. Delete the Custom Component Files
1. Using an appropriate file manager or terminal, navigate to the directory where custom components are stored, typically:
   ```
   /config/custom_components/
   ```
2. Locate the folder named `ent2dev`.
3. Delete the entire `ent2dev` folder.

### 3. Remove Any Configuration Changes
If you made manual changes to the Home Assistant configuration (e.g., in `configuration.yaml`), remove the following lines:
- Any reference to disabling the recorder for `sensor.entity_device_map`:
```yaml
recorder:
  exclude:
    entities:
      - sensor.entity_device_map
```
Also remove any dependent synthetic sensors and cards you will have created.


## 4. Restart Home Assistant
1. Restart Home Assistant to ensure all changes are applied and the integration is fully removed.
   - You can restart Home Assistant via **Settings** > **System** > **Restart**.
   - Alternatively, restart via terminal:
     ```
     ha core restart
     ```

## 5. Verify Uninstallation
1. Confirm that the `ent2dev` integration no longer appears in the **Devices & Services** section.
2. Check that the `sensor.entity_device_map` and any related entities or attributes no longer exist.


## 6. Optional: Clear Historical Data
If the integration generated significant historical data, you may want to clear it from the database:
1. Stop the Home Assistant service.
2. Use a database management tool (e.g., SQLite) to open the `home-assistant_v2.db` file.
3. Search for entries related to `sensor.entity_device_map` and delete them.

> **Warning:** Modifying the database directly can lead to data corruption if not done carefully. Always back up your database before making changes.


## 7. Remove Any Backup Files
1. If you created backup files for `ent2dev`, locate and delete those files.
2. Check any version control repositories (e.g., Git) where the integration may still exist.


These steps will ensure the complete removal of `ent2dev` from your Home Assistant setup.
