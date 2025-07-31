# 部署说明

## 🚀 从GitHub安装

### 方法一：使用安装脚本（推荐）
```bash
# 下载并运行安装脚本
wget https://raw.githubusercontent.com/songjiao/ha-kstar-solar/main/install.sh
chmod +x install.sh
./install.sh
```

### 方法二：手动安装
```bash
# 1. 进入Home Assistant配置目录
cd /path/to/your/homeassistant/config

# 2. 创建插件目录
mkdir -p custom_components/kstar_solar

# 3. 下载插件文件
wget -O custom_components/kstar_solar/manifest.json https://raw.githubusercontent.com/songjiao/ha-kstar-solar/main/custom_components/kstar_solar/manifest.json
wget -O custom_components/kstar_solar/__init__.py https://raw.githubusercontent.com/songjiao/ha-kstar-solar/main/custom_components/kstar_solar/__init__.py
wget -O custom_components/kstar_solar/config_flow.py https://raw.githubusercontent.com/songjiao/ha-kstar-solar/main/custom_components/kstar_solar/config_flow.py
wget -O custom_components/kstar_solar/const.py https://raw.githubusercontent.com/songjiao/ha-kstar-solar/main/custom_components/kstar_solar/const.py
wget -O custom_components/kstar_solar/kstar_api.py https://raw.githubusercontent.com/songjiao/ha-kstar-solar/main/custom_components/kstar_solar/kstar_api.py
wget -O custom_components/kstar_solar/sensor.py https://raw.githubusercontent.com/songjiao/ha-kstar-solar/main/custom_components/kstar_solar/sensor.py

# 4. 创建翻译目录
mkdir -p custom_components/kstar_solar/translations
wget -O custom_components/kstar_solar/translations/en.json https://raw.githubusercontent.com/songjiao/ha-kstar-solar/main/custom_components/kstar_solar/translations/en.json
wget -O custom_components/kstar_solar/translations/zh-Hans.json https://raw.githubusercontent.com/songjiao/ha-kstar-solar/main/custom_components/kstar_solar/translations/zh-Hans.json

# 5. 重启Home Assistant
```

## 📦 依赖安装

插件需要以下Python依赖：
```bash
pip install requests>=2.25.0
```

## 🔧 配置步骤

1. **获取refresh_token**：
   - 访问 http://solar.kstar.com.cn:9003
   - 登录后按F12打开开发者工具
   - 在Network标签页中找到登录请求
   - 复制响应中的refresh_token

2. **添加集成**：
   - 在Home Assistant中添加集成
   - 搜索"Kstar Solar Inverter"
   - 填写配置信息

## 🔄 更新插件

```bash
# 重新运行安装脚本即可更新
./install.sh
```

## 📝 日志查看

在Home Assistant中查看日志：
1. 进入"开发者工具" > "日志"
2. 搜索"kstar_solar"查看相关日志

## 🆘 故障排除

- **插件无法加载**：检查文件是否完整，重启Home Assistant
- **登录失败**：重新获取refresh_token
- **无法获取数据**：检查网络连接和电站ID

---

**GitHub仓库**：https://github.com/songjiao/ha-kstar-solar 