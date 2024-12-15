import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .const import DOMAIN

class Ent2DevConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Create the config entry
            return self.async_create_entry(title="Entity Device Mapper", data={})
        
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({})
        )