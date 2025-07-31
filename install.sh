#!/bin/bash

# 科士达光伏逆变器 Home Assistant 集成安装脚本
# Kstar Solar Inverter Home Assistant Integration Installer

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为root用户
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "请不要使用root用户运行此脚本"
        exit 1
    fi
}

# 检查Home Assistant配置目录
find_config_dir() {
    local config_dirs=(
        "$HOME/.homeassistant"
        "/config"
        "/opt/homeassistant/config"
        "/usr/share/hassio/homeassistant"
    )
    
    for dir in "${config_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            CONFIG_DIR="$dir"
            return 0
        fi
    done
    
    return 1
}

# 主安装函数
main() {
    print_info "科士达光伏逆变器 Home Assistant 集成安装程序"
    print_info "================================================"
    
    # 检查root用户
    check_root
    
    # 查找Home Assistant配置目录
    print_info "正在查找 Home Assistant 配置目录..."
    if find_config_dir; then
        print_success "找到配置目录: $CONFIG_DIR"
    else
        print_error "未找到 Home Assistant 配置目录"
        print_info "请手动指定配置目录路径:"
        read -p "请输入配置目录路径: " CONFIG_DIR
        if [[ ! -d "$CONFIG_DIR" ]]; then
            print_error "指定的目录不存在: $CONFIG_DIR"
            exit 1
        fi
    fi
    
    # 创建custom_components目录
    CUSTOM_COMPONENTS_DIR="$CONFIG_DIR/custom_components"
    if [[ ! -d "$CUSTOM_COMPONENTS_DIR" ]]; then
        print_info "创建 custom_components 目录..."
        mkdir -p "$CUSTOM_COMPONENTS_DIR"
    fi
    
    # 创建kstar_solar目录
    KSTAR_DIR="$CUSTOM_COMPONENTS_DIR/kstar_solar"
    if [[ -d "$KSTAR_DIR" ]]; then
        print_warning "kstar_solar 目录已存在，将备份现有文件..."
        BACKUP_DIR="$KSTAR_DIR.backup.$(date +%Y%m%d_%H%M%S)"
        mv "$KSTAR_DIR" "$BACKUP_DIR"
        print_success "现有文件已备份到: $BACKUP_DIR"
    fi
    
    # 创建目录结构
    print_info "创建插件目录结构..."
    mkdir -p "$KSTAR_DIR"
    mkdir -p "$KSTAR_DIR/translations"
    
    # 创建插件文件
    print_info "创建插件文件..."
    
    # manifest.json
    cat > "$KSTAR_DIR/manifest.json" << 'EOF'
{
  "domain": "kstar_solar",
  "name": "Kstar Solar Inverter",
  "documentation": "https://github.com/your-repo/kstar_solar",
  "dependencies": [],
  "codeowners": [],
  "requirements": ["requests>=2.25.0", "requests-toolbelt>=1.0.0"],
  "version": "1.0.0",
  "iot_class": "cloud_polling"
}
EOF

    # const.py
    cat > "$KSTAR_DIR/const.py" << 'EOF'
"""Constants for the Kstar Solar Inverter integration."""
from datetime import timedelta

DOMAIN = "kstar_solar"

# Configuration keys
CONF_HOST = "host"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_STATION_ID = "station_id"
CONF_ACCESS_TOKEN = "access_token"

# Default values
DEFAULT_HOST = "http://solar.kstar.com.cn:9003"
DEFAULT_NAME = "Kstar Solar Inverter"

# Update intervals
SCAN_INTERVAL = timedelta(minutes=5)

# API endpoints
LOGIN_URL = "/prod-api/authentication/form"
STATION_DETAIL_URL = "/prod-api/station/detail/earn"

# Sensor types
SENSOR_TYPES = {
    "realPower": {
        "name": "实时功率",
        "unit": "W",
        "icon": "mdi:solar-power",
        "device_class": "power",
    },
    "dayGeneration": {
        "name": "日发电量",
        "unit": "kWh",
        "icon": "mdi:solar-panel",
        "device_class": "energy",
    },
    "monthGeneration": {
        "name": "月发电量",
        "unit": "kWh",
        "icon": "mdi:solar-panel-large",
        "device_class": "energy",
    },
    "yearGeneration": {
        "name": "年发电量",
        "unit": "kWh",
        "icon": "mdi:solar-panel-large",
        "device_class": "energy",
    },
    "totalGeneration": {
        "name": "总发电量",
        "unit": "kWh",
        "icon": "mdi:solar-panel-large",
        "device_class": "energy",
    },
    "dayEarn": {
        "name": "日收益",
        "unit": "元",
        "icon": "mdi:currency-cny",
    },
    "totalEarn": {
        "name": "总收益",
        "unit": "元",
        "icon": "mdi:currency-cny",
    },
    "co2": {
        "name": "CO2减排量",
        "unit": "kg",
        "icon": "mdi:molecule-co2",
    },
    "coal": {
        "name": "节煤量",
        "unit": "kg",
        "icon": "mdi:fire",
    },
    "forest": {
        "name": "森林面积",
        "unit": "m²",
        "icon": "mdi:tree",
    },
}
EOF

    # __init__.py
    cat > "$KSTAR_DIR/__init__.py" << 'EOF'
"""The Kstar Solar Inverter integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, CONF_ACCESS_TOKEN
from .kstar_api import KstarSolarAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Kstar Solar Inverter from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create API client based on configuration
    if CONF_ACCESS_TOKEN in entry.data:
        # Use access token authentication
        api = KstarSolarAPI(
            host=entry.data["host"],
            station_id=entry.data["station_id"],
            access_token=entry.data[CONF_ACCESS_TOKEN],
            refresh_token=entry.data.get("refresh_token", ""),
        )
        _LOGGER.info("使用访问令牌认证方式")
    elif "refresh_token" in entry.data:
        # Use refresh token authentication
        api = KstarSolarAPI(
            host=entry.data["host"],
            station_id=entry.data["station_id"],
            refresh_token=entry.data["refresh_token"],
        )
        _LOGGER.info("使用刷新令牌认证方式")
    else:
        # Use username/password authentication
        api = KstarSolarAPI(
            host=entry.data["host"],
            username=entry.data["username"],
            password=entry.data["password"],
            station_id=entry.data["station_id"],
        )
        _LOGGER.info("使用用户名密码认证方式")

    # Test the connection
    try:
        await hass.async_add_executor_job(api.get_station_data)
    except Exception as ex:
        _LOGGER.error("Failed to connect to Kstar Solar API: %s", ex)
        raise ConfigEntryNotReady from ex

    hass.data[DOMAIN][entry.entry_id] = api

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        api = hass.data[DOMAIN].pop(entry.entry_id)
        api.close()

    return unload_ok
EOF

    # 创建其他必要文件（这里只创建基本结构，实际文件内容需要从项目中复制）
    print_info "创建其他插件文件..."
    touch "$KSTAR_DIR/config_flow.py"
    touch "$KSTAR_DIR/kstar_api.py"
    touch "$KSTAR_DIR/sensor.py"
    touch "$KSTAR_DIR/translations/en.json"
    touch "$KSTAR_DIR/translations/zh-Hans.json"
    
    print_warning "注意：此脚本只创建了基本文件结构"
    print_info "您需要手动复制以下文件到 $KSTAR_DIR/ 目录："
    print_info "  - config_flow.py"
    print_info "  - kstar_api.py"
    print_info "  - sensor.py"
    print_info "  - translations/en.json"
    print_info "  - translations/zh-Hans.json"
    
    print_success "插件目录结构已创建完成！"
    print_info "目录位置: $KSTAR_DIR"
    
    print_info ""
    print_info "下一步操作："
    print_info "1. 将完整的插件文件复制到上述目录"
    print_info "2. 重启 Home Assistant"
    print_info "3. 在集成页面添加 'Kstar Solar Inverter'"
    print_info ""
    print_info "推荐配置方式："
    print_info "- 仅使用刷新令牌（最简单，长期有效）"
    print_info "- 用户名密码登录（传统方式）"
    print_info "- 直接使用访问令牌（短期有效）"
}

# 运行主函数
main "$@" 