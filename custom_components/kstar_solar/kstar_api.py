"""API client for Kstar Solar Inverter."""
import json
import logging
import base64
from typing import Any, Dict
import aiohttp
import asyncio
from .const import STATION_DETAIL_URL

_LOGGER = logging.getLogger(__name__)

class KstarSolarAPI:
    def __init__(self, host: str, station_id: str, refresh_token: str, timeout: int = 30):
        self.host = host.rstrip("/")
        self.station_id = station_id
        self.refresh_token = refresh_token
        self.access_token = None
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

    async def _get_access_token_from_refresh_token(self) -> None:
        """从refresh_token获取access_token"""
        if not self.refresh_token:
            _LOGGER.error("没有refresh_token，无法获取访问令牌")
            raise Exception("没有refresh_token，无法获取访问令牌")
        
        try:
            _LOGGER.info("使用refresh_token获取访问令牌")
            session = await self._get_session()
            
            basic_auth = base64.b64encode(b"kstar:kstarSecret").decode('utf-8')
            headers = {
                **self._headers,
                "Authorization": f"Basic {basic_auth}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": self.host,
                "Referer": f"{self.host}/",
            }
            
            refresh_data = {
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
            }
            
            async with session.post(
                f"{self.host}/prod-api/oauth/token",
                data=refresh_data,
                headers=headers,
            ) as response:
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug("获取token响应: %s", data)
                
                if "value" in data:
                    self.access_token = data["value"]
                    if "refreshToken" in data and "value" in data["refreshToken"]:
                        self.refresh_token = data["refreshToken"]["value"]
                    
                    # 更新会话头部
                    self._headers["Authorization"] = f"bearer {self.access_token}"
                    _LOGGER.info("成功获取访问令牌")
                else:
                    _LOGGER.error("获取token失败: %s", data.get("error_description", "Unknown error"))
                    raise Exception(f"获取token失败: {data.get('error_description', 'Unknown error')}")
                    
        except Exception as e:
            _LOGGER.error("获取token异常: %s", e)
            raise

    async def get_station_data(self) -> Dict[str, Any]:
        """获取电站数据"""
        try:
            session = await self._get_session()
            
            async with session.get(
                f"{self.host}{STATION_DETAIL_URL}",
                params={"stationId": self.station_id},
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                if data.get("code") != 200:
                    error_msg = data.get("message", "Unknown error")
                    _LOGGER.error("获取电站数据失败: %s", error_msg)
                    raise Exception(f"获取电站数据失败: {error_msg}")
                
                return data.get("data", {})
                
        except aiohttp.ClientError as e:
            _LOGGER.error("获取数据请求失败: %s", e)
            # token过期自动刷新
            await self._get_access_token_from_refresh_token()
            
            try:
                session = await self._get_session()
                async with session.get(
                    f"{self.host}{STATION_DETAIL_URL}",
                    params={"stationId": self.station_id},
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    if data.get("code") != 200:
                        error_msg = data.get("message", "Unknown error")
                        raise Exception(f"获取电站数据失败: {error_msg}")
                    
                    return data.get("data", {})
                    
            except Exception as retry_error:
                _LOGGER.error("刷新token后重试失败: %s", retry_error)
                raise Exception(f"获取电站数据失败: {retry_error}")

    async def close(self) -> None:
        """关闭会话"""
        if self.session and not self.session.closed:
            await self.session.close() 