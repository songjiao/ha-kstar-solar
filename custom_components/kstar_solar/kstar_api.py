"""API client for Kstar Solar Inverter."""
import logging
import base64
from typing import Any, Dict
import aiohttp
from .const import LOGIN_URL, STATION_DETAIL_URL

_LOGGER = logging.getLogger(__name__)


class KstarSolarAPI:
    def __init__(self, host: str, station_id: str, username: str, password: str, timeout: int = 30):
        self.host = host.rstrip("/")
        self.station_id = station_id
        self.username = username
        self.password = password
        self.access_token = None
        self.refresh_token = None
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = None
        self._headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        }

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            connector = aiohttp.TCPConnector(verify_ssl=False)
            self.session = aiohttp.ClientSession(
                timeout=self.timeout,
                connector=connector,
                headers=self._headers
            )
        return self.session

    async def _login(self) -> None:
        """Login with username and encrypted password to get tokens."""
        try:
            _LOGGER.info("Logging in with username/password")
            session = await self._get_session()

            basic_auth = base64.b64encode(b"kstar:kstarSecret").decode("utf-8")
            headers = {
                **self._headers,
                "Authorization": f"Basic {basic_auth}",
                "Origin": self.host,
                "Referer": f"{self.host}/",
            }

            form_data = aiohttp.FormData()
            form_data.add_field("username", self.username)
            form_data.add_field("password", self.password)

            async with session.post(
                f"{self.host}{LOGIN_URL}",
                data=form_data,
                headers=headers,
            ) as response:
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug("Login response: %s", data)

                token_data = data.get("token", {})
                access_token = token_data.get("access_token")
                if not access_token:
                    error_msg = data.get("message", "No access_token in response")
                    _LOGGER.error("Login failed: %s", error_msg)
                    raise Exception(f"Login failed: {error_msg}")

                self.access_token = access_token
                self.refresh_token = token_data.get("refresh_token")
                self._headers["Authorization"] = f"bearer {self.access_token}"
                _LOGGER.info("Login successful")

        except Exception as e:
            _LOGGER.error("Login error: %s", e)
            raise

    async def _refresh_access_token(self) -> None:
        """Refresh access_token using refresh_token, fallback to login."""
        if self.refresh_token:
            try:
                _LOGGER.info("Refreshing access token via refresh_token")
                session = await self._get_session()

                basic_auth = base64.b64encode(b"kstar:kstarSecret").decode("utf-8")
                headers = {
                    **self._headers,
                    "Authorization": f"Basic {basic_auth}",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": self.host,
                    "Referer": f"{self.host}/",
                }

                refresh_data = {
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                }

                async with session.post(
                    f"{self.host}/prod-api/oauth/token",
                    data=refresh_data,
                    headers=headers,
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    _LOGGER.debug("Token refresh response: %s", data)

                    if "value" in data:
                        self.access_token = data["value"]
                        if "refreshToken" in data and "value" in data["refreshToken"]:
                            self.refresh_token = data["refreshToken"]["value"]
                        self._headers["Authorization"] = f"bearer {self.access_token}"
                        _LOGGER.info("Token refreshed successfully")
                        return
                    else:
                        _LOGGER.warning("Token refresh returned no value, falling back to login")
            except Exception as e:
                _LOGGER.warning("Token refresh failed (%s), falling back to login", e)

        # Fallback: re-login with username/password
        await self._login()

    async def _ensure_token(self) -> None:
        """Ensure we have a valid access_token."""
        if not self.access_token:
            await self._login()

    async def get_station_data(self) -> Dict[str, Any]:
        """Get station data from API."""
        await self._ensure_token()

        try:
            session = await self._get_session()

            async with session.get(
                f"{self.host}{STATION_DETAIL_URL}",
                params={"stationId": self.station_id},
            ) as response:
                if response.status == 401:
                    _LOGGER.info("Token expired, refreshing")
                    await self._refresh_access_token()
                    await self.close()
                    session = await self._get_session()

                    async with session.get(
                        f"{self.host}{STATION_DETAIL_URL}",
                        params={"stationId": self.station_id},
                    ) as retry_response:
                        retry_response.raise_for_status()
                        return self._parse_response(await retry_response.json())
                else:
                    response.raise_for_status()
                    return self._parse_response(await response.json())

        except aiohttp.ClientError as e:
            _LOGGER.error("Request failed: %s", e)
            if "401" in str(e):
                _LOGGER.info("Got 401 error, refreshing token")
                await self._refresh_access_token()
                await self.close()

                try:
                    session = await self._get_session()
                    async with session.get(
                        f"{self.host}{STATION_DETAIL_URL}",
                        params={"stationId": self.station_id},
                    ) as response:
                        response.raise_for_status()
                        return self._parse_response(await response.json())
                except Exception as retry_error:
                    _LOGGER.error("Retry after token refresh failed: %s", retry_error)
                    raise Exception(f"Failed to get station data: {retry_error}")
            else:
                raise Exception(f"Failed to get station data: {e}")

    def _parse_response(self, data: dict) -> Dict[str, Any]:
        """Parse and validate API response."""
        if data.get("code") != 200:
            error_msg = data.get("message", "Unknown error")
            _LOGGER.error("API returned error: %s", error_msg)
            raise Exception(f"Failed to get station data: {error_msg}")
        return data.get("data", {})

    async def close(self) -> None:
        """Close the HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None
