"""Config flow for Kstar Solar Inverter integration."""
import logging
from typing import Any, Dict, Optional
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, DEFAULT_HOST
from .kstar_api import KstarSolarAPI

_LOGGER = logging.getLogger(__name__)

class KstarSolarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        errors = {}
        if user_input is not None:
            try:
                host = user_input["host"].rstrip("/")
                if not host.startswith(("http://", "https://")):
                    host = f"http://{host}"
                api = KstarSolarAPI(
                    host=host,
                    station_id=user_input["station_id"],
                    refresh_token=user_input["refresh_token"],
                )
                await self.hass.async_add_executor_job(api.get_station_data)
                config_data = {
                    "host": host,
                    "station_id": user_input["station_id"],
                    "refresh_token": user_input["refresh_token"],
                }
                return self.async_create_entry(
                    title=f"Kstar Solar - {user_input['station_id']}",
                    data=config_data,
                )
            except Exception as ex:
                _LOGGER.exception("配置失败")
                errors["base"] = "cannot_connect"

        schema = vol.Schema({
            vol.Required("host", default=DEFAULT_HOST): str,
            vol.Required("station_id"): str,
            vol.Required("refresh_token"): str,
        })
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "help_text": (
                    "请在浏览器登录科士达后台，F12开发者工具Network中获取refresh_token。\n"
                    "无需用户名密码，配置一次长期有效。"
                )
            },
        ) 