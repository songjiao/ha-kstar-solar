# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

科士达光伏逆变器 Home Assistant 集成 - A custom Home Assistant integration for Kstar Solar Inverters that fetches solar power generation data using username + encrypted password authentication.

## Tech Stack

- **Language**: Python 3.10+
- **Framework**: Home Assistant Custom Integration
- **HTTP Client**: aiohttp (async)
- **Authentication**: Username + encrypted password login, with refresh_token fallback

## Architecture

```
custom_components/kstar_solar/
├── __init__.py      # Integration setup, creates KstarSolarAPI instance
├── config_flow.py   # UI configuration flow (ConfigFlow pattern)
├── sensor.py        # Sensor entities using DataUpdateCoordinator
├── kstar_api.py     # Async API client with token auto-refresh
├── const.py         # Domain, sensor definitions, API endpoints
├── manifest.json    # HA integration metadata
└── translations/    # i18n (en, zh-Hans)
```

**Data Flow**: `config_flow` → `__init__` creates API → `sensor.py` uses `DataUpdateCoordinator` (5-min interval) → calls `api.get_station_data()`

## Key Patterns

- **DataUpdateCoordinator**: All sensors share a single coordinator that polls the API
- **Token Management**: `_login()` for initial auth, `_refresh_access_token()` tries refresh_token first then falls back to re-login
- **State Class Handling**: `totalGeneration` uses `TOTAL_INCREASING` with zero-value protection to prevent statistics errors

## Development Commands

```bash
# Install dependencies
pip install aiohttp>=3.8.0

# Type checking
pip install mypy
mypy custom_components/kstar_solar/

# Linting with pre-commit
pip install pre-commit
pre-commit install
pre-commit run --all-files

# Run tests
pip install pytest pytest-homeassistant-custom-component
python -m pytest tests/

# Enable debug logging in HA configuration.yaml
logger:
  logs:
    custom_components.kstar_solar: debug
```

## API Details

- **Base URL**: `http://solar.kstar.com.cn:9003`
- **Login Endpoint**: `POST /prod-api/authentication/form` (Basic auth: `kstar:kstarSecret`, multipart/form-data)
- **Token Refresh Endpoint**: `/prod-api/oauth/token` (Basic auth: `kstar:kstarSecret`)
- **Data Endpoint**: `/prod-api/station/detail/earn?stationId={id}`
- **Token Format**: Bearer token in Authorization header

## Sensor Types

Defined in `const.py:SENSOR_TYPES` - includes: realPower, dayGeneration, monthGeneration, yearGeneration, totalGeneration, dayEarn, totalEarn, co2, coal, forest

## Version

Update version in `manifest.json` when releasing.
