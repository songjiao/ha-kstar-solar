"""Constants for the Kstar Solar Inverter integration."""
from datetime import timedelta

DOMAIN = "kstar_solar"

# 配置项
DEFAULT_HOST = "http://solar.kstar.com.cn:9003"

# 更新间隔
SCAN_INTERVAL = timedelta(minutes=5)

# API端点
STATION_DETAIL_URL = "/prod-api/station/detail/earn"

# 传感器类型
SENSOR_TYPES = {
    "realPower": {"name": "实时功率", "unit": "W", "icon": "mdi:solar-power", "device_class": "power"},
    "dayGeneration": {"name": "日发电量", "unit": "kWh", "icon": "mdi:solar-panel", "device_class": "energy"},
    "monthGeneration": {"name": "月发电量", "unit": "kWh", "icon": "mdi:solar-panel-large", "device_class": "energy"},
    "yearGeneration": {"name": "年发电量", "unit": "kWh", "icon": "mdi:solar-panel-large", "device_class": "energy"},
    "totalGeneration": {"name": "总发电量", "unit": "kWh", "icon": "mdi:solar-panel-large", "device_class": "energy"},
    "dayEarn": {"name": "日收益", "unit": "元", "icon": "mdi:currency-cny"},
    "totalEarn": {"name": "总收益", "unit": "元", "icon": "mdi:currency-cny"},
    "co2": {"name": "CO2减排量", "unit": "kg", "icon": "mdi:molecule-co2"},
    "coal": {"name": "节煤量", "unit": "kg", "icon": "mdi:fire"},
    "forest": {"name": "森林面积", "unit": "m²", "icon": "mdi:tree"},
} 