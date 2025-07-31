# 科士达光伏逆变器 Home Assistant 集成

这是一个专为 Home Assistant 设计的科士达光伏逆变器集成插件，**只需配置 refresh_token 即可长期稳定获取发电数据**。

## 🌟 主要特性
- 极简配置：只需后台地址、电站ID、refresh_token
- 自动Token管理：自动换取access_token，无需手动维护
- 丰富的传感器数据：实时功率、发电量、收益、CO2减排等
- 高可靠性：内置重试机制和错误处理
- 用户友好：支持中英文界面

## 🚀 快速开始（仅需refresh_token）

### 1. 获取 refresh_token
1. 在浏览器访问 [科士达光伏后台](http://solar.kstar.com.cn:9003)
2. 登录后按 F12 打开开发者工具，切换到 Network 标签页
3. 刷新页面，找到登录相关请求，在响应中复制 `refresh_token` 字段

### 2. 安装插件
```bash
wget https://raw.githubusercontent.com/songjiao/ha-kstar-solar/main/install.sh
chmod +x install.sh
./install.sh
```

### 3. 配置集成
1. 在 Home Assistant 中添加集成，搜索“Kstar Solar Inverter”
2. 填写：
   - 后台地址：`http://solar.kstar.com.cn:9003`
   - 电站ID：您的电站ID
   - 刷新令牌：上一步获取的 refresh_token

## 📊 支持的传感器
- 实时功率 (W)
- 日发电量 (kWh)
- 月发电量 (kWh)
- 年发电量 (kWh)
- 总发电量 (kWh)
- 日收益 (元)
- 总收益 (元)
- CO2减排量 (kg)
- 节煤量 (kg)
- 森林面积 (m²)

## 🔍 故障排除
- **登录失败**：请重新获取 refresh_token 并配置
- **Token过期**：插件会自动刷新，无需手动干预
- **无法获取数据**：检查网络、电站ID、refresh_token 是否正确
- **插件无法加载**：确认文件已正确复制，重启 Home Assistant

## 📝 日志查看
1. 进入 Home Assistant “开发者工具” > “日志”
2. 搜索 "kstar_solar" 查看相关日志

## 📈 数据更新
- 传感器数据每5分钟自动更新
- 支持手动刷新

## 🔒 安全说明
- refresh_token 安全存储，不会向第三方发送
- 建议定期在后台重新获取 refresh_token

---

**提示**：只需配置一次 refresh_token，插件会自动管理所有认证和数据更新，无需记住用户名密码，极致简洁！ 